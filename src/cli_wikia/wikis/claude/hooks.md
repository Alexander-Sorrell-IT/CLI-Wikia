# Hooks

Hooks are scripts (or HTTP calls or MCP tool calls or LLM judges) that fire automatically at specific lifecycle points. **They are the only mechanism that can hard-block Claude.** There are **30 event types** across 8 categories, plus 5 handler types — 3 deterministic (`command`, `http`, `mcp_tool`) and **2 LLM judges (`prompt`, `agent`) that CAN make semantic decisions**, not just pattern matches (see the support matrix under Handler types).

---

## All 30 event types

### Session lifecycle

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `SessionStart` | Session begins or resumes | No | `startup`, `resume`, `clear`, `compact` |
| `Setup` | Only on `claude --init-only`, `claude -p --init`, or `claude -p --maintenance` (NOT normal startup) | No (always continues) | `init`, `maintenance` |
| `SessionEnd` | Session terminates | No | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `InstructionsLoaded` | CLAUDE.md or `.claude/rules/*.md` loads into context | No | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |

### User input

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `UserPromptSubmit` | User submits a prompt, before Claude sees it | **Yes** | none (always fires) |
| `UserPromptExpansion` | Slash command expands into a prompt | **Yes** | command name (`slash_command`, `mcp_prompt`) |

### Tool execution

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `PreToolUse` | After Claude builds tool params, before execute | **Yes** | tool name (`Bash`, `Edit`, `mcp__server__tool`, …) |
| `PermissionRequest` | Permission dialog about to show | **Yes** | tool name |
| `PermissionDenied` | Auto-mode classifier denied the call | No (`retry: true` lets model retry) | tool name |
| `PostToolUse` | Tool succeeded | **Yes** (re-prompts Claude) | tool name |
| `PostToolUseFailure` | Tool failed | No | tool name |
| `PostToolBatch` | Whole parallel tool batch resolved, before next model call | **Yes** | none |

### Agentic loop

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `PreCompact` | Before context compaction | **Yes** | `manual`, `auto` |
| `PostCompact` | After context compaction | No | `manual`, `auto` |
| `Stop` | Claude finishes responding | **Yes** (forces continuation) | none |
| `StopFailure` | Turn ends due to API error | No (observational) | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |

### Subagents

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `SubagentStart` | Subagent spawned | No | agent type (`Bash`, `Explore`, `Plan`, custom) |
| `SubagentStop` | Subagent finished | **Yes** | agent type |

### Tasks

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `TaskCreated` | TaskCreate about to create a task | **Yes** (rolls back) | none |
| `TaskCompleted` | Task being marked complete | **Yes** (prevents) | none |

### Agent teams

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `TeammateIdle` | A teammate is about to go idle | **Yes** (keeps them working) | none |

### Filesystem & worktrees

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `FileChanged` | Watched file is created/modified/deleted | No | literal filenames (`.envrc\|.env`) |
| `CwdChanged` | Working directory changes (e.g. after `cd`) | No | none |
| `WorktreeCreate` | Worktree being created via `--worktree` or `isolation: "worktree"` | **Yes** (any non-zero fails) | none — replaces default git behavior |
| `WorktreeRemove` | Worktree being removed (session/subagent end) | No | none |

### Config & notifications

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `ConfigChange` | A config file changes mid-session | **Yes** (except `policy_settings`) | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `Notification` | Claude Code emits a notification | No | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `MessageDisplay` | While assistant message text is shown on screen (observability-only) | No (original text always displayed) | none — always fires |

### MCP elicitation (when an MCP server asks the user for input)

| Event | Fires when | Can block? | Matchers |
|---|---|---|---|
| `Elicitation` | MCP server requests user input during a tool call | **Yes** (denies) | MCP server name |
| `ElicitationResult` | User responded; before response sent back to MCP server | **Yes** (becomes decline) | MCP server name |

---

## Handler types (the `type` field)

| Type | What it is | Input | Output | Async support |
|---|---|---|---|---|
| `command` | Shell script | JSON via stdin | exit code + stdout JSON | `async`, `asyncRewake` |
| `http` | HTTP endpoint | POST body (JSON) | HTTP response (text or JSON) | implicit (timeout = non-blocking) |
| `mcp_tool` | Call an MCP tool | tool params | tool output | n/a |
| `prompt` | Single-turn LLM judge | `$ARGUMENTS` placeholder | `{"ok": …}` JSON (see below) | `timeout` only |
| `agent` | Spawn a subagent (experimental) | context injection | `{"ok": …}` JSON (see below) | yes |

