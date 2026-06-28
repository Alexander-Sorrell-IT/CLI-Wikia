# Gemini CLI

Gemini CLI is Google's command-line coding assistant. Launch an interactive
session, or run one-shot prompts with `-p`/`--prompt` (or a positional query)
for non-interactive scripting and automation.

- **Tool:** `gemini`
- **Version referenced:** 0.22.4

## Quick start

```bash
# Interactive session
gemini

# One-shot prompt (non-interactive, prints and exits)
gemini "explain this repository"

# Run a prompt, then drop into interactive mode
gemini -i "summarize the open TODOs"

# Pick a model
gemini -m <model> "write a unit test for utils.py"

# Auto-approve all actions (YOLO)
gemini -y "refactor the logging module"

# Resume the most recent session
gemini --resume latest
```

## Topics

| File | Description |
|------|-------------|
| [cli-reference.md](cli-reference.md) | Full flags, options, and subcommands |
| [models.md](models.md) | Selecting a model with `-m`/`--model` |
| [configuration.md](configuration.md) | Config locations and environment |
| [mcp.md](mcp.md) | Managing MCP servers (`gemini mcp`) |
| [extensions.md](extensions.md) | Managing Gemini CLI extensions |
| [sessions.md](sessions.md) | Resume, list, and delete sessions |

## Commands at a glance

| Command | Purpose |
|---------|---------|
| `gemini [query..]` | Launch Gemini CLI (default) |
| `gemini mcp` | Manage MCP servers |
| `gemini extensions <command>` | Manage Gemini CLI extensions |

> Verify exact values in the official docs / run `gemini --help`.
