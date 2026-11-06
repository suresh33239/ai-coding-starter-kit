# AI Coding Starter Kit for Beginners & Others

**Decide wisely. Build the foundation first. Keep AI—and the budget—under human control.**

An agent-agnostic, platform-neutral starter kit for human-directed software development with AI coding assistants. Designed for beginners and experienced developers alike. Suitable for Android, Windows, macOS, Linux, iOS, web apps, APIs, and mixed repositories.

This repository is a lightweight set of files—not a mandatory new agent platform or complicated development framework.

This is a **guardrails template**, not an application framework or a guarantee of security. Written AI instructions are advisory; actual enforcement requires limited credentials, independent checks, protected branches, and human review.

## What it includes

| Layer | File or mechanism | Purpose |
| --- | --- | --- |
| Starting point | `START_HERE.md` | Explain your idea and decide if, what, and how to build |
| Idea validation | `IDEA_RESEARCH.md`, `FEASIBILITY.md` | Competitors, market gaps, formats, credits, cost and time |
| Instructions | `AGENTS.md` | Research/forecast, plan, ask, implement, verify, report |
| Foundation | `PROJECT.md`, `AUDIT.md` | Understand the existing project before changing it |
| Planning | `ROADMAP.md`, `BACKLOG.md`, `RELEASES.md` | Milestones, priorities, release plans and due dates |
| Localization | `LOCALIZATION.md` | Translation-ready architecture from day one |
| Release decision | `RELEASE_READINESS.md` | Evidence-backed readiness for chosen release channel |
| Private limits | `templates/OWNER_LIMITS.local.template.md` | Budget, available credits, prompts/day and account inventory |
| Task history | `templates/PROMPT_LOG.local.template.md` | Private prompt, outcome, changed-file and test log |
| Owner decisions | `docs/OWNER_APPROVALS.md` | Permission boundaries and approval matrix |
| Verification | `scripts/verify.py`, `.ps1`, `.sh` | Cross-platform test runner; focused/full modes |
| Project adapters | `verification.json` + `examples/` | Explicit, project-specific checks; no silent skipping |
| Security | `scripts/scan_secrets.py`, `docs/SECURITY.md` | Basic local scan and secure-development practices |
| Evidence | `.github/PULL_REQUEST_TEMPLATE.md` | Plan, files, tests, risks, manual-review items |
| CI | `.github/workflows/guardrails.yml` | Basic tests on Windows, macOS, Linux |
| Enforcement | owner-configured GitHub ruleset and CODEOWNERS | Prevent merging without required checks and review |

## Quick start: copy the kit and say `Start`

1. Download or clone this repository. Open the **software project's root folder** in your AI coding tool (VS Code, Android Studio, another editor, or a CLI agent).
2. For a new project, copy the kit's root Markdown files (`AGENTS.md`, `README.md`, `START_HERE.md`, and the planning/audit Markdown files), `scripts/`, `docs/`, and `templates/` into that folder. Copy `verification.json` and relevant `examples/` only as **starting templates**. You may also start from a fresh copy of this entire repository.
3. For an existing application, copy the same guidance and templates **without overwriting your project's existing files**. Review any name conflicts (especially `AGENTS.md`, `README.md`, `.gitignore`, `.github/`, and `verification.json`) and merge deliberately. Do not replace a working project verifier or workflow with an example.
4. Ensure your AI tool is reading the project-root `AGENTS.md` (some tools do this automatically; others need it opened or explicitly attached). In its chat, type exactly:

   ```text
   Start
   ```

5. The agent should inspect the project **read-only**. For a new idea it asks you to describe what you want to build; for an existing application it first audits the project. It then researches, forecasts, asks only useful questions, and **waits for your approval before building**.

The word `Start` is an instruction defined by this kit, **not a universal built-in command** in every AI product. It works when the agent has actually read `AGENTS.md`. If it has not, tell it: *“Read the project-root AGENTS.md and START_HERE.md, then Start.”*

Do **not** copy this kit's example `.github/workflows/` into an existing app unchanged: its checks validate the starter kit, not your app. Keep your own CI and add tailored checks only after review.

## Start a brand-new idea (beginners or experts)

