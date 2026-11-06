# Verification model

The runner uses Python 3.11+ with **only the standard library**. Wrapper scripts work on Windows PowerShell and POSIX shells and delegate to the same implementation.

## Using this in your own app (no coding knowledge needed)

The **verification engine** (`scripts/verify.py`, `.ps1` and `.sh`) is reusable. The checked-in **`verification.json` is NOT a universal test suite**: it tests the files and Python tools in this starter kit. `scripts/check_template.py` and the kit's own test files are also specific to this repository.

If you type `Start` with your real project open, the AI agent should:

1. **Look first:** Detect the project's platform, language, build tools, operating system, current tests, and any working checks. Reuse what already exists.
2. **Explain the proposal:** Choose an example from `examples/`, list the actual app checks to set up (quick versus major-stage), flag missing tests/tools, estimate time/cost, and ask the owner before editing.
3. **Set it up after approval:** Create or adapt `verification.json` with real commands for this project and OS. Never copy the kit's default checks unchanged. Keep existing build scripts and tests intact.
4. **Preview, then check:** Run `--mode quick --dry-run` first. That only lists what would run. After owner approval, run a focused check and record the result in `reports/`.
5. **Report honestly:** A missing SDK, absent task or unsupported platform is **Blocked / Not tested**—not a pass. Recommend only the minimum additional tests needed now. Save larger checks for approved milestones.

Android example: macOS/Linux typically use `./gradlew`; Windows uses `gradlew.bat` from the project folder. See `examples/android-gradle.json` and `examples/android-gradle-windows.json`. Both are **examples requiring confirmation of actual project tasks**. iOS builds and simulator tests generally require macOS/Xcode. The assistant should handle these details; don't ask a beginner to guess.

## Commands

```text
python scripts/verify.py --mode quick --dry-run
python scripts/verify.py --mode quick
python scripts/verify.py --mode full
python scripts/verify.py --mode full --report reports/custom-report.json
```

`quick` runs only steps marked `quick`. It is suitable for ordinary focused iteration. `full` runs both `quick` and `full` steps **after an approved major stage or for a release candidate**—it should not be run after every small prompt. It does **not** mean every possible platform test exists; only configured steps can be claimed. `--dry-run` validates configuration and lists commands but runs nothing.

**When a focused check fails:** identify whether the failure was caused by this task, is pre-existing, or is unrelated. Fix confirmed in-scope regressions and rerun their affected checks. Report unrelated or historical failures with evidence and ask before expanding into a separate repair. Do not chase flaky tests or repeatedly verify unchanged components merely to obtain a green result. Never suppress, weaken, delete or quietly skip a valid failing test. A focused pass is **not** a claim that full integration, every platform, or a physical device was tested.

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
- For multi-module or multi-package projects, have the agent list the actual testable components and compare them with configured verification steps. Every relevant component must be covered, or explicitly reported **Not tested** with a reason. A passed test task for one module is not proof that the others ran. Do not import a Gradle-only module registry into an unrelated app.
- Where a framework exposes stable test counts, an app-specific adapter may compare **fresh results** with an owner-approved baseline. Detect zero tests, missing results, unexpected count drops and skipped suites; do not trust stale test-result files or a cached build as proof that tests executed now. Test counts are a tripwire, not a quality score. A deliberate reduction is possible with owner approval and documented stronger replacement coverage.
- Important bug fixes should have a focused regression test for the actual failure path where feasible. For apps storing data, consider unreadable/corrupt data, interrupted saves, failed recovery, older formats and access isolation **when relevant**; use synthetic fixtures rather than real user records.
- Compile/build, lint/static analysis, architecture boundaries, secret scans, migration checks, platform tests, accessibility, and physical-device verification belong in the app's **own** configuration and release checklist.
- A local full pass does not replace CI, production configuration review, or physical-device testing.

## Platform nuance

Android Gradle tasks vary by module and build variant; iOS builds require macOS and Xcode; Windows desktop builds may need Windows SDK; Linux desktop builds may need system packages; Web requires its runtime and package manager. Never treat a missing SDK as a passing check.
