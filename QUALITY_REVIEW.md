# Independent quality review — reusable template

**Not reviewed yet.** This file is a checklist and findings register, **not evidence that an app passed an audit**. Use for major milestones, substantial changes, a suspected regression, or release preparation—not every prompt.

## Review setup

| Item | Answer |
| --- | --- |
| Project and version / commit | TBD |
| Date, reviewer, review scope | TBD |
| Review mode | Independent fresh review / Follow-up / Targeted |
| Approved requirements and acceptance criteria | Links or Not available |
| Platforms, builds, devices and locales actually assessed | Not assessed |
| Methods and tools | Not assessed |
| What could **not** be inspected or tested | Not assessed |

## Independence and evidence rules

1. Begin from the **current code, agreed requirements and observed behavior**. Prior audits, AI completion claims, roadmaps and comments are **leads, not proof**. Make fresh observations before adopting their conclusions.
2. Do not prime the reviewer with a list of expected findings. Where feasible, have someone other than the implementer review; if the same AI is reviewing its own changes, **disclose that limitation** rather than calling the review fully independent.
3. Use separate labels for **Verified**, **Observed but not fully tested**, **Inferred**, **Unverified** and **Not applicable**. Provide exact paths, screen steps, test output and/or sanitized screenshots as evidence.
4. Look for missing and incomplete behavior, not only crashes, errors or failed tests. Compare **intended requirements against working user journeys**.
5. Work read-only unless the owner explicitly approves fixes. Findings belong here; authorized generated reports go in `reports/`, local diagnostic logs in `logs/`, screenshots in `screenshots/`.
6. Recheck important fixes with independent reproduction or focused tests. Never change status to Fixed merely because an AI says it changed code.

## Review coverage

| Area | Questions to check | Status / evidence |
| --- | --- | --- |
| Feature audit | Are approved features actually present, discoverable and usable? | Not assessed |
| Gap audit | Are requirements absent, contradicted or delivered only partly? | Not assessed |
| Issue audit | Are reported defects reproducible, duplicated, regressed or unresolved? | Not assessed |
| Missing/incomplete | Placeholder screens, no-op buttons, unfinished flows, incorrect defaults? | Not assessed |
| UI and accessibility | Navigation, scroll, screen sizes, keyboard, readable text, accessibility? | Not assessed |
| Data and security | Storage, migration, backups, recovery, encryption, permissions, privacy? | Not assessed |
| Compatibility | Supported OS/device/browser, upgrades, offline behavior, integrations? | Not assessed |
| Localization | Keys, coverage, placeholders, language switching, layouts, meaning? | Not assessed / See `LOCALIZATION.md` |
| Tests and release | Evidence, unknowns, build variants, releases and rollback? | Not assessed |

## Feature inventory versus requirements

Use **one row per important user-facing behavior**, not a row for every code function. Link the approved requirement or mark it unconfirmed. Status is **Missing / Incomplete / Implemented not tested / Verified / Not applicable**.

| ID | Requirement / expected behavior | Actual observation | Status | Evidence / missing step | Owner decision |
| --- | --- | --- | --- | --- | --- |
| F-001 | Example only: a user can save an item | Not checked | Implemented not tested | No evidence yet | Review required |

## Findings — issues, gaps and regressions

Assign stable IDs `Q-001`, `Q-002`... and prioritize by impact; do not invent severity or claim a fix without reproducing it. Add P0/P1 items that block the accepted release to `BLOCKERS.md`; use `BACKLOG.md` for approved normal work.

| ID | Priority | Type | Evidence / reproduction | Impact | Proposed smallest fix | Status / retest |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | — | No review performed | Unknown | Review first | Pending |

## Outcome and follow-up

- **Coverage:** What was checked and what remains untested? TBD
- **Critical or major risks:** TBD (not automatically "none")
- **Recommendation:** Proceed / Adjust / Defer / Stop release until resolved — **Not assessed**
- **Owner-approved deferrals and justification:** TBD
- **Follow-up reviewer, evidence and date:** TBD

This review never itself authorizes a code change, release or feature expansion.
