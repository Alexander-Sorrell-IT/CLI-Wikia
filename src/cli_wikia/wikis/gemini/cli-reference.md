# Gemini CLI Reference

Complete reference for the `gemini` command, derived from `gemini --help`
(version 0.22.4).

## Usage

```
gemini [options] [command]
```

Gemini CLI launches an interactive CLI by default. Use `-p`/`--prompt` (or a
positional query) for non-interactive mode.

## Commands

| Command | Description |
|---------|-------------|
| `gemini [query..]` | Launch Gemini CLI (default command) |
| `gemini mcp` | Manage MCP servers |
| `gemini extensions <command>` | Manage Gemini CLI extensions (alias: `extension`) |

## Positionals

| Positional | Description |
|------------|-------------|
| `query` | Positional prompt. Defaults to one-shot; use `-i`/`--prompt-interactive` for interactive. |

## Options

### General

| Flag | Description |
|------|-------------|
| `-d, --debug` | Run in debug mode (default: `false`) |
| `-m, --model` | Model (string) |
| `-v, --version` | Show version number |
| `-h, --help` | Show help |
| `--screen-reader` | Enable screen reader mode for accessibility |

### Prompting & input

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Prompt. Appended to input on stdin. *(deprecated: use positional prompt)* |
| `-i, --prompt-interactive` | Execute the provided prompt and continue in interactive mode |
| `--include-directories` | Additional directories to include in the workspace (comma-separated or multiple) |

### Approvals & sandboxing

| Flag | Description |
|------|-------------|
| `-s, --sandbox` | Run in sandbox |
| `-y, --yolo` | Automatically accept all actions (YOLO mode) (default: `false`) |
| `--approval-mode` | Approval mode: `default` (prompt), `auto_edit` (auto-approve edit tools), `yolo` (auto-approve all tools) |
| `--allowed-tools` | Tools allowed to run without confirmation (array) |
| `--allowed-mcp-server-names` | Allowed MCP server names (array) |

### Extensions

| Flag | Description |
|------|-------------|
| `-e, --extensions` | List of extensions to use. If not provided, all extensions are used (array) |
| `-l, --list-extensions` | List all available extensions and exit |

See [extensions.md](extensions.md) for the `gemini extensions` subcommand.

### Sessions

| Flag | Description |
|------|-------------|
| `-r, --resume` | Resume a previous session. Use `latest` for most recent or an index number (e.g. `--resume 5`) |
| `--list-sessions` | List available sessions for the current project and exit |
| `--delete-session` | Delete a session by index number |

See [sessions.md](sessions.md) for details.

### Output & protocols

| Flag | Description |
|------|-------------|
| `-o, --output-format` | CLI output format: `text`, `json`, `stream-json` |
| `--experimental-acp` | Start the agent in ACP (Agent Client Protocol) mode |

## MCP subcommands

| Command | Description |
|---------|-------------|
| `gemini mcp add <name> <commandOrUrl> [args...]` | Add a server |
| `gemini mcp remove <name>` | Remove a server |
| `gemini mcp list` | List all configured MCP servers |

See [mcp.md](mcp.md) for details.

> Verify exact values in the official docs / run `gemini --help`.
