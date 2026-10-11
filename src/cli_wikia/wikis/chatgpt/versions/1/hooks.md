# Codex Lifecycle Hooks

Codex CLI has a real, first-class **lifecycle hook system** — deterministic shell commands Codex runs at defined points in a session. This is the peer to Claude Code's hooks: you register command handlers that fire on events, inspect a JSON payload on stdin, and can block, rewrite, or annotate what the agent does next. From OpenAI's [Hooks](https://developers.openai.com/codex/hooks) reference.

> **Not locally verified** — sourced from official docs; Codex isn't installed here. Confirm event names and payload fields with `/hooks` and `codex --help` after installing.

Hooks are **enabled by default** (as of 2026-07-02). To turn them off, set the feature flag in `config.toml`:

```toml
[features]
hooks = false
```

---

## Events

The hook events, exactly as named in the docs:

| Event | Scope | Fires when |
|---|---|---|
| `SessionStart` | thread | A new session/thread starts |
| `SubagentStart` | subagent | A subagent thread starts |
| `UserPromptSubmit` | turn | The user submits a prompt |
| `PreToolUse` | turn | Before a tool (e.g. shell/`Bash`) runs — can deny or rewrite input |
| `PermissionRequest` | turn | An approval/permission is requested |
| `PostToolUse` | turn | After a tool finishes |
| `PreCompact` | turn | Before history is compacted |
| `PostCompact` | turn | After history is compacted |
| `SubagentStop` | turn | A subagent finishes |
| `Stop` | turn | The turn/agent stops |

---

## Where hooks live

Codex discovers hooks in two formats, sitting next to the active config layers:

1. **`hooks.json`** files — e.g. `~/.codex/hooks.json` and project-level `.codex/hooks.json`
2. **Inline `[hooks]` tables** in `config.toml` — e.g. `~/.codex/config.toml` and project-level `.codex/config.toml`

If a single layer contains both `hooks.json` and an inline `[hooks]` table, Codex merges them and warns at startup.

Each event holds one or more **matcher groups** (a regex matched against, e.g., the tool name), and each matcher group holds one or more **handlers** (the commands to run).

### `hooks.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.py",
            "statusMessage": "Checking command",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Inline `[hooks]` in `config.toml`

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "script.py"'
timeout = 30
```

---

## Payload & output

Command handlers receive a JSON object on **stdin** with shared fields including `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`, and (for turn-scoped events) `turn_id`.

A handler can influence Codex by writing JSON to stdout:

```json
{
  "continue": true,
  "stopReason": "optional",
  "systemMessage": "optional",
  "suppressOutput": false
}
```

Event-specific fields exist — for example, `PreToolUse` can return `permissionDecision: "deny"` to block a tool call, or `updatedInput` to rewrite its arguments before it runs.

---

## Trust & the `/hooks` command

Before a non-managed command hook runs, Codex requires you to **review and trust** the exact hook definition; trust is recorded against the hook's current hash, so editing a hook re-prompts. Use `/hooks` in the TUI to inspect hook sources, review new or changed hooks, trust them, or disable individual non-managed hooks. If hooks need review at startup, Codex prints a warning.

## Managed hooks (enterprise)

Admins can enforce hooks via managed configuration (`requirements.toml`). Managed hooks are trusted by policy and can't be disabled from the user hook browser. Setting `allow_managed_hooks_only = true` skips all non-managed hook sources.

```toml
allow_managed_hooks_only = true

[features]
hooks = true

[hooks]
managed_dir = "/enterprise/hooks"

[[hooks.PreToolUse]]
matcher = "^Bash$"
[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/policy.py"
```

---

## See also

- [codex-config.md](./codex-config.md) — `[features]` flags and where `[hooks]` sits in config layering
- [codex-slash-commands.md](./codex-slash-commands.md) — `/hooks`
- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — how `PermissionRequest` relates to approval policy

## Sources

- OpenAI Developers — Hooks: <https://developers.openai.com/codex/hooks> (Accessed 2026-07-02)
- OpenAI Developers — Configuration Reference: <https://developers.openai.com/codex/config-reference> (Accessed 2026-07-02)
