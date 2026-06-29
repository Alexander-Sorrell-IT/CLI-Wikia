# Plugins

Plugins bundle skills, agents, hooks, rules, and default settings into one reusable,
shareable package. The plugin model mirrors Claude Code's. This page documents the
packaging format from the install's `PLUGIN_TEMPLATE.md`.

> The shipped install has the plugin machinery wired (`enabledPlugins` in
> `settings.json`, a `~/.clawspring/plugins/` directory) but ships **no enabled
> plugins** by default. Treat plugin behavior as documented-but-unexercised here —
> *verify in the tool.*

---

## Layout

```
my-plugin/
├── .clawspring-plugin/
│   └── plugin.json        # manifest (optional)
├── skills/                # skill directories
│   └── my-skill/SKILL.md
├── agents/                # subagent definitions
│   └── specialist.md
├── hooks/
│   └── hooks.json
├── rules/                 # path-scoped rules
│   └── conventions.md
├── settings.json          # default settings applied on enable
└── README.md
```

---

## `plugin.json` schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": { "name": "Author", "email": "email@example.com" },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./skills/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "dependencies": ["helper-plugin", { "name": "other", "version": "~1.0.0" }]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Namespaced as `plugin:skill` |
| `version` | No | Semver; if omitted, the git SHA is used |
| `description` | No | Short description |
| `author` / `homepage` / `repository` / `license` / `keywords` | No | Metadata |
| `skills` | No | Custom skills dir (default `skills/`) |
| `agents` | No | Custom agents dir (default `agents/`) |
| `hooks` | No | Hook config path or inline |
| `dependencies` | No | Other required plugins (string or `{name, version}`) |

---

## Plugin scopes

A plugin is enabled at one of three scopes, each backed by a different settings file:

| Scope | Settings file | Use case |
|-------|---------------|----------|
| `user` | `~/.clawspring/settings.json` | Personal, all projects |
| `project` | `.clawspring/settings.json` | Team-shared via git |
| `local` | `.clawspring/settings.local.json` | Project-specific, gitignored |

Enabled plugins are tracked in the `enabledPlugins` object of the relevant
`settings.json`.

---

## What a plugin can bundle

| Component | Notes |
|-----------|-------|
| **Skills** | Namespaced `plugin-name:skill-name`. The most common component. |
| **Agents** | Loaded at session start. Reusable specialists. |
| **Hooks** | Fire while the plugin is enabled. |
| **Rules** | Path-scoped `*.rules.md` guidance. |
| **Settings** | Applied as defaults when the plugin is enabled. |

---

## Limitations

- **Plugin subagents do not support** `hooks`, `mcpServers`, or `permissionMode`
  (they are more constrained than user/project agents).
- Plugin skills are always namespaced — invoke them as `/plugin-name:skill-name`.
- Plugin agents are loaded at session start, not lazily.

---

## Related

- [skills.md](skills.md) — the SKILL.md format plugins bundle
- [agents.md](agents.md) — subagent definitions and the plugin precedence tier
- [hooks.md](hooks.md) — bundled `hooks.json`
- [configuration.md](configuration.md) — `enabledPlugins` and settings scopes
