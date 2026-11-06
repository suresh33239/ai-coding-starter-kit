# Review translations in one place

This folder contains a **standalone offline review page**. It does not send translations to a server or modify an app just because a button is clicked. It works on Windows, macOS and Linux in a modern browser. For Android/iOS/browser extensions, use this review workflow **alongside** the project's native translation files and tooling.

## A simple five-step workflow

1. Ask your AI agent to **audit the existing app's localization resources read-only** and create a *flat JSON interchange catalog* (same structure as `sample-catalog.json`) with the base language, chosen target languages and existing candidate translations. The sample is for format demonstration **only**, not real translations. The AI must preserve native plurals, markup and placeholders; complex resource types require a project-specific conversion step, not a silent guess.
2. From the **project root**, run:

   ```text
   python scripts/localization_review.py audit --catalog localization/your-catalog.json
   ```

   This produces `reports/localization-audit.json` (coverage, missing entries and warnings) plus `localization/review-bundle.json` (review candidates). To intentionally replace previously generated outputs, add `--overwrite`.
3. Open `localization/review.html` in a browser. **Choose file → `review-bundle.json`**, filter/search, edit candidate text, and approve or reject each. Use **Approve all**, **Reject all**, or **Auto-approve format-safe** for the current filter. Auto-approval checks only mechanical issues; it cannot validate meaning. High-risk and flagged entries require manual review. Export the full **decisions JSON**.
4. Save that file at `localization/review-decisions.json`, then run:

   ```text
   python scripts/localization_review.py apply --catalog localization/your-catalog.json --decisions localization/review-decisions.json
   ```

   This writes a **new** `localization/approved-catalog.json`, leaving your source catalog and actual application untouched. If the catalog changed after review, the tool rejects stale decisions. Invalid/missing placeholders also block approved entries.
5. Ask the AI to show you the proposed import diff **using your app's existing localization system** (Android XML, Apple String Catalog, web JSON, etc.), run syntax and UI checks, and **wait for permission** before editing production resource files. Record human/UI findings in `localization/LOCALE_AUDIT.md`, technical gaps in `QUALITY_REVIEW.md` and release-relevant evidence in `RELEASE_READINESS.md`.

## Coverage and limitations

- The catalog format is JSON with `base_locale`, `target_locales`, and `strings` mapping each locale to **simple string keys**. It can represent many platforms but is **not a drop-in Android XML, Apple `.xcstrings`, or other native resource parser**. Keep an explicit reviewed adapter for your application's format.
- Nested JSON, ICU plural/select rules, arrays and rich markup must be handled by the app adapter or separately reviewed. Do not flatten them into incorrect translations. Auto-approval refuses obvious complex-format and high-risk entries.
- The tool checks blank drafts, mismatched common `{name}`/`%s`/`%1$s`/`%@` placeholders, identical-to-base text, and declared high-risk keys. A technically valid sentence can still be culturally or linguistically wrong.
- Audit counts represent **nonempty drafts**, not independently verified translations. All candidate strings and generated review decisions are Git-ignored; inspect carefully before sharing.
- No installation, cloud service, or external JavaScript library is needed. The page runs locally and exports an ordinary JSON file for a later owner-approved import.