### Where the LLM judges (`prompt` / `agent`) can run

They are **NOT** available on every event. Both handler types are supported on exactly these **7 events**:

`UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PostToolUse`, `PostToolBatch`, `Stop`, `SubagentStop`.

> Note: `PermissionRequest` does **not** support `prompt`/`agent` — only `command`, `http`, `mcp_tool`. (Earlier docs that said "only PreToolUse/PostToolUse/PermissionRequest" were wrong on both counts.)

These judges genuinely make **semantic** decisions — e.g. a `prompt` hook on `PreToolUse(Bash)` can read the command and reason about whether it violates a content/style rule, not just regex it. That's the use case for reviewing generated text before it's typed/submitted.

### Output schema for `prompt` / `agent` judges

Unlike `command` hooks, the LLM judge returns a **simple binary decision** — NOT the `hookSpecificOutput` wrapper:

```json
{ "ok": true }
```

or, to block:

```json
{
  "ok": false,
  "reason": "explanation — fed back to Claude as feedback/instruction"
}
```

`reason` is required when `"ok": false`. `agent` hooks use the identical format and semantics.

---

## Common input fields (all events)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "hook_event_name": "PreToolUse",
  "agent_id":   "...",   // subagents only
  "agent_type": "..."    // with --agent or in subagents
}
```

Tool events also have:
- `tool_name`, `tool_input`, `tool_use_id`
- `tool_response` & `duration_ms` on `PostToolUse`
- `error` & `is_interrupt` on `PostToolUseFailure`

---

## Full output schema

```json
{
  "continue": true,
  "stopReason": "shown when continue=false",
  "suppressOutput": false,
  "systemMessage": "user-facing warning",
  "additionalContext": "string — added to Claude's context",
  "sessionTitle": "for UserPromptSubmit",
  "decision": "block|null",
  "reason": "shown to Claude when decision=block",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "...",
    "updatedInput":           { /* replaces tool params (include unchanged fields too) */ },
    "updatedMCPToolOutput":   "MCP tools only",
    "retry":                  true,
    "action":                 "accept|decline|cancel",   // Elicitation only
    "content":                { /* form values */ },     // Elicitation only
    "behavior":               "allow|deny",              // PermissionRequest only
    "updatedPermissions":     [ /* see below */ ],
    "message":                "...",
    "interrupt":              false,
    "worktreePath":           "/path"                    // WorktreeCreate only
  }
}
```

`updatedPermissions` entries:

```json
{
  "type": "addRules|replaceRules|removeRules|setMode|addDirectories|removeDirectories",
  "destination": "session|localSettings|projectSettings|userSettings",
  "rules":        [{ "toolName": "Bash", "ruleContent": "npm *" }],
  "behavior":     "allow|deny|ask",
  "mode":         "default|acceptEdits|dontAsk|bypassPermissions|plan",
  "directories":  ["/path"]
}
```

---

## Exit codes (command hooks)

| Code | Meaning | Effect |
|---|---|---|
| `0` | Success | Action proceeds; stdout JSON parsed if present |
| `2` | **Blocking error** | Blocks the action; stderr shown to Claude |
| any other | Non-blocking error | Continues; stderr shown in transcript |

> **Use `2` for policy enforcement, not `1`.** Exit `1` does *not* block.

---

## Configuration & defaults

```json
{
  "type": "command",
  "if": "Bash(rm *)",                  // permission-rule filter (tool events)
  "timeout": 600,                       // seconds
  "statusMessage": "Checking…",
  "once": true,                         // fire only once per session
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check.sh",
  "async": false,
  "asyncRewake": false,                 // background; wake Claude on exit 2
  "shell": "bash"                       // or "powershell"
}
```

Defaults: command 600s, http 30s, prompt 30s, agent 60s. Hook output injected into context is capped at **10,000 characters** — excess saved to file with a preview + path.

### HTTP hook fields

```json
{
  "type": "http",
  "url": "https://...",
  "headers": { "Authorization": "Bearer $TOKEN" },
  "allowedEnvVars": ["TOKEN"]
}
```

### MCP tool hook fields

```json
{
  "type": "mcp_tool",
  "server": "server name",
  "tool": "tool name",
  "input": { "file_path": "${tool_input.file_path}" }
}
```

### Prompt hook fields

```json
{
  "type": "prompt",
  "prompt": "Is this safe? $ARGUMENTS",
  "model": "model alias (optional, defaults to fast model)",
  "timeout": 30
}
```

The judge model must emit `{"ok": true}` to allow or `{"ok": false, "reason": "…"}` to block — see "Output schema for prompt / agent judges" above. Supported on 7 events only (UserPromptSubmit, UserPromptExpansion, PreToolUse, PostToolUse, PostToolBatch, Stop, SubagentStop).

### Agent hook fields (experimental)

```json
{
  "type": "agent",
  "prompt": "Verify the condition: $ARGUMENTS",
  "timeout": 60
}
```

Same `{"ok": …, "reason": "…"}` output and same 7-event support as `prompt`.

---

## Matchers

- `"*"` or omitted — every occurrence
- Alphanumerics + `_` + `|` — exact / pipe-separated list (`Bash`, `Edit|Write`)
- Anything else — JavaScript regex (`mcp__github__.*`, `^Notebook`)
- MCP tools name as `mcp__<server>__<tool>`; whole-server match: `mcp__server__.*`

---

## Environment variables

- `$CLAUDE_PROJECT_DIR` — project root (quote it for paths with spaces)
- `${CLAUDE_PLUGIN_ROOT}` — plugin install dir (changes on update)
- `${CLAUDE_PLUGIN_DATA}` — plugin's persistent data dir (survives updates)
- `CLAUDE_CODE_REMOTE` — `"true"` in remote/web environments
- `CLAUDE_ENV_FILE` — *only* in `SessionStart`, `CwdChanged`, `FileChanged` command hooks: a file you can `export VAR=val` into to persist env vars for subsequent Bash commands

---

## Where hooks live

| Location | Scope | Shareable |
|---|---|---|
| `~/.claude/settings.json` | All your projects | No (machine-local) |
| `.claude/settings.json` | One project, all users | Yes (commit) |
| `.claude/settings.local.json` | One project, you | No (gitignored) |
| Managed policy settings | Whole org | Yes (admin-controlled, cannot be disabled) |
| `<plugin>/hooks/hooks.json` | While plugin enabled | Yes (bundled) |
| Skill / agent frontmatter `hooks:` | While that skill/agent is active | Yes (in component) |

`"disableAllHooks": true` in settings turns everything off temporarily — but managed policy hooks override that.

---

## Two power-user patterns

### `asyncRewake` — long-running background hook that can interrupt Claude

```json
{ "type": "command", "command": "tests.sh", "asyncRewake": true }
```

Runs in background; if it exits `2`, Claude wakes up with the hook's stderr (or stdout if stderr empty) as a system reminder.

### `defer` — pause a tool call for SDK integration

```json
{ "hookSpecificOutput": { "permissionDecision": "defer" } }
```

Claude exits with `stop_reason: "tool_deferred"` and a `deferred_tool_use` payload. Resume later with `claude -p --resume <session-id>`. Single tool calls only, not parallel batches. Tokens cleaned up after `cleanupPeriodDays` (default 30). Requires `--permission-mode` to match the mode when the tool was deferred. Deferred tool unavailable if MCP server not connected on resume.

---

## Minimal example: block `rm -rf`

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-rm.sh",
        "timeout": 5
      }]
    }]
  }
}
```

```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command' < /dev/stdin)
if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "rm -rf is blocked"
    }
  }'
  exit 2
fi
exit 0
```

---

## Troubleshooting

- **JSON validation failed** → shell profile printing text on startup interferes. Output ONLY JSON to stdout; redirect debug to `>&2`.
- **Tool events missing input fields** → different tools have different `tool_input` schemas. Check the docs per tool.
- **Exit code 1 vs 2** → 1 is non-blocking, 2 is blocking. Use 2 for policy.
- **Deferred tool not resuming** → `--permission-mode` must match. Token cleanup is `cleanupPeriodDays`. MCP server must be connected on resume.

---

## See also

- [permissions.md](./permissions.md) — how hooks interact with allow/deny rules
- [permission-modes.md](./permission-modes.md) — auto-mode classifier interaction
- [skills.md](./skills.md) and [agents.md](./agents.md) — `hooks:` frontmatter
- [stacking.md](./stacking.md) — composing hooks with skills and agents
