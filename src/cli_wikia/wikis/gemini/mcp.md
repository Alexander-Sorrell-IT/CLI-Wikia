# MCP — Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP) servers extend Gemini CLI with external tools, data, and workflows. A server bridges the Gemini model to your local environment or remote services (databases, APIs, custom scripts), and exposes three kinds of capability:

- **Tools** — callable functions the model can invoke.
- **Resources** — data the CLI can read and inject into the conversation (`@server://...` references).
- **Prompts** — predefined templates invoked as slash commands.

Gemini CLI discovers these on startup, validates and namespaces them, and makes them available to the model alongside its built-in tools.

---

## Transports

Gemini CLI supports three transport types, selected automatically from the server config:

| Transport | Selected by config key | Description |
|---|---|---|
| **Stdio** | `command` | Spawns a local subprocess; communicates over stdin/stdout. |
| **SSE** | `url` | Connects to a Server-Sent Events endpoint. |
| **Streamable HTTP** | `httpUrl` | Uses HTTP streaming. |

When more than one is present, precedence is `httpUrl` → `url` → `command`.

---

## Adding servers with `gemini mcp`

The `gemini mcp` command group manages server entries in `settings.json` without hand-editing JSON.

### `gemini mcp add`

```bash
gemini mcp add [options] <name> <commandOrUrl> [args...]
```

- `<name>` — unique server name.
- `<commandOrUrl>` — the executable (stdio) or the URL (http/sse).
- `[args...]` — optional arguments for a stdio command.

| Flag | Description | Default |
|---|---|---|
| `-s, --scope` | Config scope: `user` or `project` | `project` |
| `-t, --transport` | Transport: `stdio`, `sse`, `http` | `stdio` |
| `-e, --env` | Set an env var, e.g. `-e KEY=value` (repeatable) | — |
| `-H, --header` | Set an HTTP header for sse/http, e.g. `-H "Authorization: Bearer abc"` (repeatable) | — |
| `--timeout` | Connection timeout in milliseconds | — |
| `--trust` | Trust the server (bypass all tool-call confirmations) | `false` |
| `--description` | Description for the server | — |
| `--include-tools` | Comma-separated allowlist of tools | — |
| `--exclude-tools` | Comma-separated denylist of tools | — |

The `--scope` flag determines the target file: `user` writes `~/.gemini/settings.json`, `project` writes `.gemini/settings.json`.

```bash
# Local stdio server with env vars
gemini mcp add -e API_KEY=123 -e DEBUG=true my-stdio-server /path/to/server arg1 arg2

# Local python server (note the -- before server args)
gemini mcp add python-server python server.py -- --server-arg my-value

# HTTP server
gemini mcp add --transport http http-server https://api.example.com/mcp/

# HTTP server with an auth header
gemini mcp add --transport http --header "Authorization: Bearer abc123" \
  secure-http https://api.example.com/mcp/

# SSE server with an auth header
gemini mcp add --transport sse --header "Authorization: Bearer abc123" \
  secure-sse https://api.example.com/sse/
```

### `gemini mcp list`

Lists configured servers with details and live connection status. No flags.

```bash
gemini mcp list
```

```text
✓ stdio-server: command: python3 server.py (stdio) - Connected
✓ http-server: https://api.example.com/mcp (http) - Connected
✗ sse-server: https://api.example.com/sse (sse) - Disconnected
```

> For security, `stdio` servers are only tested/shown as "Connected" when the current folder is trusted. In an untrusted folder they show "Disconnected"; run `gemini trust` to trust the folder.

### `gemini mcp remove`

```bash
gemini mcp remove <name>          # honors -s, --scope (default: project)
```

### `gemini mcp enable` / `gemini mcp disable`

Temporarily toggle a server without deleting its config. Disabled servers show as "Disabled" in `/mcp` and won't connect.

```bash
gemini mcp enable <name> [--session]
gemini mcp disable <name> [--session]
```

- `--session` — apply only for the current session (not persisted).

Enablement state persists in `~/.gemini/mcp-server-enablement.json`. The same actions are available in-session as `/mcp enable <name>` and `/mcp disable <name>`.

---

## Configuring servers in `settings.json`

Servers are defined under a top-level `mcpServers` object. Each key is a server name; the value is its config.

```json
{
  "mcpServers": {
    "serverName": {
      "command": "path/to/server",
      "args": ["--arg1", "value1"],
      "env": {
        "API_KEY": "$MY_API_TOKEN"
      },
      "cwd": "./server-directory",
      "timeout": 30000,
      "trust": false
    }
  }
}
```

