# muse MCP

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse mcp --help` + settings observation + schema.

## Servers

`muse mcp login|logout <server>` (OAuth), plus add/remove/list/reconnect
via config. `settings.json` `mcpServers` entries are streamable-HTTP
(`SessionMcpServerConfig` is a CLOSED union — unknown transports fail
`session/start` decode). Plugin family `mcpServers` supports local stdio
(`command: [argv...]`). `--mcp-config` supplies session servers at launch.

## Session surface

`McpToolInfo`, `McpToolScope` (schema) describe tool exposure;
`CapabilityName` grants include `sessionMcp`, `sessionListStream`,
`userShell`, `feedback`. MCP tools execute under the same approval gates
as native tools.
