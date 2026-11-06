# Start here — before writing code

**You do not need to know programming.** The AI should help you make an informed decision without rushing you into development, subscriptions, or unnecessary features.

## Easiest way to begin

Put the starter kit instructions and relevant folders **at the root of your project** as described in `README.md`. Make sure your AI tool can read `AGENTS.md`, then open the project in the tool and type **`Start`**. That is all you need to type initially. The agent will ask you to describe your idea, or first inspect an existing app. It must not start coding until you approve a plan. `Start` relies on the agent reading these files; it is not a built-in command supported by every AI tool.

## 1. Tell the AI your idea

Start with one question, not a long questionnaire:

> **What would you like to build? Describe the problem, who would use it, and what you hope it will do—in your own words.**

If you already have software, say so. The AI should inspect the existing project **read-only** before suggesting changes. If you have a new idea, it should research the opportunity before creating code.

The AI can then ask a few relevant follow-up questions, in plain English, based on what it knows. Questions may cover:

- Is this for yourself, a few people, testing/learning, customers, or public release?
- What devices or operating systems must it work on? Or should the AI recommend a format?
- Which 1–3 outcomes are essential for the first useful version?
- What time, money, AI credits, and equipment are available? Would you prefer a free/slow pace of 2–3 prompts daily?
- Which countries and languages are important initially? Are there any privacy, offline, or accessibility needs?

Do **not** ask all these at once if they are already answered or not relevant. Never demand a budget before discussing an idea. Actual spending limits and account readiness can go in private `OWNER_LIMITS.local.md` (copy the provided template); never store private finances or credentials in a public repository.

## 2. Research and forecast before a build decision

For a serious new product, the AI should research comparable products and alternatives using current sources. It should examine market coverage, what competitors do well, what users complain about, real pricing in the intended region, and any unmet need. See [IDEA_RESEARCH.md](IDEA_RESEARCH.md).

The AI should distinguish evidence from opinion, include links and dates, and be honest about missing market data. It must not agree with the idea automatically or discourage the person simply because competitors exist.

At the decision point, offer a constructive recommendation:

- **PROCEED:** a small, testable opportunity and feasible first version exist.
- **ADJUST:** narrow to a real gap, personal tool, prototype, or cheaper form factor.
- **DEFER:** significant blockers, costs, or unknowns should be resolved first.

Always offer a practical next option, including a tiny experiment or learning project if a commercial launch looks unattractive. **Do not start implementation without the owner's decision.**

## 3. Choose how the software should be delivered

Compare only relevant choices: native Android/iOS, cross-platform app, responsive website/PWA, browser extension, desktop app, portable executable, or simple non-installable script. Consider audience, devices, offline use, notifications, hardware access, sharing, maintenance, cost, developer accounts, and release channel. See [FEASIBILITY.md](FEASIBILITY.md) and [Platform adoption](docs/PLATFORMS.md).

The AI should recommend **one simplest appropriate starting format**, with a short reason and at most one strong alternative. A future iOS version is not a reason to build two full apps on day one.

## 4. Confirm prerequisites before development

Before choosing a framework or SDK, verify current **minimum and required versions** against official documentation and record the **check date and source**: OS/build machine, Xcode/Android SDK/runtime/browser extension manifest, supported devices, release account, signing, build tools, SDK/dependencies, privacy rules, and store requirements where relevant.

Also ask whether the owner already has any useful setup—GitHub, a domain/website, cloud hosting, Google Play/Apple developer account, Chrome Web Store account, test devices, Mac, or other tools. **Do not make them buy/register anything before it is needed.** Personal/testing projects may need none of these accounts.

If sources are unavailable or cannot be checked, mark requirements **unverified**. Do not make up latest version numbers or present old requirements as current.

## 5. Set a pace the owner can afford

Use the private [owner-limits template](templates/OWNER_LIMITS.local.template.md) to record available credits, subscriptions, money, prompts/day, desired deadline, hardware, and permission for paid calls. See [FEASIBILITY.md](FEASIBILITY.md) for the forecast format.

Give **an estimated range of days, not a guaranteed date**. Explain assumptions: implementation tasks, estimated AI interactions, manual reviews, testing/rework, platform complexity, localization, and external approvals. Show a low-cost pace and a faster pace if useful. Do not silently trigger paid research, builds, APIs, subscriptions, or publishing.

**Do not rush.** Each completed stage must have a useful result and review before the next stage. A smaller finished tool is better than a large unfinished app.

## 6. Build only the accepted first version

Typical sequence (adapt it to the project; no mandatory ceremony):

1. **Idea and market fit:** Research competitors and choose proceed/adjust/defer.
2. **Foundation:** Define audience, core use case, data safety, architecture and basic test/build setup.
3. **First usable slice:** Build the smallest real end-to-end feature; show the owner and test it.
4. **Essential features:** Add only approved functionality, reusable components, localization keys, and focused tests.
5. **Stage checkpoint:** Review scope, risks, app behavior, cost/credits, and full verification when approved; propose a Git checkpoint.
6. **Release preparation:** Test installation/upgrade/recovery, privacy/security, translations, usability, accounts and store/hosting requirements **for the chosen release channel**.
7. **Release or finish privately:** Owner explicitly approves publication—or marks the private tool complete without publishing.
8. **Maintain:** Fix real defects and prioritize the post-release backlog from evidence rather than speculation.

Track accepted work in `PROJECT.md`, `ROADMAP.md`, `BACKLOG.md`, and `RELEASES.md`. Record initial findings in `AUDIT.md` when authorized and an actual release decision in `RELEASE_READINESS.md`.

## Copy-paste opening prompt

```text
I want to explore building software with AI. Please use the project AGENTS.md
and START_HERE.md instructions. First ask me to describe the idea and why I
want it. Do not start writing code. After understanding the idea, research
existing alternatives, prices and user feedback; forecast the simplest useful
version, platform, cost, AI credits and likely time range. Tell me whether to
proceed, narrow the idea, or defer—with realistic options and sources.
Ask only relevant questions, explain clearly, and wait for my decision.
```

If you already have an application, replace the first sentence with **“I already have an application; start with a read-only project audit.”**
