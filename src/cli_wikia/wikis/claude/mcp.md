# MCP — Model Context Protocol

MCP is an open protocol for connecting Claude to external tools, APIs, databases, and services. An MCP server exposes:

- **Tools** — callable functions Claude can invoke
- **Resources** — files/data Claude can read (`@server` references)
- **Prompts** — reusable templates (invoked as `/server:prompt`)

Claude Code supports stdio (local), HTTP (remote), and SSE (remote, deprecated).

> ⚠️ **Use third-party MCP servers at your own risk.** Anthropic doesn't manage or audit third-party servers. They can expose you to prompt-injection risk.

---

## Installing MCP servers — three ways

### 1. Remote HTTP server (recommended for cloud services)

```bash
# Basic
claude mcp add --transport http <name> <url>

# Real example: Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 2. Remote SSE server (deprecated)

```bash
claude mcp add --transport sse <name> <url>

# Example
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

### 3. Local stdio server

```bash
# Note: all options come BEFORE the server name; -- separates from server command
claude mcp add [options] <name> -- <command> [args...]

# Example
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

> **Option ordering matters.** All options (`--transport`, `--env`, `--scope`, `--header`) must come **before** the server name. The `--` separates server name from command/args.

---

## Managing servers

```bash
claude mcp list                       # all configured
claude mcp get github                 # details for one
claude mcp remove github              # remove
claude mcp reset-project-choices      # re-prompt for project-scoped server approval

# Inside Claude Code
/mcp                                  # status, OAuth, enable/disable
```

### Dynamic tool updates

Claude Code supports MCP `list_changed` notifications. Servers can update their tools/prompts/resources without disconnect/reconnect — Claude Code refreshes capabilities automatically.

### Automatic reconnection (HTTP/SSE)

If an HTTP/SSE server disconnects mid-session, Claude Code reconnects with exponential backoff: up to **5 attempts**, starting at 1s, doubling each time. The server appears as pending in `/mcp` while reconnecting. After 5 fails it's marked failed; retry manually from `/mcp`. Stdio servers (local processes) are *not* reconnected automatically.

---

## Scopes

The `--scope` flag controls where the server is stored.

| Scope | Loads in | Shared with team | Stored in |
|---|---|---|---|
| `local` (default) | Current project only | No | `~/.claude.json` |
| `project` | Current project only | Yes (commit `.mcp.json`) | `.mcp.json` in project root |
| `user` | All your projects | No | `~/.claude.json` |

> "Local scope" for MCP differs from general local settings. MCP local-scoped servers go in `~/.claude.json`; general local settings use `.claude/settings.local.json`.

### Scope precedence (when same name in multiple places)

1. Local scope
2. Project scope
3. User scope
4. [Plugin-provided servers](./plugins.md)
5. claude.ai connectors

The three regular scopes match by name. Plugins and connectors match by **endpoint** — same URL/command counts as a duplicate.

### Project scope (`.mcp.json`)

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

For security, Claude Code **prompts for approval** before using project-scoped servers from `.mcp.json`. Reset choices with `claude mcp reset-project-choices`.

---

## Environment variable expansion in `.mcp.json`

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Syntax:
- `${VAR}` — value of env var
- `${VAR:-default}` — value if set, else default

Expansion locations: `command`, `args`, `env`, `url`, `headers`. If a required var is unset and has no default, Claude Code fails to parse the config.

---

## Plugin-bundled MCP servers

[Plugins](./plugins.md) can ship MCP servers in `.mcp.json` at the plugin root or inline in `plugin.json`. They start automatically when the plugin is enabled and appear alongside user-configured servers.

```json
// my-plugin/.mcp.json
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": { "DB_URL": "${DB_URL}" }
    }
  }
}
```

If you enable/disable a plugin during a session, run `/reload-plugins` to connect/disconnect its MCP servers.

Use `${CLAUDE_PLUGIN_ROOT}` for bundled files (changes on plugin update). Use `${CLAUDE_PLUGIN_DATA}` for persistent state that survives plugin updates.

---

## OAuth for remote servers

Many cloud-based servers require OAuth. Claude Code supports OAuth 2.0.

```bash
# 1. Add the server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. Inside Claude Code
/mcp        # follow browser steps to log in
```

Tips:
- Tokens stored securely, refreshed automatically.
- "Clear authentication" in `/mcp` revokes access.
- If browser doesn't open, copy the URL manually.
- If browser redirect fails after auth, paste the full callback URL into the prompt that appears in Claude Code.

### Fixed OAuth callback port

Some servers require a pre-registered redirect URI. By default Claude Code picks a random port. Use `--callback-port` to fix it:

```bash
# Fixed port + dynamic client registration
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Pre-configured OAuth credentials

