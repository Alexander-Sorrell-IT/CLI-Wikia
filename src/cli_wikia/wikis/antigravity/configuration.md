# Configuration & Data Layout

Antigravity is configured by a JSON settings file plus a small set of
customization roots, and it stores all of its state under a single data
directory. This page documents the `settings.json` keys, the on-disk layout, and
how configuration scopes are resolved.

## First-time setup

```bash
agy install     # configure PATH, shell completions, and environment
agy             # launch; press Enter to start Google OAuth sign-in
```

---

## `settings.json`

The CLI is configured via **`~/.gemini/antigravity-cli/settings.json`**. Every
exported key (v1.0.13):

| Key | Type | Description | Default |
|-----|------|-------------|---------|
| `allowNonWorkspaceAccess` | bool | Permit reading/writing files outside the workspace root | `false` |
| `altScreenMode` | string | Alternate screen buffer use (`default`, `always`, `never`) | `default` |
| `artifactReviewPolicy` | string | When to ask for artifact review (`always-proceed`, `agent-decides`, `asks-for-review`) | `asks-for-review` |
| `colorScheme` | string | CLI color scheme (`terminal`, `dark`, `light`) | `terminal` |
| `editor` | string | Editor command for `/open` (`vim`, `nano`, `auto`, …) | `auto` |
| `enableTelemetry` | bool | Anonymous usage & crash reporting | `true` |
| `enableTerminalSandbox` | bool | Run terminal commands in a restricted sandbox | `false` |
| `gcp` | object | GCP project/location config for cloud tools | `null` |
| `historySize` | int | Max history entries persisted (`-1` = unlimited) | `2000` |
| `model` | string | Active model identifier for the main agent | `gemini-3.5-flash` |
| `notifications` | bool | System notifications on task completion | `false` |
| `permissions` | object | Global allow/deny/ask rules for files, commands, URLs | `null` |
| `runningLightSpeed` | string | Typing-delay / thought visualization (`off`, `fast`, `medium`, `slow`) | `medium` |
| `showFeedbackSurvey` | bool | Periodic product feedback surveys | `true` |
| `showTips` | bool | Show tips and shortcuts | `true` |
| `statusLine` | object | TUI status-line configuration | `null` |
| `title` | object | TUI title configuration | `null` |
| `toolPermission` | string | Tool confirmation mode (`always-proceed`, `request-review`, `strict`, `proceed-in-sandbox`) | `request-review` |
| `trustedWorkspaces` | array | Directory paths trusted for execution | `[]` |
| `useG1Credits` | bool | Use Google One AI premium quotas | `false` |
| `verbosity` | string | Agent trace detail (`high`, `low`) | `high` |

Most of these are also editable interactively via `/config` (`/settings`). The
safety-related keys (`toolPermission`, `enableTerminalSandbox`,
`allowNonWorkspaceAccess`, `permissions`, `trustedWorkspaces`) are covered in
depth in [permissions.md](./permissions.md) and [sandbox.md](./sandbox.md).

---

## Customization roots

Behavior is extended from two roots (rules + skills); see
[customization.md](./customization.md):

| Scope | Location | Holds |
|-------|----------|-------|
| **Global** | `~/.gemini/config/` | `AGENTS.md` (rules), `skills/<name>/SKILL.md` |
| **Workspace** | `<project-root>/.agents/` | `AGENTS.md`, `skills/`, project-scoped customizations |

Workspace customizations override or extend the global ones for that project.

> The `.agents/` workspace folder and `~/.gemini/config/` global root come from
> the bundled docs and model interrogation; confirm the exact folder names for
> your version in official docs.

---

## On-disk data layout

Everything the CLI stores lives under **`~/.gemini/antigravity-cli/`**:

```
~/.gemini/antigravity-cli/
├── settings.json          # the config above
├── keybindings.json       # created on first /keybindings use
├── builtin/skills/        # bundled skills (e.g. antigravity_guide)
├── plugins/<name>/        # installed/imported plugins (plugin.json, mcp_config.json, skills/)
├── mcp/<name>/            # per-MCP-server staging
├── conversations/<id>.db  # conversation metadata/index (.db or .pb)
├── brain/<conversation-id>/
│   ├── .system_generated/logs/transcript.jsonl       # token-efficient transcript
│   ├── .system_generated/logs/transcript_full.jsonl  # full untruncated transcript
│   ├── scratch/           # temp scripts & outputs the agent generated
│   ├── *.md               # artifacts (plans, reports, walkthroughs)
│   └── mcp_config.json    # MCP servers active for this conversation
├── knowledge/             # indexed knowledge store
├── implicit/              # implicit context (*.pb)
├── log/                   # CLI logs
├── cache/  scratch/  updater/  bin/
```

The **`brain/<id>/`** directory is where a conversation's working memory lives:
its transcripts (as JSON Lines), scratch files, and generated artifacts.

---

## Configuration precedence

Project-specific settings take priority over global ones:

```
project config  (~/.gemini/config/projects/<project>)   ← highest priority
        ▼ overrides
global settings (~/.gemini/antigravity-cli/settings.json)
        ▼ overrides
built-in defaults
```

Per-session launch flags (e.g. `--model`, `--sandbox`, `--add-dir`) override the
persisted config for that session only.

> Per-project config under `~/.gemini/config/projects/` and its precedence over
> the global `settings.json` are confirmed by the v1.0.12 changelog.

---

## See also

- [permissions.md](./permissions.md) — `toolPermission`, `permissions`, `trustedWorkspaces`
- [sandbox.md](./sandbox.md) — `enableTerminalSandbox`, `allowNonWorkspaceAccess`
- [projects-sessions-conversations.md](./projects-sessions-conversations.md) — what lives in `brain/` and `conversations/`
