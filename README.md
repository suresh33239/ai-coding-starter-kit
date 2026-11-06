# AI Coding Starter Kit for Beginners & Others

**Your idea. Your project. Your control. AI helps you build.**

Have an app idea but don't know where to start? You don't need to be a programmer to begin. This kit gives you ready-to-use instructions and checklists so an AI coding assistant can help you **explore your idea, make a realistic plan, build step by step, and check the work**. You make the important decisions.

It works as a starting guide for Android and iPhone apps, websites, Windows, Mac and Linux software, browser extensions, and simple scripts. It's also useful if you've already started a project and want to bring it under control.

You don't have to build everything, pay for subscriptions, or publish an app. A useful personal tool is a perfectly good outcome.

## Get started: copy the kit and say `Start`

**Starting something new?**

1. Select **Code → Download ZIP** on GitHub and extract it into an empty project folder. You can also clone the repository if you know Git.
2. Open that folder in your AI coding tool, such as VS Code, Android Studio, or a coding assistant that can read project files.
3. Make sure the assistant reads `AGENTS.md`. Some tools do this automatically; in others, open the file or tell the assistant to read it.
4. Type one word in the assistant's chat:

   ```text
   Start
   ```

The assistant should begin by asking **what you want to build, who it's for, and what problem it solves**. It should help you explore the idea and plan your first small version **before writing code**.

**You don't need to know how to configure tests.** Once there's an actual app, the assistant should inspect its tools and existing tests, recommend a small verification setup, and configure it **after you approve the plan**. It should tell you in everyday language what each check does and what it cannot test.

**Already have a project?** Copy `AGENTS.md`, `START_HERE.md`, the relevant planning files, `docs/`, `scripts/`, and `templates/` into your **project's main folder**. Check for files with the same names first: don't overwrite an existing `AGENTS.md`, README, `.gitignore`, workflow, or testing setup. Merge instructions carefully and keep your existing project working. Then open the project with your assistant and say `Start`. It should inspect what you already have before suggesting changes.

`Start` is a direction from this kit, **not a built-in command in every AI tool**. If nothing happens, say: *“Read AGENTS.md and START_HERE.md in this project, then Start.”*

For tools with their own instruction files, the kit includes short pointers for **Gemini CLI** (`GEMINI.md`) and **GitHub Copilot** (`.github/copilot-instructions.md`). They refer to the same `AGENTS.md` rules; they are not competing policies. Claude Code can also use `AGENTS.md` directly. Exact instruction-file support depends on your tool and version, so confirm the agent actually read the guidance.

> **Remember:** Saying `Start` gives permission to explore and ask questions, not to install tools, spend money, change code, or publish your work.

## What happens next?

| Stage | How it helps you |
| --- | --- |
| **1. Understand your idea** | Explain it in your own words. No technical knowledge required. |
| **2. Check what's already out there** | Look for similar products, what people like or dislike, prices, and gaps worth solving. |
| **3. Decide if it's worth building** | Get an honest recommendation to proceed, simplify the idea, or wait—with practical alternatives. |
| **4. Make a realistic plan** | Compare app types, costs, available AI credits, a slow/free pace, and a likely time range. |
| **5. Build the basics first** | Start with the smallest useful feature, simple structure, essential tests, and language support. |
| **6. Review each stage** | Check what changed, what worked, what still needs testing, and where to save a Git checkpoint. |
| **7. Release when you're ready** | Review privacy, safety, installation, translations, and store requirements—or keep it as a personal project. |

The assistant should explain its reasoning, offer choices, and ask for your approval at important decisions. It shouldn't simply agree to every new feature or removal. **You can always say “Not now,” “Keep it simple,” or “Stop.”**

For the detailed first conversation, see [Start here](START_HERE.md).

## What's included in the kit?

You can use only the parts relevant to your project.

| You want to... | Look at... |
| --- | --- |
| Tell the assistant how to work with you | `AGENTS.md` and `START_HERE.md` |
| Explore competitors and decide whether to build | `IDEA_RESEARCH.md` and `FEASIBILITY.md` |
| Understand an existing project and its risks | `PROJECT.md`, `AUDIT.md`, `QUALITY_REVIEW.md` |
| Track defects and release blockers clearly | `BACKLOG.md` and `BLOCKERS.md` |
| Organize work, ideas, milestones, and future versions | `ROADMAP.md`, `BACKLOG.md`, `RELEASES.md` |
| Prepare for different languages early and review translations | `LOCALIZATION.md` and `localization/review.html` |
| Check whether your app is ready to release | `RELEASE_READINESS.md` and `docs/RELEASE_CHECKLIST.md` |
| Record your prompts, results, and changed files privately | `templates/PROMPT_LOG.local.template.md` |
| Set a spending limit and how many prompts you can use | `templates/OWNER_LIMITS.local.template.md` |
| Check your project without running every test each time | `scripts/verify.py`, `scripts/verify.ps1`, `scripts/verify.sh` |
| Set up checks for your specific app or operating system | `verification.json`, `examples/`, and `docs/VERIFICATION.md` |
| Understand permissions, safety, and Git checkpoints | `docs/OWNER_APPROVALS.md`, `docs/OWNER_SETUP.md`, `SECURITY.md` |

