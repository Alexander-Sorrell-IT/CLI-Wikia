# Codex Configuration — `config.toml`

Codex is configured with TOML. This page covers the keys documented in OpenAI's [Configuration Reference](https://developers.openai.com/codex/config-reference), [Config basics](https://developers.openai.com/codex/config-basic), and [Advanced configuration](https://developers.openai.com/codex/config-advanced).

> **Not locally verified** — sourced from official docs; Codex isn't installed here. Re-check key names with `codex doctor` / `/debug-config` after installing. The full official sample `config.toml` spans 1,100+ lines; this is the load-bearing subset.

---

## File locations & precedence

| Scope | Path |
|---|---|
| User (personal defaults) | `~/.codex/config.toml` |
| Project | `.codex/config.toml` in the repo (closest to cwd wins) |
| System | `/etc/codex/config.toml` (Unix) |
| Profiles | named profile files activated with `--profile` |

`CODEX_HOME` overrides the `~/.codex` location (config, auth, history, instructions).

**Resolution order (highest priority first):**

1. CLI flags and `-c key=value` / `--config` overrides
2. Project config (`.codex/config.toml`, nearest directory wins)
3. Profile selected with `--profile`
4. User config (`~/.codex/config.toml`)
5. System config (`/etc/codex/config.toml`)
6. Built-in defaults

> Project-scoped config **cannot** override machine-local provider, auth, notification, or telemetry settings — those only come from user/system config.

You can override any key for a single run without editing the file:

```bash
codex -c model="gpt-5.5" -c model_reasoning_effort="xhigh" -c sandbox_mode="read-only"
```

---

## Model settings

| Key | Values | Meaning |
|---|---|---|
| `model` | model id (e.g. `gpt-5.5`) | Active model — see [codex-models.md](./codex-models.md) |
| `model_reasoning_effort` | `minimal` \| `low` \| `medium` \| `high` \| `xhigh` | Reasoning depth (`none` also accepted on some models) |
| `model_reasoning_summary` | `auto` \| `concise` \| `detailed` \| `none` | How much of the reasoning summary to show |
| `model_verbosity` | `low` \| `medium` \| `high` | Output verbosity (GPT-5 Responses API) |
| `model_provider` | provider id | Which provider from `[model_providers]` to use (default `openai`) |
| `model_context_window` | integer | Override the context-window token count |
| `model_auto_compact_token_limit` | integer | Token threshold that triggers automatic history compaction |
| `model_catalog_json` | path | Custom model-catalog file |

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
model_reasoning_summary = "auto"
```

---

## Approval & sandbox

Full explanation in [codex-approvals-sandbox.md](./codex-approvals-sandbox.md).

| Key | Values | Meaning |
|---|---|---|
| `approval_policy` | `untrusted` \| `on-request` \| `never` \| `{ granular = {…} }` | When Codex must ask before acting |
| `sandbox_mode` | `read-only` \| `workspace-write` \| `danger-full-access` | What Codex can technically do |
| `sandbox_workspace_write.network_access` | bool | Allow outbound network in workspace-write |
| `sandbox_workspace_write.writable_roots` | array of paths | Extra directories writable beyond the workspace |
| `default_permissions` | `:read-only` \| `:workspace` \| `:danger-full-access` | Named permissions preset |
| `approvals_reviewer` | `auto_review` (etc.) | Route eligible approvals through an automatic reviewer agent |
| `web_search` | `cached` (default) \| `live` \| `disabled` | Web-search behavior |

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/tmp/codex-build"]
```

### Granular approval policy

```toml
approval_policy = { granular = {
  sandbox_approval    = true,
  rules               = true,
  mcp_elicitations    = true,
  request_permissions = false,
  skill_approval      = false
} }
```

---

## Authentication & providers

| Key | Values | Meaning |
|---|---|---|
| `cli_auth_credentials_store` | `file` \| `keyring` \| `auto` | Where cached credentials live |
| `forced_login_method` | `chatgpt` \| `api` | Restrict the allowed sign-in method |
| `openai_base_url` | url | Redirect the built-in OpenAI provider |
| `chatgpt_base_url` | url | Override the ChatGPT login base URL |

### Custom model providers

