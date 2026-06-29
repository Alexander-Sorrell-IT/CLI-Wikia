# Configuration

DeepSeek Code is configured across **three layers**: the CLI's own user config, the
Clawspring runtime settings, and the Clawspring harness config. Plus environment
variables and CLI flags on top. This page documents each one as it exists on disk.

> The split is a consequence of the hybrid design: `~/.deepseek-code/` holds the
> CLI-facing knobs, while `~/.clawspring/` holds the full Claude-Code-style runtime
> (permissions, hooks, sandbox, agents). Some keys appear in more than one place; the
> precedence is **CLI flags > project Clawspring settings > user Clawspring settings
> > CLI config**. *Verify the exact merge order in your install.*

---

## 1. CLI user config — `~/.deepseek-code/config.json`

Shown with `deepseek-code config`. This is the file most users edit.

```json
{
  "model": "deepseek-v4-flash",
  "effortLevel": "high",
  "thinking": "on",
  "permissionMode": "acceptEdits",
  "autoMemoryEnabled": true,
  "sessionPersistence": true
}
```

| Field | Example | Description |
|-------|---------|-------------|
| `model` | `"deepseek-v4-flash"` | Default model (`pro` / `flash` / full ID) |
| `effortLevel` | `"high"` | Default reasoning effort (`low` / `medium` / `high` / `max`) |
| `thinking` | `"on"` | Reasoning mode (`on` / `off` / `max`) |
| `permissionMode` | `"acceptEdits"` | Default permission mode |
| `autoMemoryEnabled` | `true` | Persist memory automatically |
| `sessionPersistence` | `true` | Save sessions to disk so they can be resumed |

The live file also carries read-only metadata fields (`_installed`, `_version`,
`_backend`, `_framework`) that the tool writes for its own bookkeeping.

---

## 2. Clawspring runtime settings — `~/.clawspring/settings.json`

This is the full runtime configuration, structured exactly like a Claude Code
`settings.json`. Its documented precedence (from the file's own comment) is:

```
Managed > CLI flags > .clawspring/settings.local.json > .clawspring/settings.json > ~/.clawspring/settings.json
```

### Top-level keys

| Key | Example | Description |
|-----|---------|-------------|
| `model` | `"deepseek-v4-pro"` | Runtime default model |
| `effortLevel` | `"high"` | Runtime default effort |
| `alwaysThinkingEnabled` | `true` | Keep extended thinking on for every turn |
| `autoMemoryEnabled` | `true` | Enable auto-memory |
| `permissions` | object | Allow/ask/deny rules + `defaultMode` (see [permissions.md](permissions.md)) |
| `hooks` | object | Points to `hooks.json` (see [hooks.md](hooks.md)) |
| `sandbox` | object | Filesystem deny lists + network allowlist (see below) |
| `agents` | object | `defaultModel`, `defaultMaxTurns` (25), `defaultPermissionMode` |
| `skills` | object | `descriptionBudget` (8000), `autoCompactionEnabled` |
| `memory` | object | Auto/project memory directories |
| `editor` | object | `editorMode`, `tui`, `viewMode` |
| `statusLine` | object | `enabled`, `updateInterval` |
| `autoUpdatesChannel` | `"stable"` | Update channel |
| `env` | object | Extra environment variables exported into sessions |
| `attribution` | object | Commit / PR attribution strings |
| `cleanupPeriodDays` | `30` | Retention for transient state |
| `enabledPlugins` | object | Active plugins (see [plugins.md](plugins.md)) |

### Sandbox block

The sandbox is **disabled by default** (`enabled: false`) but fully specified:

```json
"sandbox": {
  "enabled": false,
  "failIfUnavailable": false,
  "autoAllowBashIfSandboxed": true,
  "filesystem": {
    "denyRead":  ["~/.ssh/**", "~/.aws/credentials", "**/.env", "**/secrets/**",
                  "**/credentials*", "**/*.pem", "**/*.key"],
    "denyWrite": ["/etc/**", "/sys/**", "/proc/**", "~/.ssh/**"]
  },
  "network": {
    "allowedDomains": ["github.com", "api.anthropic.com", "api.deepseek.com",
                       "*.npmjs.org", "pypi.org", "crates.io", "registry.yarnpkg.com"]
  }
}
```

---

## 3. Clawspring harness config — `~/.clawspring/config.json`

A lower-level config consumed by the Clawspring Python harness. These are the
runtime ceilings for the agent loop.

```json
{
  "model": "deepseek-v4-pro",
  "max_tokens": 40000,
  "permission_mode": "accept-all",
  "verbose": false,
  "thinking": true,
  "thinking_budget": 10000,
  "custom_base_url": "",
  "max_tool_output": 32000,
  "max_agent_depth": 3,
  "max_concurrent_agents": 3,
  "session_daily_limit": 10,
  "session_history_limit": 200,
  "anthropic_api_key": ""
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `max_tokens` | `40000` | Max output tokens per turn |
| `thinking_budget` | `10000` | Token budget for extended thinking |
| `max_tool_output` | `32000` | Max characters of tool output fed back to the model |
| `max_agent_depth` | `3` | How deep subagent nesting can go |
| `max_concurrent_agents` | `3` | Parallel subagents allowed |
| `session_daily_limit` | `10` | Sessions per day |
| `session_history_limit` | `200` | Lines of memory/history loaded into context |
| `custom_base_url` | `""` | Override the API base URL |
| `permission_mode` | `"accept-all"` | Harness-level permission default |

> Note the naming/value drift between layers: this file uses snake_case and
> `permission_mode: "accept-all"`, while `settings.json` and the CLI config use
> camelCase and `acceptEdits`. They are separate stores read by different parts of the
> hybrid. *Treat `~/.deepseek-code/config.json` and the `/config` view as the
> authoritative user-facing config; the others are runtime internals.*

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `DEEPSEEK_API_KEY` | API key (alternative to `auth login`) |
| `DEEPSEEK_CODE_MODEL` | Default model |
| `DEEPSEEK_CODE_EFFORT` | Default effort level |
| `DEEPSEEK_CODE_DISABLE_HOOKS` | Disable all hooks |
| `DEEPSEEK_CODE_BARE` | Equivalent to `--bare` |
| `DEEPSEEK_CODE_LOG_LEVEL` | `debug`, `info`, `warn`, `error` |

`~/.clawspring/settings.json` can also export additional vars into every session via
its `env` block (the shipped config sets `DEEPSEEK_GLOBAL=1`).

---

## Authentication

```bash
deepseek-code auth login     # prompt for and store the API key
deepseek-code auth status    # report whether a valid key is stored
deepseek-code auth logout    # remove the stored key
```

The key is stored at `~/.config/deepseek/key`. The `DEEPSEEK_API_KEY` environment
variable takes precedence if set.

---

## Related

- [models.md](models.md) — model / effort / thinking defaults
- [permissions.md](permissions.md) — the `permissions` block in detail
- [hooks.md](hooks.md) — the `hooks` block and `hooks.json`
- [architecture.md](architecture.md) — how the layers load and merge
