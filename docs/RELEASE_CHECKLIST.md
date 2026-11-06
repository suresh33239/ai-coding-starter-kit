# Human release checklist

Release is a separate owner decision; passing `verify.py` never deploys anything.

Record actual evidence and the final owner verdict in `RELEASE_READINESS.md`. **For personal-only, non-published and test projects, mark store/marketing requirements Not applicable**; do not invent a release ceremony.

- [ ] Scope, release notes, and acceptance criteria approved.
- [ ] Source diff reviewed; no unrelated or unexplained edits.
- [ ] Feature/gap/issue review recorded in `QUALITY_REVIEW.md` (or justified Not applicable).
- [ ] Open release blockers checked against `BLOCKERS.md`; unresolved P0/P1 and accepted limitations disclosed.
- [ ] CI checks green on **relevant target platforms**; no hidden skips.
- [ ] Actual testable components and modules are covered, or missing/zero/skipped results are disclosed and accepted.
- [ ] Full configured verification completed with a report.
- [ ] Sensitive dependencies, licenses, secrets, and permissions reviewed.
- [ ] Privacy policy, data collection, backup/restore, deletion, and recovery checked where relevant.
- [ ] Migrations tested with representative **non-production** data; rollback/recovery plan verified.
- [ ] Performance, accessibility, localization, and UI tested where relevant.
- [ ] The **actual distribution artifact** opens/launches and completes its primary user journey on at least one relevant real device/browser/OS; a successful compile/package alone is not enough.
- [ ] When installation and user data are relevant, clean install, upgrade from an older version, interrupted use and backup/restore/recovery were tested or clearly documented as untested. Use synthetic data and preserve existing user data.
- [ ] Version, signing identity, environment, destination, and release account verified.
- [ ] Owner explicitly approves **this** build and **this** target.
- [ ] Post-release monitoring and recovery responsibility assigned.
