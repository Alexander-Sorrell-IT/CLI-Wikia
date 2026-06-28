# Claude Code: The Complete Wiki

A comprehensive reference covering every major aspect of Claude Code (the CLI, the SDK, the IDE extensions, the web sessions, and the entire extension surface). Each file is self-contained — read what you need.

> Sourced from <https://code.claude.com/docs/>. Last assembled 2026-04-26.
> Latest model: **Claude Opus 4.7** (1M context). See [models.md](./models.md).

---

## The Mental Model

Claude Code has a **layered extensibility model**. Each layer plugs into the same agentic loop, but each layer has different power, scope, and rules about *who* controls it (the model, the user, or the harness).

```
                 ┌──────────────────────────────────────────┐
                 │  Plugins / Marketplaces                  │  ← bundle everything
                 ├──────────────────────────────────────────┤
   Deterministic │  Hooks (28 events × 5 handler types)     │  ← only thing that can hard-block
   ─────────────►├──────────────────────────────────────────┤
                 │  Sandboxing (OS-level Bash isolation)    │
                 ├──────────────────────────────────────────┤
                 │  Permissions (allow / ask / deny rules)  │
                 ├──────────────────────────────────────────┤
                 │  MCP servers (external tools/resources)  │
                 ├──────────────────────────────────────────┤
                 │  Channels (push events INTO sessions)    │
                 ├──────────────────────────────────────────┤
   Model-driven  │  Subagents + Agent Teams                 │  ← isolated context
   ─────────────►├──────────────────────────────────────────┤
                 │  Skills (on-demand prompts)              │
                 ├──────────────────────────────────────────┤
                 │  Slash commands (built-in + bundled)     │
                 ├──────────────────────────────────────────┤
                 │  Output styles                           │
                 ├──────────────────────────────────────────┤
   Always-loaded │  CLAUDE.md + auto-memory                 │
   ─────────────►├──────────────────────────────────────────┤
                 │  Settings (permissions, env, …)          │
                 ├──────────────────────────────────────────┤
                 │  Models (Opus 4.7, Sonnet 4.6, Haiku 4.5)│
                 ├──────────────────────────────────────────┤
                 │  Core CLI / REPL (claude binary)         │
                 └──────────────────────────────────────────┘
```

**The single most important rule:** the model can *ignore* prompts (CLAUDE.md, skills, output styles) but it **cannot ignore hooks or permissions** — those run *outside* the model and are enforced by the harness. So:

- Need behavior to *happen for sure*? → write a **hook**.
- Want to *suggest* behavior? → write a **skill** or **CLAUDE.md** entry.
- Want isolation? → use a **subagent** or **agent team**.
- Want to ship to others? → wrap it in a **plugin**.

---

## Files in this Wiki

### Core

| File | What it covers |
|---|---|
| [cli-reference.md](./cli-reference.md) | Every `claude` subcommand and every CLI flag |
| [models.md](./models.md) | **Opus 4.7 (1M ctx)**, Sonnet 4.6, Haiku 4.5, fast mode, effort levels, `--model` aliases |
| [environment-variables.md](./environment-variables.md) | All `CLAUDE_CODE_*` and `CLAUDE_*` env vars |
| [settings.md](./settings.md) | Every key in `settings.json` (80+) |

### Memory & context

| File | What it covers |
|---|---|
| [memory.md](./memory.md) | `CLAUDE.md`, `~/.claude/CLAUDE.md`, `.claude/rules/`, `@imports`, auto-memory in `~/.claude/projects/<proj>/memory/`, the `/memory` and `/remember` system |
| [output-styles.md](./output-styles.md) | Default / Explanatory / Learning, custom output styles, `keep-coding-instructions` |

### Slash commands & skills

| File | What it covers |
|---|---|
| [slash-commands.md](./slash-commands.md) | Built-in commands and bundled skills (`/init`, `/compact`, `/help`, `/memory`, `/hooks`, `/mcp`, `/plugins`, `/permissions`, `/agents`, `/cost`, `/status`, `/config`, `/model`, `/effort`, `/remote-control`, `/teleport`, `/feedback`, `/simplify`, `/batch`, `/debug`, `/loop`, `/claude-api`, `/sandbox`, `/web-setup`, `/tasks`, …) |
| [skills.md](./skills.md) | Full SKILL.md frontmatter (15 fields), substitution, shell injection, supporting files, lifecycle, content cache, `Skill()` permission rules |

### Agents

| File | What it covers |
|---|---|
| [agents.md](./agents.md) | Subagents — full AGENT.md frontmatter (15 fields), tool restrictions, MCP scoping, persistent memory, isolation modes, Agent tool, `--agents` JSON, model resolution |
| [agent-teams.md](./agent-teams.md) | Multi-Claude coordination, lead/teammate model, mailbox, shared task list, in-process vs tmux/iTerm2 split panes, `TeammateIdle` hook, plan-approval workflow |

### Hooks & determinism

