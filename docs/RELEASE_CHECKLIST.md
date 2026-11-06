# Human release checklist

Release is a separate owner decision; passing `verify.py` never deploys anything.

Record actual evidence and the final owner verdict in `RELEASE_READINESS.md`. **For personal-only, non-published and test projects, mark store/marketing requirements Not applicable**; do not invent a release ceremony.

- [ ] Scope, release notes, and acceptance criteria approved.
- [ ] Source diff reviewed; no unrelated or unexplained edits.
- [ ] CI checks green on **relevant target platforms**; no hidden skips.
- [ ] Full configured verification completed with a report.
- [ ] Sensitive dependencies, licenses, secrets, and permissions reviewed.
- [ ] Privacy policy, data collection, backup/restore, deletion, and recovery checked where relevant.
- [ ] Migrations tested with representative **non-production** data; rollback/recovery plan verified.
- [ ] Performance, accessibility, localization, and UI tested where relevant.
- [ ] Upgrade/install and real-device checks completed for shipped targets.
- [ ] Version, signing identity, environment, destination, and release account verified.
- [ ] Owner explicitly approves **this** build and **this** target.
- [ ] Post-release monitoring and recovery responsibility assigned.
