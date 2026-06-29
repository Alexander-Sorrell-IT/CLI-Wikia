# Antigravity CLI (`agy`) Reference

Complete reference for the `agy` command — launch flags, subcommands,
interactive TUI slash commands, keyboard shortcuts, and environment variables.
Verified against `agy --help`, `agy plugin --help`, and the bundled
`antigravity-guide` docs (v1.0.13).

## Usage

```
agy [flags]            # launch the interactive agentic TUI
agy <subcommand> ...   # run a one-off management command
```

Running `agy` with no subcommand opens the **TUI**: a scrollable conversation
pane, a `>` prompt, and a status line showing the active model, token/quota
usage, and any running subagents. Use `-p`/`--print` for non-interactive,
scriptable runs.

---

## Launch flags

| Flag | Description |
|------|-------------|
| `--add-dir <dir>` | Add a directory to the workspace. Repeatable (default `[]`) |
| `-c`, `--continue` | Continue the most recent conversation in this workspace |
| `--conversation <id>` | Resume a specific conversation by its ID |
| `--dangerously-skip-permissions` | Auto-approve **all** tool permission requests without prompting |
| `-i`, `--prompt-interactive <text>` | Run an initial prompt, then drop into the interactive session |
| `--log-file <path>` | Override the CLI log file path |
| `--model <name>` | Model for this session (e.g. `"Gemini 3.1 Pro (High)"`) |
| `--new-project` | Create a new project for this session |
| `-p`, `--print <text>` | Run one prompt non-interactively, print the response, exit |
| `--prompt <text>` | Alias for `--print` |
| `--print-timeout <dur>` | Max wait in print mode (default `5m0s`) |
| `--project <id>` | Project ID to use for this session |
| `--sandbox` | Run with terminal sandbox restrictions enabled |

`<dur>` accepts Go-style durations like `90s`, `5m0s`, `1h`.

### Examples

```bash
# one-shot with a chosen model
agy --model "Gemini 3.1 Pro (High)" -p "review main.go for data races"

# interactive, scoped to an extra directory, sandboxed, seeded with a task
agy --add-dir ../shared --sandbox -i "start a refactor of the auth module"

# scripted run with a longer budget
agy -p "generate API docs for ./server" --print-timeout 10m > docs.md

# resume work
agy -c
agy --conversation 0dc79202-f007-48c4-8339-bd65fc6e9363
```

> `--dangerously-skip-permissions` bypasses every approval prompt. Use only in
> throwaway/sandboxed environments. See [permissions.md](./permissions.md).

---

## Subcommands

| Command | Purpose |
|---------|---------|
| `agy changelog` | Show the changelog and release notes |
| `agy help` | Show help for subcommands |
| `agy install` | Configure environment paths and shell settings (PATH, completions) |
| `agy models` | List available models — see [models.md](./models.md) |
| `agy plugin` (alias `plugins`) | Manage plugins — see [plugins.md](./plugins.md) |
| `agy update` | Update the CLI to the latest version |

### `agy plugin <command>`

| Command | Description |
|---------|-------------|
| `list` | List imported/installed plugins |
| `import [source]` | Import plugins from `gemini` or `claude` |
| `install <target>` | Install a plugin (supports `plugin@marketplace`) |
| `uninstall <name>` | Uninstall a plugin |
| `enable <name>` | Enable a plugin |
| `disable <name>` | Disable a plugin |
| `validate [path]` | Validate a plugin's schema/structure |
| `link <mp> <target>` | Generate a link to a marketplace |
| `help` | Show plugin help |

Full details in [plugins.md](./plugins.md).

> Read-only subcommands (`changelog`, `models`, `plugin list`, `help`) are safe
> to run anytime. Avoid `agy update` and `agy install` in automated contexts.

---

## Interactive TUI slash commands

Typed at the `>` prompt during a session. These exist only in the TUI, not as
shell subcommands.

### Session & conversation
| Command | Description |
|---------|-------------|
| `/clear` or `/new` | Clear the screen and scrollback buffer |
| `/rename` | Rename the active conversation thread |
| `/resume`, `/switch`, `/conversation` | Resume a past conversation by ID or name |
| `/fork` or `/branch` | Fork the current conversation into a new thread, preserving history |
| `/rewind` or `/undo` | Rewind history to a previous checkpoint |
| `/exit` or `/quit` | Exit the session |
| `/logout` | Log out of the active Google account |

### Workspace & context
| Command | Description |
|---------|-------------|
| `/add-dir` | Add a directory to the active workspace |
| `/context` | List files/symbols currently in the agent's context |
| `/diff` | Show the codebase diff of changes made this session |
| `/open` | Open a file in your preferred editor |
| `/copy` | Copy the last agent response to the clipboard |
| `/btw` | Ask a quick side-question without a full agent run |

### Agents, tasks & artifacts
| Command | Description |
|---------|-------------|
| `/agents` | List active subagents and custom agents |
| `/tasks` | Show the active task list and progress |
| `/artifact` | Open the TUI artifact viewer |
| `/planning` | Open the graphical planning / task-list editor (external builds) |

### Capabilities & config
| Command | Description |
|---------|-------------|
| `/model` | Change the active model for the session |
| `/skills` | List active skills |
| `/hooks` | List registered lifecycle hooks |
| `/mcp` | List active MCP servers and their tools |
| `/permissions` | Manage tool permissions (allow/deny lists) |
| `/config` or `/settings` | Open the configuration panel |
| `/keybindings` | View/customize keyboard shortcuts |
| `/statusline` | Toggle the status line |
| `/title` | Toggle/configure the terminal title |
| `/usage` or `/quota` | Show token usage and session cost |
| `/changelog` | Show changelog and release notes |
| `/fast` | Toggle Fast Mode (drops typing delays / thought visualization) |
| `/help` | Show the help menu |
| `/feedback` | Open the feedback/bug form |
| `/credits` | Third-party licenses and attributions |

---

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Submit prompt; on first run, start OAuth sign-in |
| `Esc` | Close active menus (e.g. `/skills`, `/settings`) |
| `Up` / `Down` | Navigate command history |
| `Ctrl+C` | First press cancels active agent operations; double-press exits |
| `Ctrl+D` | Forward-delete when the prompt has text; exit when empty (double-press) |
| `Ctrl+O` | Clear scrollback |
| `Ctrl+G` | Expanded full-screen view for tool confirmations (edit command + permissions) |
| `Shift+N` | Cycle backwards through diff blocks in unified diff review |

Shortcuts are customizable via `/keybindings`, which writes
`~/.gemini/antigravity-cli/keybindings.json` (created only when you first run the
command). Invalid key names are rejected with suggested canonical alternatives.

---

## Environment variables

| Variable | Effect |
|----------|--------|
| `AGY_CLI_CMD_OUTPUT_PERCENTAGE` | Max height of command output in the TUI, as a percent of terminal height |

> Other `AGY_*` variables may exist; this is the one confirmed in the changelog.
> Verify additional environment variables in official docs.

---

## Version

`agy --version` → `1.0.13` on this machine. Run `agy changelog` for the rolling
release history (the changelog records granular per-version fixes and features).
