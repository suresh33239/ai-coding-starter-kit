# GitHub setup the owner must do

Publishing the files is **not enough** to enforce approval rules. After creating your own public GitHub repository:

1. Set the repository's **Template repository** option if you want others to generate repos from it.
2. Keep `main` protected: Settings → Rules → Rulesets (or branch protection). Target `main`; require pull requests, passing status checks, resolved conversations, and owner reviews. Block force pushes and deletion; enable no-bypass options that your plan supports.
3. After the first successful CI run, require the checks displayed for the three operating systems. Do not guess check names before they exist. In a consuming app, replace them with checks that actually build and test that app.
4. Copy `templates/CODEOWNERS.template` to `.github/CODEOWNERS`, replace `YOUR_GITHUB_USERNAME` with a valid account that has write access, and enable **Require review from Code Owners** in the ruleset. Protect the CODEOWNERS and workflows themselves. A lone owner may need another trusted reviewer to satisfy independent review requirements; confirm the account's actual available settings.
5. Set GitHub Actions workflow permissions to **read-only** by default. The sample workflow explicitly requests `contents: read`, uses pinned official Actions, and does not handle deploy keys or production secrets.
6. Enable GitHub secret scanning, Dependabot alerts and dependency review where available. Review permissions of installed GitHub Apps, collaborator access, and branch bypass roles.
7. Put production credentials in a secret manager/environment with restricted access. Never expose production tokens to AI tasks or untrusted pull-request workflows. Add protected environments and required human reviewers before any deployment workflow.
8. Disable or strictly limit self-approval and auto-merge if human approval is essential. Review the policy after adding bots, third-party Actions, or collaborators.

GitHub UI and plan options change; consult the current [GitHub ruleset documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [CODEOWNERS documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), and [Actions security guidance](https://docs.github.com/en/actions/reference/security/secure-use).

## Public-repository checklist

- [ ] Scan working files **and commit history** for credentials; remove secrets from history and revoke compromised credentials before publication.
- [ ] Remove customer details, personal addresses, local absolute paths, private designs, and third-party proprietary code.
- [ ] Confirm the license and copyright ownership.
- [ ] Confirm no production CI secrets are exposed to public forks.
- [ ] Confirm `AGENTS.md`, CI, CODEOWNERS, and release policy are independently reviewed.
- [ ] Publish a test pull request to prove that checks/reviews block an unsafe merge.

## A hard truth about enforcement

An agent can edit local files if its machine permissions allow it. `AGENTS.md` cannot physically stop that. For stronger control, limit filesystem/network credentials, do work in isolated branches, review diffs, and use protected GitHub merges and independently governed deployment environments.
