# Hooks (Gemini CLI)

Hooks are scripts or programs that Gemini CLI executes at specific points in the
agentic loop, letting you intercept and customize behavior without modifying the
CLI's source. Hooks run **synchronously**: when an event fires, the CLI waits
for all matching hooks to finish before continuing.

With hooks you can:

- **Add context** before the model sees a request (e.g. inject git history).
- **Validate actions** and block dangerous tool calls.
- **Enforce policies** with security scanners and compliance checks.
- **Log interactions** for auditing.
- **Optimize behavior** by filtering tools or adjusting model parameters.

> ⚠️ **Hooks execute arbitrary code with your user privileges.** Project-level
> hooks are risky in untrusted projects. Gemini CLI **fingerprints** project
> hooks; if a hook's name or command changes (e.g. via `git pull`), it is
> treated as a new, untrusted hook and you are warned before it runs.

## Hook events

Hooks are triggered by lifecycle events. Each event has a different impact on
the loop:

| Event | When it fires | Impact | Can block? |
| :---- | :------------ | :----- | :--------- |
| `SessionStart` | A session begins (startup, resume, clear) | Inject context | No (advisory) |
| `SessionEnd` | A session ends (exit, clear) | Advisory | No (best effort) |
| `BeforeAgent` | After the user submits a prompt, before planning | Add context / block turn | **Yes** |
| `AfterAgent` | When the agent loop ends (final response) | Retry / halt | **Yes** |
| `BeforeModel` | Before sending a request to the LLM | Modify request / mock response / block | **Yes** |
| `AfterModel` | After receiving an LLM response chunk | Redact / replace / block | **Yes** |
| `BeforeToolSelection` | Before the LLM selects tools | Filter the available toolset | Filter only |
| `BeforeTool` | Before a tool executes | Validate / rewrite args / block | **Yes** |
| `AfterTool` | After a tool executes | Process / hide result / tail-call | **Yes** |
| `PreCompress` | Before context compression | Advisory | No (async) |
| `Notification` | When a system notification occurs (e.g. tool permission) | Advisory | No |

## I/O contract

Hooks communicate over standard streams: **JSON in via `stdin`, JSON out via
`stdout`, logs via `stderr`.**

### The "golden rule": stdout must be silent

Your script **must not** print anything to `stdout` except the final JSON
object. Even a single stray `echo`/`print` breaks parsing — the CLI then
defaults to "Allow" and treats the whole output as a `systemMessage`. Send all
logging and debugging to `stderr` (e.g. `echo "debug" >&2`); the CLI captures
`stderr` but never parses it as JSON.

### Exit codes

| Exit code | Label | Behavioral impact |
| :-------- | :---- | :---------------- |
| `0` | Success | `stdout` is parsed as JSON. **Preferred** for all logic, including intentional blocks (e.g. `{"decision": "deny"}`). |
| `2` | System block | Critical block — the target action (tool, turn, or stop) is aborted. `stderr` becomes the rejection reason. The turn continues for tool events. |
| Other | Warning | Non-fatal failure; a warning is shown and the interaction proceeds with the original parameters. |

There are two ways to block: the **structured** route (exit `0` with
`{"decision": "deny", "reason": "..."}`) is idiomatic for production; the
**emergency brake** (print to `stderr`, exit `2`) suits simple gates and rapid
prototyping.

### Base input schema

