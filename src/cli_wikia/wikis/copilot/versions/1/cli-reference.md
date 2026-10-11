# CLI Reference

Every `copilot` subcommand and command-line flag. For the interactive `/` commands you use *inside* a session, see [slash-commands.md](slash-commands.md).

```
copilot [options] [command]
```

With no command, `copilot` starts an interactive session. With `-p`/`--prompt` it runs once and exits.

---

## Subcommands

| Command | What it does |
|---|---|
| `copilot` | Start interactive session |
| `copilot login [--host <url>]` | Authenticate via OAuth device flow |
| `copilot init` | Scan the repo and write `.github/copilot-instructions.md` |
| `copilot mcp …` | Manage MCP servers (`add`/`get`/`list`/`remove`) — see [mcp.md](mcp.md) |
| `copilot plugin …` | Manage plugins and marketplaces — see [plugins.md](plugins.md) |
| `copilot skill …` | Manage skills (`add`/`list`/`remove`) — see [skills.md](skills.md) |
| `copilot update [prerelease]` | Download the latest version (stable by default) |
| `copilot version` | Show installed version and check for updates |
| `copilot completion <bash\|zsh\|fish>` | Print a shell completion script to stdout |
| `copilot help [topic]` | Built-in help. Topics: `billing`, `commands`, `config`, `environment`, `limits`, `logging`, `monitoring`, `permissions`, `providers` |

The nine `help` topics are genuinely detailed and are the most authoritative offline reference — `copilot help permissions`, `copilot help providers`, etc.

---

## Flags

### Session & prompting

| Flag | Description |
|---|---|
| `-p, --prompt <text>` | Run a prompt non-interactively, then exit |
| `-i, --interactive <prompt>` | Start interactive mode and run this prompt first |
| `--continue` | Resume the most recent session |
| `-r, --resume[=value]` | Resume a session by ID, task ID, ID prefix (7+ hex), or exact name |
| `--connect[=sessionId]` | Connect directly to a remote session/task |
| `--session-id <id>` | Resume by ID, or set the UUID for a new session |
| `-n, --name <name>` | Name the new session |
| `--attachment <path>` | Attach a file (image or document) to the initial prompt (non-interactive only; repeatable) |
| `--enable-memory` | Enable cross-session memory in prompt mode (off by default there) |

### Models, context & reasoning

| Flag | Description |
|---|---|
| `--model <model>` | Model to use, or `auto` to let Copilot pick (env: `COPILOT_MODEL`) |
| `--context <tier>` | Context window tier: `default` or `long_context` |
| `--effort, --reasoning-effort <level>` | `none`, `low`, `medium`, `high`, `xhigh`, `max` |
| `--max-ai-credits <credits>` | Cap AI credits for this session (see `copilot help limits`) |
| `--enable-reasoning-summaries` | Request reasoning summaries for OpenAI models |

See [models.md](models.md) and [providers-byok.md](providers-byok.md).

### Working directory & agents

| Flag | Description |
|---|---|
| `-C <directory>` | Change working directory before doing anything |
| `--add-dir <directory>` | Add a directory to the file-access allowlist (repeatable) |
| `--agent <agent>` | Run a named [custom agent](custom-agents.md) |

### Modes

| Flag | Description |
|---|---|
| `--mode <mode>` | Initial mode: `interactive`, `plan`, `autopilot` |
| `--plan` | Start in plan mode |
| `--autopilot` | Start in autopilot mode |
| `--max-autopilot-continues <count>` | Cap automatic continuation messages in autopilot (default 5) |

See [modes.md](modes.md).

### Permissions

| Flag | Description |
|---|---|
| `--allow-all` / `--yolo` | Enable all permissions (= tools + paths + URLs) |
| `--allow-all-tools` | Auto-run all tools without confirmation; **required for non-interactive mode** (env: `COPILOT_ALLOW_ALL`) |
| `--allow-all-paths` | Disable path verification; allow any path |
| `--allow-all-urls` | Allow all URLs without confirmation |
| `--allow-tool[=…]` / `--deny-tool[=…]` | Approve/forbid tools by pattern (deny wins) |
| `--allow-url[=…]` / `--deny-url[=…]` | Approve/forbid URLs or domains (deny wins) |
| `--available-tools[=…]` | Whitelist the tools the model can see (disables all others) |
| `--excluded-tools[=…]` | Hide specific tools from the model |
| `--disallow-temp-dir` | Don't auto-grant access to the system temp dir |
| `--no-ask-user` | Disable the `ask_user` tool so the agent never pauses to ask |
| `--secret-env-vars[=VARS]` | Env var names to strip from shell/MCP environments and redact from output |

