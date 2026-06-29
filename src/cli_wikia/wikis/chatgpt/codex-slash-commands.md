# Codex Slash Commands

Commands available inside the interactive Codex TUI, from OpenAI's [slash-commands](https://developers.openai.com/codex/cli/slash-commands) reference. Type `/` in the composer to see them.

> **Not locally verified** — sourced from official docs; Codex isn't installed here. The exact set varies by version and enabled features — run `/` in the TUI to see what your build offers.

---

## Model & behavior

| Command | What it does |
|---|---|
| `/model` | Choose the active model (and reasoning effort, when available) |
| `/fast` | Toggle a Fast service tier when the model catalog exposes one |
| `/personality` | Choose a communication style for responses |
| `/plan` | Switch to plan mode and optionally send a prompt |
| `/goal` | Set, pause, resume, view, or clear a task goal |

## Session management

| Command | What it does |
|---|---|
| `/clear` | Clear the terminal and start a fresh chat |
| `/new` | Start a new conversation inside the same CLI session |
| `/fork` | Fork the current conversation into a new thread |
| `/side` (`/btw`) | Start an ephemeral side conversation |
| `/resume` | Resume a saved conversation from your session list |
| `/archive` | Archive the current session and exit |
| `/delete` | Permanently delete the current session and exit |
| `/compact` | Summarize the visible conversation to free tokens |

## Permissions & safety

| Command | What it does |
|---|---|
| `/permissions` | Set what Codex can do without asking first |
| `/approve` | Approve one retry of a recent auto-review denial |
| `/sandbox-add-read-dir` | Grant sandbox read access to an extra directory |

(See [codex-approvals-sandbox.md](./codex-approvals-sandbox.md). `/approvals` may also appear as an alias — verify.)

## Workflow

| Command | What it does |
|---|---|
| `/diff` | Show the git diff, including files git isn't tracking |
| `/review` | Ask Codex to review your working tree |
| `/init` | Generate an `AGENTS.md` scaffold in the current directory |
| `/copy` | Copy the latest completed Codex output |
| `/status` | Display session configuration and token usage |
| `/usage` | View account token usage / rate-limit reset |
| `/mention` | Attach a file to the conversation |
| `/ide` | Include open files, current selection, and other IDE context |
| `/import` | Import Claude Code setup, project files, and recent chats |

## Tools, agents & extensions

| Command | What it does |
|---|---|
| `/mcp` | List configured MCP tools — see [codex-mcp.md](./codex-mcp.md) |
| `/plugins` | Browse installed and discoverable plugins |
| `/apps` | Browse apps (connectors) and insert them into your prompt |
| `/skills` | Browse and use skills |
| `/memories` | Configure memory use and generation |
| `/hooks` | View and manage lifecycle hooks |
| `/agent` | Switch the active agent thread |
| `/experimental` | Toggle experimental features |
| `/ps` | Show experimental background terminals and their recent output |
| `/stop` | Stop all background terminals |

## TUI customization

| Command | What it does |
|---|---|
| `/vim` | Toggle Vim mode for the composer |
| `/keymap` | Remap TUI keyboard shortcuts |
| `/statusline` | Configure status-line fields interactively |
| `/title` | Configure terminal window/tab title fields |
| `/theme` | Choose a syntax-highlighting theme |
| `/raw` | Toggle raw scrollback mode |

## Admin & utility

| Command | What it does |
|---|---|
| `/debug-config` | Print config-layer and requirements diagnostics |
| `/feedback` | Send logs to the Codex maintainers |
| `/logout` | Sign out of Codex |
| `/quit` (`/exit`) | Exit the CLI |

---

## See also

- [codex-models.md](./codex-models.md) — what `/model` and `/fast` change
- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — `/permissions`, `/approve`
- [codex-agents-md.md](./codex-agents-md.md) — `/init` output
