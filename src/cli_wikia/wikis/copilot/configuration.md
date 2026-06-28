# Configuration (GitHub Copilot CLI)

## Config directory

GitHub Copilot CLI stores its files under:

```
~/.copilot/
```

| Path | Description |
|------|-------------|
| `~/.copilot/` | Config directory |
| `~/.copilot/mcp-config.json` | MCP server configuration |
| `~/.copilot/logs/` | Log file directory (default) |

## Logging

```bash
copilot --log-dir ./mylogs --log-level debug
```

| Flag | Description |
|------|-------------|
| `--log-dir <directory>` | Log file directory (default: `~/.copilot/logs/`) |
| `--log-level <level>` | `none`, `error`, `warning`, `info`, `debug`, `all`, `default` |

For more, see `copilot help logging` and `copilot help monitoring`.

## Custom instructions

By default the CLI loads `AGENTS.md` and related instruction files. Disable
this with:

```bash
copilot --no-custom-instructions
```

Initialize instruction files with:

```bash
copilot init
```

## Memory

Memory is off by default in prompt mode. Enable it with:

```bash
copilot --enable-memory -p "remember the project conventions"
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `COPILOT_ALLOW_ALL` | Equivalent to `--allow-all-tools` (allow all tools to run automatically) |

For more environment variables, see `copilot help environment`.

## Output format

```bash
copilot -p "list dependencies" --output-format json
```

| Value | Description |
|-------|-------------|
| `text` | Human-readable output (default) |
| `json` | JSONL output |

## Related

- MCP configuration — see [mcp.md](mcp.md).
- Permissions — see [permissions.md](permissions.md).
- Billing and config help: `copilot help billing`, `copilot help config`.

> Verify exact values in the official docs / run `copilot --help`.
