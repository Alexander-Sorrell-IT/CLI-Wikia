# settings.json Reference

`settings.json` is Gemini CLI's persistent configuration file. Settings are
grouped into top-level **category objects** — every setting must live inside its
category. This page documents each category and its most useful fields. The
authoritative, always-current list is the published JSON schema:

```
https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json
```

For file locations and precedence see [configuration.md](./configuration.md).
Some fields are flagged **requires restart**. The catalog below is large but not
exhaustive — `/settings` opens an in-app editor with live validation.

```json
{
  "general": { "vimMode": true, "preferredEditor": "vscode" },
  "ui": { "theme": "GitHub Dark", "hideTips": false },
  "model": { "name": "gemini-2.5-pro", "maxSessionTurns": 100 },
  "context": { "fileName": "GEMINI.md" },
  "tools": { "useRipgrep": true },
  "security": { "folderTrust": { "enabled": true } },
  "mcpServers": { }
}
```

---

## `general`

Core behavior and session lifecycle.

| Field | Type | Notes |
|---|---|---|
| `preferredEditor` | enum | `vscode`, `vscodium`, `windsurf`, `cursor`, `zed`, `antigravity`, `sublimetext`, `vim`, `neovim`, `emacs`, `hx`, `micro`, … Falls back to `$VISUAL`/`$EDITOR`. |
| `vimMode` | boolean | Vim keybindings (default `false`). |
| `defaultApprovalMode` | enum | `default`, `auto_edit`, or `plan`. YOLO can only be set via CLI flag. |
| `checkpointing.enabled` | boolean | Snapshot project files before edits (default `false`). See [checkpointing.md](./checkpointing.md). |
| `plan.enabled` | boolean | Enable Plan Mode (default `true`). See [permissions.md](./permissions.md). |
| `plan.modelRouting` | boolean | Use Pro for planning, Flash for implementation. |
| `enableAutoUpdate` | boolean | Automatic updates (default `true`). |
| `enableNotifications` / `notificationMethod` | boolean / enum | Terminal notifications: `auto`, `osc9`, `osc777`, `bell`. |
| `sessionRetention.enabled` | boolean | Auto-clean old sessions (default `true`). |
| `sessionRetention.maxAge` / `maxCount` / `minRetention` | string / number / string | e.g. `"30d"`, `"7d"`, `"24h"`. |
| `maxAttempts` | number | Retry attempts for chat requests (max 10). |
| `topicUpdateNarration` | boolean | Structured, less-chatty progress reporting. |

## `output`

| Field | Type | Notes |
|---|---|---|
| `format` | enum | `text` or `json`. Equivalent to `--output-format`. |

## `ui`

Appearance and the TUI. A large category — highlights:

| Field | Type | Notes |
|---|---|---|
| `theme` | string | Color theme name. See [themes.md](./themes.md). |
| `customThemes` | object | Custom theme definitions. |
| `autoThemeSwitching` | boolean | Switch light/dark with the terminal. |
| `inlineThinkingMode` | enum | `off` or `full` — show model thinking inline. |
| `hideBanner` / `hideTips` / `hideFooter` / `hideContextSummary` | boolean | Trim UI chrome. |
| `footer.items` / `footer.hideCWD` / `footer.hideModelInfo` / `footer.hideContextPercentage` | array / boolean | Footer composition. |
| `showLineNumbers` / `showCitations` / `showMemoryUsage` | boolean | Chat detail toggles. |
| `loadingPhrases` / `customWittyPhrases` | enum / array | Spinner text. |
| `accessibility.screenReader` | boolean | Plain-text rendering for screen readers (`--screen-reader`). |

## `ide`

| Field | Type | Notes |
|---|---|---|
| `enabled` | boolean | Enable IDE integration. See [ide-integration.md](./ide-integration.md). |

## `privacy`

| Field | Type | Notes |
|---|---|---|
| `usageStatisticsEnabled` | boolean | Anonymous usage statistics. |

## `billing`

| Field | Type | Notes |
|---|---|---|
| `overageStrategy` | enum | Behavior when AI credits / quota are exhausted. |
| `vertexAi.requestType` / `vertexAi.sharedRequestType` | enum | Vertex AI request-type headers. |

## `model`

| Field | Type | Notes |
|---|---|---|
| `name` | string | Default model (e.g. `gemini-2.5-pro`). See [models.md](./models.md). |
| `maxSessionTurns` | number | Cap on retained user/model/tool turns. |
| `summarizeToolOutput` | object | Per-tool output summarization. |
| `compressionThreshold` | number | Context fraction at which `/compress` auto-triggers. |
| `disableLoopDetection` | boolean | Disable repetition/loop detection. |

`modelConfigs` (a separate top-level category) tunes generation parameters
(temperature, topP, thinkingBudget, …) per model. See [models.md](./models.md).

## `context`

Hierarchical context / memory. See [context-files.md](./context-files.md).

| Field | Type | Notes |
|---|---|---|
| `fileName` | string \| string[] | Context file name(s); default `GEMINI.md`. |
| `importFormat` | string | Format for `@`-imports in context files. |
| `includeDirectoryTree` | boolean | Inject the project directory tree. |
| `discoveryMaxDirs` | number | Max directories scanned for memory. |
| `includeDirectories` | array | Extra workspace directories (like `--include-directories`). |
| `fileFiltering.respectGitIgnore` | boolean | Honor `.gitignore`. |
| `fileFiltering.respectGeminiIgnore` | boolean | Honor `.geminiignore`. |
| `fileFiltering.enableRecursiveFileSearch` / `enableFuzzySearch` | boolean | `@`-completion behavior. |

## `tools`

Built-in tool behavior and gating. See [tools.md](./tools.md).

