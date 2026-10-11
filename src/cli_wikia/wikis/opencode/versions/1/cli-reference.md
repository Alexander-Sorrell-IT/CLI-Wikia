# opencode CLI reference

> wiki-version: 1 | cli-version: v2.0.22 | verified: 2026-10-10
> source: `opencode --help` + `opencode run --help` on maintainer machine.

## Usage

```
opencode <subcommand> [flags] [<directory>]
opencode run [flags] [<message...>]     # headless, message last
```

## Subcommands

| Command | Purpose |
|---------|---------|
| `run` | Run with a message (headless here) |
| `acp` | Start an Agent Client Protocol server |
| `api` | Request the running server |
| `auth` | Manage integrations and credentials |
| `mcp` | Manage MCP servers |
| `plugin` | Manage plugins |
| `models` | List available models |
| `stats` | Shareable usage statistics |
| `mini` | Minimal interactive interface |
| `session` | Manage sessions |
| `service` | Manage the background server |
| `serve` | Start the v2 API + web server |
| `reload` | Reload configuration |
| `pair` | One-time links to connect browser/app |
| `debug` | Debugging and troubleshooting tools |
| `upgrade`/`update`, `uninstall` | Install management |

## Notable flags

- `run`: `--format default|json`, `-m/--model provider/model#variant`,
  `--agent`, `-s/--session`, `-c/--continue`, `--fork`, `-f/--file`,
  `--title`, `--standalone`, `--server`
- Root: `--auto` (approve non-denied permissions), `--prompt` (TUI prompt),
  `--standalone`, `--server`, `--session/-s`, `--continue/-c`
- Global: `--log-level`, `--print-logs`, `--completions`, `--wizard`
