# qwen CLI reference

> wiki-version: 1 | cli-version: 0.24.7 | verified: 2026-10-10
> source: `qwen --help` output on maintainer machine.

## Usage

```
qwen [query..]                 # positional prompt, one-shot by default
qwen -i "{prompt}"             # execute then continue interactively
qwen [options] [command]
```

## Commands

| Command | Purpose |
|---------|---------|
| `auth` | Configure authentication (removed upstream) |
| `batch <command>` | Many independent requests via DashScope Batch API |
| `board <command>` | Share work with other agents through a board |
| `channel <command>` | Manage messaging channels (Telegram, Discord, ...) |
| `extensions <command>` | Manage extensions |
| `hooks` | Manage hooks (use `/hooks` in interactive mode) |
| `mcp` | Manage MCP servers (add/remove/list/reconnect/approve/reject) |
| `review <command>` | Non-interactive review (`run`) + `/review` skill helpers |
| `sandbox [cmd...]` | Inspect sandbox backend or run one confined command |

## Notable options

- `-p/--prompt` — prompt text (DEPRECATED, use positional instead)
- `-i/--prompt-interactive` — run prompt then stay interactive
- `-y/--yolo` — auto-approve all actions
- `--approval-mode plan|default|auto-edit|auto|yolo`
- `-m/--model`, `--advisor`, `--fallback-model` (repeatable, max 3)
- `-s/--sandbox`, `--sandbox-image` (deprecated flag, use setting)
- `--system-prompt` / `--append-system-prompt`, `--output-style`
- `--mcp-config` (JSON string or file with `{"mcpServers": {...}}`)
- `--worktree <slug|#PR|URL>` — session inside `<repo>/.qwen/worktrees/<slug>/`
- `--acp` (ACP mode), `--experimental-lsp`, `--bare`, `--debug`
- `--safe-mode` — disables hooks/extensions/skills/MCP (troubleshooting only)
- `--chat-recording` — persist chat history (`--continue/--resume` need it)
- `--proxy`, `--insecure` (TLS skip, lab only), `--json-fd`
- `--telemetry*` — all deprecated; use `telemetry.*` in settings.json
