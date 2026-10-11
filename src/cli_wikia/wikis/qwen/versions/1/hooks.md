# qwen hooks

> wiki-version: 1 | cli-version: 0.24.7 | verified: 2026-10-10
> source: `eventName:"X"` + `firePreToolUseHook` + `*HookOutput` symbols in the
> installed dist (`chunks/chunk-AN36BHDM.js` et al). Only events with firing
> evidence are listed as real.

Hooks are managed via the `/hooks` dialog (`qwen hooks`); `qwen hooks --help`
prints nothing. Protocol is Claude-compatible: hook-execution requests carry
tool name/input/ids and honor permission decisions incl. deny/block.

## Real events (fire via messageBus)

| Event | Fires when |
|-------|------------|
| `PreToolUse` | Before a tool runs (can deny/block) |
| `PostToolUse` | After a tool succeeds |
| `PostToolUseFailure` | After a tool fails |
| `PostToolBatch` | After a batch of tools completes |
| `UserPromptSubmit` | When a user prompt is submitted |
| `PermissionRequest` | When a tool needs approval |
| `Notification` | On notification display |
| `Stop` | At turn/session stop |

MessageDisplay also appears as an eventName but is internal plumbing, not a
lifecycle hook. SessionStart in the dist is an internal arena emitter event,
NOT a hook — session_start/session_end enforcement stages stay artificial.

## Enforcement mapping

6/16 stages ride real events (user_prompt, pre_tool, post_tool,
tool_failure, stop, permission). The other 10 use canonical artificial names
until qwen ships matching lifecycle events; then
`cli-enforcement sync qwen --write` replaces them.
