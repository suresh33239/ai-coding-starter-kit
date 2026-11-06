#!/usr/bin/env python3
"""Offline, platform-neutral localization audit and approval exchange.

This script handles a flat JSON interchange catalog, not native app resources.
It NEVER edits an app's Android/iOS/web resource files. Project adapters must
be reviewed before approved catalog entries are imported into those files.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys


BRACE = re.compile(r"\{[A-Za-z_][\w.]*\}")
PRINTF = re.compile(r"(?<!%)%(?:\d+\$)?[-+#0 ]*\d*(?:\.\d+)?[diouxXfFeEgGsca@]")


class ReviewError(ValueError):
    """A review input or output location cannot be trusted."""


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReviewError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReviewError(f"Cannot read valid UTF-8 JSON: {path.name} ({type(exc).__name__})") from exc
    if not isinstance(data, dict):
        raise ReviewError("JSON document must be an object")
    return data


def validate_catalog(data: dict) -> tuple[str, list[str], dict]:
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ReviewError("Catalog requires schema_version: 1")
    base = data.get("base_locale")
    strings = data.get("strings")
    if not isinstance(base, str) or not base or not isinstance(strings, dict):
        raise ReviewError("Catalog requires base_locale and strings objects")
    if base not in strings or not isinstance(strings[base], dict) or not strings[base]:
        raise ReviewError("Base locale must have a nonempty flat strings object")
    for locale, mapping in strings.items():
        if not isinstance(locale, str) or not locale or not isinstance(mapping, dict):
            raise ReviewError("Each locale must contain a flat strings object")
        if any(not isinstance(k, str) or not k or not isinstance(v, str) for k, v in mapping.items()):
            raise ReviewError(f"Non-string or nested translation in {locale}; convert with a project adapter")
    if any(not text.strip() for text in strings[base].values()):
        raise ReviewError("Base strings must not be blank")
    locales = data.get("target_locales", [locale for locale in strings if locale != base])
    if not isinstance(locales, list) or not locales or any(not isinstance(x, str) or not x or x == base for x in locales):
        raise ReviewError("target_locales must list at least one non-base locale")
    if len(set(locales)) != len(locales):
        raise ReviewError("target_locales has duplicate locale entries")
    risk = data.get("high_risk_keys", [])
    if not isinstance(risk, list) or any(not isinstance(k, str) for k in risk):
        raise ReviewError("high_risk_keys must be a list of string keys")
    return base, locales, strings


def placeholders(text: str) -> list[str]:
    return sorted(BRACE.findall(text) + PRINTF.findall(text))


def audit(data: dict) -> tuple[dict, dict]:
    base, locales, strings = validate_catalog(data)
    stamp = datetime.now(timezone.utc).isoformat()
    fingerprint = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                          separators=(",", ":")).encode("utf-8")).hexdigest()
    entries = []
    counts = []
    extras = []
    base_keys = strings[base]
    for locale in locales:
        translated = strings.get(locale, {})
        count = 0
        issues_count = 0
        for key, source in base_keys.items():
            value = translated.get(key, "")
            issues = []
            if not value.strip():
                issues.append("missing translation")
            else:
                count += 1
            if placeholders(source) != placeholders(value):
                issues.append("placeholder mismatch")
            if value.strip() and value == source:
                issues.append("same as base (may be intentional)")
            if key in data.get("high_risk_keys", []):
                issues.append("high-risk wording needs human review")
            if "plural," in source or "select," in source or "<" in source:
                issues.append("complex formatting/markup needs manual review")
            issues_count += bool(issues)
            entries.append({
                "id": f"{locale}::{key}", "locale": locale, "key": key,
                "source": source, "translation": value, "status": "pending",
                "issues": issues,
                "auto_eligible": bool(value.strip()) and not issues,
            })
        unmatched = sorted(set(translated) - set(base_keys))
        if unmatched:
            extras.append({"locale": locale, "keys": unmatched})
        counts.append({"locale": locale, "total": len(base_keys),
                       "nonempty_drafts": count, "entries_with_warnings": issues_count,
                       "missing": len(base_keys) - count, "unmatched_keys": len(unmatched)})
    bundle = {"schema_version": 1, "base_locale": base, "catalog_fingerprint": fingerprint,
              "created_utc": stamp, "entries": entries}
    report = {"schema_version": 1, "created_utc": stamp, "base_locale": base,
              "catalog_fingerprint": fingerprint, "summary": counts, "unmatched": extras,
              "note": "Nonempty and format checks do not establish translation accuracy. No app files were modified."}
    return bundle, report


def apply_decisions(catalog: dict, payload: dict) -> tuple[dict, int]:
    base, locales, strings = validate_catalog(catalog)
    bundle, _ = audit(catalog)
    if payload.get("schema_version") != 1 or payload.get("catalog_fingerprint") != bundle["catalog_fingerprint"]:
        raise ReviewError("Decisions are stale or do not belong to this catalog; run audit again")
    decisions = payload.get("decisions")
    if not isinstance(decisions, list):
        raise ReviewError("Review decisions must be an array")
    expected = {(x["locale"], x["key"]): x for x in bundle["entries"]}
    updated = deepcopy(catalog)
    changed = 0
    seen = set()
    for item in decisions:
        if not isinstance(item, dict):
            raise ReviewError("Each decision must be an object")
        pair = (item.get("locale"), item.get("key"))
        if pair in seen or pair not in expected:
            raise ReviewError("Duplicate or unknown decision locale/key")
        seen.add(pair)
        original = expected[pair]
        if item.get("id") != original["id"] or item.get("source") != original["source"]:
            raise ReviewError("Decision ID/source mismatch")
        status = item.get("status")
        if status not in ("pending", "approved", "rejected"):
            raise ReviewError("Invalid decision status")
        if status != "approved":
            continue
        text = item.get("translation")
        if not isinstance(text, str) or not text.strip():
            raise ReviewError("Cannot approve a blank translation")
        if placeholders(text) != placeholders(original["source"]):
            raise ReviewError(f"Placeholder mismatch in {original['id']}")
        if updated["strings"].setdefault(pair[0], {}).get(pair[1]) != text:
            updated["strings"][pair[0]][pair[1]] = text
            changed += 1
    return updated, changed


def output_path(value: str, root: Path, folder: str) -> Path:
    path = (root / value).resolve()
    if (not path.is_relative_to(root) or
            not path.is_relative_to((root / folder).resolve()) or path.suffix.lower() != ".json"):
        raise ReviewError(f"Output must be a JSON file within {folder}/")
    return path


def save(path: Path, data: dict, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise ReviewError(f"File exists: {path} (use --overwrite for generated output)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None, root: Path | None = None) -> int:
    root = (root or Path.cwd()).resolve()
    parser = argparse.ArgumentParser(description="Audit or apply decisions to a portable JSON localization catalog")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("audit", help="Create a report and browser-review bundle without editing app resources")
    check.add_argument("--catalog", required=True)
    check.add_argument("--report", default="reports/localization-audit.json")
    check.add_argument("--bundle", default="localization/review-bundle.json")
    check.add_argument("--overwrite", action="store_true")
    change = commands.add_parser("apply", help="Create a NEW approved interchange catalog; never edit an app resource")
    change.add_argument("--catalog", required=True)
    change.add_argument("--decisions", required=True)
    change.add_argument("--output", default="localization/approved-catalog.json")
    change.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        catalog = read_json((root / args.catalog).resolve())
        if args.command == "audit":
            bundle, report = audit(catalog)
            report_file = output_path(args.report, root, "reports")
            bundle_file = output_path(args.bundle, root, "localization")
            if report_file == bundle_file or (not args.overwrite and (report_file.exists() or bundle_file.exists())):
                raise ReviewError("Generated output exists or paths overlap; use --overwrite only after review")
            save(report_file, report, args.overwrite)
            save(bundle_file, bundle, args.overwrite)
            print(f"AUDIT: {len(bundle['entries'])} entries; report {report_file}; review bundle {bundle_file}")
        else:
            decisions_file = (root / args.decisions).resolve()
            result, changed = apply_decisions(catalog, read_json(decisions_file))
            output = output_path(args.output, root, "localization")
            if output in ((root / args.catalog).resolve(), decisions_file):
                raise ReviewError("Refusing to replace source catalog or decisions file")
            save(output, result, args.overwrite)
            print(f"PREVIEW: {changed} approved translations updated in {output}; app resources unchanged")
        return 0
    except ReviewError as exc:
        print(f"LOCALIZATION ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
