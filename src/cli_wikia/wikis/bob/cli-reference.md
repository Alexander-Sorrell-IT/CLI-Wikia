# Bob Interaction Reference

Bob has no `--help` flag or CLI subcommands — it is interactive-first. This
page documents the interaction patterns, slash commands, and natural language
triggers that control Bob's behaviour.

---

## Mode switching

| Command | Effect |
|---|---|
| `"switch to agent mode"` | Switch to Agent mode (write/execute) |
| `"switch to plan mode"` | Switch to Plan mode (design/spec) |
| `"switch to ask mode"` | Switch to Ask mode (questions/docs) |

---

## Skill activation

| Command | Effect |
|---|---|
| `"use the <skill-name> skill"` | Activate a skill by name |
| `"activate <skill-name>"` | Same |

Bob also auto-activates skills when the task description matches.

---

## Enforcement commands (when cli-enforcement is deployed)

| Command | Effect |
|---|---|
| `"unlock enforcement"` | 10-minute bypass window for editing enforcement files |
| `"recover points"` | Manually recover points (user-initiated only) |
| `"reset"` / `"/reset"` | Clear hard stop |
| `"/workflow start <description>"` | Start a new workflow (creates PRE snapshot) |
| `"/workflow verify"` | Run verification on current workflow |
| `"/workflow approve"` | Approve workflow (creates POST snapshot) |
| `"/workflow reset"` | Reset workflow to IDLE (optionally rollback) |
| `"/section start <id>"` | Start a new section within a workflow |
| `"/section finish <id>"` | Finish current section (creates POST snapshot) |

---

## Todo tracking commands

Bob uses `update_todo_list` automatically on complex tasks. You can also ask:

| Command | Effect |
|---|---|
| `"show the todo list"` | Display current task progress |
| `"mark that as done"` | Update the most recent in-progress task |
| `"add a todo: <description>"` | Add a new task to the list |

---

## Bob documentation search

| Command | Effect |
|---|---|
| `"how do hooks work in Bob?"` | Bob searches its own docs via `search_bob_docs` |
| `"what modes does Bob have?"` | Same |
| `"wikia read bob <topic>"` | Read a specific Bob wiki topic from the CLI |

---

## Subagent spawning

Bob spawns subagents automatically for focused side work. You can also direct:

| Command | Effect |
|---|---|
| `"explore the codebase and tell me how X works"` | Spawns an explore subagent |
| `"check if there are any tests for this"` | May spawn a subagent to investigate |

---

## Sources

Bob application documentation and interaction patterns. Accessed 2026-08.
