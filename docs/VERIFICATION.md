# Verification model

The runner uses Python 3.11+ with **only the standard library**. Wrapper scripts work on Windows PowerShell and POSIX shells and delegate to the same implementation.

## Commands

```text
python scripts/verify.py --mode quick --dry-run
python scripts/verify.py --mode quick
python scripts/verify.py --mode full
python scripts/verify.py --mode full --report reports/custom-report.json
```

`quick` runs only steps marked `quick`. It is suitable for ordinary focused iteration. `full` runs both `quick` and `full` steps **after an approved major stage or for a release candidate**—it should not be run after every small prompt. It does **not** mean every possible platform test exists; only configured steps can be claimed. `--dry-run` validates configuration and lists commands but runs nothing.

Each step needs a `name`, one of four baseline `category` values (`tests`, `lint`, `security`, `architecture`), a `tier`, an argument-array `command`, and a `timeout_sec`. A `build` or `other` category is also allowed for extra steps. Configuration must include all four baseline categories and at least one `tests` step. The runner refuses duplicate names, unknown keys, missing checks, unsupported placeholders, invalid working directories, and invalid commands. Configured steps are **never silently skipped**. If the platform cannot run a step, create a **separate platform-specific configuration and job** rather than making it pass by omission.

Example:

```json
{
  "schema_version": 1,
  "steps": [
    {"name":"unit","category":"tests","tier":"quick","command":["{python}","-m","unittest","discover","-s","tests"],"timeout_sec":120}
  ]
}
```

This illustrative fragment is **not valid as a complete configuration** until the other three baseline categories are added. Run `--dry-run` after editing.

The only placeholder is `{python}`, replaced by the interpreter currently running the verifier. Commands are passed as argument arrays **without a shell**. Nevertheless, they can execute arbitrary tools/scripts, so owners must review `verification.json` and invoked scripts before granting run permission.

`reports/verification-report.json` records one result per executed step and a summary; a nonzero exit, missing command, or timeout makes the overall verification fail. The runner only writes report files **inside `reports/`**. It does not persist raw command output (which might contain private information), so an owner-authorized diagnostic rerun may be needed for failures. The runner continues after ordinary failures to collect the remaining evidence. Review the report before changes are merged. Generated reports stay Git-ignored unless the owner explicitly chooses to publish a sanitized copy.

## Baseline and regression checks

- Unit/integration tests should retain meaningful assertions and coverage; test **count alone** cannot prove quality.
- Where a framework exposes stable test counts, an app-specific adapter may compare them to an owner-approved baseline. Do not auto-increase or silently lower baselines.
- Compile/build, lint/static analysis, architecture boundaries, secret scans, migration checks, platform tests, accessibility, and physical-device verification belong in the app's **own** configuration and release checklist.
- A local full pass does not replace CI, production configuration review, or physical-device testing.

## Platform nuance

Android Gradle tasks vary by module and build variant; iOS builds require macOS and Xcode; Windows desktop builds may need Windows SDK; Linux desktop builds may need system packages; Web requires its runtime and package manager. Never treat a missing SDK as a passing check.
