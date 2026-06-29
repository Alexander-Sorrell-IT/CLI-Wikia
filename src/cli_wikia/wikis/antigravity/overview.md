# Overview: What Google Antigravity Is

**Google Antigravity** is Google's **agent-first development platform**. Instead
of asking a model for a snippet and pasting it yourself, you hand an *agent* a
task and it **plans, executes, and verifies** the work end-to-end — editing
files, running terminal commands, searching the web, calling external tools over
MCP, and even driving a real browser to test what it built.

Every Antigravity surface runs on the **same agent harness**, co-trained with
Gemini models. Local agents are powered by **Gemini 3.5 Flash** by default for
speed and large context, with **Gemini 3.1 Pro** available for deeper planning
and reasoning (see [models.md](./models.md)).

---

## The four surfaces

Antigravity is one platform with four front-ends that share the same agents,
skills, rules, plugins, and permissions model:

| Surface | Form | Best for |
|---|---|---|
| **Antigravity CLI** (`agy`) | A Go binary with a terminal UI | Terminal-native devs who live in the shell; scripting one-shot agent runs |
| **Antigravity IDE** | A standalone AI-first IDE built on VS Code | In-editor tab autocomplete, inline commands, sidebar agent |
| **Antigravity 2.0** | An Electron desktop "agent manager" app | Launching and monitoring many agents in parallel, scheduled tasks |
| **Antigravity SDK** | A public Python package | Embedding agents in scripts, pipelines, and test suites |

This wiki focuses on the **CLI** (`agy`). The other surfaces are summarized in
[ide-and-app.md](./ide-and-app.md) and [sdk.md](./sdk.md).

---

## The successor to the Gemini CLI

Multiple Google and community sources describe the **Antigravity CLI as the
direct successor to the Gemini CLI**: the agent harness, plugin model, and MCP
support carry forward, and Antigravity can **import your existing Gemini CLI
plugins** in one command (`agy plugin import gemini`). On this machine the CLI
even stores its data under `~/.gemini/antigravity-cli/`, reflecting that
lineage.

If you are migrating, the conceptual map is:

| Gemini CLI idea | Antigravity equivalent |
|---|---|
| Extensions / plugins | [Plugins](./plugins.md) (`agy plugin`), importable from gemini |
| `GEMINI.md` project memory | `AGENTS.md` [rules](./customization.md) |
| Custom commands | [Skills](./customization.md) (`SKILL.md`) |
| MCP servers | [MCP](./mcp.md) (`mcp_config.json`) |
| One model (Gemini) | Multi-model: Gemini, Claude, GPT-OSS ([models.md](./models.md)) |

> The exact succession timeline and any Gemini CLI end-of-life dates should be
> **verified in official docs** — community write-ups circulate specific dates
> that this wiki does not independently confirm.

---

## What makes it "agent-first"

The defining behavior, versus a plain chat CLI:

- **Plans before it codes.** The agent produces a reviewable Task List and, for
  larger work, an Implementation Plan artifact you can comment on.
- **Verifies its own work.** For web tasks it spins up the server, opens Chrome,
  clicks through the flows, and records a **Walkthrough** with screenshots and
  video — so you watch a clip instead of re-running the app yourself.
- **Communicates through artifacts.** Plans, diffs, walkthroughs, and recordings
  are durable deliverables, not ephemeral chat. You can leave comments on them
  and the agent incorporates feedback without halting.

See [agentic-model.md](./agentic-model.md) for the full picture.

---

## Where to go next

- New to the CLI? → [cli-reference.md](./cli-reference.md)
- Want to understand how the agent works? → [agentic-model.md](./agentic-model.md)
- Configuring it? → [configuration.md](./configuration.md)
- Locking it down? → [permissions.md](./permissions.md) + [sandbox.md](./sandbox.md)
