# Getting Started

GitHub Copilot CLI brings GitHub's coding agent into your terminal. It can chat, read and edit files, run shell commands, search the codebase, plan multi-step work, talk to MCP servers, and delegate work to GitHub's cloud coding agent — all gated by a permission system you control.

The binary is `copilot`.

---

## Prerequisites

- An active **GitHub Copilot** subscription. Copilot CLI is available on Copilot Pro, Pro+, Business, and Enterprise. Your org/enterprise admin must not have disabled the CLI policy.
- **Node.js 22 or later** (for the npm install path).
- On Windows, **PowerShell v6+**.

> If your org restricts Copilot, you'll see "Access denied by policy settings." Visit <https://github.com/settings/copilot> to check feature access (this also blocks third-party MCP servers in non-interactive runs).

---

## Install

| Platform | Command |
|---|---|
| npm (all) | `npm install -g @github/copilot` |
| Homebrew (macOS/Linux) | `brew install --cask copilot-cli` |
| WinGet (Windows) | `winget install GitHub.Copilot` |
| Script (macOS/Linux) | `curl -fsSL https://gh.io/copilot-install \| bash` |

If you have `ignore-scripts=true` in `~/.npmrc`, override it for this install with `npm_config_ignore_scripts=false`.

Verify and keep current:

```bash
copilot version           # installed version + checks for updates
copilot update            # download the latest stable
copilot update prerelease # switch to the prerelease channel
```

Auto-update runs on startup by default, except in CI (detected via `CI`, `BUILD_NUMBER`, `RUN_ID`, or `SYSTEM_COLLECTIONURI`). Disable with `--no-auto-update` or `COPILOT_AUTO_UPDATE=false`.

---

## Authenticate

Interactive OAuth device flow (browser):

```bash
copilot login
# or, inside a session:
/login
```

The token is stored in your OS credential store when available, otherwise in plain text under `~/.copilot/`.

For GitHub Enterprise Cloud with data residency:

```bash
copilot login --host https://example.ghe.com
```

### Headless / CI authentication

Set one of these env vars (checked in this order of precedence) instead of running `login`:

```
COPILOT_GITHUB_TOKEN  >  GH_TOKEN  >  GITHUB_TOKEN
```

Supported token types: **fine-grained PATs (v2)** with the *Copilot Requests* permission, OAuth tokens from the Copilot CLI app, and OAuth tokens from the GitHub CLI (`gh`) app. **Classic PATs (`ghp_`) are not supported.**

---

## First session

```bash
# Interactive REPL
copilot

# Interactive, but run a prompt immediately
copilot -i "Fix the bug in main.js"

# One-shot, non-interactive (exits when done)
copilot -p "Explain this repository" --allow-all-tools
```

On first use in a directory you must **trust the folder**. Trusted folders are remembered in `~/.copilot/config.json` (`trustedFolders`).

> **Non-interactive runs require `--allow-all-tools`** (or `COPILOT_ALLOW_ALL=true`); without it the agent can't execute tools unattended. See [permissions.md](permissions.md).

### Generate project instructions

```bash
copilot init   # writes .github/copilot-instructions.md based on a read-only scan
```

This analyzes the repo (build/test commands, conventions, structure, stack) so Copilot follows your team's practices. See [custom-instructions.md](custom-instructions.md).

---

## Terminal setup

Inside a session, run `/terminal-setup` to enable multiline input (Shift+Enter). Enable shell tab-completion:

```bash
source <(copilot completion bash)         # bash, current shell
copilot completion zsh  > "${fpath[1]}/_copilot"
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

---

## Where to go next

- [cli-reference.md](cli-reference.md) — every subcommand and flag
- [slash-commands.md](slash-commands.md) — the interactive `/` commands
- [modes.md](modes.md) — plan, autopilot, fleet, delegate
- [permissions.md](permissions.md) — control what the agent may do
- [configuration.md](configuration.md) — `settings.json` and the `~/.copilot` layout
