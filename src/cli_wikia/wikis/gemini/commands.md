# Interactive Commands

Inside the Gemini CLI REPL, lines beginning with a special prefix are
interpreted as commands rather than prompts:

| Prefix | Meaning |
|---|---|
| `/` | **Slash commands** — control the CLI itself (sessions, config, tools, …) |
| `@` | **At commands** — inject file/directory content into your prompt |
| `!` | **Shell commands** — run a system command, or toggle shell mode |

Custom slash commands (from `.toml` files) and MCP prompts appear alongside the
built-ins. See [custom-commands.md](./custom-commands.md) and [mcp.md](./mcp.md).

---

## Slash commands (`/`)

### Session & history

| Command | What it does |
|---|---|
| `/chat` | Alias of `/resume` — open the session browser and manage chat checkpoints. |
| `/resume` | Browse and resume saved sessions; sub-commands `save <tag>`, `resume <tag>`, `list`, `delete <tag>`, `share [file]`, `debug`. |
| `/clear` | Clear the screen and visible scrollback (Ctrl+L). |
| `/compress` | Replace the chat context with a summary to free tokens. |
| `/copy` | Copy Gemini's last output to the clipboard (needs `xclip`/`xsel`, `pbcopy`, or `clip`). |
| `/restore [tool_call_id]` | Restore project files to the state before a tool ran (requires [checkpointing](./checkpointing.md)). |
| `/rewind` | Step back through history; revert chat, code, or both (shortcut: Esc Esc). |
| `/quit`, `/exit` | Exit. `--delete` also deletes the session's history and temp files. |
| `/stats` | Session statistics; `session`, `model` (tokens & quota), `tools`. |

All conversations auto-save — see [sessions.md](./sessions.md). Chat checkpoints
are project-scoped (`~/.gemini/tmp/<project_hash>/`).

### Context & memory

| Command | What it does |
|---|---|
| `/init` | Analyze the directory and generate a tailored `GEMINI.md`. |
| `/memory show` | Print the concatenated hierarchical memory currently loaded. |
| `/memory refresh` | Reload all `GEMINI.md` files. |
| `/memory list` | List the `GEMINI.md` files in use. |
| `/directory add <paths>` (`/dir`) | Add directories to the workspace. |
| `/directory show` | Show all workspace directories. |

See [context-files.md](./context-files.md).

### Models, tools & agents

| Command | What it does |
|---|---|
| `/model set <name> [--persist]` | Set the model; `/model manage` opens a config dialog. |
| `/tools [desc\|nodesc]` | List available tools, optionally with full descriptions. |
| `/agents list\|reload\|enable\|disable\|config` | Manage local and remote [subagents](./subagents.md). |
| `/skills list\|reload\|enable <name>\|disable <name>` | Manage [Agent Skills](./skills.md). |
| `/mcp list\|desc\|schema\|auth\|enable\|disable\|reload` | Manage [MCP servers](./mcp.md); `/mcp auth <server>` runs OAuth. |
| `/extensions list\|install\|uninstall\|enable\|disable\|update\|link\|config\|explore\|restart` | Manage [extensions](./extensions.md). |
| `/commands list\|reload` | Manage [custom slash commands](./custom-commands.md). |
| `/hooks list\|enable\|disable\|enable-all\|disable-all` | Manage [hooks](./hooks.md). |

### Permissions, plan & policies

| Command | What it does |
|---|---|
| `/plan` | Switch to read-only Plan Mode; `/plan copy` copies the approved plan. |
| `/permissions trust [path]` | Manage folder trust. |
| `/policies list` | List active [policies](./permissions.md) by mode. |

### Configuration & UI

| Command | What it does |
|---|---|
| `/settings` | Open the in-app settings editor (validated). |
| `/theme` | Change the visual [theme](./themes.md). |
| `/editor` | Pick your external editor. |
| `/vim` | Toggle Vim editing mode in the input area. |
| `/terminal-setup` | Configure terminal keybindings for multiline input (VS Code/Cursor/Windsurf). |
| `/ide install\|enable\|disable\|status` | Manage [IDE integration](./ide-integration.md). |
| `/shells` (`/bashes`) | Toggle the background-shells view. |

### Account & info

| Command | What it does |
|---|---|
| `/auth` | Change the authentication method. |
| `/privacy` | Show the privacy notice and manage data-collection consent. |
| `/upgrade` | Open the Gemini Code Assist upgrade page (Google login only). |
| `/about` | Version info (include it when filing issues). |
| `/bug [title]` | File a GitHub issue (configurable via `advanced.bugCommand`). |
| `/setup-github` | Set up GitHub Actions to triage issues and review PRs. |
| `/docs` | Open the documentation in your browser. |
| `/help` (`/?`) | Show help for all commands. |

---

## At commands (`@`)

Inject file or directory content into your prompt. Uses the `read_many_files`
tool internally and respects git-ignore / `.geminiignore` filtering.

```
@README.md            Explain this file.
@src/ Summarize the code in this directory.
What does this do? @path/to/file.txt
```

- A directory path pulls in files recursively (text files; binaries/large files
  may be skipped or truncated).
- Escape spaces in paths with a backslash: `@My\ Documents/file.txt`.
- A lone `@` with no path is passed through literally.
- Filtering is controlled by `context.fileFiltering.*` in [settings.md](./settings.md).

---

## Shell commands (`!`)

```
!ls -la           # run one command and return to the CLI
!git status
!                 # toggle persistent shell mode on/off
```

In shell mode every line is executed directly until you toggle back. Commands
run with **your full shell permissions** (`bash` on Linux/macOS, PowerShell on
Windows). Subprocesses get `GEMINI_CLI=1` in their environment so scripts can
detect they're running under Gemini CLI. See the [shell tool](./tools.md).

---

## Input editing shortcuts

| Action | Keys |
|---|---|
| Clear screen | Ctrl+L |
| Undo input | Ctrl+Z (Win) / Cmd+Z (macOS) / Alt+Z (Linux/WSL) |
| Redo input | Shift+Cmd+Z (macOS) / Shift+Alt+Z (Linux/WSL) |
| Rewind | Esc Esc |

Full bindings in [themes.md](./themes.md#keyboard-shortcuts).

---

## See also

- [cli-reference.md](./cli-reference.md) — command-line flags and subcommands
- [custom-commands.md](./custom-commands.md) — define your own `/` commands
- [sessions.md](./sessions.md) — resume, checkpoints, retention
- [mcp.md](./mcp.md) — MCP prompts as slash commands
- [tools.md](./tools.md) — what the built-in tools do