### Server config fields

One transport field is required (`command`, `url`, or `httpUrl`); the rest are optional.

| Field | Type | Description |
|---|---|---|
| `command` | string | Executable path for **stdio** transport. |
| `url` | string | **SSE** endpoint URL, e.g. `http://localhost:8080/sse`. |
| `httpUrl` | string | **Streamable HTTP** endpoint URL. |
| `args` | string[] | Command-line arguments (stdio). |
| `headers` | object | Custom HTTP headers (with `url`/`httpUrl`). |
| `env` | object | Environment variables for the process. Supports `$VAR`/`${VAR}` (all platforms), `%VAR%` (Windows). |
| `cwd` | string | Working directory (stdio). |
| `timeout` | number | Request timeout in ms. Default `600000` (10 minutes). |
| `trust` | boolean | When `true`, bypasses all tool-call confirmations for the server. Default `false`. |
| `includeTools` | string[] | Allowlist — only these tools are exposed. |
| `excludeTools` | string[] | Denylist — these tools are hidden. Takes precedence over `includeTools`. |
| `authProviderType` | string | OAuth provider: `dynamic_discovery` (default), `google_credentials`, `service_account_impersonation`. |
| `targetAudience` | string | OAuth Client ID allowlisted on the IAP-protected app (service-account impersonation). |
| `targetServiceAccount` | string | Email of the Google Cloud service account to impersonate. |

### Global MCP settings (`mcp`)

A separate top-level `mcp` object controls discovery across all servers:

| Field | Type | Description |
|---|---|---|
| `mcp.serverCommand` | string | A global command to start an MCP server. |
| `mcp.allowed` | string[] | Allowlist of server names (keys in `mcpServers`). If set, only these connect. |
| `mcp.excluded` | string[] | Denylist of server names that will not connect. |

```json
{
  "mcp": {
    "allowed": ["my-trusted-server"],
    "excluded": ["experimental-server"]
  }
}
```

> The CLI flag `--allowed-mcp-server-names` is the run-scoped equivalent of `mcp.allowed`, restricting which servers connect for a single invocation — *verify exact spelling/behavior in official docs*.

---

## Environment variables and security

### Expansion

Values in `env` are expanded so you avoid hardcoding secrets:

- POSIX/Bash: `$VAR` or `${VAR}` (all platforms)
- Windows: `%VAR%` (Windows only)

Undefined variables resolve to an empty string.

```json
"env": {
  "API_KEY": "$MY_EXTERNAL_TOKEN",
  "LOG_LEVEL": "$LOG_LEVEL",
  "TEMP_DIR": "%TEMP%"
}
```

### Environment sanitization

When spawning stdio servers, Gemini CLI **redacts sensitive host environment variables** so they don't leak to third-party servers. Redacted by default:

- Core project keys: `GEMINI_API_KEY`, `GOOGLE_API_KEY`, etc.
- Anything matching `*TOKEN*`, `*SECRET*`, `*PASSWORD*`, `*KEY*`, `*AUTH*`, `*CREDENTIAL*`.
- Certificate and private-key patterns.

To pass a sensitive variable, declare it explicitly in the server's `env` block. Explicitly-defined variables (including those from extensions) are trusted and **not** redacted — this is treated as informed consent. Even then, prefer expansion (`"MY_KEY": "$MY_KEY"`) over literal secrets.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_PERSONAL_ACCESS_TOKEN"
      }
    }
  }
}
```

---

## OAuth for remote servers

Gemini CLI supports OAuth 2.0 for remote SSE/HTTP servers.

### Automatic discovery

For servers that advertise OAuth metadata, omit OAuth config entirely:

```json
{
  "mcpServers": {
    "discoveredServer": { "url": "https://api.example.com/sse" }
  }
}
```

The CLI detects `401` responses, discovers authorization/token endpoints, performs dynamic client registration if supported, opens a browser to authenticate, exchanges the code for tokens, and retries.

### Managing auth with `/mcp auth`

```bash
/mcp auth                 # list servers requiring authentication
/mcp auth serverName      # authenticate (or re-authenticate) a server
```

OAuth requires a local browser and the ability to receive a redirect on `http://localhost:<random-port>/oauth/callback`. It won't work in headless environments, remote SSH without X11 forwarding, or containers without browser support.

