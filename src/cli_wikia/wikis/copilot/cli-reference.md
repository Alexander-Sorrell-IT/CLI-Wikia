# GitHub Copilot CLI Reference

Complete reference for the `copilot` command, derived from `copilot --help`
(version 1.0.65).

## Usage

```
copilot [options] [command]
```

Start an interactive session, or use `-p`/`--prompt` for non-interactive
scripting.

## Commands

| Command | Description |
|---------|-------------|
| `completion <shell>` | Generate a shell completion script |
| `help [topic]` | Display help information |
| `init` | Initialize Copilot instructions |
| `login [options]` | Authenticate with Copilot |
| `mcp` | Manage MCP servers |
| `plugin` | Manage plugins |
| `skill` | Manage skills |
| `update [channel]` | Download the latest version |
| `version` | Display version information |

### Help topics

`copilot help <topic>` covers: `billing`, `commands`, `config`,
`environment`, `logging`, `monitoring`, `permissions`, and `providers`
(Custom Model Providers / BYOK).

## Options

### Session & prompting

| Flag | Description |
|------|-------------|
| `-p, --prompt <text>` | Execute a prompt non-interactively (exits after) |
| `-i, --interactive <prompt>` | Start interactive mode and execute this prompt |
| `--continue` | Resume the most recent session |
| `-r, --resume[=value]` | Resume a previous session (id, task id, prefix, or name) |
| `-n, --name <name>` | Name for the new session |
| `--attachment <path>` | Attach a file to the initial prompt (non-interactive only) |
| `--enable-memory` | Enable memory in prompt mode (off by default) |

### Model & context

| Flag | Description |
|------|-------------|
| `--model <model>` | AI model to use (use `auto` to let Copilot pick) |
| `--context <tier>` | Context window tier (`default`, `long_context`) |
| `--effort, --reasoning-effort <level>` | `none`, `low`, `medium`, `high`, `xhigh`, `max` |

See [models.md](models.md) for details.

### Working directory & agents

| Flag | Description |
|------|-------------|
| `-C <directory>` | Change working directory first |
| `--add-dir <directory>` | Add a directory to the allowed list for file access |
| `--agent <agent>` | Specify a custom agent to use |

### Modes

| Flag | Description |
|------|-------------|
| `--mode <mode>` | Initial agent mode (`interactive`, `plan`, `autopilot`) |
| `--plan` | Start in plan mode |
| `--autopilot` | Start in autopilot mode |

See [modes.md](modes.md) for details.

### Permissions

| Flag | Description |
|------|-------------|
| `--allow-all` | Enable all permissions (= tools + paths + URLs) |
| `--allow-all-tools` | Allow all tools to run automatically (env: `COPILOT_ALLOW_ALL`); required for non-interactive mode |
| `--allow-all-paths` | Allow access to any path |
| `--allow-all-urls` | Allow access to all URLs without confirmation |
| `--allow-tool[=tools...]` | Tools the CLI has permission to use |
| `--deny-tool[=tools...]` | Tools the CLI may not use |
| `--allow-url[=urls...]` | Allow access to specific URLs or domains |
| `--deny-url[=urls...]` | Deny URLs/domains (precedence over `--allow-url`) |
| `--available-tools[=tools...]` | Only these tools will be available to the model |
| `--excluded-tools[=tools...]` | Tools not available to the model |
| `--no-ask-user` | Disable the `ask_user` tool (autonomous) |

See [permissions.md](permissions.md) for details.

### MCP

| Flag | Description |
|------|-------------|
| `--disable-builtin-mcps` | Disable built-in MCP servers (currently: `github-mcp-server`) |
| `--disable-mcp-server <name>` | Disable a specific MCP server |

See [mcp.md](mcp.md) for details.

### Plugins

| Flag | Description |
|------|-------------|
| `--plugin-dir <directory>` | Load a plugin from a local directory |

### Output, logging & instructions

| Flag | Description |
|------|-------------|
| `--output-format <format>` | `text` (default) or `json` (JSONL) |
| `--log-dir <directory>` | Log file directory (default: `~/.copilot/logs/`) |
| `--log-level <level>` | `none`, `error`, `warning`, `info`, `debug`, `all`, `default` |
| `--no-custom-instructions` | Disable loading `AGENTS.md` and related files |

### Protocols & remote

| Flag | Description |
|------|-------------|
| `--acp` | Start as Agent Client Protocol server |
| `--remote` | Enable remote control of your session |
| `--no-remote` | Disable remote control from GitHub web/mobile |
| `--experimental` | Enable experimental features |

> Verify exact values in the official docs / run `copilot --help`.