| File | What it covers |
|---|---|
| [hooks.md](./hooks.md) | All 28 event types, 5 handler types, complete I/O schema, exit codes, `asyncRewake`, `defer`, environment vars |
| [permissions.md](./permissions.md) | Rule syntax (Bash globs, Read/Edit gitignore patterns, `Skill()`, `Agent()`, `mcp__server__tool`), evaluation order, working dir, managed-only settings |
| [permission-modes.md](./permission-modes.md) | All 6 modes (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`), the auto-mode classifier, protected paths, model gating for auto |
| [sandboxing.md](./sandboxing.md) | macOS Seatbelt + Linux bubblewrap, filesystem rules, network proxy, weakened sandbox modes, the `dangerouslyDisableSandbox` escape hatch |

### Tools, MCP, and integrations

| File | What it covers |
|---|---|
| [mcp.md](./mcp.md) | All transports (stdio/HTTP/SSE), `claude mcp add` variants, OAuth (with `--callback-port`, `--client-id`, CIMD), scopes (local/project/user), `.mcp.json`, env-var expansion, MCPB bundles, plugin MCP, OAuth via `/mcp` |
| [plugins.md](./plugins.md) | Full `plugin.json` schema (15 fields), every component dir (skills/agents/hooks/MCP/LSP/monitors/themes/output-styles), `${CLAUDE_PLUGIN_ROOT}` vs `${CLAUDE_PLUGIN_DATA}`, `userConfig`, dependencies, install scopes |
| [marketplaces.md](./marketplaces.md) | `marketplace.json`, `claude plugin marketplace add/update`, `enabledPlugins`, `extraKnownMarketplaces`, `strictKnownMarketplaces`, `blockedMarketplaces`, plugin trust |
| [monitors.md](./monitors.md) | Background `monitors.json` in plugins, `when` triggers, the Monitor tool, notification flow |
| [channels.md](./channels.md) | Research-preview push channels (Telegram, Discord, iMessage, fakechat), `--channels`, `channelsEnabled`, `allowedChannelPlugins`, building your own |

### Sessions & remote work

| File | What it covers |
|---|---|
| [ide-integrations.md](./ide-integrations.md) | VS Code extension, JetBrains plugin, IDE MCP server, Chrome bridge |
| [headless-sdk.md](./headless-sdk.md) | `claude -p` flags (output formats, JSON schema, max-budget, max-turns, fork-session), Agent SDK (Python + TypeScript), bare mode |
| [remote-control.md](./remote-control.md) | Drive a local session from claude.ai or the mobile app — `claude remote-control`, `--rc`, `/remote-control`, server modes, push notifications |
| [claude-code-web.md](./claude-code-web.md) | Cloud sessions at claude.ai/code, `--remote`, `--teleport`, `--from-pr`, GitHub auto-fix, environment caching, the trusted-domain allowlist |
| [statusline.md](./statusline.md) | Custom `statusLine.command`, JSON input fields, multi-line examples |

### Composition & advisor

| File | What it covers |
|---|---|
| [stacking.md](./stacking.md) | **How to compose skills with agents with hooks** — the patterns, the gotchas, a complete worked example |
| [advisor.md](./advisor.md) | What the `advisor` tool is, when it's available, when to call it, how to weight its advice |

---

## Quick decision tree

| You want to… | Go to |
|---|---|
| Start with the basics | [cli-reference.md](./cli-reference.md) |
| Pick the right model | [models.md](./models.md) |
| Tell Claude facts about your project | [memory.md](./memory.md) |
| Make Claude run a multi-step workflow | [skills.md](./skills.md) |
| Isolate heavy research | [agents.md](./agents.md) |
| Run multiple Claudes in parallel | [agent-teams.md](./agent-teams.md) |
| **Force** behavior to happen | [hooks.md](./hooks.md) |
| Connect to GitHub / Sentry / etc. | [mcp.md](./mcp.md) |
| Ship all of the above to others | [plugins.md](./plugins.md) |
| Lock down what tools Claude can use | [permissions.md](./permissions.md) |
| Reduce permission prompts safely | [permission-modes.md](./permission-modes.md) (see `auto`) |
| Sandbox bash for OS-level isolation | [sandboxing.md](./sandboxing.md) |
| Drive your local Claude from your phone | [remote-control.md](./remote-control.md) |
| Run sessions on Anthropic-hosted VMs | [claude-code-web.md](./claude-code-web.md) |
| React to external events (CI, Telegram, …) | [channels.md](./channels.md) + [monitors.md](./monitors.md) |
| Embed Claude Code in another app | [headless-sdk.md](./headless-sdk.md) |
| Compose skills + agents + hooks together | [stacking.md](./stacking.md) |
| Get a second opinion mid-task | [advisor.md](./advisor.md) |

---

## Skill Priority

When multiple skills could apply to a task, Claude uses this order:

1. **Process skills first** (e.g. `brainstorming`, `systematic-debugging`) — these determine *how* to approach the task.
2. **Implementation skills second** (e.g. `frontend-design`, `mcp-builder`) — these guide execution.

So "let's build X" → brainstorming first, then implementation skills. "Fix this bug" → debugging first, then domain-specific skills.

---

## Reference URL

Full live documentation: <https://code.claude.com/docs/llms.txt>
