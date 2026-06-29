# Plugins

A plugin is a single installable package that bundles several Copilot extensions at once — custom agents, skills, hooks, MCP servers, and LSP servers — so you can share a whole toolkit with one command.

Reference: [About CLI plugins](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins) and `copilot plugin --help`.

---

## What a plugin can contain

| Component | Where in the plugin |
|---|---|
| Custom agents | `*.agent.md` files in `agents/` |
| Skills | skill subdirectories (each with a `SKILL.md`) in `skills/` |
| Hooks | `hooks.json` in the plugin root, or files in `hooks/` |
| MCP servers | `.mcp.json` in the root, or `.github/mcp.json` |
| LSP servers | `lsp.json` in the root, or in `.github/` |

The only hard requirement is a **`plugin.json` manifest** at the plugin root.

```
my-plugin/
├── plugin.json
├── agents/
├── skills/
├── hooks.json
├── .mcp.json
└── lsp.json
```

---

## Marketplaces

Two marketplaces are registered by default:

| Marketplace | Repo |
|---|---|
| `copilot-plugins` | `github/copilot-plugins` |
| `awesome-copilot` | `github/awesome-copilot` |

Browse one with `copilot plugin marketplace browse <name>`.

---

## Installing plugins

### Imperatively

```bash
copilot plugin install <source>      # source = marketplace plugin, GitHub repo,
                                     # repo subdirectory, or direct git URL
copilot plugin list
copilot plugin update [name]
copilot plugin uninstall <name>
```

Inside a session: `/plugin` (manage), or `/plugin install …`. Load a plugin straight from a local directory without installing it:

```bash
copilot --plugin-dir ./my-plugin
```

### Declaratively

Add entries to `enabledPlugins` in `~/.copilot/settings.json` (personal) or `.github/copilot/settings.json` (repo), so a checkout automatically enables the team's plugins.

---

## Managing marketplaces

```bash
copilot plugin marketplace            # manage marketplaces (browse/add/…)
```

You can register additional marketplaces (the docs reference community ones such as `claude-code-plugins` and `claudeforge-marketplace`), then install plugins from them or directly from any GitHub repository.

---

## See also

- [custom-agents.md](custom-agents.md), [skills.md](skills.md), [mcp.md](mcp.md), [hooks.md](hooks.md) — the components a plugin bundles
- [configuration.md](configuration.md) — `enabledPlugins`
