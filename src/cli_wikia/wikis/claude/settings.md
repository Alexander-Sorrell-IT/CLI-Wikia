# Settings

`settings.json` is where almost everything is configured. Hierarchy:

```
Managed (org)  >  CLI flags  >  .claude/settings.local.json
                  >  .claude/settings.json  >  ~/.claude/settings.json
```

**Scalars** in higher-precedence files override lower. **Arrays merge** across scopes (rules, hooks, allowlists from project + user + local all combine).

> If a tool is denied at any level, no other level can allow it.

---

## Settings file locations

| Scope | Path |
|---|---|
| Managed (macOS) | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Managed (Linux/WSL) | `/etc/claude-code/managed-settings.json` |
| Managed (Windows) | `C:\Program Files\ClaudeCode\managed-settings.json` (also HKLM registry) |
| User | `~/.claude/settings.json` |
| Project | `.claude/settings.json` (commit to git) |
| Local | `.claude/settings.local.json` (gitignored) |

Inspect: `/status` shows which sources are active. `/permissions` shows which file each rule came from.

---

## Complete key reference

The settings model has **80+ keys**. Full list:

### Core / model

| Key | Type | What it does |
|---|---|---|
| `$schema` | string | JSON schema URL for validation |
| `model` | string | Default model (e.g. `claude-opus-4-7`) |
| `effortLevel` | string | Persist effort: `low`, `medium`, `high`, `xhigh`, `max` |
| `availableModels` | array | Restrict which models can be selected |
| `modelOverrides` | object | Map Anthropic IDs to provider-specific IDs (Bedrock/Vertex/Foundry) |
| `alwaysThinkingEnabled` | boolean | Enable extended thinking by default |
| `showThinkingSummaries` | boolean | Show extended thinking summaries |
| `fastModePerSessionOptIn` | boolean | Require per-session Fast mode opt-in |
| `agent` | string | Run main thread as named subagent |
| `outputStyle` | string | Output style for system prompt |

### Permissions

| Key | What it does |
|---|---|
| `permissions.allow` | Allow rules array |
| `permissions.ask` | Confirm rules array |
| `permissions.deny` | Deny rules array |
| `permissions.additionalDirectories` | Extra working dirs |
| `permissions.defaultMode` | Default permission mode |
| `permissions.disableBypassPermissionsMode` | `"disable"` to prevent bypass mode |
| `permissions.disableAutoMode` | `"disable"` to prevent auto mode |
| `permissions.skipDangerousModePermissionPrompt` | Skip bypass-mode confirmation |

### Auto mode

