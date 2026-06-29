# Subagents (Gemini CLI)

> 🔬 **Experimental.** Subagents are enabled by default but ship under
> `experimental` settings and may change. Set
> `{"experimental": {"enableAgents": false}}` in `settings.json` to disable
> them.

Subagents are specialized agents that run inside your main Gemini CLI session.
The main agent can "hire" a specialist to handle a focused, complex task — deep
codebase analysis, documentation lookup, browser automation, domain reasoning —
without cluttering the main conversation's context or toolset.

Each subagent has:

- **Its own system prompt and persona** (the body of the agent definition file).
- **A specialized, optionally restricted tool set.**
- **An independent context window** — the subagent's history runs in a separate
  loop, so it doesn't bloat the main conversation.

A subagent is exposed to the main agent as a **tool of the same name**. When the
main agent calls that tool, it delegates the task; when the subagent finishes,
it reports its findings back to the main agent.

## How the model delegates

### Automatic delegation

The main agent's system prompt instructs it to call a specialized subagent when
a task matches that agent's expertise. Ask "How does the auth system work?" and
the main agent may call `codebase_investigator` to do the research. It decides
based on each agent's `description`, so a clear, specific description improves
how reliably an agent is chosen.

### Forcing a subagent (`@` syntax)

Direct a task to a specific subagent by starting your prompt with `@` followed
by the agent name. This bypasses the main agent's decision-making:

```bash
@codebase_investigator Map out the relationship between the AgentRegistry and the LocalAgentExecutor.
```

The CLI injects a system note nudging the model to use that subagent tool
immediately.

## Where agents live

Custom agents are Markdown files with YAML frontmatter, loaded from two
locations:

| Scope | Path | Notes |
| :---- | :--- | :---- |
| Project | `.gemini/agents/*.md` | Shared with your team (commit to the repo). |
| User | `~/.gemini/agents/*.md` | Personal agents. |

Agents can also be **bundled in extensions** (see the Extensions docs).

## Built-in subagents

| Name | Purpose | Default |
| :--- | :------ | :------ |
| `codebase_investigator` | Analyze the codebase, reverse-engineer, and understand complex dependencies. | Enabled |
| `cli_help` | Expert knowledge about Gemini CLI itself — commands, configuration, docs. | Enabled |
| `generalist` | All-purpose agent that inherits the main agent's tools and config; ideal for multi-file edits, high-volume execution, and action-oriented research in an isolated context. | Enabled |
| `browser_agent` | Automate web tasks (navigate, fill forms, click, extract) via the accessibility tree. | **Disabled** |

> 💡 Use `@cli_help` inside Gemini CLI for help configuring subagents.

Override a built-in agent's settings under `agents.overrides` in `settings.json`
— for example, force a model and raise the turn limit:

```json
{
  "agents": {
    "overrides": {
      "codebase_investigator": {
        "modelConfig": { "model": "gemini-3-flash-preview" },
        "runConfig": { "maxTurns": 50 }
      }
    }
  }
}
```

### Enabling the browser agent

The browser agent is disabled by default and requires **Chrome 144+** (the
bundled `chrome-devtools-mcp` server launches automatically). Enable it and
optionally set a session mode:

```json
{
  "agents": {
    "overrides": {
      "browser_agent": { "enabled": true }
    },
    "browser": {
      "sessionMode": "persistent"
    }
  }
}
```

Session modes (`agents.browser.sessionMode`): `persistent` (default, profile at
`~/.gemini/cli-browser-profile/`), `isolated` (temp profile, deleted after each
session), `existing` (attach to a running Chrome with remote debugging). A
first-run consent dialog appears once. The agent ships with security controls
(`allowedDomains`, blocked URL schemes, sensitive-action confirmation,
`blockFileUploads`, `maxActionsPerTask`) and an optional `visualModel` for
coordinate-based interaction. See the `agents.browser` configuration reference
for the full option list (verify in official docs).

## Creating custom subagents

### File format

A definition file **must** start with YAML frontmatter between triple-dashes
(`---`). The Markdown body becomes the agent's **system prompt**.

```markdown
---
name: security-auditor
description: Specialized in finding security vulnerabilities in code.
kind: local
tools:
  - read_file
  - grep_search
model: gemini-3-flash-preview
temperature: 0.2
max_turns: 10
---

You are a ruthless Security Auditor. Your job is to analyze code for potential
vulnerabilities.

Focus on:

1. SQL Injection
2. XSS (Cross-Site Scripting)
3. Hardcoded credentials
4. Unsafe file operations

When you find a vulnerability, explain it clearly and suggest a fix. Do not fix
it yourself; just report it.
```

