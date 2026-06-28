# Slash Commands

Slash commands (`/name`) come in three kinds:

1. **Built-in commands** — hard-coded, ship with Claude Code.
2. **Bundled skills** — prompt-based skills that ship with Claude Code (Claude orchestrates them with its own tools).
3. **User / project / plugin skills** — your own.

For writing your own, see [skills.md](./skills.md). This file is a reference for what's already there.

---

## Built-in commands

### Help & navigation

| Command | What it does |
|---|---|
| `/help` | Show available commands |
| `/clear` | Clear the screen |
| `/config` | Open configuration UI |
| `/status` | Show active settings sources, model, plan, etc. |
| `/cost` | Show token usage and estimated cost so far |
| `/usage` / `/extra-usage` | Plan and rate-limit usage |
| `/recap` | Recap the conversation so far |
| `/release-notes` | Show release notes |
| `/doctor` | Run health checks |
| `/feedback` | Send feedback to Anthropic |
| `/bug` | File a bug report |

### Auth & login

| Command | What it does |
|---|---|
| `/login` | Sign in via claude.ai or console |
| `/logout` | Sign out |

### Memory & context

| Command | What it does |
|---|---|
| `/memory` | Browse/edit CLAUDE.md and auto-memory |
| `/init` | Generate a starter CLAUDE.md for the current project |
| `/compact [focus]` | Compress conversation. Optional focus: `/compact keep test output` |
| `/context` | Show what's currently in the context window |

### Configuration

| Command | What it does |
|---|---|
| `/permissions` | View/edit permission rules |
| `/hooks` | List configured hooks |
| `/agents` | List configured subagents grouped by source |
| `/mcp` | Manage MCP servers (auth, enable/disable, OAuth) |
| `/plugins` | Manage plugins (install/enable/disable, marketplaces) |
| `/reload-plugins` | Re-read plugin definitions in the current session |
| `/sandbox` | Open the sandbox-mode picker |
| `/theme` | Pick a color theme |
| `/terminal-setup` | Configure terminal-specific options |
| `/vim` | Toggle vim editor mode |

### Models & effort

| Command | What it does |
|---|---|
| `/model [name]` | Open picker, or switch directly: `/model opus` |
| `/effort [level]` | Set effort: `low`, `medium`, `high`, `xhigh`, `max` |

### Sessions

| Command | What it does |
|---|---|
| `/resume` | Open session picker |
| `/rewind` | Rewind to a previous checkpoint |
| `/rename <name>` | Rename current session (shown in prompt bar) |
| `/exit` | Exit the REPL |
| `/export` | Export session to a file |

### Git/PR helpers

| Command | What it does |
|---|---|
| `/pr-comments` | View comments on the current PR |
| `/review` | Launch a code review of the current branch |
| `/security-review` | Security-focused review of pending changes |
| `/autofix-pr` | Tell Claude to watch the PR's CI and review comments and auto-fix |

### Working dirs

| Command | What it does |
|---|---|
| `/add-dir <path>` | Add a working dir for this session |

### Web sessions / Remote Control / mobile

| Command | What it does |
|---|---|
| `/remote-control` (alias `/rc`) | Convert current session to a [Remote Control](./remote-control.md) session |
| `/teleport [id]` (alias `/tp`) | Pull a [cloud session](./claude-code-web.md) into this terminal |
| `/tasks` | View web/cloud session task list |
| `/web-setup` | Sync local `gh` token to your Claude account for web sessions |
| `/remote-env` | Configure default environment for `--remote` |
| `/mobile` | Show QR code to download the Claude mobile app |
| `/schedule` | Schedule recurring routines (cron-style) |

---

## Bundled skills

Prompt-based skills shipped with Claude Code. Listed in `/help` marked **Skill** in the Purpose column.

| Skill | What it does |
|---|---|
| `/simplify` | Simplify and refine code while preserving functionality |
| `/batch` | Batch a series of repeated operations |
| `/debug` | Systematic debugging workflow |
| `/loop [interval] [task]` | Run a prompt or slash command on a recurring interval. Omit interval to let model self-pace |
| `/claude-api` | Build/debug/optimize Claude API and Agent SDK apps. Migrates code between Claude versions |

> Bundled skills are *not* the same as built-in commands. Built-ins execute fixed logic. Bundled skills give Claude a playbook to orchestrate with its own tools.

---

## Plugin commands appear namespaced

When a plugin ships skills, they appear with the plugin name prefix: `/my-plugin:skill-name`. This avoids collisions with personal skills in `~/.claude/skills/`.

Example: a plugin `code-review` with skill `audit` becomes `/code-review:audit`.

---

## Useful skill compositions (from common plugins)

These are *not* built-in but are common across plugin ecosystems — install via `/plugins`:

| Skill | What it does |
|---|---|
| `/commit` | Run a tested commit workflow |
| `/security-review` | Security audit of pending changes |
| `/refactor` | Refactoring patterns |
| `/explain-code` | Code explanation with diagrams |
| `/init` | Generate CLAUDE.md (also a built-in) |

---

## See also

- [skills.md](./skills.md) — full skill spec
- [cli-reference.md](./cli-reference.md) — flags that affect slash commands (`--disable-slash-commands`)
- [permissions.md](./permissions.md) — `Skill()` rule syntax
