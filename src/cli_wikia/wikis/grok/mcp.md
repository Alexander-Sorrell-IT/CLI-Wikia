# MCP Servers

`@vibe-kit/grok-cli` 0.0.34 has first-class MCP (Model Context Protocol) support via the
`@modelcontextprotocol/sdk`. Configuration is **project-only**: servers live in
`.grok/settings.json` under `mcpServers`, and `loadMCPConfig()` reads only project
settings (`dist/mcp/config.js:5-10`). There is **no global MCP config** — nothing
MCP-related is read from `~/.grok/user-settings.json`.

## Configuration shape

`.grok/settings.json`, keyed by server name:

```json
{
  "model": "grok-code-fast-1",
  "mcpServers": {
    "filesystem": {
      "name": "filesystem",
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": {}
    },
    "linear": {
      "name": "linear",
      "transport": "sse",
      "url": "https://mcp.linear.app/sse",
      "headers": {}
    }
  }
}
```

| Field | Applies to | Description |
|-------|-----------|-------------|
| `name` | all | Server name (matches the object key) |
| `transport` | all | `stdio`, `http`, `sse`, or `streamable_http` |
| `command` | stdio | Executable to spawn |
| `args` | stdio | Arguments for the command |
| `env` | stdio | Extra environment variables for the spawned process |
| `url` | http/sse/streamable_http | Server endpoint URL |
| `headers` | http/sse/streamable_http | HTTP headers (e.g. auth) |

## Transports

All four are dispatched in `createTransport()` (`dist/mcp/transports.js:215-224`):
`stdio`, `http`, `sse`, `streamable_http`.

## CLI management

Verified via `grok mcp --help` and `grok mcp add --help` (these commands only edit
`.grok/settings.json` / talk to the server — they do not call the paid model API):

| Command | What it does |
|---------|--------------|
| `grok mcp add <name> [options]` | Add a server (`-t` transport, `-c` command, `-a` args, `-u` url, `-h` headers `key=value`, `-e` env `key=value`) |
| `grok mcp add-json <name> '<json>'` | Add a server from a JSON blob |
| `grok mcp remove <name>` | Remove a server |
| `grok mcp list` | List configured servers |
| `grok mcp test <name>` | Test the connection to a server |

```bash
# stdio server
grok mcp add filesystem -t stdio -c npx -a -y @modelcontextprotocol/server-filesystem /tmp

# SSE server (Linear example from the npm README)
grok mcp add linear --transport sse --url "https://mcp.linear.app/sse"

# JSON form
grok mcp add-json linear '{"transport":"sse","url":"https://mcp.linear.app/sse"}'

grok mcp list
grok mcp test linear
grok mcp remove filesystem
```

`grok mcp add` defaults: `--transport stdio`, empty `args`/`headers`/`env`.

## Runtime behavior

- **Lazy background init:** servers connect asynchronously when the agent is constructed
  (`dist/agent/grok-agent.js:108-124`) — startup isn't blocked; a slow server's tools
  simply appear once it connects.
- Connected servers' tools are **appended to the model's tool list under their own
  names** (`addMCPToolsToGrokTools`, `dist/grok/tools.js:333-340`), alongside the
  built-in tools.
- **Debugging:** set `MCP_DEBUG=1` to un-suppress connection logs
  (`dist/mcp/mcp-protocol-client.js:16-17`). Suppression only applies in interactive
  mode anyway; in headless `-p` mode connection logs already go to stderr (see
  [headless.md](headless.md)).
- Since `.grok/settings.json` is per-project, MCP servers follow the working directory —
  with `grok -d <dir>`, the target directory's `.grok/settings.json` is what counts.

## Sources

Verified 2026-07-23 against the installed package (source inspection and help output
only — no model API calls):

- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/mcp/config.js`
  — `loadMCPConfig()` lines 5-10 (project-settings-only).
- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/mcp/transports.js`
  — transport dispatch lines 215-224.
- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/mcp/mcp-protocol-client.js`
  — `MCP_DEBUG` / quiet-mode logic lines 16-17.
- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/agent/grok-agent.js`
  lines 108-124 (lazy background init) and
  `.../dist/grok/tools.js` lines 333-340 (MCP tools appended).
- `grok mcp --help` and `grok mcp add --help` (2026-07-23) — subcommands, option
  spellings, and defaults reproduced verbatim.
- npm README for @vibe-kit/grok-cli 0.0.34 (via npm registry API, 2026-07-23) — the
  Linear SSE example.