### Frontmatter schema (local agents)

| Field | Type | Required | Description |
| :---- | :--- | :------- | :---------- |
| `name` | string | Yes | Unique slug used as the agent's tool name. Lowercase letters, numbers, hyphens, underscores only. |
| `description` | string | Yes | Short description shown to the main agent so it can decide when to call this subagent. |
| `kind` | string | No | `local` (default) or `remote`. |
| `tools` | array | No | Tool names this agent may use. Supports wildcards. **If omitted, inherits all tools from the parent session.** |
| `mcpServers` | object | No | Inline MCP servers isolated to this agent. |
| `model` | string | No | Model to use (e.g. `gemini-3-preview`). Defaults to `inherit` (main session model). |
| `temperature` | number | No | Model temperature, `0.0`–`2.0`. Default `1`. |
| `max_turns` | number | No | Max conversation turns before the agent must return. Default `30`. |
| `timeout_mins` | number | No | Max execution time in minutes. Default `10`. |

### Tool wildcards

In the `tools` list you can grant groups of tools at once:

- `*` — all built-in and discovered tools.
- `mcp_*` — all tools from all connected MCP servers.
- `mcp_my-server_*` — all tools from the MCP server named `my-server`.

### Isolation and recursion protection

Each subagent runs in its own isolated context loop:

- **Independent history** — does not bloat the main agent's context.
- **Isolated tools** — only the tools you grant (and any inline `mcpServers`).
- **Recursion protection** — subagents **cannot call other subagents**. Even
  with the `*` wildcard, a subagent can't see or invoke other agents.

### Inline (isolated) MCP servers

Add an `mcpServers` object to give an agent its own MCP servers, scoped to that
agent only:

```yaml
---
name: my-isolated-agent
tools:
  - grep_search
  - read_file
mcpServers:
  my-custom-server:
    command: 'node'
    args: ['path/to/server.js']
---
```

### Subagent-specific policies

The Policy Engine can grant or restrict permissions per agent. Add a `subagent`
property to a `[[rules]]` block so the rule only triggers for that agent:

```toml
[[rules]]
name = "Allow pr-creator to push code"
subagent = "pr-creator"
description = "Permit pr-creator to push branches automatically."
action = "allow"
toolName = "run_shell_command"
commandPrefix = "git push"
```

Rules without a `subagent` property apply to all agents. Subagents are also
treated as virtual tool names for policy matching — you can `deny` a whole agent:

```toml
[[rule]]
toolName = "codebase_investigator"
decision = "deny"
deny_message = "Deep codebase analysis is restricted for this session."
```

## Managing subagents (`/agents`)

Use the `/agents` slash command in an interactive session to manage agents
without editing files. (See the `/agents` command reference for full usage.)

| Command | Action |
| :------ | :----- |
| `/agents list` | List all available local and remote subagents. |
| `/agents reload` | Reload the agent registry after adding or editing definition files. |
| `/agents enable <name>` | Enable a specific subagent. |
| `/agents disable <name>` | Disable a specific subagent. |

The docs also reference `/agents` config; consult the command reference for the
exact sub-command set (verify in official docs).

## Persistent configuration (`settings.json`)

For global, persistent overrides — enforcing models or execution limits across
all sessions — use `settings.json` rather than the interactive command.

### `agents.overrides`

Enable/disable an agent or override its run configuration:

```json
{
  "agents": {
    "overrides": {
      "security-auditor": {
        "enabled": false,
        "runConfig": {
          "maxTurns": 20,
          "maxTimeMinutes": 10
        }
      }
    }
  }
}
```

### `modelConfigs.overrides`

Target a specific subagent with custom model settings using `overrideScope`:

```json
{
  "modelConfigs": {
    "overrides": [
      {
        "match": { "overrideScope": "security-auditor" },
        "modelConfig": {
          "generateContentConfig": { "temperature": 0.1 }
        }
      }
    ]
  }
}
```

### Disabling all subagents

```json
{
  "experimental": { "enableAgents": false }
}
```

## Remote subagents (Agent2Agent / A2A)

Gemini CLI can delegate to **remote** agents over the Agent-to-Agent (A2A)
protocol. It connects to any compliant A2A agent. Remote agents are defined in
the same `.gemini/agents/*.md` locations, with `kind: remote`.

Traffic to remote agents is routed through an HTTP/HTTPS proxy if configured via
`general.proxy` in `settings.json` or the `HTTP_PROXY` / `HTTPS_PROXY`
environment variables.

### Remote frontmatter schema

