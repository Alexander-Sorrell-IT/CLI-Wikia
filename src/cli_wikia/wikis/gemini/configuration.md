# Configuration (Gemini CLI)

## Workspace directories

By default the CLI operates on the current working directory. Add more
directories to the workspace with:

```bash
gemini --include-directories ../shared,../libs "run the tests"
```

`--include-directories` accepts a comma-separated list or can be passed
multiple times.

## Accessibility

```bash
gemini --screen-reader
```

Enables screen reader mode for accessibility.

## Debugging

```bash
gemini -d "why did this fail?"
```

`-d`/`--debug` runs the CLI in debug mode (default: `false`).

## Output format

Control machine-readable output for scripting:

```bash
gemini -o json "list project dependencies"
```

| Value | Description |
|-------|-------------|
| `text` | Human-readable output |
| `json` | Single JSON object |
| `stream-json` | Streamed JSON events |

## MCP & extensions configuration

- MCP servers are managed through `gemini mcp` — see [mcp.md](mcp.md).
- Extensions are managed through `gemini extensions` — see
  [extensions.md](extensions.md).

## Config files & environment variables

The version 0.22.4 `--help` output does not document specific config file
paths or environment variable names.

> Verify config file locations and environment variables in the official
> Gemini CLI docs, or run `gemini --help`.
