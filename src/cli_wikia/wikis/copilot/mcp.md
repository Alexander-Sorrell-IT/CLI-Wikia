# MCP Servers (GitHub Copilot CLI)

GitHub Copilot CLI can connect to
[Model Context Protocol](https://modelcontextprotocol.io) servers, which expose
external tools and data to the model. It also ships with built-in MCP servers.

## The mcp command

```bash
copilot mcp
```

Manages MCP servers.

> The top-level `--help` lists `copilot mcp` as the entry point for managing
> MCP servers but does not enumerate its individual subcommands. Run
> `copilot mcp --help` for the available subcommands.

## Configuration file

MCP servers are configured in:

```
~/.copilot/mcp-config.json
```

## Built-in MCP servers

Copilot includes built-in MCP servers (currently `github-mcp-server`).

| Flag | Description |
|------|-------------|
| `--disable-builtin-mcps` | Disable built-in MCP servers (currently: `github-mcp-server`) |
| `--disable-mcp-server <name>` | Disable a specific MCP server |

```bash
# Disable all built-in MCP servers
copilot --disable-builtin-mcps

# Disable one specific server
copilot --disable-mcp-server github-mcp-server
```

## Related

- See [configuration.md](configuration.md) for config paths.
- See [cli-reference.md](cli-reference.md) for the full flag list.

> Verify exact values in the official docs / run `copilot mcp --help`.
