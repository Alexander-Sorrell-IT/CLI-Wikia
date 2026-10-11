# Modes

Bob has three modes. Each mode has its own tool set and role optimisation.
Switch with the mode switcher in the Bob UI, or Bob will switch automatically
when the task requires it.

---

## Mode comparison

| Mode | ID | When to use | Can execute commands? | Can write files? |
|---|---|---|---|---|
| **Agent** | `agent` | Writing, modifying, refactoring code; implementing features; fixing bugs | **Yes** | **Yes** |
| **Plan** | `plan` | Planning, designing, architecture; breaking down complex problems before coding | No | **Yes** (docs/specs only) |
| **Ask** | `ask` | Questions about Bob itself, general technical questions, documentation lookup; no code changes | No | No |

---

## Agent mode

**Use when:** writing, modifying, or refactoring code in any language.

Available tools:
- `use_skill`, `apply_diff`, `insert_content`, `list_files`, `read_file`, `read_xlsx`
- `search_and_replace`, `update_todo_list`, `switch_mode`, `write_file`
- `execute_command` — **only in this mode**
- `search_bob_docs`, `spawn_subagent`
- All MCP tools: `mcp__filelens__*`, `mcp__sitemap__*`

Key behaviours:
- Runs `execute_command` for builds, tests, git, and system operations
- Validates changes before reporting done (lint / tests / typecheck / build)
- Uses `update_todo_list` to track progress on multi-step tasks
- Prefers editing tools (`apply_diff`, `search_and_replace`) over `write_file` for existing files

---

## Plan mode

**Use when:** the problem needs thinking, designing, or speccing before any code is written.

Available tools:
- `use_skill`, `apply_diff`, `insert_content`, `list_files`, `read_file`, `read_xlsx`
- `search_and_replace`, `switch_mode`, `write_file`
- `search_bob_docs`, `spawn_subagent`
- All MCP tools: `mcp__filelens__*`, `mcp__sitemap__*`
- **No `execute_command`, no `update_todo_list`**

Key behaviours:
- Reads and analyses code without running it
- Creates technical specs, architecture docs, and implementation plans
- Breaks down complex problems into actionable steps
- Switches to Agent mode when it's time to implement

---

## Ask mode

**Use when:** asking about Bob itself (features, tools, modes, config) or general
technical questions that don't need code changes.

Available tools:
- `use_skill`, `list_files`, `read_file`, `read_xlsx`
- `search_bob_docs`, `spawn_subagent`
- All MCP tools: `mcp__filelens__*`, `mcp__sitemap__*`
- **No write tools, no execute_command**

Key behaviours:
- Looks up Bob documentation via `search_bob_docs`
- Reads files to give grounded, accurate answers
- Does not make code changes
- Switches to Agent or Plan when the user wants to act

---

## Switching modes

Bob switches automatically when a task clearly requires a different mode, or
when the user asks explicitly. The `switch_mode` tool is available in Agent and
Plan modes. Ask mode cannot switch itself — the user must request it.

```
"switch to agent mode" → switches to agent
"switch to plan mode"  → switches to plan
"switch to ask mode"   → switches to ask
```

---

## Sources

Bob application documentation and role definitions. Accessed 2026-08.