Every hook receives these fields on `stdin`:

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "string",
  "timestamp": "string"
}
```

Individual events add their own fields (see the per-event reference below).

### Common output fields

Most hooks support these `stdout` JSON fields:

| Field | Type | Description |
| :---- | :--- | :---------- |
| `systemMessage` | string | Displayed immediately to the user in the terminal. |
| `suppressOutput` | boolean | If `true`, hides internal hook metadata from logs/telemetry. |
| `continue` | boolean | If `false`, stops the entire agent loop immediately. |
| `stopReason` | string | Shown to the user when `continue` is `false`. |
| `decision` | string | `"allow"` or `"deny"` (alias `"block"`). Exact effect depends on the event. |
| `reason` | string | Feedback/error message sent when `decision` is `"deny"`. |

Event-specific data is returned under `hookSpecificOutput` (with a matching
`hookEventName`), e.g. `additionalContext`, `tool_input`, `llm_request`,
`toolConfig`.

## Matchers

The `matcher` field filters which triggers fire a hook:

- **Tool events** (`BeforeTool`, `AfterTool`): matchers are **regular
  expressions** compared against the tool name (e.g. `"write_.*"`,
  `"write_file|replace"`). MCP tools are named `mcp_<server>_<tool>`.
- **Lifecycle events**: matchers are **exact strings** (e.g. `"startup"`,
  `"exit"`).
- **Wildcards**: `"*"` or `""` (empty string) matches all occurrences.

## Configuration

Hooks are configured in `settings.json` under the `hooks` object. The CLI merges
layers in this order of precedence (highest to lowest):

1. **Project**: `.gemini/settings.json`
2. **User**: `~/.gemini/settings.json`
3. **System**: `/etc/gemini-cli/settings.json`
4. **Extensions**: hooks defined by installed extensions

Each event holds an array of **hook definitions**; each definition holds a
`hooks` array of **hook configurations**.

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "write_file|replace",
        "hooks": [
          {
            "name": "security-check",
            "type": "command",
            "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/security.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### Hook definition fields

| Field | Type | Required | Description |
| :---- | :--- | :------- | :---------- |
| `matcher` | string | No | Regex (tools) or exact string (lifecycle) selecting when the hook runs. |
| `sequential` | boolean | No | If `true`, hooks in the group run one after another; if `false`, in parallel. |
| `hooks` | array | **Yes** | Array of hook configurations. |

### Hook configuration fields

| Field | Type | Required | Description |
| :---- | :--- | :------- | :---------- |
| `type` | string | **Yes** | Execution engine. Currently only `"command"` is supported. |
| `command` | string | **Yes\*** | Shell command to execute (required when `type` is `"command"`). |
| `name` | string | No | Friendly name shown in logs and CLI commands. |
| `timeout` | number | No | Execution timeout in milliseconds (default `60000`). |
| `description` | string | No | Brief explanation of the hook's purpose. |

> The docs reference a `hooksConfig` setting alongside `hooks`; its exact schema
> is not specified in the source — verify in official docs.

### Environment variables

Hooks run with a sanitized environment that includes:

| Variable | Description |
| :------- | :---------- |
| `GEMINI_PROJECT_DIR` | Absolute path to the project root. |
| `GEMINI_PLANS_DIR` | Absolute path to the plans directory. |
| `GEMINI_SESSION_ID` | Unique ID for the current session. |
| `GEMINI_CWD` | Current working directory. |
| `CLAUDE_PROJECT_DIR` | Alias provided for compatibility. |

## Per-event reference

### Tool hooks

**`BeforeTool`** — fires before a tool is invoked; used for argument validation,
security checks, and parameter rewriting.

- Input: `tool_name`, `tool_input` (raw model args), `mcp_context`,
  `original_request_name`.
- Output: `decision: "deny"` (alias `"block"`) prevents execution and the
  required `reason` is returned **to the agent** as a tool error;
  `hookSpecificOutput.tool_input` **merges over** the model's args before
  execution; `continue: false` kills the whole loop.
- Exit `2` blocks the tool, using `stderr` as the reason. **The turn continues.**

**`AfterTool`** — fires after a tool executes; used for auditing, context
injection, or hiding output.

- Input: `tool_name`, `tool_input`, `tool_response` (`llmContent`,
  `returnDisplay`, optional `error`), `mcp_context`, `original_request_name`.
- Output: `decision: "deny"` hides the real output (the `reason` **replaces** the
  result sent to the model); `hookSpecificOutput.additionalContext` is
  **appended** to the result; `hookSpecificOutput.tailToolCallRequest`
  (`{ name, args }`) runs another tool whose result replaces this one's;
  `continue: false` kills the loop.
- Exit `2` hides the result, using `stderr` as the replacement. The turn
  continues.

### Agent hooks

**`BeforeAgent`** — fires after the user submits a prompt, before planning.

- Input: `prompt` (original user text).
- Output: `hookSpecificOutput.additionalContext` is **appended** to the prompt
  for this turn only; `decision: "deny"` blocks the turn and **discards** the
  message (not saved to history); `continue: false` blocks the turn but **saves**
  the message to history; `reason` required when denied/stopped.
- Exit `2` aborts the turn and erases the prompt (same as `decision: "deny"`).

**`AfterAgent`** — fires once per turn after the model's final response; used for
response validation and automatic retries.

- Input: `prompt`, `prompt_response` (final agent text), `stop_hook_active`
  (already in a retry sequence?).
- Output: `decision: "deny"` rejects the response and forces a retry, sending
  `reason` **to the agent as a new prompt**; `continue: false` stops the session
  without retrying; `hookSpecificOutput.clearContext: true` clears LLM memory
  while preserving the UI display.
- Exit `2` triggers an automatic retry using `stderr` as the feedback prompt.

### Model hooks

**`BeforeModel`** — fires before sending a request to the LLM; operates on a
stable, SDK-agnostic request format.

- Input: `llm_request` (`model`, `messages`, `config`).
- Output: `hookSpecificOutput.llm_request` **overrides** parts of the outgoing
  request (e.g. swap model or temperature);
  `hookSpecificOutput.llm_response` provides a **synthetic response** that skips
  the LLM call entirely; `decision: "deny"` blocks and aborts the turn.
- Exit `2` aborts the turn and skips the LLM call, using `stderr` as the error.

**`BeforeToolSelection`** — fires before the LLM decides which tools to call;
used to filter the toolset or force a tool mode.

- Input: `llm_request` (same format as `BeforeModel`).
- Output: `hookSpecificOutput.toolConfig.mode` is `"AUTO" | "ANY" | "NONE"`
  (`"NONE"` disables all tools and wins over other hooks; `"ANY"` forces at least
  one tool call); `hookSpecificOutput.toolConfig.allowedFunctionNames` is a
  whitelist of tool names.
- **Union strategy:** multiple hooks' whitelists are **combined**. This event
  does **not** support `decision`, `continue`, or `systemMessage`.

**`AfterModel`** — fires immediately after an LLM response chunk; used for
real-time redaction or PII filtering.

- Input: `llm_request` (original), `llm_response` (response or a single
  streaming chunk).
- Output: `hookSpecificOutput.llm_response` **replaces** the response chunk;
  `decision: "deny"` discards the chunk and blocks the turn; `continue: false`
  kills the loop.
- **Streaming:** fires for **every chunk**; modifications affect only the current
  chunk. Exit `2` aborts the turn and discards the output.

### Lifecycle & system hooks

**`SessionStart`** — fires on startup, resume, or after `/clear`.

- Input: `source` (`"startup" | "resume" | "clear"`).
- Output: `hookSpecificOutput.additionalContext` is injected as the first turn
  (interactive) or prepended to the prompt (non-interactive); `systemMessage`
  shown at session start.
- **Advisory only:** `continue` and `decision` are ignored — startup is never
  blocked.

**`SessionEnd`** — fires when the CLI exits or a session is cleared.

- Input: `reason` (`"exit" | "clear" | "logout" | "prompt_input_exit" |
  "other"`).
- Output: `systemMessage` shown during shutdown.
- **Best effort:** the CLI does not wait for completion and ignores all
  flow-control fields.

**`Notification`** — fires on a system alert (e.g. tool permissions).

- Input: `notification_type` (`"ToolPermission"`), `message`, `details`.
- Output: `systemMessage`. **Observability only** — cannot block alerts or grant
  permissions; flow-control fields ignored.

**`PreCompress`** — fires before history is summarized to save tokens.

- Input: `trigger` (`"auto" | "manual"`).
- Output: `systemMessage`. **Advisory only**, fired asynchronously — cannot block
  or modify compression.

### Stable model API

To keep hooks working across SDK updates, `llm_request` / `llm_response` use
stable shapes:

```typescript
// LLMRequest
{
  "model": string,
  "messages": Array<{ "role": "user" | "model" | "system", "content": string }>,
  "config": { "temperature": number },
  "toolConfig": { "mode": string, "allowedFunctionNames": string[] }
}

