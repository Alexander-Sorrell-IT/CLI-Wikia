# Agent Teams

Coordinate multiple Claude Code instances working together. One session is the **lead**, coordinating work; **teammates** run in their own context windows and can communicate directly with each other.

> Experimental — disabled by default. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Requires Claude Code v2.1.32+.

Unlike [subagents](./agents.md), which run within a single session and only report back to the main agent, agent teams let you also interact with each teammate directly without going through the lead.

---

## When to use

| Use case | Why teams help |
|---|---|
| Research and review | Multiple teammates investigate different aspects in parallel and challenge each other |
| New modules / features | Each teammate owns a separate piece; no stepping on toes |
| Debugging with competing hypotheses | Teammates test different theories and converge faster |
| Cross-layer coordination | Frontend / backend / tests each owned by a different teammate |

Teams add **coordination overhead** and use **significantly more tokens** than a single session. Bad fit for sequential tasks, same-file edits, or work with tight dependencies.

---

## Subagents vs agent teams

| | Subagents | Agent teams |
|---|---|---|
| Context | Own window; results return to caller | Own window; fully independent |
| Communication | Report results to main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| Token cost | Lower (results summarized back) | Higher (each teammate is a separate Claude instance) |

Use **subagents** for quick focused workers that report back. Use **agent teams** when teammates need to share findings, challenge each other, and coordinate on their own.

---

## Enabling

```json
// settings.json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
}
```

Or set the env var directly.

---

## Starting a team

In natural language — Claude proposes the structure:

```
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles:
one teammate on UX, one on technical architecture, one playing devil's advocate.
```

Claude creates the team, spawns teammates, manages a shared task list, has them explore, synthesizes findings, and tries to clean up when finished.

Claude **won't create a team without your approval** — even if it proposes one.

---

## Display modes

| Mode | Behavior |
|---|---|
| **In-process** (default in plain terminals) | All teammates run in your main terminal. `Shift+Down` cycles through them. Type to message. |
| **Split panes** | Each teammate gets its own pane. Click into a pane to interact. Requires tmux or iTerm2. |

Set persistently:

```json
{ "teammateMode": "in-process" }   // or "tmux", or "auto" (default)
```

Override per-session:

```bash
claude --teammate-mode in-process
```

`auto` uses split panes if you're already in a tmux session, in-process otherwise. `tmux` enables split panes and auto-detects whether to use tmux or iTerm2 based on your terminal.

### Split-pane requirements

