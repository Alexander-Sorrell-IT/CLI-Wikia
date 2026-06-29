# Enterprise Deployment

Patterns for deploying and managing Gemini CLI across an organization: centralized configuration, locked-down policy, restricted authentication, tool allow/deny lists, telemetry for auditing, and token caching for cost control.

> **Not a security boundary.** These controls are designed to enforce corporate policy and prevent accidental misuse in a managed environment. A determined user with local administrative rights may still circumvent them. For controls that are immutable at the local level, use [Enterprise Admin Controls](#enterprise-admin-controls) via the Management Console.

## System settings files and precedence

Settings are merged from four files. The precedence order for single-value settings (like `theme`) is, from lowest to highest:

1. **System defaults** — `system-defaults.json`
2. **User settings** — `~/.gemini/settings.json`
3. **Workspace settings** — `<project>/.gemini/settings.json`
4. **System overrides** — `settings.json`

The **System Overrides** file has the final say. For settings that are arrays (`includeDirectories`) or objects (`mcpServers`), values are **merged** rather than replaced — arrays are concatenated in precedence order, and objects are combined with the higher-precedence definition winning on key conflicts.

### System settings file location

| Platform | Path |
|---|---|
| Linux | `/etc/gemini-cli/settings.json` |
| Windows | `C:\ProgramData\gemini-cli\settings.json` |
| macOS | `/Library/Application Support/GeminiCli/settings.json` |

The path can be overridden with the `GEMINI_CLI_SYSTEM_SETTINGS_PATH` environment variable. The system settings file should be owned and protected by administrators with appropriate file permissions to prevent user modification.

### Merge example

Given these inputs:

```json
// system-defaults.json
{ "ui": { "theme": "default-corporate-theme" },
  "context": { "includeDirectories": ["/etc/gemini-cli/common-context"] } }

// ~/.gemini/settings.json (user)
{ "ui": { "theme": "user-preferred-dark-theme" },
  "mcpServers": { "corp-server": { "command": "/usr/local/bin/corp-server-dev" },
                  "user-tool": { "command": "npm start --prefix ~/tools/my-tool" } },
  "context": { "includeDirectories": ["~/gemini-context"] } }

// <project>/.gemini/settings.json (workspace)
{ "ui": { "theme": "project-specific-light-theme" },
  "mcpServers": { "project-tool": { "command": "npm start" } },
  "context": { "includeDirectories": ["./project-context"] } }

// settings.json (system overrides)
{ "ui": { "theme": "system-enforced-theme" },
  "mcpServers": { "corp-server": { "command": "/usr/local/bin/corp-server-prod" } },
  "context": { "includeDirectories": ["/etc/gemini-cli/global-context"] } }
```

The merged result:

- `theme` → `system-enforced-theme` (highest precedence wins).
- `mcpServers` → objects merged; `corp-server` takes the system-override definition; unique `user-tool` and `project-tool` are kept.
- `includeDirectories` → arrays concatenated in order: system defaults, user, workspace, system overrides.

### Enforcing the system settings path

A user could re-point `GEMINI_CLI_SYSTEM_SETTINGS_PATH` to bypass the corporate file. To mitigate this, deploy a wrapper script named `gemini` earlier in the user's `PATH` than the real binary:

```bash
#!/bin/bash
# Always load the corporate system settings.
export GEMINI_CLI_SYSTEM_SETTINGS_PATH="/etc/gemini-cli/settings.json"

REAL_GEMINI_PATH=$(type -aP gemini | grep -v "^$(type -P gemini)$" | head -n 1)
if [ -z "$REAL_GEMINI_PATH" ]; then
  echo "Error: The original 'gemini' executable was not found." >&2
  exit 1
fi
exec "$REAL_GEMINI_PATH" "$@"
```

On Windows, set the variable in the system-wide or user PowerShell profile:

```powershell
Add-Content -Path $PROFILE -Value '$env:GEMINI_CLI_SYSTEM_SETTINGS_PATH="C:\ProgramData\gemini-cli\settings.json"'
```

### Isolating state in shared environments

By default state lives in `~/.gemini`. In shared compute (build servers, ML runners), set `GEMINI_CLI_HOME` to give each user or job a unique directory; the CLI creates a `.gemini` folder inside it.

```bash
export GEMINI_CLI_HOME="/tmp/gemini-job-123"
gemini
```

## Restricting authentication

Enforce a single authentication method for all users by setting `security.auth.enforcedType` in the system `settings.json`. Users with a different method are prompted to switch; in non-interactive mode the CLI exits with an error on mismatch.

```json
{
  "security": {
    "auth": { "enforcedType": "oauth-personal" }
  }
}
```

`oauth-personal` enforces "Sign in with Google". Other values correspond to the supported auth types — verify the exact identifiers in official docs.

### Restricting logins to corporate domains

For Google Workspace, you can require corporate Google accounts. This is a **network-level** control configured on a proxy (not in Gemini CLI itself): intercept requests to `google.com` and add the `X-GoogApps-Allowed-Domains` header listing approved domains.

```
X-GoogApps-Allowed-Domains: my-corporate-domain.com, secondary-domain.com
```

See Google Workspace Admin Help on [blocking access to consumer accounts](https://support.google.com/a/answer/1668854).

## Restricting tool access

### Allowlisting with `tools.core` (recommended)

Explicitly list the tools and commands users may run. Anything not on the list is blocked.

```json
{
  "tools": {
    "core": ["ReadFileTool", "GlobTool", "ShellTool(ls)"]
  }
}
```

### Blocklisting with `tools.exclude` (deprecated)

Less secure than allowlisting, because it relies on blocking known-bad strings that clever users may bypass. Prefer the Policy Engine.

```json
{
  "tools": {
    "exclude": ["ShellTool(rm -rf)"]
  }
}
```

### Disabling YOLO mode

Force every tool execution to require user confirmation. Highly recommended in enterprise environments.

```json
{
  "security": { "disableYoloMode": true }
}
```

### Enforcing sandboxing

Isolate tool execution in a container. A custom hardened image can be supplied via a `sandbox.Dockerfile`.

```json
{
  "tools": { "sandbox": "docker" }
}
```

## Managing MCP servers

`mcpServers` definitions from System, Workspace, and User settings are **merged**. When the same server name appears at multiple levels, precedence is **System > Workspace > User** — so a user cannot override a system-defined server, but can add new uniquely-named ones.

To create a secure catalog, the system administrator must do **both** in system settings:

1. **Define** the full configuration for every approved server in `mcpServers`.
2. **Allowlist** their names in `mcp.allowed`. If `mcp.allowed` is omitted, the CLI merges and allows any user-defined server.

```json
{
  "mcp": { "allowed": ["corp-data-api", "source-code-analyzer"] },
  "mcpServers": {
    "corp-data-api": { "command": "/usr/local/bin/start-corp-api.sh", "timeout": 5000 },
    "source-code-analyzer": { "command": "/usr/local/bin/start-analyzer.sh" }
  }
}
```

Within a single server, restrict exposed tools using `includeTools` (allowlist) and `excludeTools`:

```json
{
  "mcp": { "allowed": ["third-party-analyzer"] },
  "mcpServers": {
    "third-party-analyzer": {
      "command": "/usr/local/bin/start-3p-analyzer.sh",
      "includeTools": ["code-search", "get-ticket-details"]
    }
  }
}
```

### Routing MCP traffic through a proxy

```json
{
  "mcpServers": {
    "proxied-server": {
      "command": "node",
      "args": ["mcp_server.js"],
      "env": {
        "HTTP_PROXY": "http://proxy.example.com:8080",
        "HTTPS_PROXY": "http://proxy.example.com:8080"
      }
    }
  }
}
```

## Enterprise Admin Controls

Unlike system settings (which privileged users can still edit), **Enterprise Admin Controls are enforced globally and cannot be overridden locally**. Secure defaults are enabled automatically for enterprise users and are customizable via the [Management Console](https://goo.gle/manage-gemini-cli).

| Control | Default | Effect when restricting |
|---|---|---|
| **Strict Mode** | Enabled | Users cannot enter YOLO mode. |
| **Extensions** | Disabled | Users cannot use or install extensions. |
| **MCP** | Disabled | Users cannot use MCP servers. |
| **Unmanaged Capabilities** | Disabled | Disables certain features (currently Agent Skills). |

### MCP allowlist (preview)

Admins can define an explicit allowlist of MCP servers. When the allowlist contains one or more servers, **all locally configured servers not present in the allowlist are ignored**. For a server to be active it must exist in **both** the admin allowlist and the user's local config (matched by name). The client then:

- Takes `url`, `type`, and `trust` from the admin allowlist (overriding local values).
- Applies admin `includeTools`/`excludeTools` exclusively if either is defined; otherwise falls back to local tool settings.
- Clears local execution fields (`command`, `args`, `env`, `cwd`, `httpUrl`, `tcp`) so users cannot change the connection method.
- A server in the allowlist but missing locally is **not** initialized (users keep final control over which permitted servers run).

```json
{
  "mcpServers": {
    "external-provider": {
      "url": "https://api.mcp-provider.com",
      "type": "sse",
      "trust": true,
      "includeTools": ["toolA", "toolB"],
      "excludeTools": []
    }
  }
}
```

### Required MCP servers (preview)

Servers that are **always injected** into the user's environment regardless of local config, after allowlist filtering. They support only remote transports (`sse`, `http`); `trust` defaults to `true`. A required server with the same name as a local one **completely overrides** the local definition.

```json
{
  "requiredMcpServers": {
    "corp-compliance-tool": {
      "url": "https://mcp.corp/compliance",
      "type": "http",
      "trust": true,
      "description": "Corporate compliance tool"
    }
  }
}
```

Supported fields include `url`, `type`, `trust`, `description`, `authProviderType` (`dynamic_discovery`, `google_credentials`, `service_account_impersonation`), `oauth` (`scopes`, `clientId`, `clientSecret`), `targetAudience`, `targetServiceAccount`, `headers`, `includeTools`/`excludeTools`, and `timeout`.

## Telemetry and auditing

Gemini CLI has built-in [OpenTelemetry](https://opentelemetry.io/) support, emitting **logs, metrics, and traces**. Data can stay local for debugging or export to any OTLP backend (Google Cloud, Jaeger, Prometheus, Datadog, etc.). Configure it under `telemetry.*` in `settings.json`; environment variables override settings.

### Telemetry settings

| Setting | Environment variable | Description | Values | Default |
|---|---|---|---|---|
| `enabled` | `GEMINI_TELEMETRY_ENABLED` | Enable/disable telemetry | `true`/`false` | `false` |
| `traces` | `GEMINI_TELEMETRY_TRACES_ENABLED` | Detailed attribute tracing | `true`/`false` | `false` |
| `target` | `GEMINI_TELEMETRY_TARGET` | Where to send data | `"gcp"`/`"local"` | `"local"` |
| `otlpEndpoint` | `GEMINI_TELEMETRY_OTLP_ENDPOINT` | OTLP collector endpoint | URL | `http://localhost:4317` |
| `otlpProtocol` | `GEMINI_TELEMETRY_OTLP_PROTOCOL` | OTLP transport | `"grpc"`/`"http"` | `"grpc"` |
| `outfile` | `GEMINI_TELEMETRY_OUTFILE` | Save to file (overrides `otlpEndpoint`) | path | - |
| `logPrompts` | `GEMINI_TELEMETRY_LOG_PROMPTS` | Include prompt text in logs | `true`/`false` | `true` |
| `useCollector` | `GEMINI_TELEMETRY_USE_COLLECTOR` | Use external OTLP collector | `true`/`false` | `false` |
| `useCliAuth` | `GEMINI_TELEMETRY_USE_CLI_AUTH` | Use CLI OAuth creds (GCP target only) | `true`/`false` | `false` |
| - | `GEMINI_CLI_SURFACE` | Custom label for traffic reporting | string | - |

> **Set `logPrompts` to `false` in enterprise settings** to avoid collecting potentially sensitive prompt content. Detailed trace attributes (full prompts, tool outputs) are off unless `traces` is `true`.

### Local target (development)

```json
{
  "telemetry": {
    "enabled": true,
    "target": "local",
    "outfile": ".gemini/telemetry.log"
  }
}
```

Logs and metrics are written to the `outfile`. For Jaeger/Genkit setups, see the local development guide.

### Google Cloud target (auditing)

Exports directly to Cloud Trace, Cloud Monitoring, and Cloud Logging. If `otlpEndpoint` is not set it defaults to `http://localhost:4317`.

```json
{
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "logPrompts": false
  }
}
```

Prerequisites:

1. Set the project: `OTLP_GOOGLE_CLOUD_PROJECT` (separate telemetry project) or `GOOGLE_CLOUD_PROJECT` (same as inference).
2. Authenticate with Application Default Credentials (`gcloud auth application-default login` or `GOOGLE_APPLICATION_CREDENTIALS`), or set `useCliAuth: true` to reuse your login OAuth credentials (requires direct export; cannot be combined with `useCollector`).
3. Grant the account: **Cloud Trace Agent**, **Monitoring Metric Writer**, **Logs Writer**.
4. Enable APIs: `cloudtrace.googleapis.com`, `monitoring.googleapis.com`, `logging.googleapis.com`.

View data in the Logs Explorer, Metrics Explorer, and Trace Explorer. A pre-configured dashboard, "**Gemini CLI Monitoring**", is available under Cloud Monitoring Dashboard Templates.

### What is logged

All telemetry data carries common attributes: `session.id`, `installation.id`, `active_approval_mode`, and `user.email` (when authenticated). Logged events include (non-exhaustive):

| Category | Example events |
|---|---|
| Sessions | `gemini_cli.config` (startup config), `gemini_cli.user_prompt` (prompt text excluded when `logPrompts` is `false`) |
| Tools | `gemini_cli.tool_call`, `gemini_cli.tool_output_truncated`, `gemini_cli.edit_strategy` |
| Files | `gemini_cli.file_operation` (create/read/update) |
| API | `gemini_cli.api_request`, `gemini_cli.api_response`, `gemini_cli.api_error` |
| Routing | `gemini_cli.model_routing`, `gemini_cli.slash_command` |
| Agents | `gemini_cli.agent.start`, `gemini_cli.agent.finish` |
| IDE | `gemini_cli.ide_connection` |

Metrics include `gemini_cli.session.count`, `gemini_cli.tool.call.count`/`latency`, `gemini_cli.api.request.count`/`latency`, `gemini_cli.token.usage`, `gemini_cli.file.operation.count`, plus standard GenAI semantic-convention metrics (`gen_ai.client.token.usage`, `gen_ai.client.operation.duration`). Trace spans follow OpenTelemetry GenAI conventions (`gen_ai.operation.name`, `gen_ai.agent.name` = `gemini-cli`, token counts, etc.).

### Client identification

Gemini CLI tags its `User-Agent` so you can distinguish traffic sources (terminal vs. Code Assist vs. IDE).

| Environment | User-Agent prefix | Surface tag |
|---|---|---|
| Gemini Code Assist (Agent Mode) | `GeminiCLI-a2a-server` | `vscode` |
| Zed (via ACP) | `GeminiCLI-acp-zed` | `zed` |
| Standard terminal | `GeminiCLI` | `terminal` |

Set `GEMINI_CLI_SURFACE` to add a custom surface label for your own scripts or distribution channels.

## Token caching

Gemini CLI automatically reuses prior system instructions and context to cut the tokens processed in subsequent requests, lowering API cost. No configuration is required (implicit caching).

| Auth method | Token caching |
|---|---|
| Gemini API key | Supported |
| Vertex AI (with project + location) | Supported |
| OAuth (Google Personal/Enterprise via Code Assist) | Not supported — the Code Assist API does not support cached content creation |

View token usage and cached-token savings with `/stats`. Cached token counts appear in the output **only when cached tokens are actually being used**; their absence with OAuth auth is expected, not a bug. Total token usage is always shown.

## Example: locked-down system `settings.json`

```json
{
  "tools": {
    "sandbox": "docker",
    "core": ["ReadFileTool", "GlobTool", "ShellTool(ls)", "ShellTool(cat)", "ShellTool(grep)"]
  },
  "mcp": { "allowed": ["corp-tools"] },
  "mcpServers": {
    "corp-tools": { "command": "/opt/gemini-tools/start.sh", "timeout": 5000 }
  },
  "telemetry": {
    "enabled": true,
    "target": "gcp",
    "otlpEndpoint": "https://telemetry-prod.example.com:4317",
    "logPrompts": false
  },
  "advanced": {
    "bugCommand": { "urlTemplate": "https://servicedesk.example.com/new-ticket?title={title}&details={info}" }
  },
  "privacy": { "usageStatisticsEnabled": false }
}
```

This forces tools into a Docker sandbox, allowlists a small set of safe tools, defines one approved MCP server, enables auditing telemetry without prompt content, redirects `/bug` to an internal tracker, and disables general usage statistics.

## See also

- [configuration.md](./configuration.md) — full settings reference and precedence
- [mcp.md](./mcp.md) — configuring and using MCP servers
- [environment-variables.md](./environment-variables.md) — `GEMINI_CLI_*` and `GEMINI_TELEMETRY_*` variables
- [cli-reference.md](./cli-reference.md) — command-line flags
