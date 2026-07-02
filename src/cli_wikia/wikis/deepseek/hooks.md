# Hooks

Hooks are scripts that fire automatically at lifecycle points in a session. **They
are the only mechanism that can hard-block the agent** — they run in the Clawspring
harness, outside the model, so the model cannot ignore them. The hooks subsystem is
adapted directly from Claude Code's: the shipped `hooks.json` even labels itself
"Based on Claude Code hooks architecture — adapted for DeepSeek Clawspring".

There are **28 event types** (re-verified 2026-07-02 against the installed tool:
`deepseek-code hooks` and `~/.clawspring/hooks.json` list exactly these 28 events,
as top-level keys of `hooks.json` — *not* nested under a `"hooks"` key as in
Claude Code's `settings.json`). The shipped install registers a handler for every one.

```bash
deepseek-code hooks    # list configured hooks with a handler count per event
```

---

## The 28 events

### Session lifecycle

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `SessionStart` | A session begins or resumes | No |
| `SessionEnd` | A session terminates | No |
| `InstructionsLoaded` | CLAWSPRING.md / rules load into context | No |

### User input

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `UserPromptSubmit` | The user submits a prompt, before the model sees it | **Yes** |
| `UserPromptExpansion` | A slash command expands into a prompt | **Yes** |

### Tool execution

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `PreToolUse` | After tool params are built, before execution | **Yes** |
| `PermissionRequest` | A permission check is about to run | **Yes** |
| `PermissionDenied` | A permission was denied | No |
| `PostToolUse` | A tool succeeded | **Yes** |
| `PostToolUseFailure` | A tool failed | No |
| `PostToolBatch` | A whole parallel tool batch resolved | **Yes** |

### Agentic loop

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `PreCompact` | Before context compaction | **Yes** |
| `PostCompact` | After context compaction | No |
| `Stop` | The agent is about to finish responding | **Yes** (forces continuation) |
| `StopFailure` | A turn ended due to an error | No |

### Subagents & tasks

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `SubagentStart` | A subagent is spawned | No |
| `SubagentStop` | A subagent finishes | **Yes** (keeps it working) |
| `TaskCreated` | A task is created | **Yes** |
| `TaskCompleted` | A task is marked complete | **Yes** |
| `TeammateIdle` | A teammate is about to go idle | **Yes** |

### Filesystem & worktrees

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `FileChanged` | A watched file is created/modified/deleted | No |
| `CwdChanged` | The working directory changes | No |
| `WorktreeCreate` | A git worktree is being created | **Yes** |
| `WorktreeRemove` | A git worktree is being removed | No |

### Config, notifications & elicitation

| Event | Fires when | Can block? |
|-------|-----------|------------|
| `ConfigChange` | A config file changes mid-session | **Yes** |
| `Notification` | The tool emits a notification | No |
| `Elicitation` | A tool requests user input | **Yes** |
| `ElicitationResult` | The user responded, before the result is sent back | **Yes** |

---

## The `hooks.json` schema

Hooks live in `~/.clawspring/hooks.json` (global) and `.clawspring/hooks.json`
(project); the two are merged at runtime. Each event maps to an array of **rule
objects**, each with a `matcher` and a list of `hooks`:

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "$HOME/.clawspring/hooks/pre-bash.sh",
          "timeout": 10,
          "async": false,
          "statusMessage": "Checking command…"
        }
      ]
    }
  ]
}
```

### Handler fields

| Field | Description |
|-------|-------------|
| `type` | `"command"` — the handler kind. The shipped install uses command (shell) handlers throughout. |
| `command` | Path to the script. Supports `$HOME` and `$CLAWSPRING_HOME` expansion. |
| `timeout` | Seconds before the hook is killed |
| `async` | `true` = fire-and-forget; doesn't block the turn (used by the general `PostToolUse` logger) |
| `statusMessage` | Text shown to the user while the hook runs |

A hook entry may also be a **bare string** path — shorthand for
`{"type": "command", "command": "<path>"}`. The shipped project hooks use this form.

> Clawspring's documentation describes a Claude-Code-style "28 events × 5 handler
> types" model (command / http / mcp_tool / prompt / agent). In practice every
> handler in this install is `type: "command"`. Non-command handler types should be
> treated as *aspirational / verify in the tool* unless you confirm support.

### Matchers

| Pattern | Matches |
|---------|---------|
| `"*"` | Everything (or omit the matcher) |
| `"Bash"` | The Bash tool, any arguments |
| `"Bash(git commit *)"` | Bash with a `git commit` command |
| `"Write\|Edit"` | Write OR Edit (pipe-separated) |
| `".envrc\|.env\|CLAUDE.md\|*.rules.md"` | Filename patterns (for `FileChanged`) |

---

## Exit codes (command hooks)

| Code | Meaning | Effect |
|------|---------|--------|
| `0` | Pass | The action proceeds |
| `1` | Warn | Logged, but the action continues |
| `2` | **Block** | The action is denied; stderr is surfaced |
| other | Error | Logged as a hook bug; non-blocking |

> Use `2` for enforcement — exit `1` does **not** block.

A command hook reads event JSON on stdin and may print JSON on stdout to influence the
turn (e.g. a `Stop` hook printing `{"continue": false, "stopReason": "…"}` to force
the agent to keep working).

---

## The installed hook scripts

The global install ships ~31 scripts in `~/.clawspring/hooks/`, one per event (plus a
few tool-specific ones). The notable enforcing ones:

| Script | Event | What it does |
|--------|-------|--------------|
| `startup.sh` | SessionStart | Initialize the session, detect the project |
| `user-prompt-submit.sh` | UserPromptSubmit | Log prompts, block dangerous intents |
| `pre-bash.sh` | PreToolUse(Bash) | **Block** `sudo`, `rm -rf /`, fork bombs, `curl\|sh` |
| `pre-write.sh` | PreToolUse(Write\|Edit) | **Block** writes to secret files / outside the workspace |
| `pre-web.sh` | PreToolUse(WebFetch\|WebSearch) | **Block** internal IPs / localhost |
| `post-tool.sh` | PostToolUse(*) | Async logging of tool + duration |
| `post-commit.sh` | PostToolUse(git commit) | Suggest a code review after commits |
| `stop-check.sh` | Stop | **Gate** completion on an advisor check |
| `cwd-changed.sh` | CwdChanged | Bootstrap a new `.clawspring/` if missing |
| `subagent-stop.sh` | SubagentStop | Can block to keep a subagent working |

Project-level hooks live in `.clawspring/hooks/` and run *in addition to* the global
ones. Always check **both** directories when debugging hook behavior.

---

## Configuring a hook — step by step

**1. Write the script** (any executable — bash, python, a binary):

```bash
#!/usr/bin/env bash
# ~/.clawspring/hooks/check-env.sh
set -euo pipefail
if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "ERROR: DATABASE_URL not set — blocking" >&2
  exit 2          # BLOCK
