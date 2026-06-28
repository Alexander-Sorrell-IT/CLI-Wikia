# MCP Servers (Gemini CLI)

Gemini CLI can connect to [Model Context Protocol](https://modelcontextprotocol.io)
servers, which expose external tools and data to the model. Manage them with
the `gemini mcp` command.

## Subcommands

| Command | Description |
|---------|-------------|
| `gemini mcp add <name> <commandOrUrl> [args...]` | Add a server |
| `gemini mcp remove <name>` | Remove a server |
| `gemini mcp list` | List all configured MCP servers |

## Examples

```bash
# Add a server launched from a local command (with args)
gemini mcp add my-server npx -y @example/mcp-server

# Add a server by URL
gemini mcp add my-remote https://mcp.example.com

# List configured servers
gemini mcp list

# Remove a server
gemini mcp remove my-server
```

## Restricting MCP servers at launch

Limit which MCP servers a session may use:

```bash
gemini --allowed-mcp-server-names server-a,server-b "do the task"
```

| Flag | Description |
|------|-------------|
| `--allowed-mcp-server-names` | Allowed MCP server names (array) |

## Related

- `--allowed-tools` — tools allowed to run without confirmation.
- See [cli-reference.md](cli-reference.md) for the full flag list.

> Verify exact values in the official docs / run `gemini mcp --help`.
