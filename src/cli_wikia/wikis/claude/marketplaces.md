# Plugin Marketplaces

A marketplace is a source of plugins — typically a git repo with a `marketplace.json` listing available plugins. The official marketplace is `claude-plugins-official` at [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

---

## Add a marketplace

```bash
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin marketplace add github.com/your-org/your-plugins
claude plugin marketplace add /path/to/local/marketplace
claude plugin marketplace update <name>
claude plugin marketplace remove <name>
claude plugin marketplace list
```

In the REPL:

```
/plugins             # marketplace UI
/plugins marketplace add github.com/owner/repo
```

---

## `marketplace.json` schema

```json
{
  "name": "claude-plugins-official",
  "description": "Official Claude Code plugins",
  "plugins": [
    {
      "name": "code-review",
      "description": "AI code review plugin",
      "version": "1.0.0",
      "source": "./plugins/code-review",
      "homepage": "https://docs.example.com",
      "keywords": ["review", "ai"]
    },
    {
      "name": "external-plugin",
      "source": "https://github.com/other/plugin",
      "version": "2.0.0"
    }
  ]
}
```

`source` can be a path within the marketplace repo or a URL to another git repo.

If `version` is set in both `marketplace.json` and the plugin's own `plugin.json`, the **plugin's `plugin.json` wins**.

---

## Persistent enable/disable

Once installed, plugins are enabled via `enabledPlugins` in [settings.json](./settings.md):

```json
{
  "enabledPlugins": {
    "code-review@claude-plugins-official": true,
    "telegram@claude-plugins-official": true,
    "old-thing@somewhere": false
  }
}
```

This is the only durable on/off mechanism — `claude plugin enable` writes here.

---

## Define additional marketplaces in settings

```json
{
  "extraKnownMarketplaces": {
    "internal": {
      "source": "github.com/my-org/internal-plugins"
    },
    "another": {
      "source": "/mnt/shared/plugins"
    }
  }
}
```

Each entry is a name → source object. These show up in `/plugins` browse alongside the official marketplace.

---

## Org policy: managed marketplace restrictions

Admins can lock down which marketplaces and plugins users can use:

| Setting | Effect |
|---|---|
| `strictKnownMarketplaces` | Allowlist of allowed marketplace sources. Blocks anything else from being added |
| `blockedMarketplaces` | Blocklist. Checked **before** download — never touches the filesystem |
| `pluginTrustMessage` | Custom message appended to the plugin trust warning shown before installation |

```json
// managed settings
{
  "strictKnownMarketplaces": [
    "claude-plugins-official",
    "internal-org-plugins"
  ],
  "blockedMarketplaces": [
    "untrusted-source"
  ],
  "pluginTrustMessage": "Internal plugins must be approved by IT — see go/plugins."
}
```

Combined with `extraKnownMarketplaces`, this lets you whitelist exactly which third-party plugins are allowed.

---

## Plugin trust warning

Before installation, Claude Code shows a trust warning explaining that plugins can run code. Org admins can append a custom message via `pluginTrustMessage`. Always read what a plugin contains before installing — plugins ship hooks and MCP servers that run at the same trust level as your shell.

---

## See also

- [plugins.md](./plugins.md) — building a plugin
- [channels.md](./channels.md) — `claude-plugins-official` ships Telegram, Discord, iMessage channels
- [permissions.md](./permissions.md) — managed-only marketplace settings
- [settings.md](./settings.md) — `enabledPlugins`, `extraKnownMarketplaces`, `strictKnownMarketplaces`, `blockedMarketplaces`, `pluginTrustMessage`