// LLMResponse
{
  "candidates": Array<{
    "content": { "role": "model", "parts": string[] },
    "finishReason": string
  }>,
  "usageMetadata": { "totalTokenCount": number }
}
```

## Managing hooks (`/hooks`)

Manage hooks from an interactive session without editing JSON:

| Command | Action |
| :------ | :----- |
| `/hooks panel` | View configured hooks. |
| `/hooks enable-all` | Enable all hooks. |
| `/hooks disable-all` | Disable all hooks. |
| `/hooks enable <name>` | Enable a single hook by name. |
| `/hooks disable <name>` | Disable a single hook by name. |

## Worked examples

### Log every tool execution

`.gemini/hooks/log-tools.sh` — note logs go to `stderr`, only JSON to `stdout`:

```bash
#!/usr/bin/env bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

echo "Logging tool: $tool_name" >&2
echo "[$(date)] Tool executed: $tool_name" >> .gemini/tool-log.txt

echo "{}"
exit 0
```

### Block secrets before a write (structured denial, exit 0)

`.gemini/hooks/block-secrets.sh`:

```bash
#!/usr/bin/env bash
input=$(cat)
content=$(echo "$input" | jq -r '.tool_input.content // .tool_input.new_string // ""')

if echo "$content" | grep -qE 'api[_-]?key|password|secret'; then
  echo "Blocked potential secret" >&2
  cat <<EOF
{
  "decision": "deny",
  "reason": "Security Policy: Potential secret detected in content.",
  "systemMessage": "🔒 Security scanner blocked operation"
}
EOF
  exit 0