1. Read [START_HERE.md](START_HERE.md) and use its short opening prompt with your AI agent.
2. Tell the agent the idea in your own words. **No code yet.** It should research existing options and user feedback and suggest a proceed/adjust/defer decision using [IDEA_RESEARCH.md](IDEA_RESEARCH.md).
3. Choose a realistic form factor and pace with [FEASIBILITY.md](FEASIBILITY.md). If you want to share budgets/credit limits, copy `templates/OWNER_LIMITS.local.template.md` to private `OWNER_LIMITS.local.md` (Git-ignored).
4. Review the first useful scope and stages, including source-checked minimum toolchain versions and whether any developer accounts are really needed.
5. Only after you agree, create the project foundation, basic tests, translation-ready strings, and a small working feature. A commercial release is **optional**.

## Use in an existing project

1. Copy `AGENTS.md`, `START_HERE.md`, `PROJECT.md`, `ROADMAP.md`, `BACKLOG.md`, `RELEASES.md`, `AUDIT.md`, `IDEA_RESEARCH.md`, `FEASIBILITY.md`, `LOCALIZATION.md`, `RELEASE_READINESS.md`, `scripts/`, and relevant `docs/` into your project **as needed**; adapt template placeholders instead of inventing facts. Keep MIT license notices where required.
2. Copy `templates/PROMPT_LOG.local.template.md` to `PROMPT_LOG.local.md` in your project root, and copy the relevant `.gitignore` rules. **Do not commit the private prompt history.**
3. Tell the AI agent to **begin with a read-only project audit** and ask only important unanswered questions. See the [starter prompt](docs/START_HERE_PROMPT.md). For a substantial **new feature/product idea**, perform proportionate market research before changing the roadmap.
4. Copy the closest file from `examples/` to **`verification.json`**, then replace every sample command with a command verified to work in **your** repository. Keep the required `tests`, `lint`, `security`, and `architecture` categories or add documented equivalents.
5. Start with `python scripts/verify.py --mode quick --dry-run`. A dry run lists commands but **does not test the app**. With owner approval, run focused checks during development and reserve `--mode full` for accepted major stages or release candidates.
6. Adapt the GitHub Actions workflow for the actual tools and target operating systems. Desktop and mobile builds usually need extra SDKs, signing, emulators, or physical devices.
7. Create `.github/CODEOWNERS` from `templates/CODEOWNERS.template`, replacing `YOUR_GITHUB_USERNAME` with a real owner who has repository write access.
8. Configure a GitHub ruleset for `main` (see [Owner setup](docs/OWNER_SETUP.md)). Files alone **do not activate** repository protection.

## Run this template's own self-checks

Requirements: Python 3.11+ and standard library only.

```bash
python scripts/verify.py --mode quick
python scripts/verify.py --mode full
```

On Windows PowerShell, use `./scripts/verify.ps1 --mode full`. On macOS/Linux, use `sh scripts/verify.sh --mode full`. These wrappers invoke the **same Python runner**, avoiding divergent verification logic.

`quick` and `full` do not grant authorization to execute commands. First obtain the approval specified in `AGENTS.md` and `docs/OWNER_APPROVALS.md`.

The AI should propose a Git checkpoint after a tested milestone. It must not silently stage, commit, push, or deploy. **No full verification run is required after every small prompt.**

The runner produces `artifacts/verification-report.json`, with the commands, exit codes, durations, and results. Failures are not hidden and a dry run cannot report passing tests. For more detail see [Verification](docs/VERIFICATION.md).

## Adoption rule

**Do not copy this repository and call an application verified.** The included configuration checks this template itself. Every real application needs its own build, test, lint, architecture, security, data-migration, and release-specific checks. See [Platforms](docs/PLATFORMS.md).

## Collaboration

- [Contributing](CONTRIBUTING.md)
- [Start from an idea](START_HERE.md)
- [Copy-paste AI starter prompt](docs/START_HERE_PROMPT.md)
- [Security reporting](SECURITY.md)
- [License](LICENSE)

## Important limitations

- An AI assistant can disobey text instructions, and a local script can be edited or skipped. Only external controls (permissions, review, protected branches, CI) help enforce the process.
- The included scanner catches a narrow set of obvious credential formats, **not every secret**. Add a mature secret scanner and GitHub secret scanning where appropriate.
- CI on three desktop operating systems tests this **template's Python tooling**, not Android/iOS binaries, desktop UI, mobile UX, or hardware integrations.
- A market forecast is an evidence-backed recommendation, not proof of sales. AI credit, monetary and day estimates must show assumptions and may change.
- One codebase may target several platforms, but no framework removes platform-specific testing, packaging, API or release work.
- A repository owner may still be able to override protections, depending on configured roles and rules. Review your GitHub ruleset carefully.
