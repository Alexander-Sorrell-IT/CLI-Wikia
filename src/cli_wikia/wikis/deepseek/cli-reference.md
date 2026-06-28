# DeepSeek Code Reference

Complete reference for the `deepseek-code` command, derived from its `--help`
output (version 2.0.0).

## Usage

```
deepseek-code [options] ["query"]
deepseek-code <subcommand> [args]
```

## Subcommands

| Command | Description |
|---------|-------------|
| `deepseek-code` | Start interactive REPL |
| `deepseek-code "query"` | Start REPL with an initial prompt |
| `deepseek-code -p "query"` | One-shot print mode, then exit |
| `deepseek-code -c` | Continue most recent session |
| `deepseek-code -c -p "query"` | Continue via SDK |
| `deepseek-code -r <id> "query"` | Resume a specific session |
| `deepseek-code update` | Check for updates |
| `deepseek-code auth login` | Save DeepSeek API key |
| `deepseek-code auth status` | Check authentication status |
| `deepseek-code config` | Show/edit config |
| `deepseek-code sessions` | List saved sessions |
| `deepseek-code agents` | List configured agents |
| `deepseek-code skills` | List available skills |
| `deepseek-code hooks` | List configured hooks |
| `deepseek-code version` | Show version info |

## Session flags

| Flag | Description |
|------|-------------|
| `--name, -n <name>` | Set display name for session |
| `--continue, -c` | Resume most recent session in cwd |
| `--resume, -r <id>` | Resume specific session |
| `--print, -p [query]` | Print mode — non-interactive |
| `--session-id <uuid>` | Use specific session ID |

See [sessions-and-agents.md](sessions-and-agents.md) for details.

## Model flags

| Flag | Description |
|------|-------------|
| `--model <name>` | `pro`, `flash`, or a full model ID |
| `--effort <level>` | `low`, `medium`, `high`, `max` (default: `high`) |
| `--thinking on\|off\|max` | Control reasoning mode |
| `--fallback-model <name>` | Auto-fallback when default overloaded |

See [models.md](models.md) for details.

## Permission flags

| Flag | Description |
|------|-------------|
| `--permission-mode <mode>` | `default`, `acceptEdits`, `plan`, `auto` |
| `--allowed-tools <list>` | Tools allowed without prompting |
| `--disallowed-tools <list>` | Tools removed from model |
| `--dangerously-skip-permissions` | Bypass all permission prompts |

See [permissions.md](permissions.md) for details.

## Tool / agent / skill flags

| Flag | Description |
|------|-------------|
| `--agent <name>` | Run main thread as named agent |
| `--agents <json>` | Define subagents from JSON |
| `--bare` | Skip discovery (hooks, skills, plugins, CLAUDE.md) |

## Output flags

| Flag | Description |
|------|-------------|
| `--output-format <fmt>` | `text`, `json`, `stream-json` |
| `--max-turns <N>` | Limit agentic turns |
| `--max-budget-usd <amount>` | Cap dollar spend |
| `--verbose` | Verbose output |
| `--quiet` | Minimal output |

## Environment variables

| Variable | Description |
|----------|-------------|
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `DEEPSEEK_CODE_MODEL` | Default model |

See [configuration.md](configuration.md) for the config file.

> Verify exact values in the official docs / run `deepseek-code --help`.
