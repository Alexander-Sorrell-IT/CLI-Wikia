# CLI Reference

Every `gemini` subcommand, flag, and positional argument. By default `gemini`
launches an interactive REPL; pass a prompt (positional or `-p`) for
non-interactive one-shot mode.

> The flags below reflect the current published docs. The installed binary
> (v0.22.4) ships a slightly smaller flag set — a few items here (`-w/--worktree`,
> `--skip-trust`, `--experimental-zed-integration`, the `plan` approval mode,
> and the `gemini skills`/`gemini update` subcommands) appear in newer releases.
> Run `gemini --help` to confirm what your build supports.

---

## Invocation patterns

```bash
gemini                                  # interactive REPL
gemini "explain this repository"        # prompt, then continue interactively (in a TTY)
gemini -p "summarize README.md"         # one-shot, print, exit (non-interactive)
cat logs.txt | gemini -p "find errors"  # pipe stdin; -p text is appended to stdin
gemini -i "what does this project do?"  # run prompt, then stay interactive
gemini -r latest "check for type errors"# resume most recent session with a new prompt
gemini -r <session-id> "finish the PR"  # resume a specific session by id
gemini update                           # update to the latest version
```

`query` is a variadic positional prompt. In a TTY it defaults to interactive;
`-p`/`--prompt` forces non-interactive execution. The `-p` flag is marked
deprecated in favor of the positional prompt but still works.

---

## Subcommands

| Command | What it does |
|---|---|
| `gemini [query..]` | Launch Gemini CLI (default command) |
| `gemini mcp` | Manage MCP servers — see [mcp.md](./mcp.md) |
| `gemini extensions <command>` | Manage extensions (alias `extension`) — see [extensions.md](./extensions.md) |
| `gemini skills <command>` | Manage Agent Skills — see [skills.md](./skills.md) *(newer releases)* |
| `gemini update` | Update to the latest version *(newer releases)* |

### `gemini mcp`

```
gemini mcp add <name> <commandOrUrl> [args...]   # add a server (stdio or URL)
gemini mcp remove <name>                         # remove a server
gemini mcp list                                  # list configured servers
```

Notable `add` flags: `--transport stdio|http|sse`, `--env KEY=value`,
`--scope user|project`, `--include-tools`, `--exclude-tools`, `--header`,
`--timeout`, `--trust`. Full detail in [mcp.md](./mcp.md).

### `gemini extensions <command>`

```
install <source> [--ref <r>] [--auto-update] [--pre-release]
uninstall <names..>          list                 update [<name>] [--all]
enable [--scope] <name>      disable [--scope] <name>
link <path>                  new <path> [template]
validate <path>              settings <command>
```

See [extensions.md](./extensions.md).

### `gemini skills <command>` *(newer releases)*

```
list      install <source>     link <path>      uninstall <name>
enable <name> | --all          disable <name> | --all
```

See [skills.md](./skills.md).

---

## Options

### Prompting & input

| Flag | Alias | Type | Description |
|---|---|---|---|
| `--prompt` | `-p` | string | Non-interactive prompt. Appended to stdin if piped. (Deprecated in favor of the positional prompt.) |
| `--prompt-interactive` | `-i` | string | Run the prompt, then continue interactively. Cannot be combined with piped stdin. |
| `--include-directories` | | array | Add directories to the workspace (comma-separated or repeated). Max 5. |

### Model

| Flag | Alias | Description |
|---|---|---|
| `--model` | `-m` | Model alias (`auto`, `pro`, `flash`, `flash-lite`) or concrete name. Default `auto`. See [models.md](./models.md). |

### Approvals & sandboxing

| Flag | Alias | Description |
|---|---|---|
| `--approval-mode` | | `default` (prompt), `auto_edit` (auto-approve edits), `yolo` (auto-approve all), `plan` (read-only). |
| `--yolo` | `-y` | Auto-approve all actions. Deprecated; prefer `--approval-mode=yolo`. |
| `--sandbox` | `-s` | Run tool execution in a sandbox. See [sandboxing.md](./sandboxing.md). |
| `--allowed-tools` | | Tools that run without confirmation. Deprecated; prefer the [Policy Engine](./permissions.md). |
| `--allowed-mcp-server-names` | | Restrict which MCP servers the session may use. |
| `--skip-trust` | | Trust the current workspace for this session, skipping the folder-trust check. *(newer releases)* |

### Extensions

| Flag | Alias | Description |
|---|---|---|
| `--extensions` | `-e` | Restrict the session to specific extensions. `gemini -e none` disables all. |
| `--list-extensions` | `-l` | List available extensions and exit. |

### Sessions

| Flag | Alias | Description |
|---|---|---|
| `--resume` | `-r` | Resume a session: `latest`, an index number, or a full UUID. Bare `--resume` = `latest`. |
| `--list-sessions` | | List sessions for the current project and exit. |
| `--delete-session` | | Delete a session by index number or UUID. |

See [sessions.md](./sessions.md).

### Output & protocols

| Flag | Alias | Description |
|---|---|---|
| `--output-format` | `-o` | `text` (default), `json`, or `stream-json`. See [headless.md](./headless.md). |
| `--experimental-acp` | | Start in Agent Communication Protocol (ACP) mode. Experimental. |
| `--experimental-zed-integration` | | Run in Zed editor integration mode. Experimental. *(newer releases)* |

### Worktrees *(newer releases)*

| Flag | Alias | Description |
|---|---|---|
| `--worktree` | `-w` | Start in a new git worktree (auto-named if omitted). Requires `experimental.worktrees: true` in settings. |

### General

| Flag | Alias | Description |
|---|---|---|
| `--debug` | `-d` | Verbose debug logging. Open the debug console with F12. Default `false`. |
| `--screen-reader` | | Screen-reader-friendly TUI mode. |
| `--version` | `-v` | Print version and exit. |
| `--help` | `-h` | Show help. |

### Testing-only flags

`--fake-responses <file>` and `--record-responses <file>` inject or capture
model responses for testing.

---

## Common usage patterns

```bash
# One-shot, machine-readable JSON for scripting
gemini -p "list the project's dependencies" -o json | jq .

# Stream events as they happen
gemini -p "write a haiku about TCP" -o stream-json

# Pipe a file in and ask about it
cat src/server.ts | gemini -p "explain this file and flag any bugs"

# Pick a faster model for a simple task
gemini -m flash -p "rename git branch main to trunk — give me the commands"

# Run with sandboxed tool execution and auto-approve edits
gemini -s --approval-mode auto_edit "add unit tests for utils.py"

# Limit a session to two MCP servers and one extension
gemini --allowed-mcp-server-names github,sentry -e github "triage open issues"

# Add extra workspace directories
gemini --include-directories ../shared,../libs "run the tests"
```

---

## Interactive REPL commands

Inside the REPL, commands are prefixed with `/` (slash), `@` (inject file
content), or `!` (shell). A few reload helpers:

```
/skills reload   /agents reload   /commands reload   /memory reload
/mcp reload      /extensions reload   /help   /quit
```

The full set is documented in [commands.md](./commands.md).

---

## See also

- [commands.md](./commands.md) — slash, at, and shell commands inside the REPL
- [configuration.md](./configuration.md) — config files, layers, precedence
- [settings.md](./settings.md) — every `settings.json` field
- [environment-variables.md](./environment-variables.md) — all env vars
- [models.md](./models.md) — model aliases and routing
- [headless.md](./headless.md) — non-interactive output formats and scripting