fi

echo '{"decision": "allow"}'
exit 0
```

Wire it up in `.gemini/settings.json`:

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "write_file",
        "hooks": [
          { "name": "security", "type": "command", "command": "node .gemini/hooks/security.js" }
        ]
      }
    ]
  }
}
```

### Inject dynamic context (`BeforeAgent`)

```bash
#!/usr/bin/env bash
context=$(git log -5 --oneline 2>/dev/null || echo "No git history")
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "BeforeAgent",
    "additionalContext": "Recent commits:\n$context"
  }
}
EOF
```

### Filter the toolset by intent (`BeforeToolSelection`)

Return a whitelist (whitelists from multiple hooks are unioned; `mode: "NONE"`
overrides to disable everything):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "BeforeToolSelection",
    "toolConfig": {
      "mode": "ANY",
      "allowedFunctionNames": ["write_todos", "read_file", "list_directory"]
    }
  }
}
```

### Validate the final response and force a retry (`AfterAgent`)

```javascript
#!/usr/bin/env node
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0));
const response = input.prompt_response;

if (!response.includes('Summary:')) {
  console.log(JSON.stringify({
    decision: 'block', // triggers an automatic retry turn
    reason: 'Your response is missing a Summary section. Please add one.',
    systemMessage: '🔄 Requesting missing summary...'
  }));
  process.exit(0);
}

console.log(JSON.stringify({ decision: 'allow' }));
```

Project-level hooks can be shared across repositories by packaging them as a
Gemini CLI extension.

## See also

- [commands.md](./commands.md) — the `/hooks` slash command and others.
- [settings.md](./settings.md) — the `hooks` object and settings precedence.
- [permissions.md](./permissions.md) — the Policy Engine alongside hook blocks.
- [subagents.md](./subagents.md) — subagents and per-agent policies.
- [mcp.md](./mcp.md) — MCP tool naming used in `BeforeTool`/`AfterTool` matchers.
