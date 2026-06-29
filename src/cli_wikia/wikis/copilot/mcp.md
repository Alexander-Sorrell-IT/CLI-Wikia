# MCP Servers

[Model Context Protocol](https://modelcontextprotocol.io) servers give Copilot extra tools and data — local processes (stdio) or remote endpoints (HTTP/SSE). Copilot CLI ships with one built-in server (`github-mcp-server`) and lets you add your own.

---

## Configuration sources

`copilot mcp` loads servers from several places (later sources augment earlier ones):

| Scope | Location |
|---|---|
| User | `~/.copilot/mcp-config.json` |
| Workspace | `.mcp.json`, or `.github/mcp.json` |
| Plugin | MCP servers bundled by installed [plugins](plugins.md) |
| Session | `--additional-mcp-config <json-or-@file>` (repeatable; this run only) |

---

## Managing servers from the CLI

```bash
copilot mcp list                 # all configured servers
copilot mcp get <name>           # details for one server
copilot mcp add <name> …         # add to user config
copilot mcp remove <name>        # remove
```

`copilot mcp add` covers both transports:

```bash
# Local stdio server: command after --
copilot mcp add context7 -- npx -y @upstash/context7-mcp

# Local with env vars
copilot mcp add github --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx \
  -- npx -y @modelcontextprotocol/server-github

# Remote HTTP server
copilot mcp add --transport http notion https://mcp.notion.com/mcp

# Remote with an auth header
copilot mcp add --transport http \
  --header "Authorization: Bearer rk_live_xxx" stripe https://mcp.stripe.com
```

`add` options:

| Option | Purpose |
|---|---|
| `--transport <stdio\|http\|sse>` | Server transport (default `stdio`) |
| `--env KEY=VALUE` | Env var for a local server (repeatable) |
| `--header "Name: value"` | HTTP header for a remote server (repeatable) |
| `--tools <filter>` | Tool filter: `*` (all, default), a comma-separated list, or `""` (none) |
| `--timeout <ms>` | Connection timeout |
| `--json` | Print the resulting config as JSON |
| `--show-secrets` | Reveal env/header values (masked by default) |

Inside a session, `/mcp` opens the same management UI.

---

## Config file format

`~/.copilot/mcp-config.json` (and the workspace/plugin equivalents) describe servers by name. A local server uses `command`/`args`/`env`; a remote one uses a `url` and optional `headers`. Conceptually:

```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {}
    },
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp",
      "headers": { "Authorization": "Bearer ..." },
      "tools": "*"
    }
  }
}
```

Prefer `copilot mcp add` and `--additional-mcp-config` to manage this rather than hand-editing. Use `copilot mcp get <name>` to see the exact stored shape.

> If your organization restricts Copilot, **third-party MCP servers may be disabled by policy** — only built-in servers will be available, and the CLI will return an "Access denied by policy settings" error.

---

## The built-in GitHub MCP server

`github-mcp-server` ships enabled and exposes GitHub actions (PRs, issues, etc.) directly in your session. By default only a **CLI subset** of its tools is on. Adjust the scope:

| Flag | Effect |
|---|---|
| `--enable-all-github-mcp-tools` | Turn on every GitHub MCP tool (overrides the toolset/tool flags below) |
| `--add-github-mcp-toolset <toolset>` | Enable a named toolset (repeatable; `all` for everything) |
| `--add-github-mcp-tool <tool>` | Enable one tool (repeatable; `*` for all) |

Disable built-ins entirely:

```bash
copilot --disable-builtin-mcps                  # all built-ins
copilot --disable-mcp-server github-mcp-server  # just one
```

---

## Tool permissions for MCP

MCP tools are gated like any other tool. Use the `<server>(tool)` permission pattern:

```bash
copilot --allow-tool='MyMCP' --deny-tool='MyMCP(dangerous_tool)'
```

See [permissions.md](permissions.md).

---

## See also

- [plugins.md](plugins.md) — plugins can bundle MCP servers
- [permissions.md](permissions.md) — gating MCP tools
- [cli-reference.md](cli-reference.md) — every `--*-mcp-*` flag
