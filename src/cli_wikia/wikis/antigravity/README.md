# Google Antigravity (`agy`) Wiki

A comprehensive reference for **Google Antigravity** — Google's agent-first
development platform — focused on the terminal CLI, invoked as `agy`.
Documented against **v1.0.13** (the version installed on this machine).

> **Why this lives alongside the Gemini CLI wiki.** Antigravity is Google's
> newer, long-term agentic tooling. Multiple Google sources describe the
> Antigravity CLI as the **successor to the Gemini CLI**, with Antigravity now
> the surface Google is investing in. Both are documented here during the
> transition. See the [gemini](../gemini/README.md) wiki for the older tool.

---

## What Antigravity is

Antigravity is not just a chatbot in your terminal. It is an **agentic platform**:
you describe a task at a high level and an agent **plans, executes, and verifies**
it across your **editor, terminal, and browser** — writing code, running
commands, driving a real browser to test what it built, and handing back
reviewable **artifacts** (plans, diffs, walkthroughs, screenshots, recordings).

The same agent harness — co-trained with Gemini models — is exposed through four
surfaces:

| Surface | What it is | Doc |
|---|---|---|
| **Antigravity CLI** (`agy`) | Terminal-native agent (Go binary, TUI) | this wiki |
| **Antigravity IDE** | Standalone AI-first IDE (built on VS Code) | [ide-and-app.md](./ide-and-app.md) |
| **Antigravity 2.0** | Electron desktop app / agent manager | [ide-and-app.md](./ide-and-app.md) |
| **Antigravity SDK** | Public Python SDK for programmatic agents | [sdk.md](./sdk.md) |

---

## Quick start

```bash
agy                          # interactive agentic TUI session
agy -p "explain this repo"   # one-shot: print the response and exit
agy -c                       # continue the most recent conversation
agy --model "Gemini 3.1 Pro (High)" -p "review main.go for races"
agy models                   # list available models
agy plugin import claude     # bring over your Claude plugins
```

On first run, press **Enter** to start the browser OAuth flow, sign in with your
Google account, and paste the code back into the terminal.

---

## Mental model

```
                 ┌───────────────────────────────────────────┐
                 │ Plugins  (bundle skills + MCP + rules)     │  ← share & install
                 ├───────────────────────────────────────────┤
   Deterministic │ Hooks    (lifecycle execution boundaries)  │  ← can hard-block
   ─────────────►├───────────────────────────────────────────┤
                 │ Sandbox  (terminal / OS isolation)         │
                 ├───────────────────────────────────────────┤
                 │ Permissions (tool policy, allow/deny)      │
                 ├───────────────────────────────────────────┤
                 │ MCP servers (external tools/resources)     │
                 ├───────────────────────────────────────────┤
   Model-driven  │ Subagents + background/scheduled tasks     │
   ─────────────►├───────────────────────────────────────────┤
                 │ Skills (on-demand, directory-based)        │
                 ├───────────────────────────────────────────┤
                 │ Rules  (AGENTS.md, always-applied)         │
                 ├───────────────────────────────────────────┤
   Always-loaded │ settings.json (model, permissions, …)      │
   ─────────────►├───────────────────────────────────────────┤
                 │ Models (Gemini 3.5 Flash / 3.1 Pro, …)     │
                 ├───────────────────────────────────────────┤
                 │ Core CLI / TUI (the agy binary)            │
                 └───────────────────────────────────────────┘
```

The same composition idea as other agent CLIs: **rules and skills *suggest*
behavior** (the model can ignore them), while **hooks and permissions *enforce*
it** (they run outside the model). Want isolation? Use a **subagent**. Want to
ship a bundle to others? Wrap it in a **plugin**.

---

## Topics

### Core
| File | What it covers |
|------|----------------|
| [overview.md](./overview.md) | What Antigravity is, its four surfaces, the Gemini-CLI succession |
| [cli-reference.md](./cli-reference.md) | Every `agy` flag, subcommand, TUI slash command, keybinding, env var |
| [agentic-model.md](./agentic-model.md) | Plan→execute→verify, subagents, artifacts, browser verification, scheduled tasks |
| [models.md](./models.md) | Model roster, effort/reasoning tiers, `/model` |

### Configuration & state
| File | What it covers |
|------|----------------|
| [configuration.md](./configuration.md) | `settings.json` keys, the `~/.gemini/antigravity-cli/` data layout, config precedence |
| [projects-sessions-conversations.md](./projects-sessions-conversations.md) | Projects, sessions, durable conversations, fork/resume/rewind |

### Safety
| File | What it covers |
|------|----------------|
| [permissions.md](./permissions.md) | Tool-permission modes, allow/deny rules, internet & browser policy, trusted workspaces |
| [sandbox.md](./sandbox.md) | Terminal sandbox, `--sandbox`, non-workspace file access |
| [hooks.md](./hooks.md) | Deterministic lifecycle hooks |

### Extensibility
| File | What it covers |
|------|----------------|
| [plugins.md](./plugins.md) | Plugin structure, importing from gemini/claude, marketplaces |
| [customization.md](./customization.md) | Rules (`AGENTS.md`) and skills (`SKILL.md`), global vs workspace |
| [mcp.md](./mcp.md) | Model Context Protocol servers, `mcp_config.json` |

### Beyond the CLI
| File | What it covers |
|------|----------------|
| [ide-and-app.md](./ide-and-app.md) | Antigravity IDE + Antigravity 2.0 desktop / agent manager |
| [sdk.md](./sdk.md) | Public Python SDK (`pip install google-antigravity`) |
| [cli-vs-api.md](./cli-vs-api.md) | How the `agy` agent relates to the underlying model APIs |

---

## Sources & accuracy

This wiki was assembled from, in priority order:

1. **Google's bundled offline docs** shipped inside the CLI at
   `~/.gemini/antigravity-cli/builtin/skills/antigravity_guide/` (the
   `antigravity-guide` skill — `cli.md`, `app.md`, `ide.md`, `sdk.md`).
2. **The live `agy` binary** (`agy --help`, `agy plugin --help`, `agy models`,
   `agy changelog`) and the on-disk data layout.
3. **Official online docs** at <https://antigravity.google/docs> and Google's
   developer blog / codelabs.

The public web docs at `antigravity.google/docs` are a JavaScript single-page
app and could not be scraped directly; where a feature area is documented only
in the docs sitemap (skills, rules, hooks, plugins, sidecars, MCP, browser,
agent-permissions) and not in the bundled offline subdocs, details are marked
**"verify in official docs."** Antigravity is new and moving fast — run
`agy changelog` and check <https://antigravity.google/docs> for the latest.