```toml
model = "gpt-5.4"
model_provider = "proxy"

[model_providers.proxy]
name = "OpenAI via LLM proxy"
base_url = "http://proxy.example.com"
env_key = "OPENAI_API_KEY"
wire_api = "responses"            # protocol; "responses" for OpenAI
requires_openai_auth = true       # bool

[model_providers.mistral]
name = "Mistral"
base_url = "https://api.mistral.ai/v1"
env_key = "MISTRAL_API_KEY"

# command-backed token auth
[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

Provider keys: `base_url`, `env_key`, `http_headers`, `requires_openai_auth`, `wire_api`.

---

## MCP servers

A short form lives here; the full transport reference (stdio vs streamable HTTP, all keys, `codex mcp add`) is in [codex-mcp.md](./codex-mcp.md).

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
```

---

## Shell environment policy

Controls which environment variables are passed to spawned subprocesses.

| Key | Values | Meaning |
|---|---|---|
| `inherit` | `all` \| `core` \| `none` | Baseline set to start from |
| `include_only` | array of patterns | Whitelist of variable names |
| `exclude` | array of patterns | Variables to strip (e.g. `AWS_*`) |
| `set` | map | Explicit overrides |
| `allow_login_shell` | bool (default `true`) | Run commands via a login shell |

```toml
[shell_environment_policy]
inherit = "core"
exclude = ["AWS_*", "AZURE_*"]
set = { CI = "1" }
```

---

## History & output

| Key | Values | Meaning |
|---|---|---|
| `history.persistence` | `save-all` \| `none` | Whether transcripts are saved under `CODEX_HOME` |
| `history.max_bytes` | integer | Cap on the history file size |
| `file_opener` | `vscode` \| `vscode-insiders` \| `windsurf` \| `cursor` \| `none` | Make file citations clickable in that editor |
| `hide_agent_reasoning` | bool | Suppress reasoning events in output |
| `tool_output_token_limit` | integer | Token budget for tool outputs |

```toml
[history]
persistence = "save-all"
max_bytes = 104857600   # 100 MiB
```

---

## AGENTS.md tuning

| Key | Default | Meaning |
|---|---|---|
| `project_doc_max_bytes` | `32768` (32 KiB) | Max combined size of loaded `AGENTS.md` content |
| `project_doc_fallback_filenames` | `[]` | Extra filenames to treat as instructions (e.g. `TEAM_GUIDE.md`, `.agents.md`) |
| `project_root_markers` | — | Customize how the project root is detected |

```toml
project_doc_max_bytes = 65536
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
```

See [codex-agents-md.md](./codex-agents-md.md).

---

## Feature flags

Toggle capabilities under `[features]` (or with `codex features` / `--enable`/`--disable`).

| Key | Meaning |
|---|---|
| `features.multi_agent` | Enable agent-collaboration / subagent tools |
| `features.memories` | Enable the memory system |
| `features.hooks` | Enable lifecycle hooks |
| `features.network_proxy` | Bool or table with domain/socket policies |
| `features.unified_exec` | PTY-backed exec tool (on by default except Windows) |
| `features.shell_snapshot` | Shell snapshotting |

---

## Profiles

A **profile** is a named bundle of settings you can switch into with `--profile`. Define profiles as separate config files (or `[profiles.<name>]` tables — verify which your build uses).

```toml
# ~/.codex/deep-review.config.toml
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
model_catalog_json = "/Users/me/.codex/model-catalogs/deep-review.json"
```

```bash
codex --profile deep-review
```

Profiles layer **above** user config but **below** project config and CLI flags, so a profile only needs the keys that differ from your defaults.

---

## Notifications

Run an external program on Codex events; it receives one JSON argument with fields like `type`, `thread-id`, `input-messages`, `last-assistant-message`.

```toml
notify = ["python3", "/path/to/notify.py"]
```

---

## Projects & trust

```toml
[projects."/Users/me/work/api"]
trust_level = "trusted"     # "trusted" | "untrusted"
```

Trusting a project relaxes first-run prompts for that directory.

---

## TUI

The `[tui]` table controls notifications, animations, alternate-screen behavior, status-line fields, and key bindings. (See `/statusline`, `/keymap`, `/theme` in [codex-slash-commands.md](./codex-slash-commands.md).)

---

## See also

- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — the safety model in depth
- [codex-models.md](./codex-models.md) — model ids & reasoning effort
- [codex-mcp.md](./codex-mcp.md) — full MCP transport keys
- [codex-agents-md.md](./codex-agents-md.md) — `AGENTS.md` discovery & merging
- [codex-cli-reference.md](./codex-cli-reference.md) — flags that override these keys
