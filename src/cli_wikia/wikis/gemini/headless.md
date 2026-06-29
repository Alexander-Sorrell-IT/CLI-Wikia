# Headless mode

Headless mode gives Gemini CLI a programmatic interface that returns structured
text or JSON without an interactive terminal UI. Use it for scripting, CI
pipelines, and automation.

## Triggering headless mode

Headless mode runs when either condition is true:

- You pass a query with the `-p` (or `--prompt`) flag, or
- The CLI is run in a **non-TTY** environment (for example, piped input or
  output).

```bash
# Prompt flag
gemini -p "summarize the README"

# Piped via stdin (non-TTY)
cat error.log | gemini -p "what is causing these errors?"
```

> A bare positional prompt (`gemini "..."`) may also be accepted depending on
> your version — verify in official docs. The reliably documented entry point is
> `-p`/`--prompt`.

## Output formats

Select the format with `--output-format`. The default is human-readable text.

| Format        | Flag value    | Description                                              |
| ------------- | ------------- | ------------------------------------------------------- |
| Text          | `text`        | Plain final answer (default).                           |
| JSON          | `json`        | A single JSON object with the response and usage stats. |
| Streaming JSON | `stream-json` | Newline-delimited JSON (JSONL) events as they occur.    |

### JSON output

Returns one JSON object:

| Field      | Type             | Description                              |
| ---------- | ---------------- | ---------------------------------------- |
| `response` | string           | The model's final answer.                |
| `stats`    | object           | Token usage and API latency metrics.     |
| `error`    | object, optional | Error details if the request failed.     |

```bash
gemini -p "list 3 git tips" --output-format json
```

```json
{
  "response": "...",
  "stats": { }
}
```

### Streaming JSON output

Returns a stream of newline-delimited JSON (JSONL) events:

| Event type    | Meaning                                                              |
| ------------- | ------------------------------------------------------------------- |
| `init`        | Session metadata (session ID, model).                               |
| `message`     | User and assistant message chunks.                                  |
| `tool_use`    | Tool call requests with arguments.                                  |
| `tool_result` | Output from executed tools.                                         |
| `error`       | Non-fatal warnings and system errors.                               |
| `result`      | Final outcome with aggregated stats and per-model token breakdowns. |

```bash
gemini -p "refactor utils.ts" --output-format stream-json
```

## Exit codes

| Code | Meaning                              |
| ---- | ------------------------------------ |
| `0`  | Success.                             |
| `1`  | General error or API failure.        |
| `42` | Input error (invalid prompt/args).   |
| `53` | Turn limit exceeded.                 |

## Automation patterns

```bash
# Capture just the answer for use elsewhere
answer=$(gemini -p "generate a commit message for staged changes" --output-format text)

# Parse JSON with jq
gemini -p "list the API endpoints" --output-format json | jq -r '.response'

# Pipe a file in, branch on exit code
if cat config.yaml | gemini -p "is this valid? answer yes or no"; then
  echo "checked"
fi

# Stream events to a processor
gemini -p "run the test suite and summarize" --output-format stream-json \
  | while read -r line; do echo "$line" | jq -r '.type'; done
```

## ACP mode (Agent Client Protocol)

ACP mode is a special operational mode for programmatic control, primarily for
IDE and developer-tool integrations. It speaks **JSON-RPC 2.0 over stdio**
between the Gemini CLI agent (server) and a client (editor/IDE). Start it with:

```bash
gemini --acp
gemini --acp --debug      # add general debugging logs
```

> Some versions expose this as `--experimental-acp`; verify the flag name for
> your build in official docs.

ACP standardizes how AI coding agents talk to editors so an agent can be
implemented once and work with any ACP-compliant client. Gemini CLI is listed in
the ACP Agent Registry.

### Methods

| Category        | Methods                                                              |
| --------------- | ------------------------------------------------------------------- |
| Core            | `initialize`, `authenticate`, `newSession`, `loadSession`, `prompt`, `cancel` |
| Session control | `setSessionMode` (e.g. `auto-approve`), `unstable_setSessionModel`  |

ACP includes a **proxied file system**: the agent reads and writes files through
the client, so it only touches files the user has allowed. The client can also
expose its own functionality as **MCP** tools — during the `initialize`
handshake the client provides its MCP server connection details, and Gemini CLI
discovers those tools and offers them to the model.

### Telemetry

Capture detailed ACP/agent telemetry to a file with environment variables:

```bash
GEMINI_TELEMETRY_ENABLED=true \
GEMINI_TELEMETRY_TARGET=local \
GEMINI_TELEMETRY_OUTFILE=/path/to/log.json \
gemini --acp
```

## System prompt override

The built-in system prompt can be completely replaced with your own Markdown via
the `GEMINI_SYSTEM_MD` environment variable. This is a **full replacement, not a
merge** — none of the original core instructions apply unless you include them.

| Value                          | Effect                                                            |
| ------------------------------ | ---------------------------------------------------------------- |
| `1` or `true`                  | Read `./.gemini/system.md` (relative to the project directory).  |
| `/abs/path.md`, `./rel.md`, `~/f.md` | Use a custom file (relative resolved from CWD; `~` expands). |
| `0`, `false`, or unset         | Use the built-in prompt.                                         |

If the override is enabled but the file is missing, the CLI errors with
`missing system prompt file '<path>'`. When active, the UI shows a `|⌐■_■|`
indicator.

Set it temporarily in your shell, or persist it in a `.gemini/.env` file:

```bash
GEMINI_SYSTEM_MD=1 gemini                 # one-off, project ./.gemini/system.md
GEMINI_SYSTEM_MD=~/prompts/system.md gemini
```

### Export the default prompt first (recommended)

Write the current built-in prompt to a file so you can review and selectively
edit it:

```bash
GEMINI_WRITE_SYSTEM_MD=1 gemini                       # writes ./.gemini/system.md
GEMINI_WRITE_SYSTEM_MD=~/prompts/DEFAULT_SYSTEM.md gemini
```

### Variable substitution

Inside a custom system prompt you can inject built-in content dynamically:

| Variable                  | Injects                                              |
| ------------------------- | --------------------------------------------------- |
| `${AgentSkills}`          | A complete section of all available agent skills.   |
| `${SubAgents}`            | A complete section of available sub-agents.         |
| `${AvailableTools}`       | A bulleted list of all enabled tool names.          |
| `${<tool>_ToolName}`      | The actual name of a tool, e.g. `${write_file_ToolName}`. |

```markdown
# Custom System Prompt

You are a helpful assistant. ${AgentSkills}
${SubAgents}

The following tools are available to you: ${AvailableTools}
You can use ${write_file_ToolName} to save logs.
```

> Think of **system.md** as firmware (non-negotiable safety and tool-use rules,
> stable across tasks) and **GEMINI.md** as strategy (persona, goals, project
> context that evolves). Keep system.md minimal but complete for safe operation.

## See also

- [cli-reference.md](./cli-reference.md) — `-p`, `--output-format`, `--acp`
- [configuration.md](./configuration.md) — `GEMINI_SYSTEM_MD`, `.gemini/.env`
- [mcp.md](./mcp.md) — exposing client tools via MCP under ACP
- [context-files.md](./context-files.md) — GEMINI.md vs. system.md
