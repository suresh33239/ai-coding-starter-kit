#!/usr/bin/env python3
"""Owner-reviewed, cross-platform verification command dispatcher.

Runs configured commands as argv arrays (never through a shell). It validates
the configuration, reports actual results, and fails when any check fails.
It cannot enforce owner permission to run a command: see AGENTS.md.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = {"tests", "lint", "security", "architecture", "build", "other"}
REQUIRED_CATEGORIES = {"tests", "lint", "security", "architecture"}
TIERS = {"quick", "full"}
ALLOWED_CONFIG_KEYS = {"schema_version", "steps"}
ALLOWED_STEP_KEYS = {"name", "category", "tier", "command", "timeout_sec", "cwd"}


class ConfigurationError(ValueError):
    """A configuration is missing or unsafe/ambiguous."""


def within_root(relative_path: str, root: Path = ROOT) -> Path:
    """Resolve a repository-relative path, rejecting traversal and symlinks out."""
    if not isinstance(relative_path, str) or not relative_path:
        raise ConfigurationError("Path must be a nonempty string")
    if Path(relative_path).is_absolute():
        raise ConfigurationError("Absolute paths are not permitted: " + relative_path)
    result = (root / relative_path).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ConfigurationError("Path escapes repository: " + relative_path)
    return result


def load_config(config_path: Path, root: Path = ROOT) -> list[dict[str, Any]]:
    if not config_path.is_file():
        raise ConfigurationError(f"Configuration not found: {config_path}")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"Could not read configuration: {exc}") from exc
    if not isinstance(config, dict) or set(config) - ALLOWED_CONFIG_KEYS:
        raise ConfigurationError("Unexpected top-level verification configuration keys")
    if type(config.get("schema_version")) is not int or config["schema_version"] != 1:
        raise ConfigurationError("Only schema_version=1 is supported")
    steps = config.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ConfigurationError("At least one verification step is required")
    names: set[str] = set()
    categories: set[str] = set()
    for index, step in enumerate(steps):
        if not isinstance(step, dict) or set(step) - ALLOWED_STEP_KEYS:
            raise ConfigurationError(f"Unexpected fields in step {index}")
        name = step.get("name")
        if not isinstance(name, str) or not name.strip() or len(name) > 100:
            raise ConfigurationError(f"Invalid step name at index {index}")
        if name in names:
            raise ConfigurationError(f"Duplicate step name: {name}")
        names.add(name)
        category = step.get("category")
        tier = step.get("tier")
        if (not isinstance(category, str) or not isinstance(tier, str) or
                category not in CATEGORIES or tier not in TIERS):
            raise ConfigurationError(f"Invalid category/tier for {name}")
        categories.add(category)
        command = step.get("command")
        if (not isinstance(command, list) or not command or
                not all(isinstance(arg, str) and bool(arg) for arg in command)):
            raise ConfigurationError(f"Step {name} must have a nonempty argv-array command")
        for arg in command:
            if "{" in arg or "}" in arg:
                if arg != "{python}":
                    raise ConfigurationError(f"Unknown command placeholder in step {name}: {arg}")
        timeout = step.get("timeout_sec")
        if type(timeout) is not int or not 1 <= timeout <= 3600:
            raise ConfigurationError(f"Invalid timeout_sec for step {name} (1–3600)")
        cwd = step.get("cwd", ".")
        directory = within_root(cwd, root)
        if not directory.is_dir():
            raise ConfigurationError(f"Working directory does not exist for step {name}: {cwd}")
    missing = REQUIRED_CATEGORIES - categories
    if missing:
        raise ConfigurationError("Missing required check categories: " + ", ".join(sorted(missing)))
    return steps


def selected_steps(steps: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    if mode not in TIERS:
        raise ConfigurationError("mode must be quick or full")
    chosen = [step for step in steps if mode == "full" or step["tier"] == "quick"]
    if not chosen or not any(step["category"] == "tests" for step in chosen):
        raise ConfigurationError(f"Mode {mode} must run at least one tests step")
    if mode == "full":
        missing = REQUIRED_CATEGORIES - {step["category"] for step in chosen}
        if missing:
            raise ConfigurationError("Full mode missing: " + ", ".join(sorted(missing)))
    return chosen


def argv_for(step: dict[str, Any]) -> list[str]:
    return [sys.executable if argument == "{python}" else argument
            for argument in step["command"]]


def run_step(step: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    command = argv_for(step)
    cwd = within_root(step.get("cwd", "."), root)
    start = time.monotonic()
    outcome = "failed"
    code: int | None = None
    detail = ""
    try:
        # No shell. Output is discarded to avoid memory exhaustion and leaking
        # potential tokens in logs/reports. Command side effects still depend
        # on the owner's approval of the underlying project scripts.
        result = subprocess.run(
            command, cwd=cwd, timeout=step["timeout_sec"],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False,
        )
        code = result.returncode
        if code == 0:
            outcome = "passed"
        else:
            detail = f"Process exited with status {code}; output intentionally not persisted"
    except subprocess.TimeoutExpired:
        outcome = "timeout"
        detail = f"Timed out after {step['timeout_sec']} seconds"
    except OSError as exc:
        detail = f"Could not start command: {type(exc).__name__}"

    return {
        "name": step["name"],
        "category": step["category"],
        "tier": step["tier"],
        "command": command,
        "status": outcome,
        "exit_code": code,
        "duration_seconds": round(time.monotonic() - start, 3),
        "detail": detail,
    }


def main(arguments: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description="Run owner-approved configured project checks")
    parser.add_argument("--mode", choices=["quick", "full"], default="quick")
    parser.add_argument("--config", default="verification.json", help="Repo-relative JSON path")
    parser.add_argument("--report", default="artifacts/verification-report.json", help="Repo-relative report path")
    parser.add_argument("--dry-run", action="store_true", help="Print plan, do not execute checks")
    args = parser.parse_args(arguments)
    try:
        config_path = within_root(args.config, root)
        report_path = within_root(args.report, root)
        steps = selected_steps(load_config(config_path, root), args.mode)
        if not report_path.suffix.lower() == ".json":
            raise ConfigurationError("Report path must end in .json")
        if not report_path.is_relative_to((root / "artifacts").resolve()):
            raise ConfigurationError("Report path must stay under the artifacts/ folder")
    except ConfigurationError as exc:
        print(f"CONFIGURATION ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"VERIFICATION: mode={args.mode}, steps={len(steps)}")
    if args.dry_run:
        for step in steps:
            print(f"  PLAN {step['name']} [{step['category']}]: {argv_for(step)}")
        print("DRY RUN ONLY — no checks executed and no tests passed")
        return 0

    results = []
    for step in steps:
        print(f"RUN {step['name']} [{step['category']}]", flush=True)
        result = run_step(step, root)
        results.append(result)
        print(f"  {result['status'].upper()} (exit={result['exit_code']}, "
              f"{result['duration_seconds']}s) {result['detail']}", flush=True)

    success = all(item["status"] == "passed" for item in results)
    report = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "all_passed": success,
        "executed_steps": len(results),
        "passed_steps": sum(item["status"] == "passed" for item in results),
        "failed_steps": sum(item["status"] != "passed" for item in results),
        "results": results,
    }
    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"REPORT ERROR: Could not write verification report: {exc}", file=sys.stderr)
        return 3
    print("ALL CONFIGURED CHECKS PASSED" if success else "VERIFICATION FAILED")
    print(f"Report: {report_path.relative_to(root)}")
    return 0 if success else 1


if __name__ == "__main__":
    if sys.version_info < (3, 11):
        print("Python 3.11+ is required; verification did not run", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main())
