# Model Context Protocol (MCP)

Antigravity speaks **MCP**, the open Model Context Protocol, to give agents
external tools and data sources — GitHub, databases, documentation indexes,
cloud SDKs, browser automation, and anything else exposed as an MCP server. MCP
carries forward from the Gemini CLI, so existing MCP servers work with `agy`.

---

## Inspecting active servers

```
/mcp       # in a session: list active MCP servers and their exposed tools
```

---

## Configuration: `mcp_config.json`

MCP servers are declared in **`mcp_config.json`** files. The schema is the
familiar `mcpServers` map. A **remote (HTTP) server** looks like this (the
bundled `github` plugin):

```json
{
  "mcpServers": {
    "github": {
      "command": "",
      "args": null,
      "cwd": "",
      "env": null,
      "serverUrl": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

A **local (stdio) server** instead populates `command`, `args`, `cwd`, and `env`:

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "npx",
      "args": ["-y", "@scope/my-mcp-server"],
      "cwd": "",
      "env": { "API_KEY": "..." },
      "serverUrl": ""
    }
  }
}
```

| Field | Meaning |
|-------|---------|
| `command` | Executable to launch a local stdio server (empty for remote) |
| `args` | Arguments to that command |
| `cwd` | Working directory for the launched server |
| `env` | Environment variables passed to the server |
| `serverUrl` | URL of a remote HTTP/SSE MCP server (empty for local) |

---

## Where MCP config lives

| Location | Scope |
|----------|-------|
| `~/.gemini/antigravity-cli/plugins/<name>/mcp_config.json` | MCP server shipped by a [plugin](./plugins.md) |
| `~/.gemini/antigravity-cli/mcp/<name>/` | Per-server staging directory |
| `~/.gemini/antigravity-cli/brain/<conversation-id>/mcp_config.json` | MCP servers active for a specific conversation |

The most common way to add MCP servers is therefore to **install a plugin that
bundles one** (e.g. `github`, `context7`, `terraform`, `FileSearch`,
`cloudbase-ai-toolkit`, `mcp-db-context-enrichment` are all pre-staged with their
own `mcp_config.json`).

---

## Mentioning MCP tools

In the desktop app (and where supported in the CLI), typing `@` opens a mention
menu that includes **MCP servers/tools** alongside files, folders, conversations,
terminals, and rules — letting you point the agent at a specific tool for a
message.

> The full MCP setup surface (any `agy mcp` management commands, OAuth flows for
> remote servers, transport options) is documented at
> `https://antigravity.google/docs/mcp`. The `mcp_config.json` schema above is
> confirmed from real on-disk configs; verify additional management commands in
> official docs.

---

## See also

- [plugins.md](./plugins.md) — plugins are the usual delivery vehicle for MCP servers
- [agentic-model.md](./agentic-model.md) — how the agent calls tools during execution
- [permissions.md](./permissions.md) — gating what MCP-driven actions may do
