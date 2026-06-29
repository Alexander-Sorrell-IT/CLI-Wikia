# Codex & MCP (Model Context Protocol)

MCP lets Codex use third-party tools and context sources — and lets Codex itself be used as a tool by other agents. From OpenAI's [MCP](https://developers.openai.com/codex/mcp) docs.

> **Not locally verified** — sourced from official docs; Codex isn't installed here. Confirm key names with `codex mcp --help` and `/mcp` after installing.

---

## Adding a server — two ways

### 1. CLI

```bash
# generic form
codex mcp add <name> [--env VAR=VALUE ...] -- <stdio-command> [args...]

# example: Context7 docs server
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

Related: `codex mcp list`, `codex mcp remove <name>` (verify exact subcommand names with `codex mcp --help`). In the TUI, `/mcp` lists configured servers and their tools.

### 2. config.toml

Add `[mcp_servers.<name>]` tables to `~/.codex/config.toml` (or project `.codex/config.toml`) for granular control.

---

## STDIO servers (local process)

| Key | Required | Meaning |
|---|---|---|
| `command` | ✓ | Executable that launches the server |
| `args` | | Argument array |
| `env` | | Static environment variables (table) |
| `env_vars` | | Variable names to forward from Codex's own environment |
| `cwd` | | Working directory for the process |
| `experimental_environment` | | `remote` for remote-executor environments |

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
env_vars = ["LOCAL_TOKEN"]

[mcp_servers.context7.env]
MY_ENV_VAR = "MY_ENV_VALUE"
```

---

## Streamable HTTP servers (network)

| Key | Required | Meaning |
|---|---|---|
| `url` | ✓ | Server endpoint |
| `bearer_token_env_var` | | Env var holding a bearer token |
| `http_headers` | | Static headers (table) |
| `env_http_headers` | | Headers sourced from env vars |

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
```

---

## Options for any server

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Disable without deleting the entry |
| `required` | `false` | Fail Codex startup if this server doesn't initialize |
| `startup_timeout_sec` | `10` | Server initialization timeout |
| `tool_timeout_sec` | `60` | Per-tool execution timeout |
| `enabled_tools` | all | Allow-list of tool names |
| `disabled_tools` | none | Deny-list of tool names |
| `default_tools_approval_mode` | — | `auto` \| `prompt` \| `approve` |

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
startup_timeout_sec = 20
tool_timeout_sec = 45
```

---

## Codex as an MCP server

Run Codex itself as an MCP server so other agents/tools can invoke it:

```bash
codex mcp-server
```

(Exact invocation may also appear as `codex mcp serve` — verify with `codex mcp --help`.)

---

## Approvals & MCP

MCP tool calls participate in Codex's [approval policy](./codex-approvals-sandbox.md). The granular policy's `mcp_elicitations` toggle and each server's `default_tools_approval_mode` control whether MCP prompts interrupt you.

---

## See also

- [codex-config.md](./codex-config.md) — where `[mcp_servers]` lives in the config layering
- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — how MCP calls are gated
- [codex-slash-commands.md](./codex-slash-commands.md) — `/mcp`
