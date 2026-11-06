# Localization from the foundation, without translating everything at once

Localize the **architecture** from the beginning; translate additional languages when there is a real user need and a review plan. Retrofitting hard-coded text late can be expensive, but translating every hypothetical locale on day one is also wasteful.

## Foundation rules

- Keep all user-visible strings in one framework-appropriate resource system: e.g. Android string resources, Apple string catalogs, or web i18n catalogs.
- Use stable descriptive keys, plural/quantity support, format placeholders, and reusable text. Never concatenate translated sentence fragments.
- Use locale-aware dates, numbers, currency, sorting, measurements, units and time zones where relevant. Keep **stored data** locale-neutral.
- Plan for longer strings, different scripts, right-to-left layouts, accessibility labels, and text scaling.
- Make the base language complete before scaling. Add only priority locales approved for the release.
- Machine translation is a draft: validate placeholders, XML/JSON syntax, truncation, meaning, and especially safety, finance, privacy and medical language. Be transparent when native-language review is unavailable.
- Keep translation scope tied to accepted features; do not translate obsolete or unapproved screens.

## Localization plan

| Item | Decision |
| --- | --- |
| Base language | TBD |
| Launch locales | TBD |
| Later locales | TBD |
| Translation method and review capacity | TBD |
| Locale formatting and RTL testing | TBD |
| Language switch / fallback behavior | TBD |

**Stage checkpoints:** (1) extracted resources and base strings; (2) priority launch translations; (3) focused UI and functional checks; (4) release validation. Do not hold up a usable prototype to fully translate every possible language.

## Localization review, when a project uses multiple languages

At an approved localization milestone and before releasing supported locales, run a **read-only localization audit**. Cover the base catalog and chosen target locales, missing keys, extra/obsolete keys, duplicates, untranslated drafts, placeholders, plurals/markup, layout and language-switching behavior. Confirm the actual app resource format and OS/build requirements before choosing an adapter. Record **tested**, **inferred** and **not linguistically reviewed** separately.

The reusable offline workflow in [`localization/README.md`](localization/README.md) provides:

- A standard JSON interchange for approved simple strings and a Python coverage/placeholder audit (`scripts/localization_review.py`). Reports go to `reports/` and candidate files to `localization/`.
- A local browser page (`localization/review.html`) to edit translations, approve/reject individually, **approve all**, **reject all**, or **auto-approve entries with no detected format warnings**. Filter by locale, text and review status; export decisions once for all languages.
- A separate **reviewed proposed catalog** generated from those decisions. An AI agent must show the diff and obtain approval before importing it into native Android/iOS/web/desktop resource files. The kit does not claim to modify those formats directly.

**Auto-approval is never proof of language accuracy.** It must not silently approve high-risk wording or formatting warnings. An approved bulk decision is a review decision, not a release verdict. Run project-native checks and actual UI tests after an authorized import; unresolved issues belong in `QUALITY_REVIEW.md` and `BLOCKERS.md` when release-blocking.

Record the manual, UI, fallback and linguistic review in [`localization/LOCALE_AUDIT.md`](localization/LOCALE_AUDIT.md). This complements the generated JSON report, and must explicitly note when a language has no qualified human reviewer.
