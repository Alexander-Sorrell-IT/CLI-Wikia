# Gemini CLI: The Complete Wiki

A comprehensive reference for **Gemini CLI** — Google's open-source, terminal-based
AI coding agent (`gemini`). Each file is self-contained; read what you need.

> Sourced from the official docs at <https://google-gemini.github.io/gemini-cli/>
> and the `google-gemini/gemini-cli` repository. Cross-checked against the
> installed binary (**v0.22.4**). Some documented features ship in newer
> releases than 0.22.4 — those are flagged inline. Anything uncertain is marked
> "verify in official docs."

---

## Install & first run

```bash
npm install -g @google/gemini-cli   # or: npx https://github.com/google-gemini/gemini-cli
gemini                              # launches the REPL; pick an auth method on first run
```

Authenticate with **Sign in with Google** (free tier), a **Gemini API key**, or
**Vertex AI / Code Assist** for enterprise. See [getting-started.md](./getting-started.md).

---

## The mental model

Gemini CLI is an agentic loop over Gemini models with several layers of control.
From the model's prompt outward to hard, harness-enforced gates:

```
  Enforced by      ┌───────────────────────────────────────────────┐
  the harness      │  Folder Trust  (is this workspace trusted?)   │
   ───────────────►├───────────────────────────────────────────────┤
                   │  Policy Engine + Approval Modes (allow/ask/deny)│
                   ├───────────────────────────────────────────────┤
                   │  Sandboxing (Seatbelt / Docker / Podman)       │
                   ├───────────────────────────────────────────────┤
                   │  Hooks (lifecycle scripts that can block)      │
   ───────────────►├───────────────────────────────────────────────┤
  Model-driven     │  Subagents (delegated, isolated tasks)         │
                   ├───────────────────────────────────────────────┤
                   │  Tools: file, shell, web, MCP, memory, todos   │
                   ├───────────────────────────────────────────────┤
                   │  Skills + custom commands + MCP prompts        │
   ───────────────►├───────────────────────────────────────────────┤
  Always-loaded    │  GEMINI.md context  +  settings.json           │
                   ├───────────────────────────────────────────────┤
                   │  Model (auto / pro / flash / flash-lite)       │
                   ├───────────────────────────────────────────────┤
                   │  Core CLI / REPL  (gemini binary)              │
                   └───────────────────────────────────────────────┘
```

Configuration stacks: **defaults → system defaults → user → project → system →
env vars → CLI flags** (later wins). The system *settings* file sits above user
and project files so admins can enforce policy — see [enterprise.md](./enterprise.md).

---

## Files in this wiki

### Core

| File | What it covers |
|---|---|
| [cli-reference.md](./cli-reference.md) | Every `gemini` subcommand, flag, and positional argument |
| [getting-started.md](./getting-started.md) | Install, authentication options, quota/pricing, first tasks, uninstall |
| [commands.md](./commands.md) | Slash (`/`), at (`@`), and shell (`!`) commands inside the REPL |
| [models.md](./models.md) | Aliases (`auto`/`pro`/`flash`/`flash-lite`), model routing, steering, generation settings, Gemini 3, Gemma |

### Configuration

| File | What it covers |
|---|---|
| [configuration.md](./configuration.md) | Settings-file locations, the seven config layers, precedence, `.env` loading |
| [settings.md](./settings.md) | Every `settings.json` category and its notable fields |
| [environment-variables.md](./environment-variables.md) | All `GEMINI_*` / `GOOGLE_*` env vars and secret redaction |
| [context-files.md](./context-files.md) | `GEMINI.md` hierarchical context, `/memory`, the memory import processor, auto-memory, `.geminiignore` |
| [custom-commands.md](./custom-commands.md) | Personal `/` commands via TOML — args, shell `!{}`, file `@{}` injection |
| [themes.md](./themes.md) | Built-in & custom themes, keyboard shortcuts, terminal notifications |

### Tools, MCP & extensions