The kit also includes basic GitHub workflow and pull-request examples. These are **examples, not ready-made testing setups for every app**. Adapt them to your actual project rather than copying them unchanged.

## Keep your project folder tidy

These folders are included and ready to use:

| Folder | What belongs there |
| --- | --- |
| `reports/` | Generated test results, independent review reports, localization audit reports |
| `logs/` | Private prompt history, diagnostic and build logs |
| `screenshots/` | Screenshots for bug reports, visual checks and localization reviews |
| `localization/` | Translation review page, language audit template, review bundles and approval exports |

Generated files in these folders are **ignored by Git by default**, except for the provided templates and tools. This helps prevent private logs, screenshots and candidate translations from being published by accident. Review and sanitize anything before choosing to share it.

## Keep the budget and workload manageable

- Tell the assistant how much time, money, or AI usage you can afford. A pace of **two or three prompts a day** is fine if that's what works for you.
- Ask for a range of days, not a promised completion date. Testing, corrections, and review take time.
- Build one useful part at a time. Features you might want later can go into the backlog.
- Ask for focused checks while making small changes. Save larger verification runs for major milestones.
- Set up a Git checkpoint after a completed, tested stage, with your approval.
- Keep private budgets, prompt histories, keys, and personal information out of public GitHub repositories.

## Want to customize the checks? (Optional)

You can leave this until you've decided what to build. **If you're new to coding, ask your AI assistant to do these setup steps and explain its plan before changing files.** You do not need to edit JSON or know build commands yourself.

1. Start with a **read-only project review**. Ask the assistant what already works, what needs attention, and which questions still matter. See the [starter prompt](docs/START_HERE_PROMPT.md).
2. Make private copies of the budget and prompt-log templates. Save them as `OWNER_LIMITS.local.md` (project root) and `logs/PROMPT_LOG.local.md` (logs folder); both stay out of Git using the supplied `.gitignore` rules. Never commit private information.
3. Have the assistant select the example in `examples/` closest to your app. After inspecting actual build/test commands and getting approval, it should create a **project-specific** `verification.json`. The repository's default configuration **only tests this starter kit** and cannot verify your app. Preserve checks for tests, code quality, safety, and structure (or document appropriate equivalents).
4. Run `python scripts/verify.py --mode quick --dry-run` to **preview** the checks. This does not run tests. With your approval, run focused checks during development and save the full check for a completed major stage or release candidate.
5. If you use GitHub, adapt the example automated workflow to your app. Set an actual owner in `templates/CODEOWNERS.template` before using it, and configure protection for your main branch. The files alone cannot enforce these protections. See [Owner setup](docs/OWNER_SETUP.md).

Keep any existing project README, tests, build tools, and workflow unless you've reviewed a specific reason to change them. If you reuse or redistribute kit files, retain required license notices.

## For developers: check this starter kit itself

The following commands verify **the starter kit's own files**. They do not prove that an Android, iOS, website, or desktop app is ready to release. They require Python 3.11 or newer (no extra Python packages).

```bash
python scripts/verify.py --mode quick
python scripts/verify.py --mode full
```

On Windows PowerShell, use `./scripts/verify.ps1 --mode full`. On macOS/Linux, use `sh scripts/verify.sh --mode full`. These all use the same verification tool.

Neither command gives an assistant permission to run expensive or risky tasks. The approval rules are in `AGENTS.md` and `docs/OWNER_APPROVALS.md`.

The assistant should suggest saving a Git checkpoint after a tested milestone. It must not silently commit, push, or publish. **A full test run is not needed after every small prompt.**

The checks produce `reports/verification-report.json`, showing what ran, how long it took, and what passed or failed. See [Verification](docs/VERIFICATION.md) for details.

## A few important things to know

This is a **guide and collection of templates**, not an app builder that automatically produces finished software. Each real app needs its own tests, privacy and security review, and checks on the devices or systems it will run on. See [Supported project types](docs/PLATFORMS.md).

Written instructions help an assistant behave responsibly, but they **cannot guarantee** it will follow them. Limit permissions and spending, review important changes, and use GitHub branch protections and independent checks where appropriate.

This kit supports planning for iOS and Android, but it does not magically turn one codebase into a tested app for every platform. The assistant should help you choose the simplest suitable starting approach and explain what additional work other platforms require.

## Collaboration

- [Contributing](CONTRIBUTING.md)
- [Start from an idea](START_HERE.md)
- [Copy-paste AI starter prompt](docs/START_HERE_PROMPT.md)
- [Security reporting](SECURITY.md)
- [License](LICENSE)

### Honest limitations

- Research and forecasts can help you decide, but they cannot promise customers, sales, exact costs, or a finish date.
- The included basic secret check doesn't catch every password or key. Public projects need extra care and stronger security scanning where appropriate.
- The supplied GitHub tests run this template's Python tools on Windows, macOS, and Linux. They do **not** test mobile apps, desktop interfaces, or real devices.
- GitHub protections depend on the rules and permissions you actually configure; an owner may still be able to override some rules.