Some servers don't support Dynamic Client Registration ("Incompatible auth server" error). Claude Code also supports Client ID Metadata Documents (CIMD) — auto-discovered. If both fail, register an OAuth app and provide credentials:

```bash
# claude mcp add: --client-secret prompts with masked input
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp

# claude mcp add-json: oauth object inline
claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
  --client-secret

# CI: env var skips the prompt
MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

---

## Tool naming and permissions

MCP tools surface as `mcp__<server>__<tool>` — that's the name to use in:

- **Permissions:** `mcp__github__list_issues` (exact) or `mcp__github__*` (whole server)
- **Hooks:** matcher `mcp__github__.*`
- **Skills' `allowed-tools`:** `mcp__github__*`

Permission rule examples:

```json
{
  "permissions": {
    "allow": ["mcp__github__list_issues", "mcp__github__get_issue"],
    "deny":  ["mcp__github__delete_*"]
  }
}
```

---

## Output limits and timeouts

- Claude Code warns when MCP tool output exceeds **10,000 tokens**. Increase: `MAX_MCP_OUTPUT_TOKENS=50000`
- Server startup timeout: `MCP_TIMEOUT=10000` (10 seconds)

---

## MCP resources (`@server`)

Servers can expose resources Claude can read:

```
@github What's the latest issue on my repo?
```

The `@server` prefix lets Claude reference resources from a specific server.

---

## MCP prompts (`/server:prompt`)

Servers can expose reusable prompt templates:

```
/asana:create-task "Fix the auth bug"
```

These appear in `/help` alongside other commands.

---

## MCP elicitation

When an MCP server requests user input during a tool call, Claude Code surfaces an interactive form. Two hooks gate this:

- `Elicitation` — fires before the form is shown; can deny.
- `ElicitationResult` — fires after user responds; can transform/decline.

See [hooks.md](./hooks.md).

---

## Push events INTO sessions: channels

An MCP server can also push messages into your session for Claude to react to. The server declares the `claude/channel` capability and you opt it in with `--channels`:

```bash
claude --channels plugin:fakechat@claude-plugins-official
```

See [channels.md](./channels.md).

---

## Managed MCP configuration

Org admins can lock down MCP via [managed settings](./settings.md):

```json
{
  "allowAllProjectMcpServers": true,        // auto-approve all .mcp.json servers
  "allowedMcpServers": ["github", "sentry"],
  "deniedMcpServers": ["arbitrary"],
  "allowManagedMcpServersOnly": true,       // only managed allowed servers respected
  "disabledMcpjsonServers": ["risky-tool"], // reject specific .mcp.json servers
  "enabledMcpjsonServers": ["safe-tool"]    // pre-approve specific .mcp.json servers
}
```

---

## Built-in IDE MCP server

The VS Code/JetBrains extensions automatically run an internal MCP server on `127.0.0.1` (random port; auth token in `~/.claude/ide/`). It's not visible in `/mcp` (it's internal RPC). Provides:

- `mcp__ide__getDiagnostics` — read VS Code Problems pane
- `mcp__ide__executeCode` — run Jupyter cells (asks confirmation)

---

## Practical examples

### Sentry for production debugging

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
# In Claude: /mcp to authenticate
```

```
What are the most common errors in the last 24 hours?
Show me the stack trace for error abc123
Which deployment introduced these new errors?
```

### GitHub remote MCP with PAT

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

### Read-only Postgres

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

### Playwright (browser automation, scoped to a subagent)

```yaml
# in an agent file
---
name: browser-tester
description: Tests features in a real browser
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
---
```

---

## See also

- [plugins.md](./plugins.md) — bundling MCP servers with plugins
- [permissions.md](./permissions.md) — `mcp__server__tool` rules
- [hooks.md](./hooks.md) — intercepting MCP tool calls, `Elicitation*` events
- [channels.md](./channels.md) — using MCP for push events
- [environment-variables.md](./environment-variables.md) — `MCP_TIMEOUT`, `MAX_MCP_OUTPUT_TOKENS`