| File | What it covers |
|---|---|
| [tools.md](./tools.md) | The built-in tool set (file, shell, web fetch/search, memory, todos, …) and how tools are gated |
| [mcp.md](./mcp.md) | Model Context Protocol — `gemini mcp`, transports, OAuth, `@server` resources, MCP prompts |
| [extensions.md](./extensions.md) | `gemini-extension.json`, the `gemini extensions` lifecycle, what extensions bundle |
| [skills.md](./skills.md) | Agent Skills — `SKILL.md`, discovery tiers, `gemini skills` / `/skills` |

### Agents, hooks & automation

| File | What it covers |
|---|---|
| [subagents.md](./subagents.md) | Local and remote subagents (🔬), definitions, `/agents`, delegation |
| [hooks.md](./hooks.md) | Lifecycle hooks, events, the I/O contract, `/hooks`, blocking behavior |
| [headless.md](./headless.md) | Non-interactive scripting, `--output-format`, ACP mode, system-prompt override |

### Safety & control

| File | What it covers |
|---|---|
| [permissions.md](./permissions.md) | Approval modes, the Policy Engine, Trusted Folders, Plan Mode |
| [sandboxing.md](./sandboxing.md) | macOS Seatbelt profiles, Docker/Podman containers, custom sandbox Dockerfiles |
| [checkpointing.md](./checkpointing.md) | Automatic pre-edit snapshots, `/restore`, and Rewind |
| [sessions.md](./sessions.md) | Auto-saved sessions, `/resume` & chat checkpoints, retention, deletion |
| [git-worktrees.md](./git-worktrees.md) | Per-session isolated checkouts via `-w/--worktree` (🔬) |

### Operations

| File | What it covers |
|---|---|
| [enterprise.md](./enterprise.md) | System-settings lockdown, admin controls, telemetry (OpenTelemetry), token caching |
| [ide-integration.md](./ide-integration.md) | VS Code / Cursor / Windsurf / Zed companions, `/ide`, native diffing |
| [cli-vs-api.md](./cli-vs-api.md) | When to use the Gemini CLI vs the Gemini API |

---

## Quick decision tree

| You want to… | Go to |
|---|---|
| Install and sign in | [getting-started.md](./getting-started.md) |
| Look up a flag | [cli-reference.md](./cli-reference.md) |
| Run a slash/at/shell command | [commands.md](./commands.md) |
| Pick or route a model | [models.md](./models.md) |
| Tell Gemini about your project | [context-files.md](./context-files.md) |
| Tune a `settings.json` field | [settings.md](./settings.md) |
| Connect GitHub / a database / an API | [mcp.md](./mcp.md) |
| Add or build an extension | [extensions.md](./extensions.md) |
| Give Gemini on-demand expertise | [skills.md](./skills.md) |
| Delegate isolated work | [subagents.md](./subagents.md) |
| **Force** behavior deterministically | [hooks.md](./hooks.md) |
| Control what runs without prompting | [permissions.md](./permissions.md) |
| Isolate tool execution at the OS level | [sandboxing.md](./sandboxing.md) |
| Undo file changes a tool made | [checkpointing.md](./checkpointing.md) |
| Script Gemini non-interactively | [headless.md](./headless.md) |
| Lock it down for an organization | [enterprise.md](./enterprise.md) |

---

## Commands at a glance

| Command | Purpose |
|---|---|
| `gemini` | Launch the interactive REPL |
| `gemini -p "…"` | One-shot, non-interactive query |
| `gemini -r latest "…"` | Resume the most recent session |
| `gemini mcp …` | Manage [MCP servers](./mcp.md) |
| `gemini extensions …` | Manage [extensions](./extensions.md) |
| `gemini skills …` | Manage [Agent Skills](./skills.md) *(newer releases)* |
| `gemini update` | Update to the latest version |

---

## Reference

Full live documentation: <https://google-gemini.github.io/gemini-cli/>
· Repository: <https://github.com/google-gemini/gemini-cli>
· Settings schema: `schemas/settings.schema.json`
