# GitHub Copilot CLI

The GitHub Copilot CLI is an AI-powered coding assistant. Start an interactive
session, or use `-p`/`--prompt` for non-interactive scripting.

- **Tool:** `copilot`
- **Version referenced:** 1.0.65

## Quick start

```bash
# Interactive session
copilot

# Execute a prompt non-interactively (exits after)
copilot -p "explain this repository"

# Start interactive mode with an initial prompt
copilot -i "summarize the open TODOs"

# Pick a model (or let Copilot choose)
copilot --model auto -p "write a unit test for utils.py"

# Resume the most recent session
copilot --continue
```

## Authentication

```bash
copilot login        # Authenticate with Copilot
copilot init         # Initialize Copilot instructions
```

## Topics

| File | Description |
|------|-------------|
| [cli-reference.md](cli-reference.md) | Full flags and subcommands |
| [models.md](models.md) | Selecting a model and context/effort options |
| [configuration.md](configuration.md) | Config files, logs, and env vars |
| [mcp.md](mcp.md) | Managing MCP servers (`copilot mcp`) |
| [permissions.md](permissions.md) | Allow/deny tools, paths, and URLs |
| [modes.md](modes.md) | Interactive, plan, and autopilot modes |

## Commands at a glance

| Command | Purpose |
|---------|---------|
| `copilot completion <shell>` | Generate a shell completion script |
| `copilot help [topic]` | Display help information |
| `copilot init` | Initialize Copilot instructions |
| `copilot login` | Authenticate with Copilot |
| `copilot mcp` | Manage MCP servers |
| `copilot plugin` | Manage plugins |
| `copilot skill` | Manage skills |
| `copilot update [channel]` | Download the latest version |
| `copilot version` | Display version information |

> Verify exact values in the official docs / run `copilot --help`.
