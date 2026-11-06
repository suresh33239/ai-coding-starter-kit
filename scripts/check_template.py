#!/usr/bin/env python3
"""Checks the integrity of *this starter template*, not downstream apps."""

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "AGENTS.md", "README.md", "LICENSE", "verification.json",
    "START_HERE.md", "IDEA_RESEARCH.md", "FEASIBILITY.md",
    "LOCALIZATION.md", "RELEASE_READINESS.md",
    "PROJECT.md", "ROADMAP.md", "BACKLOG.md", "RELEASES.md", "AUDIT.md",
    "docs/OWNER_APPROVALS.md", "docs/OWNER_SETUP.md",
    "docs/VERIFICATION.md", "docs/PLATFORMS.md",
    "docs/RELEASE_CHECKLIST.md", "docs/DECISION_LOG.md", "docs/START_HERE_PROMPT.md",
    "scripts/verify.py", "scripts/verify.ps1", "scripts/verify.sh",
    "scripts/scan_secrets.py", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/guardrails.yml", "templates/CODEOWNERS.template",
    "templates/PROMPT_LOG.local.template.md", "templates/OWNER_LIMITS.local.template.md",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        print("Missing required starter files: " + ", ".join(missing), file=sys.stderr)
        return 1
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
    for phrase in ["owner approval", "stop", "verify", "report", "secrets"]:
        if phrase not in agents:
            print(f"AGENTS.md missing expected topic: {phrase}", file=sys.stderr)
            return 1
    if args.strict:
        workflow = (ROOT / ".github/workflows/guardrails.yml").read_text(encoding="utf-8")
        if "permissions:" not in workflow or "contents: read" not in workflow:
            print("Workflow must declare read-only repository permissions", file=sys.stderr)
            return 1
        if "pull_request_target" in workflow or "@v4\n" in workflow:
            print("Workflow security check failed", file=sys.stderr)
            return 1
    print("Template structure and basic policy checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
