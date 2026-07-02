# Hooks

Hooks let you intercept the agent's behavior at defined lifecycle events and run your own logic — for validation, logging, blocking a tool call, or injecting extra context. They are configured as JSON keyed by event name, and Copilot CLI honors **both** its native camelCase event names **and** the Claude-format (PascalCase, nested `{ "matcher", "hooks": [...] }`) shape, so Claude-style hook files work unchanged.

As of 2026-07-02 (CLI 1.0.68) Copilot CLI has a working hook system with the events below. This is verified against `copilot help config`, the bundled `changelog.json`, and the official docs.

---

## Events

The table lists the Claude-format (PascalCase) event name that Copilot accepts alongside its native camelCase key. Either name works in a hook file.

| Event | Native key | When it fires |
|---|---|---|
| `SessionStart` | `sessionStart` | A session starts. `additionalContext` from the hook is injected into the conversation. |
| `UserPromptSubmit` | `userPromptSubmitted` | The user submits a prompt, before the model runs. Its `additionalContext` is folded into the model-facing prompt. |
| `PreToolUse` | `preToolUse` | Before a tool runs. Can return a `permissionDecision` (`allow` / `deny` / `ask`), rewrite the call via `modifiedArgs` / `updatedInput`, or add `additionalContext`. A hook **error denies** the call; `allow` suppresses the approval prompt. |
| `PostToolUse` | `postToolUse` | After a tool succeeds. Can inject `additionalContext` (delivered to the model as a system message). |
| `PostToolUseFailure` | `postToolUseFailure` | After a tool call fails. |
| `PreMcpToolCall` | `preMcpToolCall` | Before an outgoing MCP tool call, to control the request metadata. |
| `PermissionRequest` | `permissionRequest` | When a tool permission decision is being made. |
| `Notification` | `notification` | When a user-attention notification (e.g. a permission prompt) is shown. |
| `PreCompact` | `preCompact` | Before the conversation is compacted. |
| `SubagentStart` | `subagentStart` | A sub-agent begins. Fires for sub-agent tool calls. |
| `SubagentStop` | `subagentStop` | A sub-agent finishes. |
| `Stop` | `agentStop` | The agent stops its turn (including on `task_complete`). |
| `SessionEnd` | `sessionEnd` | A session ends. |

Matchers are **regular expressions** matched against the tool name (e.g. `Edit|Write`, `Bash`, `*`). After recent fixes a `matcher` runs only for tool names that fully match the regex. In Claude-format payloads the tool name is the Claude spelling (`Bash`, not `bash`).

---

## Where hooks are defined

| Scope | Location |
|---|---|
| Repo-level (files) | `.github/hooks/*.json` |
| User-level (files) | `~/.copilot/hooks/` (personal hooks, `*.json`) |
| User-level (inline) | `hooks` key in `~/.copilot/settings.json` |
| Plugin | a plugin's `hooks/` directory or bundled hook files |

The inline `hooks` setting uses the **same schema** as `.github/hooks/*.json`. In global user settings these act as **user-level** hooks; in a repo they act as **repo-level** hooks.

Native (flat) schema, keyed by event:

```json
{
  "preToolUse": [
    { "matcher": "Bash|shell", "type": "command", "command": "./validate.sh", "timeoutSec": 30 }
  ]
}
```

Claude-format (nested groups) — also honored:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "./validate.sh" } ] }
    ]
  }
}
```

A handler is either a local **command** (`"type": "command"`) or an **HTTP** hook (`"type": "http"`, `"url": "https://..."`) that POSTs the JSON payload to a URL. A `timeoutSec` (seconds) is supported; if a hook times out the tool call is allowed to continue.

---

## Command hook I/O contract

A command hook receives the event payload as **JSON on stdin** (event name, tool name, tool input/args, session info) and returns **JSON on stdout**. Recognized response fields include `permissionDecision` (`allow` / `deny` / `ask`), `additionalContext`, `modifiedArgs` / `updatedInput`, `continue`, `reason`, and `systemMessage`. For `PreToolUse`, a non-zero exit / hook error denies the tool call. Plugin hooks additionally receive `PLUGIN_ROOT`, `COPILOT_PLUGIN_ROOT`, and `CLAUDE_PLUGIN_ROOT` env vars.

---

## Prompt / non-interactive mode (`-p`)

In prompt mode (`copilot -p ...`), repo hooks from `.github/hooks/` load only when the folder is already trusted, and are additionally gated behind opt-in env vars for secure-by-default behavior:

- `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS` — enable repo `.github/hooks/` in `-p` mode.
- `GITHUB_COPILOT_PROMPT_MODE_WORKSPACE_MCP` — enable workspace MCP in `-p` mode.

---

## Disabling hooks

| Setting / flag | Effect |
|---|---|
| `disableAllHooks: true` (settings.json) | Disable all hooks, both repo- and user-level |

Use `/env` in a session to see how many hooks loaded and from which source.

---

## Relationship to permissions

Hooks complement [permissions](permissions.md): permissions decide *whether* a tool runs and prompt you; hooks let you attach deterministic logic around events (and a `PreToolUse` hook can itself allow/deny/ask). Use permissions for coarse allow/deny of tools, paths, and URLs; use hooks for custom, event-driven behavior.

---

## See also

- [plugins.md](plugins.md) — plugins can ship hooks
- [permissions.md](permissions.md) — the primary gating mechanism
- [configuration.md](configuration.md) — `hooks` and `disableAllHooks`

## Sources

- GitHub Copilot CLI 1.0.68, `copilot help config` (documents `hooks`, `disableAllHooks`). Accessed 2026-07-02.
- Bundled `@github/copilot` `changelog.json` (v1.0.68; event names incl. `preMcpToolCall`, matcher/`-p` semantics, HTTP hooks, `disableAllHooks`, plugin env vars). Accessed 2026-07-02.
- [GitHub Copilot hooks reference — GitHub Docs](https://docs.github.com/en/copilot/reference/hooks-configuration) — Accessed 2026-07-02.
- [Using hooks with GitHub Copilot CLI — GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks) — Accessed 2026-07-02.
