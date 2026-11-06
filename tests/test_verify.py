"""Regression tests for verification policy, not product-specific app tests."""

from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify  # noqa: E402
import scan_secrets  # noqa: E402


def step(name: str, category: str = "tests", tier: str = "quick",
         command: list[str] | None = None) -> dict:
    return {
        "name": name,
        "category": category,
        "tier": tier,
        "command": command or ["{python}", "-c", "print('ok')"],
        "timeout_sec": 5,
    }


def steps() -> list[dict]:
    return [step("tests"), step("lint", "lint"),
            step("secrets", "security"), step("arch", "architecture")]


class ConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / "verification.json"

    def write_config(self, entries: list[dict], **extra) -> None:
        self.config.write_text(json.dumps({"schema_version": 1,
                                           "steps": entries, **extra}), encoding="utf-8")

    def test_four_required_categories(self) -> None:
        self.write_config(steps())
        self.assertEqual(4, len(verify.load_config(self.config, self.root)))

    def test_missing_required_category_fails_closed(self) -> None:
        self.write_config(steps()[:3])
        with self.assertRaisesRegex(verify.ConfigurationError, "Missing required"):
            verify.load_config(self.config, self.root)

    def test_duplicate_step_name_fails(self) -> None:
        entries = steps() + [step("tests")]
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "Duplicate"):
            verify.load_config(self.config, self.root)

    def test_shell_string_disallowed(self) -> None:
        entries = steps()
        entries[0]["command"] = "python -m unittest"
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "argv-array"):
            verify.load_config(self.config, self.root)

    def test_unrecognized_placeholder_disallowed(self) -> None:
        entries = steps()
        entries[0]["command"] = ["{bad}"]
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "Unknown command placeholder"):
            verify.load_config(self.config, self.root)

    def test_outside_working_dir_disallowed(self) -> None:
        entries = steps()
        entries[0]["cwd"] = "../"
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "escapes repository"):
            verify.load_config(self.config, self.root)

    def test_nonexistent_working_dir_disallowed(self) -> None:
        entries = steps()
        entries[0]["cwd"] = "not-a-directory"
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "does not exist"):
            verify.load_config(self.config, self.root)

    def test_invalid_timeout_disallowed(self) -> None:
        entries = steps()
        entries[0]["timeout_sec"] = 0
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "timeout"):
            verify.load_config(self.config, self.root)

    def test_unknown_config_key_disallowed(self) -> None:
        self.write_config(steps(), disable_all_checks=True)
        with self.assertRaisesRegex(verify.ConfigurationError, "Unexpected"):
            verify.load_config(self.config, self.root)

    def test_bad_category_type_disallowed(self) -> None:
        entries = steps()
        entries[0]["category"] = ["tests"]
        self.write_config(entries)
        with self.assertRaisesRegex(verify.ConfigurationError, "Invalid category"):
            verify.load_config(self.config, self.root)

    def test_quick_requires_tests_not_only_full(self) -> None:
        entries = steps()
        entries[0]["tier"] = "full"
        with self.assertRaisesRegex(verify.ConfigurationError, "tests step"):
            verify.selected_steps(entries, "quick")

    def test_all_platform_examples_are_valid_configuration_templates(self) -> None:
        project = Path(__file__).resolve().parent.parent
        examples = sorted((project / "examples").glob("*.json"))
        self.assertGreaterEqual(len(examples), 8)
        for example in examples:
            with self.subTest(example=example.name):
                configured = verify.load_config(example, project)
                self.assertTrue(verify.selected_steps(configured, "quick"))
                self.assertTrue(verify.selected_steps(configured, "full"))


class ExecutionTests(unittest.TestCase):
    def test_passing_step(self) -> None:
        result = verify.run_step(step("success"))
        self.assertEqual("passed", result["status"])
        self.assertEqual(0, result["exit_code"])

    def test_nonzero_exit_is_failure(self) -> None:
        result = verify.run_step(step("failure", command=["{python}", "-c", "import sys;sys.exit(7)"]))
        self.assertEqual("failed", result["status"])
        self.assertEqual(7, result["exit_code"])

    def test_missing_command_is_failure(self) -> None:
        result = verify.run_step(step("missing", command=["nonexistent_ai_guardrail_executable_2026"]))
        self.assertEqual("failed", result["status"])

    def test_timeout_is_failure(self) -> None:
        entry = step("timeout", command=["{python}", "-c", "import time;time.sleep(5)"])
        entry["timeout_sec"] = 1
        result = verify.run_step(entry)
        self.assertEqual("timeout", result["status"])

    def test_dry_run_does_not_execute_commands_or_write_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entries = steps()
            marker = root / "created.txt"
            entries[0]["command"] = ["{python}", "-c", f"open({str(marker)!r}, 'w').close()"]
            (root / "verification.json").write_text(json.dumps({"schema_version": 1,
                                                                 "steps": entries}), encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(0, verify.main(["--dry-run"], root))
            self.assertFalse(marker.exists())
            self.assertFalse((root / "reports/verification-report.json").exists())

    def test_failed_step_causes_nonzero_main_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entries = steps()
            entries[0]["command"] = ["{python}", "-c", "import sys;sys.exit(9)"]
            (root / "verification.json").write_text(json.dumps({"schema_version": 1,
                                                                 "steps": entries}), encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(1, verify.main(["--mode", "full"], root))
            report = json.loads((root / "reports/verification-report.json").read_text(encoding="utf-8"))
            self.assertFalse(report["all_passed"])
            self.assertEqual(1, report["failed_steps"])

    def test_report_cannot_overwrite_project_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = json.dumps({"schema_version": 1, "steps": steps()})
            (root / "verification.json").write_text(data, encoding="utf-8")
            with redirect_stderr(StringIO()):
                self.assertEqual(2, verify.main(["--report", "verification.json"], root))
            self.assertEqual(data, (root / "verification.json").read_text(encoding="utf-8"))


class SecretScanTests(unittest.TestCase):
    def test_constructed_example_token_is_detected(self) -> None:
        token = "ghp_" + ("a" * 36)
        self.assertIn("github-token", scan_secrets.scan_text("x=" + token))

    def test_plain_english_is_not_secret(self) -> None:
        self.assertEqual([], scan_secrets.scan_text("Never put your API key in source code."))


if __name__ == "__main__":
    unittest.main()
