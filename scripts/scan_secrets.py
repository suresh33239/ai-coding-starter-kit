#!/usr/bin/env python3
"""Small high-confidence credential pattern scanner, not a complete scanner."""

from pathlib import Path
import os
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "build", "dist", ".gradle",
    "target", "bin", "obj", "artifacts", "__pycache__", ".idea", ".next",
}
SENSITIVE_FILENAME = re.compile(r"^\.env(?:\..+)?$", re.IGNORECASE)
PATTERNS = {
    "private-key-header": re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"(?:ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{36}"),
    "github-fine-grained-token": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    "aws-access-key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "google-api-key": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    "openai-project-key": re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}"),
}


def scan_text(content: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if pattern.search(content)]


def main() -> int:
    flagged = 0
    scanned = 0
    for folder, subfolders, filenames in os.walk(ROOT, followlinks=False):
        subfolders[:] = [name for name in subfolders
                         if name not in SKIP_DIRS and not (Path(folder) / name).is_symlink()]
        for filename in filenames:
            path = Path(folder) / filename
            if path.is_symlink():
                continue
            relative = path.relative_to(ROOT)
            if SENSITIVE_FILENAME.match(path.name) and path.name != ".env.example":
                print(f"POTENTIAL SECRET FILE: {relative} (content not displayed)")
                flagged += 1
            try:
                size = path.stat().st_size
                if size > 5 * 1024 * 1024:
                    print(f"UNSCANNED LARGE FILE: {relative}")
                    flagged += 1
                    continue
                raw = path.read_bytes()
                if b"\x00" in raw[:4096]:  # likely binary; use a dedicated artifact scanner
                    continue
                content = raw.decode("utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            scanned += 1
            for finding in scan_text(content):
                flagged += 1
                print(f"POTENTIAL SECRET: {relative} ({finding}; value not displayed)")
    print(f"Basic secret scan: {scanned} text files inspected; {flagged} warning(s)")
    return 1 if flagged else 0


if __name__ == "__main__":
    raise SystemExit(main())
