# Hooks

Hooks let you intercept the agent's behavior at defined events and run your own logic — for validation, logging, or blocking actions. They're configured as JSON keyed by event name.

> Hooks are a newer, lighter surface in Copilot CLI than in some other agents. The CLI exposes the configuration shape and a master kill-switch; the full catalog of event names and payloads is best confirmed in the official docs. **Verify event-level details in the official docs before depending on them.**

---

## Where hooks are defined

| Scope | Location |
|---|---|
| Repo-level | `.github/hooks/*.json` |
| Repo settings | `hooks` key in `.github/copilot/settings.json` |
| User-level | `hooks` key in `~/.copilot/settings.json` (global `config.json`) |
| Plugin | `hooks.json` in a plugin root, or files in the plugin's `hooks/` |

The inline `hooks` setting uses the **same schema** as `.github/hooks/*.json`. In the global config these act as **user-level** hooks; in repo settings they act as **repo-level** hooks.

```json
{
  "hooks": {
    "<event-name>": [
      { /* handler definition */ }
    ]
  }
}
```

---

## Disabling hooks

| Setting / flag | Effect |
|---|---|
| `disableAllHooks: true` (settings.json) | Disable all hooks, both repo- and user-level |

---

## Relationship to permissions

Hooks complement [permissions](permissions.md): permissions decide *whether* a tool runs and prompt you; hooks let you attach deterministic logic around events. Use permissions for allow/deny of tools, paths, and URLs; use hooks for custom event-driven behavior.

---

## See also

- [plugins.md](plugins.md) — plugins can ship hooks
- [permissions.md](permissions.md) — the primary gating mechanism
- [configuration.md](configuration.md) — `hooks` and `disableAllHooks`
