# CLI Reference

The `deepseek-code` command starts an interactive REPL by default, runs one-shot in
print mode with `-p`, and exposes a handful of read-only management subcommands. This
page is the complete surface as reported by `deepseek-code --help` and
`deepseek-code help --all` (v2.0.0).

## Usage

```
deepseek-code [options] ["query"]
deepseek-code <subcommand> [args]
```

If the first argument is a known subcommand it is dispatched; otherwise a bare string
is treated as the opening prompt for a REPL session. With no arguments at all you get
an interactive REPL.

---

## Subcommands

| Command | What it does |
|---------|--------------|
| `deepseek-code` | Start the interactive REPL |
| `deepseek-code "query"` | Start the REPL with an initial prompt |
| `deepseek-code -p "query"` | One-shot print mode, then exit |
| `deepseek-code -c` | Continue the most recent session in the cwd |
| `deepseek-code -c -p "query"` | Continue the last session non-interactively (SDK-style) |
| `deepseek-code -r <id> "query"` | Resume a specific session by ID |
| `deepseek-code update` | Check for CLI updates *(do not run unless you intend to update)* |
| `deepseek-code auth login` | Save your DeepSeek API key |
| `deepseek-code auth status` | Report whether a key is stored |
| `deepseek-code auth logout` | Remove the stored key |
| `deepseek-code config` | Show the current configuration |
| `deepseek-code sessions` | List saved sessions |
| `deepseek-code agents` | List configured agents |
| `deepseek-code skills` | List available skills |
| `deepseek-code hooks` | List configured hooks (with handler counts per event) |
| `deepseek-code version` | Show version / backend / runtime info |
| `deepseek-code help --all` | Extended help (also lists REPL slash commands) |

The `config`, `sessions`, `agents`, `skills`, and `hooks` subcommands are **read-only
listings** — safe to run. `auth login` and `update` mutate state.

---

## Session flags

| Flag | Description |
|------|-------------|
| `--name`, `-n <name>` | Set a display name for the session |
| `--continue`, `-c` | Resume the most recent session in the cwd |
| `--resume`, `-r <id>` | Resume a specific session by ID |
| `--print`, `-p [query]` | Print mode — non-interactive, exits after the turn |
| `--session-id <uuid>` | Use a specific session ID |

See [sessions.md](sessions.md) for the full session model.

## Model flags

| Flag | Description |
|------|-------------|
| `--model <name>` | `pro`, `flash`, or a full model ID (e.g. `deepseek-v4-flash`) |
| `--effort <level>` | `low`, `medium`, `high`, `max` (default `high`) |
| `--thinking on\|off\|max` | Control extended reasoning |
| `--fallback-model <name>` | Auto-fall back when the primary model is overloaded |

See [models.md](models.md).

## Permission flags

| Flag | Description |
|------|-------------|
| `--permission-mode <mode>` | `default`, `acceptEdits`, `plan`, `auto` |
| `--allowed-tools <list>` | Tools allowed without prompting |
| `--disallowed-tools <list>` | Tools removed from the model entirely |
| `--dangerously-skip-permissions` | Bypass all permission prompts |

See [permissions.md](permissions.md). The full set of permission *modes* (including
`dontAsk` and `bypassPermissions`) is larger than what the `--permission-mode` flag
advertises — see that page.

## Tool / agent / skill flags

| Flag | Description |
|------|-------------|
| `--agent <name>` | Run the main thread as a named agent |
| `--agents <json>` | Define subagents inline from a JSON string |
| `--bare` | Skip discovery of hooks, skills, plugins, and CLAUDE.md |

`--bare` is the deterministic/CI escape hatch: it loads none of the extension
surface and gives you a clean model session. See [agents.md](agents.md) and
[skills.md](skills.md).

## Output flags

| Flag | Description |
|------|-------------|
| `--output-format <fmt>` | `text`, `json`, or `stream-json` |
| `--max-turns <N>` | Cap the number of agentic turns |
| `--max-budget-usd <amount>` | Cap dollar spend for the run |
| `--verbose` | Verbose output |
| `--quiet` | Minimal output |

`--max-turns` and `--max-budget-usd` are the two hard bounds for an autonomous run;
combine them with `-p` and `--bare` for unattended scripting.

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `DEEPSEEK_API_KEY` | DeepSeek API key (alternative to `auth login`) |
| `DEEPSEEK_CODE_MODEL` | Default model |
| `DEEPSEEK_CODE_EFFORT` | Default effort level |
| `DEEPSEEK_CODE_DISABLE_HOOKS` | Disable all hooks |
| `DEEPSEEK_CODE_BARE` | Equivalent to `--bare` |
| `DEEPSEEK_CODE_LOG_LEVEL` | `debug`, `info`, `warn`, `error` |

See [configuration.md](configuration.md) for how these interact with the config files.

---

## On-disk files

| Path | Purpose |
|------|---------|
| `~/.deepseek-code/config.json` | User settings for the CLI |
| `~/.deepseek-code/sessions/` | Session storage |
| `~/.deepseek-code/logs/` | CLI logs |
| `~/.clawspring/settings.json` | Clawspring settings (permissions, hooks, sandbox, env) |
| `~/.clawspring/hooks.json` | Hook event → handler configuration |
| `~/.clawspring/permissions.json` | Allow / ask / deny rules |
| `~/.clawspring/agents/` | Global subagent definitions |
| `~/.clawspring/skills/` | Global skills |
| `~/.clawspring/hooks/` | Hook scripts |
| `~/.config/deepseek/key` | Stored API key |
| `CLAUDE.md` / `.clawspring/` | Project-level memory & rules |

---

## REPL slash commands

When you are inside the interactive REPL, these slash commands are available (from
`deepseek-code help --all`):

| Command | Action |
|---------|--------|
| `/help` | Show available commands |
| `/model [pro\|flash]` | Switch model |
| `/effort [level]` | Set effort: low, medium, high, max |
| `/compact [focus]` | Compress conversation history |
| `/init` | Generate a CLAUDE.md for the current project |
| `/memory` | View/edit project memory |
| `/hooks` | List active hooks |
| `/agents` | List available subagents |
| `/skills` | List available skills |
| `/permissions` | View/edit permission rules |
| `/config` | Show current configuration |
| `/cost` | Show session token usage & cost |
| `/status` | Show session status |
| `/resume` | Open the session picker |
| `/rename <name>` | Rename the current session |
| `/export` | Export the session to a file |
| `/tasks` | Manage the task list |
| `/feedback` | Send feedback |
| `/exit` | Exit the REPL |

---

## Examples

```bash
deepseek-code                              # interactive REPL (Flash)
deepseek-code --model pro                  # REPL with Pro
deepseek-code -p "fix the bug in main.py"  # one-shot
deepseek-code -c                           # continue last session
deepseek-code --bare -p "lint and fix"     # CI / deterministic
cat logs.txt | deepseek-code -p "explain"  # piped input
```
