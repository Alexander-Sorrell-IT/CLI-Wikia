# Slash Commands

Inside an interactive session, type `/` to run a command. These are different from CLI flags (see [cli-reference.md](cli-reference.md)). Run `/help` for the live list, or `copilot help commands` from a shell.

---

## Agent environment

| Command | What it does |
|---|---|
| `/init` | Initialize Copilot instructions for this repo (`.github/copilot-instructions.md`) |
| `/agent [name]` | Browse and select a [custom agent](custom-agents.md) |
| `/skills` | Manage [skills](skills.md) |
| `/mcp` | Manage [MCP server](mcp.md) configuration |
| `/plugin` | Manage [plugins](plugins.md) and marketplaces |
| `/instructions` | View and toggle custom instruction files |
| `/env` | Show loaded environment: instructions, MCP servers, skills, agents, hooks, plugins, LSPs, extensions |

## Agents, subagents & delegation

| Command | What it does |
|---|---|
| `/model` | Pick the AI model (`auto` lets Copilot choose); shows relative cost |
| `/subagents` | Configure default and per-agent subagent models |
| `/sidekicks` | View running sidekick agents |
| `/fleet` | Enable fleet mode for parallel subagent execution |
| `/autopilot` | Toggle [autopilot mode](modes.md) |
| `/plan` | Create an implementation plan before coding (also Shift+Tab) |
| `/tasks` | View and manage tasks (subagents and shell commands) |
| `/delegate` | Send the session to GitHub; Copilot's cloud agent creates a PR |

## Code

| Command | What it does |
|---|---|
| `/ide` | Connect to an IDE workspace |
| `/diff` | Review changes in the current directory |
| `/pr` | Operate on pull requests for the current branch |
| `/review` | Run the code-review agent on your changes |
| `/security-review` | Analyze staged and unstaged changes for vulnerabilities |
| `/lsp` | Manage language-server configuration |
| `/terminal-setup` | Configure the terminal for multiline input (Shift+Enter) |

## Permissions

| Command | What it does |
|---|---|
| `/allow-all` | Enable all permissions (tools, paths, URLs) |
| `/add-dir` | Add a directory to the file-access allowlist |
| `/list-dirs` | Show all allowed directories |
| `/cwd` | Change or show the working directory |
| `/reset-allowed-tools` | Reset the list of allowed tools |

## Session

| Command | What it does |
|---|---|
| `/new` | Start a new conversation |
| `/resume` | Switch to a different session (by ID, task ID, or name) |
| `/rename` | Rename the session (or auto-generate a name) |
| `/clear` | Abandon this session and start fresh |
| `/restart` | Restart the CLI, preserving the session |
| `/context` | Show context-window token usage and a visualization |
| `/usage` | Session usage metrics and statistics |
| `/session` | View and manage sessions (has subcommands) |
| `/compact [focus]` | Summarize history to reclaim context (optional focus instructions) |
| `/share` | Save the session/research report to markdown, HTML, or a GitHub gist |
| `/remote` | Toggle remote control from GitHub web and mobile |
| `/copy` | Copy the last response to the clipboard |
| `/rewind`, `/undo` | Rewind the last turn and revert file changes |
| `/memory` | Show memory status, or enable/disable cross-session memory |
| `/chronicle` | Session history tools and insights |
| `/search` | Search the conversation timeline (experimental) |

## Help, status & settings

| Command | What it does |
|---|---|
| `/help` | Help for interactive commands |
| `/settings` | Open the settings UI, or `show`/set a single value (`/settings show <key>`) |
| `/statusline`, `/footer` | Configure status-line items (e.g. `ai-credits`, `ai-used`, `quota`) |
| `/theme` | View or set color mode |
| `/keep-alive [on\|off\|busy\|<dur>]` | Prevent system sleep while the session is active |
| `/changelog [summarize]` | Show the version changelog (optionally AI-summarized) |
| `/version` | Version info and update check |
| `/update` | Update the CLI to the latest version |
| `/experimental` | Show/enable/disable experimental features |
| `/diagnose` | Analyze the current session log |
| `/feedback` | Send feedback about the CLI |
| `/voice` | Manage voice mode (dictation via Foundry Local) |
| `/streamer-mode` | Hide model names and quota details (staff-gated) |
| `/app` | Open the GitHub Copilot desktop app |

## Research & other

| Command | What it does |
|---|---|
| `/research` | Deep-research investigation using GitHub search + web sources |
| `/ask` | Ask a quick side question without adding it to history (experimental) |
| `/login`, `/logout` | Manage authentication |
| `/user` | Manage the GitHub user list |
| `/exit` | Exit (use `/exit print` to print the session after leaving the alt screen) |

> Some commands are gated by `--experimental` or by staff/org policy and may not appear in every build. `/every` and `/after` (mentioned in docs for scheduled runs) drive the `beepOnSchedule` setting.

---

## See also

- [modes.md](modes.md) — plan, autopilot, fleet, delegate in depth
- [sessions.md](sessions.md) — resume, share, rewind, remote, memory
- [configuration.md](configuration.md) — what `/settings` writes
