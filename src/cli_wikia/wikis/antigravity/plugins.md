# Plugins

A **plugin** is a distributable bundle of agent extensions — it can package
[skills](./customization.md), [MCP servers](./mcp.md), rules, and hooks together
so they can be installed, enabled, and shared as a unit. Antigravity's plugin
model is inherited from the Gemini CLI, and Antigravity can **import plugins
directly from both the Gemini CLI and Claude**, which is the main migration path
onto the platform.

```bash
agy plugin <command> [arguments]
# `agy plugins` is an alias for `agy plugin`
```

---

## Commands

| Command | Description |
|---------|-------------|
| `agy plugin list` | List imported/installed plugins |
| `agy plugin import [source]` | Import plugins from `gemini` or `claude` |
| `agy plugin install <target>` | Install a plugin (supports `plugin@marketplace`) |
| `agy plugin uninstall <name>` | Uninstall a plugin |
| `agy plugin enable <name>` | Enable a plugin |
| `agy plugin disable <name>` | Disable a plugin |
| `agy plugin validate [path]` | Validate a plugin's schema/structure |
| `agy plugin link <mp> <target>` | Generate a link to a marketplace |
| `agy plugin help` | Show plugin help |

---

## Importing from Gemini CLI / Claude

This is the headline migration feature:

```bash
agy plugin import gemini     # bring over your Gemini CLI plugins
agy plugin import claude     # bring over your Claude plugins
agy plugin list              # confirm what was imported
```

Importing stages the source tool's plugins into Antigravity's plugin directory so
their skills and MCP servers become available to `agy`.

---

## Installing from a marketplace

```bash
agy plugin install some-plugin@some-marketplace
agy plugin enable some-plugin
```

`agy plugin link <marketplace> <target>` generates a shareable marketplace link.
`enable` / `disable` toggle a plugin without uninstalling it.

---

## Plugin structure on disk

Plugins live under **`~/.gemini/antigravity-cli/plugins/<name>/`**. A real
installed plugin is minimal — a manifest plus whatever components it ships:

```
plugins/
├── github/
│   ├── plugin.json          # { "name": "github" }
│   └── mcp_config.json      # MCP server(s) this plugin provides
├── gemini-cli-security/
│   ├── plugin.json
│   ├── mcp_config.json
│   └── skills/
│       ├── analyze/SKILL.md
│       └── analyze-github-pr/SKILL.md
└── conductor/
    ├── plugin.json
    └── skills/ ...
```

`plugin.json` is the manifest (at minimum a `name`). A plugin can bundle:

| Component | File(s) | Doc |
|-----------|---------|-----|
| **Skills** | `skills/<name>/SKILL.md` | [customization.md](./customization.md) |
| **MCP servers** | `mcp_config.json` | [mcp.md](./mcp.md) |
| **Rules / hooks** | per official plugin spec | [customization.md](./customization.md), [hooks.md](./hooks.md) |

Example: the bundled `github` plugin ships only an MCP server pointing at the
GitHub MCP endpoint; the `gemini-cli-security` plugin ships two security-audit
skills plus an MCP server.

> The full `plugin.json` schema (version, components, metadata) is documented at
> `https://antigravity.google/docs/plugins`. On-disk examples here confirm the
> directory layout and that the manifest carries at least `name`; verify the
> complete schema in official docs.

---

## Where plugins come from

Plugins seen pre-staged on this machine include `github`, `code-review`,
`conductor`, `context7`, `terraform`, `cloudbase-ai-toolkit`, `FileSearch`,
`criticalthink`, `gemini-cli-security`, `gemini-cli-jules`, `open-aware`,
`Endor-Labs-Code-Security`, and `mcp-db-context-enrichment` — a mix of
first-party and ecosystem plugins, several clearly carried over from the Gemini
CLI ecosystem.

---

## See also

- [customization.md](./customization.md) — the skills a plugin can bundle
- [mcp.md](./mcp.md) — the MCP servers a plugin can bundle
- [hooks.md](./hooks.md) — deterministic hooks a plugin can register
