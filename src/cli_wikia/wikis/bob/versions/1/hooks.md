# Hooks

Bob is built on Claude Code and **inherits its full hook system unchanged**.
All 30 Claude Code hook events are available. See the
[claude/hooks.md](../claude/hooks.md) for the complete event reference, handler
types, I/O schema, and configuration format.

This page documents the Bob-specific wiring and the cli-enforcement integration.

---

## Hook configuration location

| Scope | Location |
|---|---|
| Project | `.agents/settings.json` (under `"hooks"` key) |
| User | `~/.config/bob/settings.json` (under `"hooks"` key) |

The format is identical to Claude Code's `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": ".agents/mcp/enforce_check.py" }
        ]
      }
    ]
  }
}
```

---

## All 30 inherited hook events

Bob inherits all events from Claude Code verbatim. The full list:

**Session:** `SessionStart`, `Setup`, `SessionEnd`, `InstructionsLoaded`

**User input:** `UserPromptSubmit`, `UserPromptExpansion`

**Tool execution:** `PreToolUse`, `PermissionRequest`, `PermissionDenied`,
`PostToolUse`, `PostToolUseFailure`, `PostToolBatch`

**Agentic loop:** `PreCompact`, `PostCompact`, `Stop`, `StopFailure`

**Subagents:** `SubagentStart`, `SubagentStop`

**Tasks:** `TaskCreated`, `TaskCompleted`

**Agent teams:** `TeammateIdle`

**Filesystem:** `FileChanged`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`

**Config & notifications:** `ConfigChange`, `Notification`, `MessageDisplay`

**MCP elicitation:** `Elicitation`, `ElicitationResult`

See [claude/hooks.md](../claude/hooks.md) for what each event fires on, whether
it can block, its matchers, and its input/output schema.

---

## cli-enforcement on Bob

The cli-enforcement engine deploys to Bob exactly as it does to Claude Code.
Bob's config root is `.agents/` — the deployer uses this automatically:

```bash
cli-enforcement deploy bob --write
```

This wires all 16 enforcement stages to their matching Claude hook events,
deploys 32+ engine scripts into `.agents/mcp/`, and generates KB gates from
the Bob wikia topics.

When the enforcement engine is deployed, Bob gains:
- **Pre-edit blocking** (10 checks before every Edit/Write)
- **Points system** (start at 500; earn/lose based on behaviour)
- **Anti-hallucination** (must read a file before editing it)
- **KB gates** (must read understanding docs before editing components)
- **Cascade investigation** (subagent deployed on hard blocks)

See [enforcement.md](./enforcement.md) for details.

---

## Bob-specific hook: AGENTS.md protection

When enforcement is deployed, `enforce_check.py` adds `AGENTS.md` to the
read-only document list (alongside `CLAUDE.md`). Edits to `AGENTS.md` are
blocked during a workflow unless the user says `unlock enforcement`.

---

## Sources

Bob application documentation, Claude Code hooks reference, and installed cli-enforcement. Accessed 2026-08.
