# CLI Reference

Every `claude` subcommand and flag. (`claude --help` does *not* list every flag — absence from `--help` doesn't mean a flag is unavailable.)

---

## Subcommands

| Command | What it does |
|---|---|
| `claude` | Start interactive REPL |
| `claude "query"` | Start REPL with an initial prompt |
| `claude -p "query"` | One-shot print mode (SDK-style), then exit |
| `cat file \| claude -p "query"` | Pipe content as input |
| `claude -c` | Continue most recent conversation in this dir |
| `claude -c -p "query"` | Continue via SDK |
| `claude -r "<id-or-name>" "query"` | Resume a specific session |
| `claude update` | Update to latest version |
| `claude install [version]` | Install/reinstall the native binary. `stable`, `latest`, or `2.1.118` |
| `claude auth login` | Sign in to Anthropic. `--email`, `--sso`, `--console` |
| `claude auth logout` | Log out |
| `claude auth status` | Show auth status (JSON; `--text` for human form). Exit 0 if logged in, 1 if not |
| `claude agents` | List configured subagents grouped by source |
| `claude auto-mode defaults` | Print the built-in auto-mode classifier rules as JSON |
| `claude auto-mode config` | Print effective auto-mode config with settings applied |
| `claude mcp` | Manage MCP servers (see [mcp.md](./mcp.md)) |
| `claude plugin` (alias `plugins`) | Manage plugins (see [plugins.md](./plugins.md)) |
| `claude remote-control` | Start a [Remote Control](./remote-control.md) server |
| `claude setup-token` | Generate a long-lived OAuth token for CI/scripts |

If you mistype a subcommand, Claude Code suggests the closest match (`claude udpate` → "Did you mean claude update?").

---

## Flags

### Session basics

| Flag | What it does |
|---|---|
| `--add-dir <path>...` | Add additional working dirs Claude can read/edit |
| `--name`, `-n <name>` | Set a display name (shown in `/resume` and terminal title) |
| `--session-id <uuid>` | Use a specific session ID (must be valid UUID) |
| `--continue`, `-c` | Resume most recent session in cwd |
| `--resume`, `-r [id]` | Resume specific session, or open picker |
| `--fork-session` | When resuming, create a new session ID instead of reusing the original |
| `--from-pr <number-or-url>` | Resume sessions linked to a specific PR (GitHub, GitHub Enterprise, GitLab, Bitbucket) |
| `--print`, `-p [query]` | Print mode — non-interactive |

### Models & effort

| Flag | What it does |
|---|---|
| `--model <name>` | `sonnet`, `opus`, or full ID (`claude-opus-4-7`) |
| `--effort <level>` | `low`, `medium`, `high`, `xhigh`, `max` |
| `--fallback-model <name>` | Auto-fallback when default is overloaded (print mode only) |
| `--betas <header>` | Beta API headers (API-key users only) |

### Permissions

| Flag | What it does |
|---|---|
| `--permission-mode <mode>` | `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` |
| `--allow-dangerously-skip-permissions` | Add `bypassPermissions` to Shift+Tab cycle without starting in it |
| `--dangerously-skip-permissions` | Equivalent to `--permission-mode bypassPermissions` |
| `--allowedTools <list>` | Tools that execute without prompting |
| `--disallowedTools <list>` | Tools removed from model's context (cannot be used) |
| `--tools <list>` | **Restrict** which built-in tools Claude has at all (`""` disables all, `"default"` for all, or `"Bash,Edit,Read"`) |
| `--permission-prompt-tool <mcp-tool>` | MCP tool to handle permission prompts in non-interactive mode |

### Tools/agents/skills

| Flag | What it does |
|---|---|
| `--agent <name>` | Run main thread *as* a named subagent (overrides `agent` setting) |
| `--agents <json>` | Define subagents dynamically from JSON |
| `--disable-slash-commands` | Disable all skills and commands for this session |

### MCP

| Flag | What it does |
|---|---|
| `--mcp-config <path-or-json>` | Load MCP servers from JSON file(s) or inline |
| `--strict-mcp-config` | Only use servers from `--mcp-config`, ignoring all other MCP config |

### Plugins / channels / chrome / IDE

| Flag | What it does |
|---|---|
| `--plugin-dir <path>` | Load plugins from a directory (repeat for multiple) |
| `--channels <plugin:name@marketplace ...>` | (Research preview) Channel plugins to listen on |
| `--dangerously-load-development-channels <entries>` | Load channels not on the approved allowlist (for dev) |
| `--chrome` / `--no-chrome` | Toggle Chrome browser integration |
| `--ide` | Auto-connect to IDE on startup (if exactly one is available) |

### Worktrees & teams

| Flag | What it does |
|---|---|
| `--worktree`, `-w [name]` | Start in an isolated git worktree at `<repo>/.claude/worktrees/<name>` |
| `--tmux[=classic]` | Create a tmux session for the worktree (uses iTerm2 panes when available) |
| `--teammate-mode <mode>` | `auto` (default), `in-process`, or `tmux` for [agent teams](./agent-teams.md) |

### Web sessions / Remote Control

| Flag | What it does |
|---|---|
| `--remote "<task>"` | Create a new [web session](./claude-code-web.md) on claude.ai with this task |
| `--teleport [id]` | Resume a web session in your local terminal |
| `--remote-control [name]`, `--rc` | Start interactive session with [Remote Control](./remote-control.md) enabled |
| `--remote-control-session-name-prefix <p>` | Prefix for auto-generated RC session names (default: hostname) |

### Headless / streaming output

| Flag | What it does |
|---|---|
| `--output-format <fmt>` | `text`, `json`, or `stream-json` |
| `--input-format <fmt>` | `text` or `stream-json` |
| `--include-partial-messages` | Include partial streaming events (requires `--print --output-format stream-json`) |
| `--include-hook-events` | Include all hook lifecycle events in output (requires `--output-format stream-json`) |
| `--replay-user-messages` | Re-emit user messages from stdin back on stdout for ack |
| `--json-schema <schema>` | Validate structured output against JSON schema (print mode) |
| `--max-turns <N>` | Limit agentic turns (print mode) |
| `--max-budget-usd <amount>` | Cap dollar spend on API calls (print mode) |
| `--no-session-persistence` | Don't save session to disk (print mode) |

### System prompts (4 mutually-exclusive-ish flags)

| Flag | Behavior |
|---|---|
| `--system-prompt <text>` | **Replace** the entire default system prompt |
| `--system-prompt-file <path>` | **Replace** with file contents |
| `--append-system-prompt <text>` | **Append** to default prompt |
| `--append-system-prompt-file <path>` | **Append** file contents |
| `--exclude-dynamic-system-prompt-sections` | Move per-machine sections (cwd, env, memory paths, git status) into first user message — improves prompt-cache reuse across users |

`--system-prompt` and `--system-prompt-file` are mutually exclusive. Append flags can combine with either.

### Settings

| Flag | What it does |
|---|---|
| `--settings <path-or-json>` | Path or JSON string to load extra settings |
| `--setting-sources <list>` | Comma-separated: `user`, `project`, `local` |

### Speed / debugging

| Flag | What it does |
|---|---|
| `--bare` | Skip auto-discovery of hooks, skills, plugins, MCP, auto-memory, CLAUDE.md. Has Bash/Read/Edit only. Sets `CLAUDE_CODE_SIMPLE` |
| `--init` | Run init hooks and start interactive |
| `--init-only` | Run init hooks and exit (no session) |
| `--maintenance` | Run maintenance hooks and start interactive |
| `--debug [categories]` | Debug mode with category filter (e.g. `"api,hooks"`, `"!statsig,!file"`) |
| `--debug-file <path>` | Write debug logs to a path (implies `--debug`) |
| `--verbose` | Show full turn-by-turn output |

### Misc

| Flag | What it does |
|---|---|
| `--version`, `-v` | Print version |

---

## Common usage patterns

```bash
# Start interactive in plan mode with verbose logs
claude --permission-mode plan --verbose

# One-shot, with structured JSON output validated against a schema
claude -p "list functions in auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}}}' \
  | jq .structured_output

# CI mode: locked down, no surprises
claude --bare -p "lint" --allowedTools "Bash(npm run lint),Read"

# Stream tokens in real time
claude -p "write a poem" \
  --output-format stream-json --verbose --include-partial-messages \
  | jq -rj 'select(.type=="stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'

# Multi-turn with continuation
session_id=$(claude -p "review this" --output-format json | jq -r '.session_id')
claude -p "focus on errors" --resume "$session_id"

# Worktree + tmux for parallel work
claude -w feature-auth --tmux

# Send a task to the cloud, keep working locally
claude --remote "fix the failing test in auth.spec.ts"

# Pull a cloud session back to your terminal
claude --teleport
```

---

## Built-in slash commands inside the REPL

A subset of these is always available without any plugin or skill:

```
/help          /clear         /memory         /hooks         /mcp
/plugins       /agents        /permissions    /config        /status
/model         /effort        /add-dir        /init          /compact
/context       /resume        /rewind         /cost          /vim
/bug           /release-notes /pr-comments    /review        /security-review
/terminal-setup /export       /login          /logout        /doctor
/sandbox       /reload-plugins /tasks         /usage         /extra-usage
/recap         /rename        /feedback       /mobile        /remote-env
/web-setup     /remote-control (alias /rc)    /teleport (alias /tp)
/autofix-pr    /theme         /schedule       /exit
```

Plus the **bundled skills** that ship with Claude Code:

```
/simplify      /batch         /debug          /loop          /claude-api
```

See [slash-commands.md](./slash-commands.md) for what each does.

---

## Tool naming aliases

In **v2.1.63** the `Task` tool was renamed to **`Agent`**. Existing `Task(...)` references in settings and agent definitions still work as aliases.

---

## See also

- [headless-sdk.md](./headless-sdk.md) — deeper coverage of `-p` and the Agent SDK
- [permission-modes.md](./permission-modes.md) — what each mode actually does
- [models.md](./models.md) — model aliases and IDs
- [environment-variables.md](./environment-variables.md) — env vars that change CLI behavior
