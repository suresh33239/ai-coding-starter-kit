"""Focused checks for the offline, platform-neutral localization workflow."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import localization_review as loc  # noqa: E402


def example():
    return {
        "schema_version": 1, "base_locale": "en", "target_locales": ["te", "hi"],
        "high_risk_keys": ["privacy"],
        "strings": {
            "en": {"welcome": "Hello {name}", "save": "Save", "privacy": "Privacy"},
            "te": {"welcome": "హలో {name}", "save": "సేవ్", "privacy": "", "unused": "extra"},
            "hi": {"welcome": "नमस्ते", "save": "Save", "privacy": ""},
        },
    }


class CatalogTests(unittest.TestCase):
    def test_audit_reports_coverage_missing_placeholders_extras(self):
        bundle, report = loc.audit(example())
        self.assertEqual(6, len(bundle["entries"]))
        counts = {x["locale"]: x for x in report["summary"]}
        self.assertEqual(1, counts["te"]["missing"])
        self.assertEqual(1, counts["te"]["unmatched_keys"])
        entries = {(x["locale"], x["key"]): x for x in bundle["entries"]}
        self.assertTrue(entries[("te", "save")]["auto_eligible"])
        self.assertFalse(entries[("hi", "welcome")]["auto_eligible"])
        self.assertIn("placeholder mismatch", entries[("hi", "welcome")]["issues"])
        self.assertFalse(entries[("te", "privacy")]["auto_eligible"])

    def test_reject_nested_strings(self):
        data = example()
        data["strings"]["en"]["save"] = {"value": "Save"}
        with self.assertRaises(loc.ReviewError):
            loc.audit(data)

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "a.json"
            path.write_text('{"schema_version": 1, "schema_version": 2}', encoding="utf-8")
            with self.assertRaisesRegex(loc.ReviewError, "Duplicate"):
                loc.read_json(path)

    def test_placeholders_cover_android_swift_and_named(self):
        self.assertEqual(loc.placeholders("Hi {name}: %1$s, %@, %d"),
                         loc.placeholders("%d, %@, {name} and %1$s"))


class ReviewImportTests(unittest.TestCase):
    def decisions(self, catalog):
        bundle, _ = loc.audit(catalog)
        return {"schema_version": 1, "catalog_fingerprint": bundle["catalog_fingerprint"],
                "decisions": [{"id": e["id"], "locale": e["locale"], "key": e["key"],
                               "source": e["source"], "translation": e["translation"],
                               "status": "pending"} for e in bundle["entries"]]}

    def test_only_approved_entries_are_applied_to_new_catalog(self):
        original = example()
        data = self.decisions(original)
        chosen = next(x for x in data["decisions"] if x["locale"] == "hi" and x["key"] == "welcome")
        chosen["translation"] = "नमस्ते {name}"
        chosen["status"] = "approved"
        updated, count = loc.apply_decisions(original, data)
        self.assertEqual(1, count)
        self.assertEqual("नमस्ते {name}", updated["strings"]["hi"]["welcome"])
        self.assertEqual("नमस्ते", original["strings"]["hi"]["welcome"])

    def test_invalid_approved_placeholder_aborts_batch(self):
        original = example()
        data = self.decisions(original)
        chosen = next(x for x in data["decisions"] if x["locale"] == "hi" and x["key"] == "welcome")
        chosen["translation"] = "नमस्ते"
        chosen["status"] = "approved"
        with self.assertRaisesRegex(loc.ReviewError, "Placeholder mismatch"):
            loc.apply_decisions(original, data)

    def test_stale_decisions_are_refused(self):
        original = example()
        data = self.decisions(original)
        original["strings"]["en"]["save"] = "Save now"
        with self.assertRaisesRegex(loc.ReviewError, "stale"):
            loc.apply_decisions(original, data)

    def test_cli_uses_separate_folders_and_never_overwrites_by_default(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "localization").mkdir()
            catalog = root / "localization/catalog.json"
            catalog.write_text(json.dumps(example(), ensure_ascii=False), encoding="utf-8")
            self.assertEqual(0, loc.main(["audit", "--catalog", "localization/catalog.json"], root))
            self.assertTrue((root / "reports/localization-audit.json").is_file())
            self.assertTrue((root / "localization/review-bundle.json").is_file())
            self.assertEqual(2, loc.main(["audit", "--catalog", "localization/catalog.json"], root))
            self.assertEqual(2, loc.main(["audit", "--catalog", "localization/catalog.json",
                                          "--report", "../escape.json"], root))
            decisions = self.decisions(example())
            for item in decisions["decisions"]:
                if item["key"] == "save" and item["locale"] == "hi":
                    item["status"] = "approved"
                    item["translation"] = "सहेजें"
            (root / "localization/review-decisions.json").write_text(
                json.dumps(decisions, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(0, loc.main(["apply", "--catalog", "localization/catalog.json",
                                           "--decisions", "localization/review-decisions.json"], root))
            self.assertTrue((root / "localization/approved-catalog.json").exists())
            self.assertEqual(example(), json.loads(catalog.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
