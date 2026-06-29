# The Agentic Model

Antigravity's defining feature is *how* it works, not just *what* it can do. An
Antigravity agent operates on a **plan → execute → verify** loop and
communicates through durable **artifacts** rather than ephemeral chat. This page
explains that loop, subagents, background and scheduled tasks, browser
verification, and the artifact system.

---

## Plan → Execute → Verify

When you give the agent a non-trivial task, it doesn't immediately start editing
files. It:

1. **Plans.** It produces a structured **Task List** and, for larger work, an
   **Implementation Plan** artifact describing the changes it intends to make.
   You review (and optionally comment on) the plan before it proceeds.
2. **Executes.** It edits files, runs terminal commands, searches the web, and
   calls external tools (over [MCP](./mcp.md)) — checking off tasks as it goes.
3. **Verifies.** For web work it spins up the server, drives a real Chrome
   browser through the app, captures screenshots and video, and produces a
   **Walkthrough** so you can confirm the result without re-running anything.

You can watch progress live in the TUI with `/tasks` (task list) and `/diff`
(running code diff).

---

## Artifacts

An **artifact** is a structured deliverable the agent creates to do its work and
to communicate its thinking. Artifacts are reviewable like a document — you can
read them, and in many cases leave a comment and the agent will incorporate your
feedback **without stopping** its execution flow.

| Artifact | What it is |
|---|---|
| **Task List** | The agent's structured plan, generated before coding. Reviewable; sometimes commentable |
| **Implementation Plan** | Technical architecture of the change — what files/edits are needed, meant for human review |
| **Walkthrough** | Post-implementation summary of what changed and how to test it |
| **Screenshots / Browser recordings** | For web tasks: the agent's own testing session captured as images/video |
| **Diffs & reports** | Code diffs and generated markdown reports (analysis, research notes, etc.) |

In the CLI, open the artifact viewer with `/artifact`. Whether the agent pauses
for artifact review is governed by `artifactReviewPolicy` /
**Artifact Review Mode** (`always-proceed`, `agent-decides`, `asks-for-review`)
— see [configuration.md](./configuration.md).

> The artifact taxonomy above is corroborated by Google's developer blog and the
> docs sitemap (`/docs/artifacts`); exact naming may evolve — verify in official
> docs.

---

## Browser automation & verification

A standout capability: the agent can **operate a real browser** as part of its
work. When it builds or changes a web app it can launch the server, open Chrome,
navigate, click through flows, take screenshots, and record video — then attach
that as a verification Walkthrough.

- Browser access is gated by the **Browser Allowlist** (which domains the
  agent's browser tools may visit) — see [permissions.md](./permissions.md).
- The changelog notes browser prompt sections in the agent's prompt registry,
  confirming browser tasks are a first-class, shipping capability.
- Browser automation can also be combined with external tooling (e.g. a Browser
  MCP server / Playwright) for UI testing workflows.

> Detailed browser-tool configuration lives at
> `https://antigravity.google/docs/browser` — verify specifics there.

---

## Subagents

The agent can delegate work to **subagents** — child agent threads that run
**asynchronously** and report back to the parent conversation. This isolates
heavy or parallelizable work (e.g. "analyze each file for vulnerabilities")
without polluting the main thread's context.

- List them live with `/agents`.
- Each subagent gets its own working context and reports results upward.
- Internally, the SDK exposes this as an `invoke_subagent`-style capability
  (see [sdk.md](./sdk.md)).

---

## Background & scheduled tasks (sidecars)

Antigravity supports work that outlives a single turn:

- **Background tasks** — long-running operations the agent kicks off and monitors
  while you keep working (track with `/tasks`).
- **Scheduled tasks ("cron sidecars")** — recurring background tasks and
  one-time delayed timers. These are surfaced prominently in the Antigravity 2.0
  desktop app's **Scheduled Tasks** sidebar.

> Sidecars/scheduled tasks are documented at
> `https://antigravity.google/docs/sidecars`. The CLI's exact controls for
> scheduling are thinner than the desktop app's — verify in official docs.

---

## How the pieces compose

```
You: high-level task
        │
        ▼
   ┌─────────┐   plan      ┌──────────────────┐
   │  Agent  │────────────►│ Task List /       │  ← you review/comment
   │ (Gemini)│             │ Implementation Plan│
   └────┬────┘             └──────────────────┘
        │ execute
        ├── edit files / run commands  ──► gated by permissions + sandbox
        ├── call MCP tools             ──► external systems
        ├── delegate ──► subagents (async)
        │ verify
        └── drive browser ──► screenshots + Walkthrough recording
```

---

## See also

- [models.md](./models.md) — which model powers the agent, and effort tiers
- [permissions.md](./permissions.md) — what the agent is allowed to do
- [customization.md](./customization.md) — rules & skills that steer the agent
- [mcp.md](./mcp.md) — giving the agent external tools
