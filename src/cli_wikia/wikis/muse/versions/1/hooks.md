# muse hooks

> wiki-version: 2 | cli-version: 1.4.4 | verified: 2026-10-10
> source: MSP schema export (`muse schema`, exact for this binary) + live
> fire probes with `--provider echo` under an isolated HOME. Every route
> below was proven by marker-file side effects, not inferred from --help.

Muse has a real, Claude-compatible hook system (v1: this page wrongly said
"none" from a `--help` grep alone — corrected after schema + fire probing).

## Events (20, from MSP schema HookEventName)

Wire spelling is camelCase; config + plugin manifests use Claude-case.
Table uses Claude-case so `hook_events()` parses them.

| Event | Fires when |
|-------|------------|
| `SessionStart` | Session begins |
| `SessionEnd` | Session ends |
| `SessionFork` | Session forks |
| `UserPromptSubmit` | User prompt submitted (fire-proven) |
| `PreToolUse` | Before a tool runs |
| `ToolUseStart` | Tool execution starts |
| `PostToolUse` | After a tool succeeds |
| `PostToolUseFailure` | After a tool fails |
| `PostToolBatch` | After a tool batch completes |
| `PermissionRequest` | Tool needs approval |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction |
| `PreLLMCall` | Before an LLM call |
| `PostLLMCall` | After an LLM call |
| `SubagentStart` | Subagent starts |
| `SubagentStop` | Subagent stops |
| `Stop` | Turn/session stop |
| `StopFailure` | Stop hook failure path |
| `Notification` | Notification display |
| `Interrupt` | Interrupt signal |

Handler origins (`HookHandlerKind`): `managed`, `user`, `project`, `plugin`.
Run outcomes (`HookRunStatus`): completed, blocked, failed, timedOut,
cancelled. `hook/list` MSP method is per-session (scope follows workspace +
plugin state).

## Route 1 — user settings (fire-proven)

`~/.config/muse/settings.json` accepts a top-level `hooks` member
(an unknown member is named at startup; `hooks` is not). Groups are
Claude-shaped; event names MUST be Claude-case (`userPromptSubmit` is
rejected with `UnsupportedEvent`):

```json
{"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "touch /tmp/fired"}]}]}}
```

Startup reports `muse: Hooks: N runnable · M warnings`. A group with a
bare `command` field is skipped with `D66: unknown matcher-group field`.

## Route 2 — project plugin (fire-proven, nesting proven)

A workspace dir containing `.muse-plugin/plugin.json`:

```json
{"schemaVersion": 1, "name": "x", "compat": {"source": "native", "manifestDir": ".muse-plugin"},
 "capabilities": {"hooks": [{"id": "probe", "event": "UserPromptSubmit",
  "command": ["sh", "hooks/mark.sh"], "timeoutMs": 5000}] ...}}
```

Hook `command` is structured argv; relative paths resolve from the PLUGIN
ROOT (not `.muse-plugin/`). Flow: trust workspace (`trust.json`) →
`muse plugins install <dir> --scope project` → `muse plugins approve <id>`
("hooks require review before activation") → hooks fire. Untrusted
workspaces block install. Nesting under `.muse/plugin/` proven working.

Observed quirk (needs follow-up): a project install from workspace A fired
while cwd was workspace B — project scoping may be install-time, not
run-time. Treat project hooks as host-active once approved until proven
otherwise.

## Enforcement mapping

13/16 stages ride real events (all except the three below). Missing from
the schema, covered by canonical artificial names until muse ships them:
`InstructionsLoaded`, `ConfigChange`, `TaskCompleted`. Then
`cli-enforcement sync muse --write` replaces them.
