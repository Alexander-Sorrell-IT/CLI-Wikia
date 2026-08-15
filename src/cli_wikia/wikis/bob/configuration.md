# Configuration

Bob is configured through custom modes (`.bob-profiles/`) and workspace
settings (`.agents/settings.json`). The Bob application manages the profile
system; the workspace settings are project-specific.

---

## Config layout

```
~/.bob-profiles/
└── bob-5/                  ← active profile
    ├── custom_modes.yaml   ← mode definitions
    └── settings.json       ← user-level settings (hooks, MCP servers, etc.)

<project-root>/
├── .agents/
│   ├── settings.json       ← project-level settings
│   ├── mcp/                ← cli-enforcement engine scripts (if deployed)
│   ├── config/
│   │   ├── points_config.yaml
│   │   └── project_config.yaml
│   ├── docs/
│   │   ├── HOOKS.md
│   │   └── POINTS.md
│   └── skills/             ← project-scoped skills
└── AGENTS.md               ← project instructions (always loaded)
```

---

## Custom modes (`custom_modes.yaml`)

Defines the three built-in modes and any user-created modes.

```yaml
- slug: agent
  name: Agent
  roleDefinition: "You are Bob, a highly skilled software engineer..."
  groups:
    - read
    - edit
    - command
    - mcp
  source: global

- slug: plan
  name: Plan
  roleDefinition: "You are Bob, in plan mode..."
  groups:
    - read
    - edit
    - mcp
  source: global

- slug: ask
  name: Ask
  roleDefinition: "You are Bob, in ask mode..."
  groups:
    - read
    - mcp
  source: global
```

Use the `create-mode` skill for the full schema and gotchas:
```
use_skill("create-mode")
```

---

## settings.json keys

| Key | Description |
|---|---|
| `hooks` | Hook registry — same format as Claude Code's `settings.json` |
| `mcpServers` | MCP server definitions (stdio, SSE, HTTP) |
| `permissions` | Tool allow/deny rules |
| `env` | Environment variables injected into every Bash command |

---

## AGENTS.md

The project instructions file. Bob reads it at session start (via
`InstructionsLoaded` hook). Put project conventions, architecture notes, and
coding standards here.

Location: `<project-root>/AGENTS.md` (or `.agents/AGENTS.md`).

When cli-enforcement is deployed, `AGENTS.md` is added to the read-only
document list and cannot be edited during a workflow without `unlock enforcement`.

---

## Sources

Bob application documentation and the Bob profile system. Accessed 2026-08.