fi
exit 0            # PASS
```

```bash
chmod +x ~/.clawspring/hooks/check-env.sh
```

**2. Register it** under the event in `hooks.json`:

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash(python *)",
      "hooks": [
        { "type": "command",
          "command": "$HOME/.clawspring/hooks/check-env.sh",
          "timeout": 10,
          "statusMessage": "Checking environment…" }
      ]
    }
  ]
}
```

**3. Pick a scope** — global (`~/.clawspring/hooks.json`) for all projects, or
project (`.clawspring/hooks.json`) for one. Both merge at runtime.

---

## Turning hooks off

Set `DEEPSEEK_CODE_DISABLE_HOOKS` (env var) or run with `--bare` to skip hook
discovery entirely for a clean session. This is the CI/deterministic path.

---

## Related

- [permissions.md](permissions.md) — how `PreToolUse` hooks reinforce permission rules
- [agents.md](agents.md#the-advisor) — the advisor + `Stop` hook quality gate
- [architecture.md](architecture.md) — the full hook-event flow through a session


## Sources

No public documentation exists for DeepSeek Code or the Clawspring Agent Runtime as of 2026-07-02. Web searches for "Clawspring agent runtime" and "clawspring deepseek-code" return only unrelated third-party DeepSeek CLIs and DeepSeek's official API docs, none of which describe this tool. Everything here was verified against the installed tool on 2026-07-02:

- `deepseek-code --version` -> `DeepSeek Code v2.0.0` / `clawspring v3.05.5`
- `deepseek-code hooks` lists 28 events, one handler each; `~/.clawspring/hooks.json` inspected — the 28 event names are **top-level keys** (not nested under a `"hooks"` wrapper); hook scripts live in `~/.clawspring/hooks/`.
