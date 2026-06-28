# Monitors (Background Tasks)

Plugins can declare **background monitors** — long-running shell processes that Claude Code starts automatically when the plugin is active. Each monitor delivers every stdout line to Claude as a notification, so Claude can react to log entries, status changes, or polled events without being asked to start the watch itself.

Plugin monitors use the same mechanism as the Monitor tool and share its constraints. They run only in **interactive CLI sessions**, run **unsandboxed** at the same trust level as [hooks](./hooks.md), and are skipped on hosts where the Monitor tool is unavailable.

> Requires Claude Code v2.1.105+.

---

## Where monitors live

`monitors/monitors.json` in the plugin root, or inline in `plugin.json` under `monitors`.

```json
[
  {
    "name": "deploy-status",
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

To declare inline, set the `monitors` key in `plugin.json` to the same array. To load from a non-default path, set `monitors` to a relative path string like `"./config/monitors.json"`.

---

## Required fields

| Field | Description |
|---|---|
| `name` | Identifier unique within the plugin. Prevents duplicate processes on plugin reload or skill re-invocation |
| `command` | Shell command run as a persistent background process in the session working directory |
| `description` | Short summary of what is being watched. Shown in the task panel and in notification summaries |

## Optional fields

| Field | Description |
|---|---|
| `when` | Controls when the monitor starts. `"always"` (default) starts at session start and on plugin reload. `"on-skill-invoke:<skill-name>"` starts the first time the named skill in this plugin is dispatched |

---

## Variable substitutions in `command`

Same as MCP/LSP server configs:

- `${CLAUDE_PLUGIN_ROOT}` — plugin install dir (changes on update)
- `${CLAUDE_PLUGIN_DATA}` — plugin's persistent data dir (survives updates)
- `${user_config.<name>}` — values from `userConfig` prompts
- `${ENV_VAR}` — any environment variable

Prefix with `cd "${CLAUDE_PLUGIN_ROOT}" && ` if the script needs to run from the plugin's own directory.

---

## How notifications arrive

Each line of stdout from the monitor process becomes a notification event in the running session. Claude can react to it directly, or you can register a `Notification` hook to handle it programmatically — see [hooks.md](./hooks.md).

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "permission_prompt",
      "hooks": [{ "type": "command", "command": "..." }]
    }]
  }
}
```

---

## Lifecycle

- Monitors start when the plugin is enabled and the session is interactive.
- **Disabling a plugin mid-session does NOT stop monitors that are already running.** They stop only when the session ends.
- `/reload-plugins` reloads the plugin, but the `name` field prevents duplicate processes.

---

## Hooks vs monitors vs channels

|  | Trigger | Output | Use for |
|---|---|---|---|
| **Hook** | Lifecycle event (PreToolUse, PostToolUse, FileChanged, etc.) | Decision JSON, blocks/modifies | Validation, enforcement, reactions to known events |
| **Monitor** | Continuous (long-running shell process) | Stdout lines → notifications | Watching logs, polling status, ambient awareness |
| **Channel** | Push from external service (chat, CI, webhook) | Two-way messages | Driving the session from outside |

---

## Pattern: "ambient awareness"

A common composition: monitor + Notification hook + skill.

1. **Monitor** tails an audit log.
2. **`Notification` hook** parses each line. On a critical event, it adds context to the next user prompt.
3. **Skill** has instructions: "If the auth-failure context is present, escalate the response."

This lets Claude *react* to external state changes without you having to ask.

---

## Async hooks vs monitors

If you only need a one-shot background task (not a continuous watcher), use an `asyncRewake` hook instead — see [hooks.md](./hooks.md#two-power-user-patterns). Hooks fire on lifecycle events; monitors run for the lifetime of the session.

---

## See also

- [plugins.md](./plugins.md) — packaging monitors with a plugin
- [hooks.md](./hooks.md) — `Notification` hook + `asyncRewake`
- [channels.md](./channels.md) — push events from external systems instead