| Key | What it does |
|---|---|
| `autoMode` | Customize auto-mode classifier rules — see [`auto-mode-config`](https://code.claude.com/docs/en/auto-mode-config) |
| `useAutoModeDuringPlan` | Use auto mode during plan mode |
| `disableAutoMode` | (Top-level) `"disable"` blocks auto |

### Sandbox

| Key | What it does |
|---|---|
| `sandbox.enabled` | Enable bash sandboxing |
| `sandbox.failIfUnavailable` | Hard-fail if sandbox can't start |
| `sandbox.autoAllowBashIfSandboxed` | Auto-approve sandboxed bash (default `true`) |
| `sandbox.excludedCommands` | Commands to run outside sandbox |
| `sandbox.allowUnsandboxedCommands` | Allow `dangerouslyDisableSandbox` escape hatch (default `true`) |
| `sandbox.filesystem.allowWrite` | Paths sandbox can write |
| `sandbox.filesystem.denyWrite` | Paths sandbox cannot write |
| `sandbox.filesystem.allowRead` | Paths to re-allow within `denyRead` |
| `sandbox.filesystem.denyRead` | Paths sandbox cannot read |
| `sandbox.filesystem.allowManagedReadPathsOnly` | (Managed) Only managed `allowRead` respected |
| `sandbox.network.allowedDomains` | Allowed outbound domains |
| `sandbox.network.deniedDomains` | Blocked outbound domains |
| `sandbox.network.allowAllUnixSockets` | (macOS) Allow all Unix sockets |
| `sandbox.network.allowUnixSockets` | (macOS) Specific Unix socket paths |
| `sandbox.network.allowLocalBinding` | (macOS) Allow localhost binding |
| `sandbox.network.allowMachLookup` | (macOS) XPC/Mach service names |
| `sandbox.network.allowManagedDomainsOnly` | (Managed) Only managed allowed domains respected |
| `sandbox.network.httpProxyPort` | HTTP proxy port |
| `sandbox.network.socksProxyPort` | SOCKS5 proxy port |
| `sandbox.enableWeakerNestedSandbox` | Weaker sandbox for Docker (reduces security) |
| `sandbox.enableWeakerNetworkIsolation` | (macOS) Allow TLS trust service access (reduces security) |

### Hooks

| Key | What it does |
|---|---|
| `hooks` | Hook configuration object (see [hooks.md](./hooks.md)) |
| `disableAllHooks` | Disable all hooks and status line |
| `allowedHttpHookUrls` | Allowlist of HTTP hook URL patterns |
| `httpHookAllowedEnvVars` | Allowlist of env vars HTTP hooks can use |
| `allowManagedHooksOnly` | (Managed) Only managed/SDK/force-enabled hooks load |

### MCP

| Key | What it does |
|---|---|
| `enabledMcpjsonServers` | Pre-approve specific `.mcp.json` servers |
| `disabledMcpjsonServers` | Reject specific `.mcp.json` servers |
| `enableAllProjectMcpServers` | Auto-approve all project `.mcp.json` servers |
| `allowAllProjectMcpServers` | Same as above (alias) |
| `allowedMcpServers` | (Managed) Allowlist of MCP servers |
| `deniedMcpServers` | (Managed) Denylist of MCP servers |
| `allowManagedMcpServersOnly` | (Managed) Only managed allowed servers respected |

### Plugins & marketplaces

| Key | What it does |
|---|---|
| `enabledPlugins` | `{"plugin@marketplace": true/false}` |
| `extraKnownMarketplaces` | `{"name": {"source": "..."}}` — define additional marketplaces |
| `strictKnownMarketplaces` | (Managed) Allowlist of marketplaces |
| `blockedMarketplaces` | (Managed) Blocklist of marketplaces (checked before download) |
| `pluginTrustMessage` | (Managed) Custom plugin trust warning message |

### Channels (research preview)

| Key | What it does |
|---|---|
| `channelsEnabled` | (Team/Enterprise) Master switch for channels |
| `allowedChannelPlugins` | (Managed) Allowlist of channel plugins |

### Auto-memory

| Key | What it does |
|---|---|
| `autoMemoryEnabled` | Toggle auto-memory |
| `autoMemoryDirectory` | Custom directory for auto-memory storage |

### Auth & login

| Key | What it does |
|---|---|
| `apiKeyHelper` | Custom script generating auth value |
| `forceLoginMethod` | `"claudeai"` or `"console"` |
| `forceLoginOrgUUID` | Require login to specific org(s) (string or array) |

### AWS / cloud providers

| Key | What it does |
|---|---|
| `awsAuthRefresh` | Custom script for AWS credential refresh |
| `awsCredentialExport` | Custom script outputting AWS credentials JSON |
| `otelHeadersHelper` | Script for dynamic OpenTelemetry headers |

### Update channel & versions

| Key | What it does |
|---|---|
| `autoUpdatesChannel` | `"stable"` or `"latest"` |
| `minimumVersion` | Minimum Claude Code version floor |
| `forceRemoteSettingsRefresh` | (Managed) Block CLI startup until remote settings fetched |
| `wslInheritsWindowsSettings` | (Managed; Windows) WSL reads Windows policy chain |

### Editor / UI

| Key | What it does |
|---|---|
| `editorMode` | `"normal"` or `"vim"` |
| `tui` | `"fullscreen"` or `"default"` |
| `viewMode` | `"default"`, `"verbose"`, `"focus"` |
| `autoScrollEnabled` | Follow new output in fullscreen |
| `prefersReducedMotion` | Reduce/disable UI animations |
| `spinnerTipsEnabled` | Show tips in spinner |
| `spinnerTipsOverride` | Custom spinner tips object |
| `spinnerVerbs` | Custom action verbs for spinner |
| `terminalProgressBarEnabled` | Show terminal progress bar |
| `showTurnDuration` | Show turn duration messages |
| `language` | Preferred response language (e.g. `"japanese"`) |

### Status line

| Key | What it does |
|---|---|
| `statusLine.command` | Shell script for the status line |
| `statusLine.updateInterval` | Refresh interval (ms) |

### Voice (legacy + new)

| Key | What it does |
|---|---|
| `voice.enabled` | Voice dictation on |
| `voice.mode` | Voice mode |
| `voice.autoSubmit` | Auto-submit recognized text |
| `voiceEnabled` | (Legacy) Voice dictation enabled |

### File / dir

| Key | What it does |
|---|---|
| `fileSuggestion` | Custom script for `@` file autocomplete |
| `plansDirectory` | Custom dir for plan files |
| `respectGitignore` | Respect `.gitignore` in file picker |
| `disableSkillShellExecution` | Block `` !` ` `` shell injection in non-bundled skills |

### Git / attribution

| Key | What it does |
|---|---|
| `attribution.commit` | Commit attribution string |
| `attribution.pr` | PR attribution string |
| `includeCoAuthoredBy` | (Deprecated) Include co-authored-by byline |
| `includeGitInstructions` | Include git workflow in system prompt |
| `prUrlTemplate` | URL template for the PR badge |

### Plan mode

| Key | What it does |
|---|---|
| `showClearContextOnPlanAccept` | Show "clear context" option on plan accept |

### Cleanup & sessions

| Key | What it does |
|---|---|
| `cleanupPeriodDays` | Session file retention (default 30) |
| `awaySummaryEnabled` | Show recap when returning |
| `feedbackSurveyRate` | Quality survey probability (0–1) |
| `companyAnnouncements` | Announcements at startup |

### Channels (managed-only)

See `channelsEnabled`, `allowedChannelPlugins`.

### Web / network

| Key | What it does |
|---|---|
| `skipWebFetchPreflight` | Skip WebFetch domain safety check |

### SSH (Desktop app)

| Key | What it does |
|---|---|
| `sshConfigs` | Pre-configured SSH connections for Desktop |

### Worktrees

| Key | What it does |
|---|---|
| `worktree.symlinkDirectories` | Dirs to symlink into worktrees |
| `worktree.sparsePaths` | Dirs to sparse-checkout in worktrees |

### Default shell

| Key | What it does |
|---|---|
| `defaultShell` | `"bash"` or `"powershell"` for `!` commands |

### Agent teams

| Key | What it does |
|---|---|
| `teammateMode` | `"auto"`, `"in-process"`, `"tmux"` |

### Env

| Key | What it does |
|---|---|
| `env` | `{"VAR": "value"}` — env vars for every session |

---

## Worked example

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-opus-4-7",
  "effortLevel": "xhigh",
  "outputStyle": "Explanatory",
  "alwaysThinkingEnabled": false,
  "autoMemoryEnabled": true,
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100",
  "editorMode": "vim",
  "tui": "fullscreen",
  "viewMode": "verbose",
  "showTurnDuration": true,
  "spinnerTipsEnabled": true,
  "terminalProgressBarEnabled": true,
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git *)", "Read", "Edit"],
    "deny":  ["Bash(curl *)", "Read(./.env)", "WebFetch"],
    "ask":   ["Bash(git push *)"],
    "defaultMode": "acceptEdits",
    "additionalDirectories": ["../docs"]
  },
  "sandbox": {
    "enabled": true,
    "filesystem": { "denyRead": ["~/.aws/credentials", "**/.env"] },
    "network":    { "allowedDomains": ["github.com", "*.npmjs.org"] }
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/safety-check.sh"
      }]
    }]
  },
  "statusLine": {
    "command": "~/.claude/status-line.sh",
    "updateInterval": 1000
  },
  "env": {
    "NODE_ENV": "development",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "enabledPlugins": {
    "code-review@claude-plugins-official": true
  },
  "attribution": {
    "commit": "🤖 Generated with Claude Code",
    "pr":     "🤖 Generated with Claude Code"
  }
}
```

---

## See also

- [permissions.md](./permissions.md) — managed-only keys table
- [permission-modes.md](./permission-modes.md) — `defaultMode`, `disableAutoMode`
- [sandboxing.md](./sandboxing.md) — full `sandbox.*` semantics
- [hooks.md](./hooks.md) — `hooks` shape
- [environment-variables.md](./environment-variables.md) — env vars vs settings