| Field | Type | Required | Description |
| :---- | :--- | :------- | :---------- |
| `kind` | string | Yes | Must be `remote`. |
| `name` | string | Yes | Unique slug (lowercase letters, numbers, hyphens, underscores). |
| `agent_card_url` | string | Yes\* | URL of the agent's A2A card endpoint. Required if `agent_card_json` is absent. |
| `agent_card_json` | string | Yes\* | Inline JSON string of the A2A card. Required if `agent_card_url` is absent. |
| `auth` | object | No | Authentication configuration (see below). |

```markdown
---
kind: remote
name: my-remote-agent
agent_card_url: https://example.com/agent-card
---
```

A single file may define **multiple remote agents** as a YAML list. Mixed
local/remote agents, or multiple local agents, in one file are **not** supported
— the list format is remote-only.

```markdown
---
- kind: remote
  name: remote-1
  agent_card_url: https://example.com/1
- kind: remote
  name: remote-2
  agent_card_url: https://example.com/2
---
```

When you don't have a card endpoint, supply the card inline via
`agent_card_json`. In YAML, a literal block scalar (`|`) is recommended for
multiline JSON because it avoids quote escaping.

### Authentication

Add an `auth` block to the agent's frontmatter. Supported types align with the
A2A security specification:

| Type | Description |
| :--- | :---------- |
| `apiKey` | Send a static API key as an HTTP header (default header `X-API-Key`). |
| `http` | HTTP auth — `Bearer` token, `Basic` credentials, or any IANA-registered scheme. |
| `google-credentials` | Google Application Default Credentials (ADC). Auto-selects access vs identity tokens. |
| `oauth` | OAuth 2.0 Authorization Code flow with PKCE; opens a browser for sign-in. |

**Dynamic secret values** — for `apiKey` and `http`, the secret fields (`key`,
`token`, `username`, `password`, `value`) support:

| Format | Description | Example |
| :----- | :---------- | :------ |
| `$ENV_VAR` | Read from an environment variable. | `$MY_API_KEY` |
| `!command` | Run a shell command, use trimmed output. | `!gcloud auth print-token` |
| literal | Use the string as-is. | `sk-abc123` |
| `$$` / `!!` | Escape prefix — `$$FOO` becomes literal `$FOO`. | `$$NOT_AN_ENV_VAR` |

> **Security tip:** Prefer `$ENV_VAR` or `!command` over embedding secrets in
> project-level agent files that are checked into version control.

API key example:

```yaml
---
kind: remote
name: my-agent
agent_card_url: https://example.com/agent-card
auth:
  type: apiKey
  key: $MY_API_KEY
---
```

HTTP Bearer example:

```yaml
auth:
  type: http
  scheme: Bearer
  token: $MY_BEARER_TOKEN
```

Google ADC example (Cloud Run):

```yaml
---
kind: remote
name: cloud-run-agent
agent_card_url: https://my-agent-xyz.run.app/.well-known/agent.json
auth:
  type: google-credentials
---
```

`google-credentials` notes:

- Token type is chosen by host: `*.googleapis.com` → **access token**,
  `*.run.app` → **identity token**. Both are cached and auto-refreshed.
- Tokens are only sent to allowed Google-owned hosts (`*.googleapis.com`,
  `*.run.app`); any other host is rejected. Set up ADC with
  `gcloud auth application-default login` (local) or
  `GOOGLE_APPLICATION_CREDENTIALS` / workload identity (CI/cloud).
- Treated as compatible with `http` Bearer security schemes.

OAuth notes: provide `client_id` (and `client_secret` for confidential
clients); `authorization_url`, `token_url`, and `scopes` are discovered from the
agent card when omitted. Tokens persist to disk and refresh automatically.

### Auth behavior

- **Validation:** On load, the CLI validates your `auth` against the agent
  card's declared `securitySchemes` and errors if required auth is missing.
- **Retry:** All providers retry on `401`/`403` by re-fetching credentials (up
  to 2 retries); `apiKey` `!command` values are re-executed for a fresh key.
- **Card fetching:** The agent card is fetched **without** auth first; on
  `401`/`403` it's retried **with** auth. Cards can be public while task
  endpoints stay protected.

## See also

- [commands.md](./commands.md) — the `/agents` slash command and others.
- [mcp.md](./mcp.md) — MCP servers (inline and global).
- [permissions.md](./permissions.md) — the Policy Engine and per-subagent rules.
- [settings.md](./settings.md) — `agents`, `modelConfigs`, and `experimental`.
- [skills.md](./skills.md) — related extensibility features.
