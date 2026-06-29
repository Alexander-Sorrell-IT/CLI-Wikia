# Modes & Autonomy

Copilot CLI can run at different levels of autonomy — from asking before every action, to planning first, to running unattended, to handing the whole task to GitHub's cloud agent.

---

## The three agent modes

Set the starting mode with `--mode <interactive|plan|autopilot>`, or the shortcut flags `--plan` / `--autopilot`. Switch live with `/plan`, `/autopilot`, or Shift+Tab.

| Mode | Behavior |
|---|---|
| `interactive` | Default. Chats and acts, but asks for approval on file edits and commands |
| `plan` | Produces an implementation plan *before* writing code — good for reviewing an approach with your team first |
| `autopilot` | Runs more autonomously, continuing through multi-step work without stopping for each approval |

```bash
copilot --plan -i "design the migration"
copilot --autopilot -p "implement the migration" --allow-all-tools
```

### Plan mode

Plan mode decomposes a task into steps you can review and edit (open it in your editor via `COPILOT_EDITOR`/`EDITOR`). It's a collaborative step, not a commitment — you approve before execution. In OTel traces it shows up as a dedicated `plan` span.

### Autopilot mode

Autopilot keeps the agent moving through continuation steps on its own. To stop usage running away unattended, it **pauses after a number of automatic continuations** (default **5**):

```bash
copilot --autopilot --max-autopilot-continues 20 -p "build and test" --allow-all-tools
```

Autopilot is most useful combined with broad permissions and `--no-ask-user`:

```bash
copilot --autopilot --allow-all --no-ask-user -p "run the full workflow"
```

---

## Fleet mode (parallel subagents)

`/fleet` enables **fleet mode**, running multiple subagents in parallel. Subagents are isolated workers Copilot spins up for sub-tasks (exploration, execution, review, research, general-purpose). Manage them with:

- `/tasks` — view and manage tasks (subagents and shell commands).
- `/sidekicks` — view running sidekick agents.
- `/subagents` — configure default and per-agent subagent models (each field can `inherit` the parent session's model/effort/context). Persisted under `subagents.agents.<name>` in `settings.json`.

---

## Delegating to the cloud coding agent

`/delegate` sends the current session to GitHub, where the **Copilot coding agent** continues the work in the cloud and opens a **pull request** for you. This is different from local autopilot — the work runs on GitHub's infrastructure, not your machine.

Related session bridges:

- `--remote` / `/remote` — let GitHub web and mobile **control** your running local session.
- `--remote-export` — **export** the session read-only to web/mobile (no control).
- `--connect[=sessionId]` — attach directly to a remote session/task.

---

## Choosing a mode

| You want to… | Use |
|---|---|
| Stay in the loop, approve each step | `interactive` (default) |
| Agree on an approach before any code | `plan` (`--plan`, Shift+Tab) |
| Let it grind through a well-scoped task | `autopilot` + permissions |
| Parallelize independent sub-tasks | `/fleet` |
| Offload the whole task and get a PR | `/delegate` |

---

## See also

- [permissions.md](permissions.md) — what autonomy needs in terms of grants
- [slash-commands.md](slash-commands.md) — `/plan`, `/autopilot`, `/fleet`, `/delegate`, `/tasks`
- [sessions.md](sessions.md) — remote control and export
