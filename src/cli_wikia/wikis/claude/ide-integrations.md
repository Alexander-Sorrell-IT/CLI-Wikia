# IDE Integrations

Claude Code integrates natively with VS Code (extension) and JetBrains IDEs (plugin). Both offer graphical interfaces for conversation, diff review, file references, and session management.

---

## VS Code Extension

### Install

```bash
code --install-extension anthropic.claude-code
```

Or search "Claude Code" in the Marketplace.

### Open

- Click the **Spark icon** in the Editor Toolbar (top-right when a file is open)
- Or click the icon in the bottom status bar

### Features

| Feature | How |
|---|---|
| **Diff view** | Side-by-side comparison; review & approve inline |
| **`@`-mentions** | `@filename`, `@folder/`, `@file.pdf#pages=1-5`. Press **Alt+K** (Mac) / **Option+K** to auto-insert file + selection |
| **Permission modes** | Button at bottom of prompt box — toggle default → plan → acceptEdits → auto (if allowed) |
| **Session history** | "Session history" button — search by keyword or time range; resume any session |
| **Multiple conversations** | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` opens a new tab |
| **Focus toggle** | `Cmd+Esc` toggles focus between editor and Claude |
| **New conversation** | `Cmd+N` (if enabled) |
| **Checkpoints** | Hover over a message → rewind button: fork, rewind code, or both |
| **Chrome integration** | `@browser` in prompt; requires Claude in Chrome extension |
| **MCP management** | `/mcp` to enable/disable servers, manage OAuth |
| **Plugin management** | `/plugins` to install/enable/disable; manage marketplaces |
| **Remote Control** | `/remote-control` or `/rc` to make this session driveable from claude.ai |
| **Terminal mode** | Set `useTerminal: true` in VS Code settings to use the CLI inside VS Code instead of the panel |

### Initial permission mode in extension settings

```json
{ "claudeCode.initialPermissionMode": "acceptEdits" }
```

(Doesn't accept `auto` — set `defaultMode` in `settings.json` for that.)

### Required extension settings for some modes

`auto` and `bypassPermissions` appear in the mode indicator only after enabling **Allow dangerously skip permissions** in extension settings.

### Built-in IDE MCP server

When the extension is active, an internal MCP server runs:
- Bound to `127.0.0.1` on a random port
- Auth token stored in `~/.claude/ide/`
- **Not visible in `/mcp`** — it's internal RPC

Provides:
- `mcp__ide__getDiagnostics` — read VS Code Problems pane
- `mcp__ide__executeCode` — run Jupyter cells (asks confirmation)

---

## JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)

### Install

Search "Claude Code" in the Marketplace, or install via plugin settings.

### Open

- Spark icon in toolbar
- Or **Tools → Claude Code**

### Features

| Feature | How |
|---|---|
| Open / focus | `Cmd+Shift+A` (Mac) / `Ctrl+Shift+A` (Windows/Linux) |
| Diff view | Built-in IDE diff viewer |
| `@`-mentions | Reference files; similar to VS Code |
| Session history | View and resume past conversations |
| Mode switching | Same as CLI: `Shift+Tab` cycles, or pass `--permission-mode` when launching |

The JetBrains plugin runs Claude Code in the IDE terminal, so most CLI flags and behaviors apply directly.

---

## When to drop to the CLI even with the extension installed

- **Full slash-command coverage** — extensions don't surface every CLI command
- **Scripts and automation** (`claude -p`)
- **Worktrees** (`-w` flag)
- **MCP configuration** (use `claude mcp add`, then manage in extension)
- **Custom hooks/skills testing**
- **Piped input** (`cat file | claude -p "prompt"`)

---

## Chrome integration

`--chrome` enables Chrome browser automation. Add `@browser` in your prompt to interact with web pages:

```
@browser navigate to localhost:3000 and screenshot the home page
```

Requires the **Claude in Chrome** extension. Disable with `--no-chrome`.

---

## See also

- [cli-reference.md](./cli-reference.md) — `--ide`, `--chrome`, `--no-chrome`, `--remote-control`
- [remote-control.md](./remote-control.md) — driving local sessions from the web/mobile
- [mcp.md](./mcp.md) — `mcp__ide__*` tools
