# Plugins

Plugins are reusable packages that bundle skills, agents, hooks, MCP servers, LSP servers, monitors, themes, and configuration. Distributed via marketplaces (see [marketplaces.md](./marketplaces.md)). One plugin install can wire up everything at once.

---

## Layout

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json            # manifest (optional but usual)
├── skills/                    # /name shortcuts
│   └── code-reviewer/SKILL.md
├── commands/                  # flat .md files (alternative to skills)
│   └── format.md
├── agents/                    # subagents
│   └── reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json                  # MCP servers
├── .lsp.json                  # LSP servers
├── monitors/
│   └── monitors.json          # background watchers
├── output-styles/
│   └── trainer/OUTPUT_STYLE.md
├── themes/
│   └── dracula.json
├── bin/                       # executables added to PATH
├── settings.json              # default settings on enable
└── README.md
```

The manifest is **optional**. If omitted, Claude Code auto-discovers components in default locations and derives the plugin name from the directory name. Use a manifest when you need metadata or custom paths.

---

## `plugin.json` — complete schema

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "themes": "./themes/",
  "lspServers": "./.lsp.json",
  "monitors": "./monitors.json",
  "userConfig": { /* see below */ },
  "channels": [ /* see below */ ],
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Required fields

Only `name` is required if a manifest exists. Used for namespacing — plugin `plugin-dev`'s skill `agent-creator` becomes `/plugin-dev:agent-creator`.

### Metadata fields

| Field | Type | Description |
|---|---|---|
| `version` | string | Semantic version. **Pinning behavior:** if set, users only get updates when bumped. If omitted, falls back to git commit SHA (every commit = new version). If also set in marketplace entry, `plugin.json` wins |
| `description` | string | Brief explanation |
| `author` | object | `{name, email, url}` |
| `homepage` | string | Docs URL |
| `repository` | string | Source code URL |
| `license` | string | `MIT`, `Apache-2.0`, etc. |
| `keywords` | array | Discovery tags |

### Component path fields (string OR array OR inline object)

| Field | Description |
|---|---|
| `skills` | Custom skill directories (replaces default `skills/`) |
| `commands` | Flat `.md` skill files or dirs (replaces default `commands/`) |
| `agents` | Custom agent files (replaces default `agents/`) |
| `hooks` | Hook config paths or inline config |
| `mcpServers` | MCP config paths or inline config |
| `outputStyles` | Custom output-style files/dirs |
| `themes` | Color theme files/dirs |
| `lspServers` | LSP server configs |
| `monitors` | Background monitor configs |
| `userConfig` | User-configurable values (prompted at enable) |
| `channels` | Channel declarations for push messaging |
| `dependencies` | Other plugins this plugin requires (with optional semver) |

---

## Plugin variables

Two important interpolation variables:

- **`${CLAUDE_PLUGIN_ROOT}`** — the plugin's installation directory. Use it in hooks, MCP configs, monitors, anywhere you reference bundled scripts/files. **Changes on plugin update.**
- **`${CLAUDE_PLUGIN_DATA}`** — the plugin's persistent data directory. **Survives plugin updates.** Use this for state, caches, user-supplied tokens.

Other supported substitutions in plugin component configs:
- `${user_config.<name>}` — values from `userConfig` prompts.
- `${ENV_VAR}` — any environment variable.

---

## User configuration

Declare values prompted at enable time:

```json
{
  "userConfig": {
    "api_endpoint": {
      "description": "Endpoint URL for the deployment monitor",
      "default": "https://api.internal.example.com",
      "required": true
    }
  }
}
```

Reference in component configs as `${user_config.api_endpoint}`.

---

## Components in detail

### Skills / commands

Same skills as in [skills.md](./skills.md). They appear as `/plugin-name:skill-name` to avoid collisions.

### Agents

Same agents as in [agents.md](./agents.md). Plugin agents **don't support `hooks`, `mcpServers`, or `permissionMode`** — those fields are ignored. To use them, copy the agent file to `.claude/agents/` or `~/.claude/agents/`.

### Hooks

Standard [hooks.md](./hooks.md) config in `hooks/hooks.json` or inline in `plugin.json`. Active when plugin is enabled.

### MCP servers

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": { "DB_PATH": "${CLAUDE_PLUGIN_DATA}" }
    }
  }
}
```

