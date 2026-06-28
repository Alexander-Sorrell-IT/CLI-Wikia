# DeepSeek Code

DeepSeek Code is a command-line coding assistant. Start an interactive REPL,
or use `-p`/`--print` for one-shot, non-interactive runs and scripting.

- **Tool:** `deepseek-code`
- **Version referenced:** 2.0.0 (DeepSeek V4 × Claude Code Hybrid)
- **Backend:** DeepSeek V4 Pro 1.6T / Flash 284B
- **Framework:** Clawspring Agent Runtime

## Quick start

```bash
# Interactive REPL
deepseek-code

# REPL with an initial prompt
deepseek-code "explain this repository"

# One-shot print mode, then exit
deepseek-code -p "write a unit test for utils.py"

# Continue the most recent session
deepseek-code -c

# Resume a specific session
deepseek-code -r <id> "keep going"

# Pick a model
deepseek-code --model pro "refactor the logging module"
```

## Authentication

```bash
deepseek-code auth login     # Save DeepSeek API key
deepseek-code auth status    # Check authentication status
```

## Topics

| File | Description |
|------|-------------|
| [cli-reference.md](cli-reference.md) | Full flags and subcommands |
| [models.md](models.md) | Selecting a model, effort, and thinking |
| [configuration.md](configuration.md) | Config file fields and env vars |
| [permissions.md](permissions.md) | Permission modes and tool controls |
| [sessions-and-agents.md](sessions-and-agents.md) | Sessions, agents, skills, hooks |

## Subcommands at a glance

| Command | Purpose |
|---------|---------|
| `deepseek-code` | Start interactive REPL |
| `deepseek-code update` | Check for updates |
| `deepseek-code auth login` / `auth status` | Manage authentication |
| `deepseek-code config` | Show/edit config |
| `deepseek-code sessions` | List saved sessions |
| `deepseek-code agents` | List configured agents |
| `deepseek-code skills` | List available skills |
| `deepseek-code hooks` | List configured hooks |
| `deepseek-code version` | Show version info |

> Verify exact values in the official docs / run `deepseek-code --help`.
