# Antigravity IDE & Antigravity 2.0

The `agy` CLI is one of four Antigravity surfaces. Two are graphical and share
the same agents, skills, rules, plugins, and permission model as the CLI: the
**Antigravity IDE** (in-editor) and **Antigravity 2.0** (a standalone desktop
agent manager). They coexist — pick the one that fits your workflow.

---

## Antigravity IDE

A standalone, **AI-first IDE built on VS Code** that bakes agentic workflows into
the editor. It offers three interaction modalities, from passive to fully
collaborative:

### A. Passive — Antigravity Tab (autocomplete)
Next-intent prediction routed to a single keystroke.

- **Context-aware suggestions** from surrounding code, open tabs, terminal
  output, and (optionally) clipboard.
- **Autocomplete** (code at the cursor) and **Supercomplete** (larger diffs,
  including deletions, in floating windows).
- **Tab to Jump** — anticipates your next navigation point.
- **Tab to Import** — auto-adds missing imports.
- Accept with `Tab`, cancel with `Esc`, accept word-by-word with
  `Ctrl/⌘ + →`.

### B. Instructive — Inline Command (`Ctrl/⌘ + I`)
Localized edits: highlight a block and instruct a refactor/explain/modify; invoke
with no selection to generate net-new code. Great for docstrings and comments.

### C. Collaborative — Sidebar Chat & Agent
The full agent: a sidebar to ask/plan/discuss, **Agent Mode** (reads/writes
files, runs build/test commands, searches the web, uses MCP tools), and
**Planning Mode** to review the agent's step-by-step plan before execution.

### Editor integrations
- **Inline Code Lenses** — action buttons above symbols (Refactor, Write Tests,
  Explain) to trigger targeted agent commands.
- **Visual Diff Overlays** — inline red/green proposed edits to accept/reject
  in-context.
- **Diagnostic Auto-Fix** — trigger the agent from compiler errors, lint
  warnings, or the Problems pane.

The IDE auto-discovers `<project-root>/.agents/` for workspace-scoped rules,
skills, and plugins — the same [customization](./customization.md) the CLI uses.

---

## Antigravity 2.0

A **desktop Electron application** that launches and monitors agents on your
machine — an "agent manager" independent of any editor. It's built for running
and overseeing **multiple agents in parallel**.

### Left-hand sidebar
| Section | Purpose |
|---------|---------|
| **New Conversation** | Start a new agent chat |
| **Projects** | Manage/switch between workspaces and repos |
| **Scheduled Tasks** | Define/monitor recurring (cron) and one-time delayed tasks |
| **Skills & Customizations** | Manage active skills, rules, plugins, MCP servers |
| **Settings** | App preferences, model selection, permissions |

### Chat canvas
- **Slash commands** (`/`) trigger built-in workflows / dedicated subagents.
- **`@` mentions** attach context: files/folders, previous conversations,
  terminal sessions, rules, and MCP servers/tools.
- **Media uploads** — drag-drop or paste images/files as context.

### Settings & permissions
Global controls (with per-project overrides) mirror the CLI's config:

- **Model selection** (Gemini Flash / Pro / Next).
- **Tool Execution Policy** (`always-proceed`, `request-review`, `strict`,
  `proceed-in-sandbox`) — see [permissions.md](./permissions.md).
- **Terminal Sandbox** toggle — see [sandbox.md](./sandbox.md).
- **Non-Workspace File Access** and **Internet Access** policies
  (`allow`/`ask`/`deny`).
- **Command Allowlist/Denylist**, **Browser Allowlist**.
- **Artifact Review Mode** (`always-proceed`/`agent-decides`/`asks-for-review`).
- Notifications, appearance, and app behavior (keep awake, run in background,
  auto-update).

**Project-level settings** override their global counterparts when a project is
active: file-access, internet-access, sandbox, auto-execution, artifact-review,
and permission grants.

---

## Choosing a surface

| If you… | Use |
|---------|-----|
| Live in the terminal / want scriptable runs | **CLI** (`agy`) — this wiki |
| Want AI inside a full editor with autocomplete | **Antigravity IDE** |
| Want to launch & monitor many agents, schedule tasks | **Antigravity 2.0** |
| Want to embed agents in code | **[SDK](./sdk.md)** |

> The IDE and Antigravity 2.0 are summarized here from Antigravity's bundled
> `ide.md` and `app.md` references. For installation, keybindings, and the latest
> feature set, see `https://antigravity.google/docs`.

---

## See also

- [overview.md](./overview.md) — the four surfaces and the Gemini-CLI succession
- [permissions.md](./permissions.md) / [sandbox.md](./sandbox.md) — the shared safety model
- [sdk.md](./sdk.md) — the programmatic surface
