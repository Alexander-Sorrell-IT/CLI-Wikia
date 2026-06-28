# Claude Code on the Web

Cloud sessions on Anthropic-managed VMs at [claude.ai/code](https://claude.ai/code). Sessions persist even if you close your browser. Monitor from the Claude mobile app.

> Research preview for Pro, Max, Team users, and Enterprise users with premium seats or Chat + Claude Code seats.

---

## GitHub authentication

Cloud sessions need access to clone code and push branches. Two ways:

| Method | How | Best for |
|---|---|---|
| **GitHub App** | Install the Claude GitHub App on specific repos during web onboarding. Per-repo authorization | Teams that want explicit per-repo control |
| **`/web-setup`** | Run in your terminal — syncs your local `gh` CLI token to your Claude account. Access matches your `gh` token | Individual developers who already use `gh` |

Either works. `/schedule` checks for either form and prompts you to run `/web-setup` if neither is configured.

The **GitHub App is required** for [Auto-fix](#auto-fix-pull-requests) (it uses the App to receive PR webhooks). If you connected with `/web-setup` and want Auto-fix, install the App on those repos.

Team/Enterprise admins can disable `/web-setup` with the Quick web setup toggle in admin settings.

> Orgs with [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention) cannot use `/web-setup` or other cloud session features.

---

## What's available in cloud sessions

Each session runs in a fresh VM with your repository cloned. Anything committed to the repo is available; anything only on your machine is not.

| | In cloud sessions? | Why |
|---|---|---|
| Repo's `CLAUDE.md` | ✅ | Part of the clone |
| Repo's `.claude/settings.json` hooks | ✅ | Part of the clone |
| Repo's `.mcp.json` MCP servers | ✅ | Part of the clone |
| Repo's `.claude/rules/` | ✅ | Part of the clone |
| Repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/` | ✅ | Part of the clone |
| Plugins in `.claude/settings.json` `enabledPlugins` | ✅ | Installed at session start from the marketplace you declared. Requires network access to reach the marketplace source |
| Your user `~/.claude/CLAUDE.md` | ❌ | Lives on your machine, not in the repo |
| Plugins enabled only in your user settings | ❌ | User-scoped `enabledPlugins` lives in `~/.claude/settings.json` — declare in repo's `.claude/settings.json` instead |
| MCP servers added with `claude mcp add` | ❌ | That writes to your local user config, not the repo. Declare in `.mcp.json` instead |
| Static API tokens / credentials | ❌ | No dedicated secrets store yet |
| Interactive auth (AWS SSO) | ❌ | Requires browser-based login that can't run in a cloud session |

To make config available in cloud sessions, **commit it to the repo**. Both env vars and setup scripts are visible to anyone who can edit that environment configuration.

---

## Pre-installed tools

| Category | Includes |
|---|---|
| Python | 3.x with pip, poetry, uv, black, mypy, pytest, ruff |
| Node.js | 20, 21, 22 via nvm + npm, yarn, pnpm, **bun** (known proxy issues), eslint, prettier, chromedriver |
| Ruby | 3.1, 3.2, 3.3 with gem, bundler, rbenv |
| PHP | 8.4 with Composer |
| Java | OpenJDK 21 with Maven and Gradle |
| Go | latest stable, module support |
| Rust | rustc and cargo |
| C/C++ | GCC, Clang, cmake, ninja, conan |
| Docker | docker, dockerd, docker compose |
| Databases | PostgreSQL 16, Redis 7.0 (not running by default — `service postgresql start`) |
| Utilities | git, jq, yq, ripgrep, tmux, vim, nano |

For exact versions, ask Claude in a cloud session: `check-tools` (cloud-only command).

> `gh` is **not** pre-installed. Install in setup script: `apt install -y gh`. Set `GH_TOKEN` env var (no `gh auth login` step needed).

---

## Resource limits

- **4 vCPUs**
- **16 GB RAM**
- **30 GB disk**

For larger workloads, use [Remote Control](./remote-control.md) on your own hardware.

---

## Configure environments

Environments control [network access](#network-access), env vars, and [setup scripts](#setup-scripts).

| Action | How |
|---|---|
| Add | Select current env to open selector → **Add environment** |
| Edit | Settings icon next to env name |
| Archive | Open for editing → **Archive**. Hidden from selector but existing sessions keep running |
| Set default for `--remote` | `/remote-env` in your terminal |

Env vars use `.env` format — one `KEY=value` per line, no quotes.

---

## Setup scripts

Bash script that runs when a new cloud session starts, before Claude Code launches. Runs as **root on Ubuntu 24.04** — `apt install` and most language package managers work.

```bash
#!/bin/bash
apt update && apt install -y gh
```

Non-zero exit fails the session. Append `|| true` to non-critical commands.

### Environment caching

The setup script runs the **first time** you start a session in an environment. Anthropic snapshots the filesystem after, then reuses that snapshot for later sessions — dependencies, tools, Docker images already on disk; setup script step skipped.

The cache captures **files, not running processes**. Files persist; services/containers don't. Start those per-session via Claude or a SessionStart hook.

The setup script reruns to rebuild the cache when:
- You change the script
- You change allowed network hosts
- The cache reaches its expiry (~7 days)

### Setup scripts vs SessionStart hooks

|  | Setup script | SessionStart hook |
|---|---|---|
| Attached to | Cloud environment | Repository |
| Configured in | Cloud env UI | `.claude/settings.json` |
| Runs | Before Claude Code launches, when no cached env | After Claude Code launches, every session including resumed |
| Scope | Cloud only | Both local and cloud |

Use a setup script for things the cloud needs but your laptop already has. Use a SessionStart hook for project setup that should run everywhere.

### Run a hook only in the cloud

```bash
#!/bin/bash
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then exit 0; fi
npm install
pip install -r requirements.txt
```

Limitations of SessionStart hooks in cloud:
- No cloud-only scoping (use `CLAUDE_CODE_REMOTE` check)
- Need network access to reach package registries (default Trusted allowlist covers npm, PyPI, RubyGems, crates.io)
- All outbound traffic passes through the security proxy. **Bun has known proxy issues** for package fetching
- Adds startup latency every session (no env caching benefit)

To persist env vars for subsequent Bash commands, write to `$CLAUDE_ENV_FILE`.

---

## Network access

| Level | Outbound |
|---|---|
| **None** | No network |
| **Trusted** (default) | [Allowlisted domains only](https://code.claude.com/docs/en/claude-code-on-the-web#default-allowed-domains) — package registries, GitHub, cloud SDKs |
| **Full** | Any domain |
| **Custom** | Your allowlist (optionally including defaults) |

Use `*.` for wildcard subdomain matching. Check **Also include default list of common package managers** to keep Trusted domains alongside your custom entries.

GitHub operations use a **separate proxy** (independent of this setting):

- Manages GitHub auth securely (git client uses scoped credential inside sandbox; proxy translates to your real token)
- Restricts `git push` to the current working branch for safety
- Enables cloning, fetching, PR ops while maintaining boundaries

The **security proxy** (HTTP/HTTPS) handles all outbound — protection against malicious requests, rate limiting, content filtering.

---

## Manage context in cloud sessions

| Command | Works in cloud | Notes |
|---|---|---|
| `/compact` | ✅ | Optionally pass focus: `/compact keep the test output` |
| `/context` | ✅ | Show what's in context |
| `/clear` | ❌ | Start a new session from the sidebar instead |

Auto-compaction runs at ~95% capacity by default. Trigger earlier:

```bash
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70    # compacts at 70%
```

To change the effective window for compaction calculations: `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.

[Subagents](./agents.md) work the same as locally. [Agent teams](./agent-teams.md) are off by default; enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in env vars.

---

## Move tasks between web and terminal

### Terminal → web (`--remote`)

```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Creates a new cloud session. Clones your current dir's GitHub remote at your current branch — **push first** if you have local commits. The task runs in the cloud while you continue locally.

> `--remote` creates **cloud sessions**. `--remote-control` is unrelated — that exposes a local CLI session for monitoring from the web. See [remote-control.md](./remote-control.md).

`/tasks` in the CLI shows progress. Open at claude.ai or in the mobile app to interact directly.

#### Tips

```bash
# Plan locally, execute remotely
claude --permission-mode plan
# (collaborate on the plan, save to docs/migration-plan.md, push)
claude --remote "Execute the migration plan in docs/migration-plan.md"

# Run multiple in parallel
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

#### Repos without GitHub

When you run `claude --remote` from a non-GitHub repo, Claude Code **bundles your local repo and uploads it directly**. Includes full history across branches plus uncommitted changes to tracked files.

Force bundling even with GitHub: `CCR_FORCE_BUNDLE=1 claude --remote "..."`

Limits:
- Must be a git repo with at least one commit
- Bundle must be < 100 MB (falls back to current branch only, then squashed snapshot, then fails)
- Untracked files not included — `git add` first
- Sessions from a bundle can't push back to a remote unless GitHub auth is configured

### Web → terminal (`--teleport`)

```bash
claude --teleport                    # interactive picker
claude --teleport <session-id>       # specific session
```

Or in an existing CLI session: `/teleport` (alias `/tp`).

From `/tasks` (background sessions): press `t` to teleport into one.

When you teleport, Claude:
1. Verifies you're in the correct repository (not a fork)
2. Fetches and checks out the branch from the cloud session
3. Loads full conversation history into your terminal

Requirements:
- Clean git state (you'll be prompted to stash if needed)
- Same repo (not a fork)
- Branch pushed to remote
- Same claude.ai account

`--teleport` is distinct from `--resume`: `--resume` reopens a conversation from this machine's local history; `--teleport` pulls a cloud session and its branch.

#### `--teleport` unavailable?

Requires claude.ai subscription auth. If you're on API key, Bedrock, Vertex, or Foundry, run `/login` to sign in with claude.ai instead. If still unavailable, your org may have disabled cloud sessions.

---

## Auto-fix pull requests

Claude can watch a PR and automatically respond to CI failures and review comments — Claude subscribes to GitHub events on the PR, and when a check fails or a reviewer comments, Claude investigates and pushes a fix if one is clear.

> Requires the Claude GitHub App on your repository.

Ways to turn on:

- **PRs created in cloud sessions**: open the CI status bar → **Auto-fix**
- **From your terminal**: `/autofix-pr` while on the PR's branch (detects open PR with `gh`, spawns web session, turns on auto-fix in one step)
- **From mobile**: tell Claude to auto-fix the PR
- **Any existing PR**: paste the PR URL into a session, tell Claude to auto-fix

How Claude handles PR activity:
- **Clear fixes**: makes the change, pushes it, explains what was done
- **Ambiguous requests**: asks you before acting
- **Duplicates / no-action events**: notes them and moves on

Claude may reply to review comment threads on GitHub as part of resolving them — replies are posted under your account but labeled as coming from Claude Code.

> ⚠️ If your repo uses `issue_comment`-triggered automation (Atlantis, Terraform Cloud, custom GH Actions), Claude can reply on your behalf and trigger those workflows. Review your automation before enabling auto-fix on repos where a PR comment can deploy infrastructure.

---

## Sessions sidebar

| Action | How |
|---|---|
| Review changes | Diff indicator (`+42 -18`) → opens diff view. Inline comments → send to Claude with next message |
| Share | Toggle visibility. **Team/Enterprise**: Private or Team (with repo-access verification by default). **Max/Pro**: Private or Public |
| Archive | Hover session → archive icon |
| Delete | Filter for archived → delete icon. Or open session → menu → Delete. Permanent |

---

## Security & isolation

- **Isolated VMs**: each session in an Anthropic-managed VM
- **Network controls**: limited by default, can be disabled
- **Credential protection**: git/signing keys never inside the sandbox. Auth via secure proxy with scoped credentials
- **Secure analysis**: code analyzed/modified in isolated VMs before creating PRs

---

## Limitations

- **Rate limits shared** with all other Claude/Claude Code usage in your account
- **GitHub repo auth required** to teleport
- **Platform restrictions**: cloning + PR creation requires GitHub. GitHub Enterprise Server supported on Team/Enterprise. GitLab/Bitbucket can be sent as a [local bundle](#repos-without-github), but can't push back

---

## See also

- [remote-control.md](./remote-control.md) — keep Claude Code on your machine
- [cli-reference.md](./cli-reference.md) — `--remote`, `--teleport`, `--from-pr`
- [environment-variables.md](./environment-variables.md) — `CLAUDE_CODE_REMOTE`, `CCR_FORCE_BUNDLE`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`
- [hooks.md](./hooks.md) — `SessionStart` for cloud setup hooks