Tokens are stored in `~/.gemini/mcp-oauth-tokens.json`, refreshed when expired, validated before each connection, and cleaned up when invalid.

### OAuth config properties (`oauth` object)

| Property | Type | Description |
|---|---|---|
| `enabled` | boolean | Enable OAuth for the server. |
| `clientId` | string | Client identifier (optional with dynamic registration). |
| `clientSecret` | string | Client secret (optional for public clients). |
| `authorizationUrl` | string | Authorization endpoint (auto-discovered if omitted). |
| `tokenUrl` | string | Token endpoint (auto-discovered if omitted). |
| `scopes` | string[] | Required OAuth scopes. |
| `redirectUri` | string | Custom redirect URI (defaults to an OS-assigned random port). |
| `tokenParamName` | string | Query parameter name for tokens in SSE URLs. |
| `audiences` | string[] | Audiences the token is valid for. |

### Provider types

- **`dynamic_discovery`** (default) — discover OAuth config from the server.
- **`google_credentials`** — use Google Application Default Credentials (ADC); you must specify `scopes`.
- **`service_account_impersonation`** — impersonate a Google Cloud service account (designed for IAP-protected Cloud Run); set `targetAudience` and `targetServiceAccount`.

```json
{
  "mcpServers": {
    "googleCloudServer": {
      "httpUrl": "https://my-gcp-service.run.app/mcp",
      "authProviderType": "google_credentials",
      "oauth": { "scopes": ["https://www.googleapis.com/auth/userinfo.email"] }
    },
    "myIapProtectedServer": {
      "url": "https://my-iap-service.run.app/sse",
      "authProviderType": "service_account_impersonation",
      "targetAudience": "YOUR_IAP_CLIENT_ID.apps.googleusercontent.com",
      "targetServiceAccount": "your-sa@your-project.iam.gserviceaccount.com"
    }
  }
}
```

---

## Example configurations

```json
// Python stdio server
{
  "mcpServers": {
    "pythonTools": {
      "command": "python",
      "args": ["-m", "my_mcp_server", "--port", "8080"],
      "cwd": "./mcp-servers/python",
      "env": { "DATABASE_URL": "$DB_CONNECTION_STRING", "API_KEY": "${EXTERNAL_API_KEY}" },
      "timeout": 15000
    }
  }
}
```

```json
// HTTP server with custom headers
{
  "mcpServers": {
    "httpServerWithAuth": {
      "httpUrl": "http://localhost:3000/mcp",
      "headers": {
        "Authorization": "Bearer your-api-token",
        "X-Custom-Header": "custom-value"
      },
      "timeout": 5000
    }
  }
}
```

```json
// Tool filtering
{
  "mcpServers": {
    "filteredServer": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "includeTools": ["safe_tool", "file_reader", "data_processor"],
      "timeout": 30000
    }
  }
}
```

---

## Tool naming and namespaces

To prevent collisions, every discovered tool gets a fully qualified name:

```
mcp_{serverName}_{toolName}
```

The registry maps these FQNs back to their server. If two servers share a name and expose tools with the same name, the last-registered tool wins.

During discovery, tool names are sanitized for the Gemini API: characters other than letters, numbers, `_`, `-`, `.`, `:` become underscores, and names over 63 characters are truncated with a middle `...`. Parameter schemas are also adjusted — `$schema` and `additionalProperties` are stripped, and `anyOf` defaults are removed for Vertex AI compatibility.

> **Avoid underscores in server names** (use `my-server`, not `my_server`). The policy parser splits FQNs on the first underscore after `mcp_`; an underscore in the server name breaks server identity and can cause wildcard/security rules to fail silently.

---

## Trust and confirmations

By default, each MCP tool call requires confirmation. The execution layer resolves trust in this order:

1. **Server `trust: true`** — bypasses all confirmations for that server.
2. **Dynamic allow-lists** built up during the session:
   - Server-level (`serverName`) — all tools from the server are trusted.
   - Tool-level (`serverName.toolName`) — that one tool is trusted.

When a confirmation dialog appears, you can choose: **Proceed once**, **Always allow this tool**, **Always allow this server**, or **Cancel**. For fine-grained auto-approve/deny rules, see the Policy Engine's MCP syntax (`mcp_{server}_{tool}`).

---

## The `/mcp` command

Run `/mcp` in an interactive session to inspect your setup. It shows the server list, each server's connection status (`CONNECTED` / `CONNECTING` / `DISCONNECTED`), a config summary (excluding secrets), discovered tools, prompts, and resources, plus the overall discovery state.

