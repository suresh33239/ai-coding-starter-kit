# Active blockers and accepted deferrals

**No assessment performed yet.** An empty list is not evidence of zero blockers. Review `QUALITY_REVIEW.md`, `BACKLOG.md`, real test results and release gates first.

Use this file only for **current, actionable blockers or significant accepted risks**. Ordinary features and minor improvements belong in `BACKLOG.md`.

## Priority guide

| Priority | Meaning | Typical action |
| --- | --- | --- |
| **P0 Critical** | Data loss, security/privacy exposure, unusable core workflow or release-stopping safety issue | Stop affected release/workflow; fix and retest |
| **P1 Major** | Important approved functionality fails, severe compatibility issue or must-fix release condition | Resolve or explicitly justify a restricted/non-public outcome |
| **P2 Minor** | Limited defect with tolerable workaround | May defer with owner decision and visible limitation |
| **P3 Enhancement** | Optional improvement, not a blocker | Record in backlog, not as a release blocker |

## Live register

| ID | P0/P1/P2 | Impact and evidence | Affected platform/version | Owner / next action | Status | Retest proof / accepted deferral |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | No blocker audit performed | Not assessed | Review at next milestone | Not assessed | — |

Allowed statuses: **New / Investigating / Fix approved / In progress / Needs retest / Resolved and verified / Deferred by owner**. Record exact test/build evidence for resolution. An issue is **not resolved** merely because the code changed, a build passed or an agent declared success.

## Release decision

- Target release / scope: TBD
- Unresolved P0: Unknown
- Unresolved P1: Unknown
- Known limitations and owner-approved P2 deferrals: TBD
- Can this release proceed? **Not assessed** — update `RELEASE_READINESS.md` with evidence and owner approval.

Do not routinely mark a speculative feature as a blocker. A private learning script may have no store-related requirements; mark irrelevant gates Not applicable.