See [permissions.md](permissions.md).

### MCP

| Flag | Description |
|---|---|
| `--additional-mcp-config <json>` | Extra MCP servers as JSON string or `@file` (repeatable; augments `~/.copilot/mcp-config.json` for this session) |
| `--disable-builtin-mcps` | Disable all built-in MCP servers (currently `github-mcp-server`) |
| `--disable-mcp-server <name>` | Disable one MCP server (repeatable) |
| `--enable-all-github-mcp-tools` | Enable the full GitHub MCP toolset instead of the default CLI subset |
| `--allow-all-mcp-server-instructions` | Include initialization instructions from **all** MCP servers in the system prompt (not just allowlisted ones) |
| `--add-github-mcp-toolset <toolset>` | Enable a GitHub MCP toolset (repeatable; `all` for everything) |
| `--add-github-mcp-tool <tool>` | Enable a specific GitHub MCP tool (repeatable; `*` for all) |

See [mcp.md](mcp.md).

### Plugins & instructions

| Flag | Description |
|---|---|
| `--plugin-dir <directory>` | Load a plugin from a local directory (repeatable) |
| `--no-custom-instructions` | Don't load `AGENTS.md` and related instruction files |

### Output, logging & scripting

| Flag | Description |
|---|---|
| `--output-format <text\|json>` | `json` emits JSONL (one object per line) |
| `-s, --silent` | Output only the agent's response (no stats); pairs with `-p` |
| `--share[=path]` | After a non-interactive run, write the session to markdown (default `./copilot-session-<id>.md`) |
| `--share-gist` | After a non-interactive run, write the session to a secret GitHub gist |
| `--log-dir <directory>` | Log directory (default `~/.copilot/logs/`) |
| `--log-level <level>` | `none`, `error`, `warning`, `info`, `debug`, `all`, `default` |
| `--stream <on\|off>` | Toggle streaming output |
| `--plain-diff` | Disable rich diff rendering (env: `PLAIN_DIFF`) |
| `--no-color` | Disable color (env: `NO_COLOR`) |

### Remote control & protocols

| Flag | Description |
|---|---|
| `--remote` / `--no-remote` | Enable/disable remote control from GitHub web and mobile |
| `--remote-export` / `--no-remote-export` | Export the session read-only to web/mobile (no control) |
| `--acp` | Start as an [Agent Client Protocol](https://agentclientprotocol.com) server (for editor integration) |
| `--extension-sdk-path <dir>` | Override the bundled `@github/copilot-sdk` for extension subprocesses |

### Terminal & UX

| Flag | Description |
|---|---|
| `--banner` | Show the startup banner |
| `--mouse` / `--no-mouse` | Mouse support in alt-screen mode (persists to config) |
| `--bash-env` / `--no-bash-env` | Toggle `BASH_ENV` support for bash shells (persists) |
| `--screen-reader` | Screen-reader optimizations |

### Misc

| Flag | Description |
|---|---|
| `--experimental` / `--no-experimental` | Toggle experimental features |
| `--no-auto-update` | Don't auto-download updates (env: `COPILOT_AUTO_UPDATE=false`) |
| `-v, --version` | Print version |
| `-h, --help` | Help for a command |

---

## Common usage

```bash
# One-shot, fully autonomous, scriptable
copilot -p "run the test suite and fix failures" --allow-all-tools --silent

# Allow all git except push
copilot --allow-tool='shell(git:*)' --deny-tool='shell(git push)'

# Allow all but one tool from an MCP server named MyMCP
copilot --deny-tool='MyMCP(denied_tool)' --allow-tool='MyMCP'

# Pick a model and a big context window
copilot --model gpt-5.4 --context long_context

# Plan first, then implement on autopilot
copilot --plan -i "design the migration"

# Resume the last session with auto-approval
copilot --allow-all-tools --resume

# JSONL output for a pipeline
copilot -p "list the dependencies" --output-format json --allow-all-tools

# Start a fresh session at a specific UUID
copilot --session-id=0cb916db-26aa-40f2-86b5-1ba81b225fd2
```

---

## See also

- [slash-commands.md](slash-commands.md) — interactive `/` commands
- [environment-variables.md](environment-variables.md) — env-var equivalents of many flags
- [cli-vs-api.md](cli-vs-api.md) — when to use the CLI vs a programmatic API

---

## Sources

- `copilot --help` and `copilot help` (GitHub Copilot CLI 1.0.68) — full flag/subcommand/topic list. Accessed 2026-07-02.
- [GitHub Copilot CLI docs](https://docs.github.com/copilot/how-tos/copilot-cli) — Accessed 2026-07-02.