Subcommands:

| Command | Action |
|---|---|
| `/mcp list` | List servers and their status/tools. |
| `/mcp desc` | Show tool descriptions. |
| `/mcp schema` | Show full tool parameter schemas. |
| `/mcp auth [name]` | Manage OAuth authentication. |
| `/mcp enable <name>` | Enable a server in-session. |
| `/mcp disable <name>` | Disable a server in-session. |
| `/mcp reload` | Re-run discovery and refresh capabilities. |

> To reduce startup noise, MCP connection errors are silent by default; a single hint ("MCP issues detected. Run /mcp list for status.") is shown. Full diagnostics re-enable when you run an interactive `/mcp` command, when the model calls a tool from a server, or when you invoke one of its prompts.

---

## Resources (`@server://...`)

Some servers expose contextual **resources** in addition to tools. The CLI fetches each server's `resources/list` during discovery and shows a Resources section in `/mcp`.

Reference a resource in chat with the same `@` syntax used for files:

```
@server://resource/path
```

Resource URIs appear in the completion menu alongside filesystem paths. On submit, the CLI calls `resources/read` and injects the content into the conversation.

Two built-in tools let the model work with resources directly:

| Tool | Kind | Parameters | Confirmation |
|---|---|---|---|
| `list_mcp_resources` | Search | `serverName` (optional filter) | No (read-only) |
| `read_mcp_resource` | Read | `uri` (required) | No (read-only) |

`read_mcp_resource` extracts text or binary data; binary returns a placeholder describing the data type.

---

## Prompts as slash commands

MCP servers can expose predefined **prompts**. Once discovered, each prompt becomes a slash command named after the prompt. The CLI parses arguments, calls `prompts/get` on the server with them, and sends the returned text to the model.

```bash
# named arguments
/poem-writer --title="Gemini CLI" --mood="reverent"

# positional arguments
/poem-writer "Gemini CLI" reverent
```

---

## Rich tool results

MCP tools aren't limited to text. A tool's `CallToolResult.content` array may mix `text`, `image`, `audio`, `resource` (embedded), and `resource_link` blocks. Gemini CLI combines text into one `functionResponse` part, passes binary data as separate `inlineData` parts, and shows a user-friendly summary.

```json
{
  "content": [
    { "type": "text", "text": "Here is the logo you requested." },
    { "type": "image", "data": "BASE64_DATA", "mimeType": "image/png" }
  ]
}
```

---

## Overriding extension-provided servers

If an MCP server comes from an extension (e.g. `google-workspace`), you can override it in your local `settings.json`. Merge rules ensure the most restrictive policy wins:

- **`excludeTools`** arrays are **unioned** — if either source blocks a tool, it stays blocked.
- **`includeTools`** arrays are **intersected** — if both define allowlists, only tools in both are enabled.
- `excludeTools` always beats `includeTools`.
- **`env`** objects are merged; your local value wins on conflicts.
- Scalar properties (`command`, `url`, `timeout`, …) are replaced by your local values.
- A server defined in both `settings.json` and an extension: the `settings.json` definition takes precedence.

```json
{
  "mcpServers": {
    "google-workspace": { "excludeTools": ["gmail.send"] }
  }
}
```

---

## Server instructions

Gemini CLI honors [MCP server instructions](https://modelcontextprotocol.io/specification/2025-06-18/schema#initializeresult): a server's declared instructions are appended to the system prompt.

---

## Troubleshooting

| Symptom | Things to check |
|---|---|
| Server `DISCONNECTED` | Verify `command`/`args`/`cwd`; run the command manually; check dependencies, permissions, and CLI logs. |
| Connects but no tools | Confirm the server actually registers tools and implements MCP tool listing; check stderr. |
| Tools fail to execute | Validate parameters and JSON Schema; check for unhandled exceptions; raise `timeout`. |
| Fails under sandbox | Use Docker servers with bundled deps; ensure executables, network, and required env vars are available in the sandbox. |

Debugging tips: run with `--debug` (or press **F12** for the debug console in interactive mode), watch captured server stderr, test the server in isolation, and use `/mcp` frequently during development.

---

## See also

- [extensions.md](./extensions.md) — bundling MCP servers, commands, and context in an extension
- [configuration.md](./configuration.md) — `settings.json` structure and scopes
- [cli-reference.md](./cli-reference.md) — full command and flag reference
