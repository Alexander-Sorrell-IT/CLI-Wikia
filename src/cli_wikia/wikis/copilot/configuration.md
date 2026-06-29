# Configuration

Copilot CLI is configured through a user `settings.json`, optional repo-level settings, command-line flags, and environment variables. This page covers files and settings keys. For env vars see [environment-variables.md](environment-variables.md).

---

## The `~/.copilot` directory

All config and state lives under `~/.copilot/` by default. Override the location with the `COPILOT_HOME` environment variable.

| Path | Contents |
|---|---|
| `~/.copilot/settings.json` | **Your editable user settings** |
| `~/.copilot/config.json` | Auto-managed state (login, trusted folders, tokens). Don't hand-edit |
| `~/.copilot/mcp-config.json` | User-scope [MCP servers](mcp.md) |
| `~/.copilot/permissions-config.json` | Persisted permission grants |
| `~/.copilot/copilot-instructions.md` | Personal [custom instructions](custom-instructions.md) |
| `~/.copilot/agents/` | Personal [custom agents](custom-agents.md) (`*.agent.md`) |
| `~/.copilot/skills/` | Personal [skills](skills.md) |
| `~/.copilot/memories/` | Cross-session [memory](sessions.md#memory) store |
| `~/.copilot/logs/` | Session logs (override with `--log-dir`) |
| `~/.copilot/session-state/`, `session-store.db` | Saved sessions for resume |

> `~/.copilot/config.json` may contain your OAuth token in plain text when no OS credential store is available. Treat it as a secret.

---

## Settings precedence

```
CLI flags  >  repo settings (.github/copilot/settings.json)  >  user settings (~/.copilot/settings.json)  >  defaults
```

Edit settings three ways:

- `/settings` — interactive UI inside a session.
- `/settings show <key>` / `/settings <key> <value>` — read or set one key.
- Edit `~/.copilot/settings.json` directly.

---

## Settings keys (`settings.json`)

From `copilot help config`. Defaults shown where notable.

### Models & context

| Key | Default | Meaning |
|---|---|---|
| `model` | — | Default model (see [models.md](models.md)) |
| `contextTier` | `default` | Context window tier (`default`, `long_context`) for tiered models |
| `subagents.agents.<name>` | — | Per-subagent `model`, `effortLevel`, `contextTier` (each can be `inherit`) |

### Permissions, URLs & trust

| Key | Meaning |
|---|---|
| `allowedUrls` | URLs/domains allowed without prompting. Supports exact URLs, `domain.com`, and `*.domain.com` |
| `deniedUrls` | Denied URLs/domains. **Denials take precedence over allows** |
| `trustedFolders` | Folders granted read/execute permission |

### Behavior & agent

| Key | Default | Meaning |
|---|---|---|
| `memory` | `true` | Agentic cross-session fact recall (toggle with `/memory`) |
| `includeCoAuthoredBy` | `true` | Add a `Co-authored-by` trailer to commits |
| `continueOnAutoMode` | `false` | On eligible rate-limit errors, auto-switch to `auto` model and retry (not for BYOK or global 429s) |
| `customAgents.defaultLocalOnly` | `false` | Only use local custom agents, ignoring remote org/enterprise ones |
| `keepAlive` | `off` | Prevent sleep: `off`, `on`, `busy`, or a duration |

### Hooks

| Key | Meaning |
|---|---|
| `hooks` | Inline hook definitions keyed by event name (same schema as `.github/hooks/*.json`). In global config they act as user-level hooks. See [hooks.md](hooks.md) |
| `disableAllHooks` | Disable all hooks (repo- and user-level); default `false` |

### Updates & startup

| Key | Default | Meaning |
|---|---|---|
| `autoUpdate` | `true` | Auto-download CLI updates |
| `banner` | `once` | Animated banner frequency: `always`, `never`, `once` |
| `companyAnnouncements` | — | Messages shown in the startup banner (one chosen at random) |
| `showTipsOnStartup` | `true` | Show a random command tip on launch |
| `experimental` | `false` | Enable experimental features |
| `logLevel` | `default` | Set to `all` for debug logging |

### Display & terminal

| Key | Default | Meaning |
|---|---|---|
| `theme` | `auto` | `auto`/`dark`/`light` or a named theme |
| `colorMode` | `github` | `default`, `github`, `dim`, `high-contrast`, `colorblind` |
| `renderMarkdown` | `true` | Render markdown in the terminal |
| `inlineImages` | `true` | Render images inline (Kitty graphics protocol; needs experimental flag + supported terminal) |
| `stream` | `true` | Streaming output |
| `mouse` | `true` | Mouse support in alt-screen mode |
| `scrollbar` | `true` | Show the scrollbar in scrollable views |
| `copyOnSelect` | `true` on macOS, else `false` | Copy selected text on mouse release |
| `compactPaste` | `true` | Collapse pastes >10 lines into `[Paste #N - X lines]` |
| `terminalProgress` | `true` | Emit OSC 9;4 progress indicators |
| `updateTerminalTitle` | `true` | Update the terminal title with current intent |
| `screenReader` | `false` | Screen-reader optimizations |
| `respectGitignore` | `true` | Exclude gitignored files from the `@` picker |
| `statusLine` | — | Custom status line: `{ type: "command", command, padding }`. The command gets session JSON on stdin and prints the status line |
| `tabs` | — | Home-screen tab bar: `enabled`, `sort`, `hide` (identifiers: `copilot`, `agents`, `issues`, `pull-requests`, `gists`) |

### Sound

| Key | Default | Meaning |
|---|---|---|
| `beep` | `false` | Beep when attention is required |
| `beepOnSchedule` | `true` | Beep when a `/every` or `/after` run finishes (needs `beep`) |

### Shell, proxy & IDE

| Key | Default | Meaning |
|---|---|---|
| `bashEnv` | `false` | Enable `BASH_ENV` support for bash shells |
| `powershellFlags` | `["-NoProfile","-NoLogo"]` | Flags passed to pwsh on Windows. Avoid `-Command`/`-File`/`-NoExit`/etc. — they break the runtime |
| `proxyUrl` | — | HTTP(S) proxy (overridden by `HTTP_PROXY`/`HTTPS_PROXY`; restart required) |
| `proxyKerberosServicePrincipal` | — | Kerberos/Negotiate SPN (overridden by `COPILOT_PROXY_KERBEROS_SPN`) |
| `ide.autoConnect` | `true` | Auto-connect to an IDE workspace on startup |
| `ide.openDiffOnEdit` | `true` | Open edit diffs in the connected IDE for approval |

---

## Repo-level settings

Place a `settings.json` at `.github/copilot/settings.json` to share config with a team. It can set things like `enabledPlugins` (declaratively install [plugins](plugins.md)) and repo-level `hooks`.

---

## Related

- [environment-variables.md](environment-variables.md) — every supported env var
- [logging.md](logging.md) and [monitoring.md](monitoring.md) — logs and OpenTelemetry
- [permissions.md](permissions.md) — `allowedUrls`/`deniedUrls` and tool permissions in depth