- **tmux**: install via package manager. iTerm2's `tmux -CC` is the suggested entry.
- **iTerm2**: install [`it2` CLI](https://github.com/mkusaka/it2), enable Python API in **iTerm2 → Settings → General → Magic → Enable Python API**.

Not supported: VS Code's integrated terminal, Windows Terminal, Ghostty.

---

## Specify teammates and models

```
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

Or let Claude decide based on the task.

---

## Plan approval gates

For complex/risky tasks, require teammates to plan before implementing:

```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

The teammate works in **read-only plan mode** until the lead approves. When done planning, it sends a plan-approval request. The lead reviews and either approves or rejects with feedback (revises and resubmits). Once approved, the teammate exits plan mode and begins implementation.

The lead makes approval decisions autonomously. To influence its judgment, give it criteria in your prompt: "only approve plans that include test coverage" or "reject plans that modify the database schema."

---

## Talking to teammates directly

Each teammate is a full, independent Claude Code session.

- **In-process**: `Shift+Down` to cycle through teammates, then type a message. `Enter` enters their session view, `Esc` interrupts their current turn. `Ctrl+T` toggles the task list.
- **Split panes**: click into a teammate's pane.

---

## Shared task list

Tasks have three states: pending, in_progress, completed. Tasks can also depend on each other; pending tasks with unresolved dependencies cannot be claimed.

Two ways to assign:

- **Lead assigns**: tell the lead which task to give to which teammate.
- **Self-claim**: after finishing a task, a teammate picks up the next unassigned, unblocked task.

Task claiming uses **file locking** to prevent race conditions.

---

## Shutting down teammates

```
Ask the researcher teammate to shut down
```

The lead sends a shutdown request. The teammate can approve (exits gracefully) or reject with an explanation.

---

## Cleanup

```
Clean up the team
```

Removes shared team resources. Cleanup checks for active teammates and fails if any are still running — shut them down first.

> Always use the **lead** to clean up. Teammates should not run cleanup because their team context may not resolve correctly.

---

## Quality gates via hooks

| Hook | When | Use |
|---|---|---|
| [`TeammateIdle`](./hooks.md) | A teammate is about to go idle | Exit code 2 → send feedback, keep them working |
| [`TaskCreated`](./hooks.md) | Task being created | Exit code 2 → prevent creation, send feedback |
| [`TaskCompleted`](./hooks.md) | Task being marked complete | Exit code 2 → prevent completion, send feedback |

---

## Architecture

| Component | Role |
|---|---|
| Team lead | Main session — creates team, spawns teammates, coordinates |
| Teammates | Separate Claude Code instances, each on assigned tasks |
| Task list | Shared work items teammates claim and complete |
| Mailbox | Messaging between agents |

Teammate messages arrive at the lead automatically. Task dependencies unblock automatically when prerequisites complete.

### Local storage

```
~/.claude/teams/{team-name}/config.json    # team config (runtime state)
~/.claude/tasks/{team-name}/                # task list
```

Both are auto-generated and updated as teammates join, idle, or leave. **Don't edit the config by hand or pre-author it** — your changes are overwritten on the next state update.

The team config contains a `members` array with each teammate's name, agent ID, and agent type. Teammates can read this file to discover other team members.

> No project-level equivalent. A `.claude/teams/teams.json` in your project is **not** recognized as configuration; Claude treats it as a regular file.

---

## Use subagent definitions for teammates

```
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

The teammate honors that subagent definition's `tools` allowlist and `model`, and the definition's body is **appended** to the teammate's system prompt as additional instructions (not replacing it). Team coordination tools (`SendMessage`, task tools) are always available even when `tools` restricts other tools.

> The `skills` and `mcpServers` fields in a subagent definition are **not applied** when that definition runs as a teammate. Teammates load skills and MCP servers from your project and user settings, the same as a regular session.

---

## Permissions

Teammates start with the lead's permission settings. If the lead runs with `--dangerously-skip-permissions`, all teammates do too. After spawning, you can change individual teammate modes — but you **can't set per-teammate modes at spawn time**.

---

## Context and communication

Each teammate has its own context. On spawn it loads the same project context as a regular session: CLAUDE.md, MCP servers, skills. **The lead's conversation history does not carry over** — it gets the spawn prompt only.

How teammates share info:

- **Automatic message delivery** — messages sent are delivered automatically; lead doesn't poll.
- **Idle notifications** — when a teammate finishes and stops, it auto-notifies the lead.
- **Shared task list** — all agents see status and claim work.
- **Teammate messaging** — send to one specific teammate by name. To reach everyone, send one message per recipient.

The lead names every teammate it spawns. To get **predictable names** for later prompts, tell the lead what to call each one in your spawn instruction.

---

## Token usage

Significantly more tokens than a single session. Each teammate has its own context. Worth it for research/review/new-feature work; not for routine tasks.

See [agent team token costs](https://code.claude.com/docs/en/costs#agent-team-token-costs).

---

## Best practices

1. **Give teammates enough context.** Project context loads automatically (CLAUDE.md, MCP, skills) but **not** the lead's history. Include task-specific details in the spawn prompt.
2. **Team size: 3–5 teammates** for most workflows. Coordination overhead grows; diminishing returns past that. Five focused beats five scattered.
3. **5–6 tasks per teammate** keeps everyone productive without context-switching. 15 independent tasks → 3 teammates is a good start.
4. **Size tasks "just right"**: too small wastes coordination; too large risks wasted effort. Self-contained units producing a clear deliverable.
5. **Wait for teammates to finish.** If the lead starts implementing instead of waiting: `Wait for your teammates to complete their tasks before proceeding`.
6. **Start with research/review.** New to teams? Begin with PR review or library research — clear boundaries, no parallel-implementation conflicts.
7. **Avoid file conflicts.** Two teammates editing the same file = overwrites. Break work so each teammate owns a different file set.
8. **Monitor and steer.** Check in, redirect approaches that aren't working, synthesize as findings come in.

---

## Use case examples

### Parallel code review

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Investigation with competing hypotheses

```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk
to each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

The debate structure is the key — sequential investigation suffers from anchoring; competing investigators with disprove-each-other prompts converge on the actual root cause.

---

## Limitations

- **No session resumption with in-process teammates.** `/resume` and `/rewind` don't restore them. The lead may try messaging non-existent teammates after resume — tell it to spawn new ones.
- **Task status can lag.** Teammates sometimes fail to mark complete, blocking dependents. Update manually or nudge the teammate.
- **Shutdown can be slow.** Teammates finish current request/tool call before exiting.
- **One team per session.** Clean up before starting a new one.
- **No nested teams.** Teammates can't spawn their own teams or teammates.
- **Lead is fixed.** No promotion or transfer of leadership.
- **Permissions set at spawn.** Per-teammate modes only after spawning.
- **Split panes need tmux/iTerm2.** Not supported in VS Code, Windows Terminal, Ghostty.

---

## Troubleshooting

- **Teammates not appearing**: in in-process mode they may already be running but not visible — `Shift+Down`. Or check tmux is installed (`which tmux`) for split panes. For iTerm2, verify `it2` CLI installed and Python API enabled.
- **Too many permission prompts**: pre-approve common ops in [permission settings](./permissions.md) before spawning teammates.
- **Teammates stopping on errors**: check output, give additional instructions directly, or spawn a replacement.
- **Lead shuts down before work is done**: tell it to keep going, or to wait for teammates to finish.
- **Orphaned tmux sessions**: `tmux ls` to list, `tmux kill-session -t <name>` to clean up.

---

## See also

- [agents.md](./agents.md) — subagents (lighter-weight delegation, single session)
- [hooks.md](./hooks.md) — `TeammateIdle`, `TaskCreated`, `TaskCompleted`
- [permissions.md](./permissions.md) — pre-approve ops to reduce prompts
- [cli-reference.md](./cli-reference.md) — `--teammate-mode`, `--tmux`