| Field | Type | Notes |
|---|---|---|
| `core` | array | Allowlist restricting which built-in tools exist. |
| `allowed` | array | Tools that bypass the confirmation dialog. |
| `confirmationRequired` | array | Tools that always require confirmation (takes precedence). |
| `exclude` | array | Tools removed from discovery. |
| `useRipgrep` | boolean | Use ripgrep for content search. |
| `discoveryCommand` / `callCommand` | string | Custom project tool discovery/invocation. |
| `shell.enableInteractiveShell` | boolean | node-pty interactive shell. |
| `shell.pager` / `shell.showColor` / `shell.inactivityTimeout` | string / boolean / number | Shell tool behavior. |
| `sandbox` / `sandboxAllowedPaths` / `sandboxNetworkAccess` | string / array / boolean | Legacy full-process sandbox. See [sandboxing.md](./sandboxing.md). |

## `mcp`

| Field | Type | Notes |
|---|---|---|
| `allowed` / `excluded` | array | Allow/exclude lists of MCP server names. |
| `serverCommand` | string | Command to start an MCP server. |

`mcpServers.<NAME>` (top-level) defines each server (command/args/env/url/
headers/timeout/trust/includeTools/excludeTools). See [mcp.md](./mcp.md).

## `agents`

Subagent and built-in browser-agent configuration. See [subagents.md](./subagents.md).

| Field | Type | Notes |
|---|---|---|
| `overrides` | object | Per-agent model/limit overrides. |
| `browser.sessionMode` / `browser.headless` / `browser.allowedDomains` / `browser.maxActionsPerTask` / `browser.confirmSensitiveActions` | various | Built-in browser agent controls. |

## `security`

| Field | Type | Notes |
|---|---|---|
| `folderTrust.enabled` | boolean | Folder-trust enforcement. See [permissions.md](./permissions.md). |
| `toolSandboxing` | boolean | Per-tool sandbox isolation. |
| `disableYoloMode` | boolean | Block YOLO even if a flag enables it. |
| `disableAlwaysAllow` / `enablePermanentToolApproval` / `autoAddToPolicyByDefault` | boolean | Confirmation-dialog policy. |
| `blockGitExtensions` / `allowedExtensions` | boolean / array | Restrict extension installation. |
| `allowedEnvironmentVariables` / `blockedEnvironmentVariables` | array | Override env-var redaction (also under `environmentVariableRedaction.*`). |
| `auth.selectedType` / `auth.enforcedType` / `auth.useExternal` | string / boolean | Authentication method selection and enforcement. |

## `advanced`

| Field | Type | Notes |
|---|---|---|
| `autoConfigureMemory` | boolean | Auto-size memory. |
| `excludedEnvVars` | array | Env vars excluded from project `.env` loading. |
| `dnsResolutionOrder` | string | DNS resolution order. |
| `bugCommand` | object | Override the `/bug` target. |

## `experimental`

Opt-in / preview features. Selected flags:

| Field | Notes |
|---|---|
| `enableAgents` | Enable [subagents](./subagents.md) (🔬). |
| `worktrees` | Enable the `-w/--worktree` flag. |
| `modelSteering` | Model steering. See [models.md](./models.md). |
| `autoMemory` | Automatic memory. See [context-files.md](./context-files.md). |
| `gemma` / `gemmaModelRouter.*` | Local Gemma model routing. |
| `voiceMode` / `voice.*` | Voice input. |
| `extensionManagement` / `extensionRegistry*` / `extensionReloading` | Extension system previews. |
| `taskTracker`, `contextManagement`, `directWebFetch`, `dynamicModelConfiguration` | Misc previews. |

## `skills`

| Field | Type | Notes |
|---|---|---|
| `enabled` | boolean | Enable Agent Skills. See [skills.md](./skills.md). |
| `disabled` | array | Disabled skill names. |

## `hooks` and `hooksConfig`

`hooks.<Event>` arrays register lifecycle hooks (`BeforeTool`, `AfterTool`,
`BeforeAgent`, `AfterAgent`, `Notification`, `SessionStart`, `SessionEnd`,
`PreCompress`, `BeforeModel`, `AfterModel`, `BeforeToolSelection`).
`hooksConfig.enabled` / `disabled` / `notifications` toggle the system. See
[hooks.md](./hooks.md).

## `contextManagement`

Fine-grained context-window budgeting (`historyWindow.maxTokens`,
`messageLimits.*`, tool output distillation/masking). Mostly for advanced tuning.

## `admin`

Enterprise lockdown — best set in the system settings file. See
[enterprise.md](./enterprise.md).

| Field | Type | Notes |
|---|---|---|
| `secureModeEnabled` | boolean | Enforce secure mode. |
| `extensions.enabled` / `mcp.enabled` / `skills.enabled` | boolean | Globally allow/deny subsystems. |
| `mcp.config` / `mcp.requiredConfig` | object | Mandated MCP configuration. |

## `telemetry`

OpenTelemetry export. Fields include `enabled`, `target` (`local`/`gcp`),
`otlpEndpoint`, `otlpProtocol`, `logPrompts`, `outfile`, `useCollector`. All
overridable via `GEMINI_TELEMETRY_*` env vars. See [enterprise.md](./enterprise.md).

## `policyPaths` and `adminPolicyPaths`

Top-level arrays of extra policy files/directories for the
[Policy Engine](./permissions.md). Both **require restart**.

---

## See also

- [configuration.md](./configuration.md) — file locations, layers, precedence
- [environment-variables.md](./environment-variables.md) — env-var equivalents
- [commands.md](./commands.md) — `/settings` editor and reload commands
- [permissions.md](./permissions.md) — policy engine, approval modes, folder trust
