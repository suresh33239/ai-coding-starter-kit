# Localization quality audit (human-readable)

**Not assessed.** Use only when the app has multiple supported languages. The generated `reports/localization-audit.json` covers **flat-string technical checks**; this document records additional resource, layout and language-quality evidence.

| Field | Answer |
| --- | --- |
| App version, source commit and date | TBD |
| Base language / approved target locales | TBD |
| Native resource format and import adapter | TBD |
| Reviewer(s) and actual languages they understand | TBD |
| Screen/device/platform coverage | Not tested |
| Generated technical report | Not run |

## Per-language review

| Locale | Missing / extra / obsolete keys | Placeholders, plurals and formatting | UI/layout/fallback | Meaning and sensitive wording | Verdict |
| --- | --- | --- | --- | --- | --- |
| TBD | Not audited | Not audited | Not tested | Not linguistically reviewed | Pending |

## Findings and open risks

| ID | Locale / key / screen | Evidence | Impact | Proposed correction | Approval and retest |
| --- | --- | --- | --- | --- | --- |
| — | — | No audit performed | Unknown | Audit first | Pending |

## Rules

- Run the audit on **actual resource keys** and candidate translations, not only code comments or an AI summary. Include supported fallback behavior and missing entries.
- A translation can pass placeholder checks and still be incorrect, misleading or offensive. Explicitly mark languages **Not linguistically reviewed** when no qualified reviewer is available. Do not invent approval.
- Test real device/browser screen sizes, text scaling, right-to-left layouts where relevant, and localized dates/numbers/currencies.
- Use `localization/review.html` for batch decisions and export. Convert to and from native resources only through a reviewed app-specific adapter; show a diff and get owner approval before any writes.
- Put unresolved high-impact findings into `QUALITY_REVIEW.md` and genuine release blockers into `BLOCKERS.md`. No need for a full re-audit after every string fix; retest affected locales/screens.