Start automatically when plugin enabled. Disabled mid-session: run `/reload-plugins`. See [mcp.md](./mcp.md#plugin-bundled-mcp-servers).

### LSP servers (Language Server Protocol)

For real-time code intelligence (diagnostics, go-to-definition, hover):

```json
// .lsp.json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Or inline in `plugin.json` under `lspServers`.

| Field | Required | Description |
|---|---|---|
| `command` | Yes | LSP binary (must be in PATH) |
| `extensionToLanguage` | Yes | `{".ext": "lang-id"}` |
| `args` | No | CLI args |
| `transport` | No | `stdio` (default) or `socket` |
| `env` | No | Env vars |
| `initializationOptions` | No | Server init options |
| `settings` | No | Sent via `workspace/didChangeConfiguration` |
| `workspaceFolder` | No | Workspace folder path |
| `startupTimeout` | No | Max startup ms |
| `shutdownTimeout` | No | Max graceful shutdown ms |
| `restartOnCrash` | No | Auto-restart |
| `maxRestarts` | No | Max restart attempts |

> **Install the language server binary separately.** LSP plugins configure the connection; they don't ship the server. If `/plugin` Errors tab shows `Executable not found in $PATH`, install it.

Available LSP plugins:
- `pyright-lsp` — `pip install pyright` or `npm install -g pyright`
- `typescript-lsp` — `npm install -g typescript-language-server typescript`
- `rust-lsp` — [rust-analyzer](https://rust-analyzer.github.io/manual.html#installation)

### Monitors

Background watchers — see [monitors.md](./monitors.md).

### Themes

```json
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error":  "#ff5555",
    "success":"#50fa7b"
  }
}
```

Selecting a plugin theme persists `custom:<plugin-name>:<slug>` in user config. Plugin themes are read-only — `Ctrl+E` on one in `/theme` copies it to `~/.claude/themes/` so the user can edit the copy.

### Channels

For push-event integration. See [channels.md](./channels.md).

### Output styles

Same as in [output-styles.md](./output-styles.md), but in the plugin's `output-styles/` dir.

---

## Plugin scopes

| Scope | Settings file | Use case |
|---|---|---|
| `user` | `~/.claude/settings.json` | Personal, all your projects (default) |
| `project` | `.claude/settings.json` | Team-shared via git |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | [Managed settings](./settings.md) | Org-deployed (read-only, update only) |

---

## Installing & enabling

```bash
# From a marketplace
claude plugin install code-review@claude-plugins-official
claude plugin enable code-review@claude-plugins-official
claude plugin disable code-review@claude-plugins-official
claude plugin list

# Local directory (for development)
claude --plugin-dir ./my-plugin            # ephemeral, this session

# Marketplace management — see marketplaces.md
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin marketplace update claude-plugins-official
```

In the REPL: `/plugins` → install/enable/disable interactively.

After installing a plugin that ships a configure command, run `/reload-plugins` to activate it.

---

## Enabled plugins setting

```json
// settings.json
{
  "enabledPlugins": {
    "code-review@claude-plugins-official": true,
    "deploy-tools@my-internal-marketplace": true,
    "old-plugin@somewhere": false
  }
}
```

This is the persistent on/off list. Project `enabledPlugins` is loaded from `.claude/settings.json` even when the project is opened via `--add-dir` (one of the few config exceptions).

---

## Dependencies

```json
{
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

Semver constraints supported. See [plugin dependencies docs](https://code.claude.com/docs/en/plugin-dependencies).

---

## Lifecycle

Disabling a plugin **does not stop monitors that are already running** — they keep running until the session ends.

Plugin update changes `${CLAUDE_PLUGIN_ROOT}` (new install dir). `${CLAUDE_PLUGIN_DATA}` survives.

---

## CLI reference

```bash
claude plugin install <plugin@marketplace>
claude plugin enable  <plugin@marketplace>
claude plugin disable <plugin@marketplace>
claude plugin list
claude plugin search <keyword>
claude plugin marketplace add <source>
claude plugin marketplace update <name>
claude plugin marketplace remove <name>
```

---

## See also

- [marketplaces.md](./marketplaces.md) — how to discover and ship plugins
- [skills.md](./skills.md), [agents.md](./agents.md), [hooks.md](./hooks.md), [mcp.md](./mcp.md), [monitors.md](./monitors.md) — components in detail
- [stacking.md](./stacking.md) — how plugins compose all of these
- [settings.md](./settings.md) — `enabledPlugins`, `extraKnownMarketplaces`, `pluginTrustMessage`, `strictKnownMarketplaces`, `blockedMarketplaces`
