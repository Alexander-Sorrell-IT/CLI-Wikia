# Tools

Bob's available tools depend on the active mode. This is the complete tool
inventory across all modes.

---

## Tool availability by mode

| Tool | Agent | Plan | Ask |
|---|---|---|---|
| `use_skill` | ✅ | ✅ | ✅ |
| `apply_diff` | ✅ | ✅ | — |
| `insert_content` | ✅ | ✅ | — |
| `list_files` | ✅ | ✅ | ✅ |
| `read_file` | ✅ | ✅ | ✅ |
| `read_xlsx` | ✅ | ✅ | ✅ |
| `search_and_replace` | ✅ | ✅ | — |
| `update_todo_list` | ✅ | — | — |
| `switch_mode` | ✅ | ✅ | — |
| `write_file` | ✅ | ✅ | — |
| `execute_command` | ✅ | — | — |
| `search_bob_docs` | ✅ | ✅ | ✅ |
| `spawn_subagent` | ✅ | ✅ | ✅ |
| `mcp__filelens__*` | ✅ | ✅ | ✅ |
| `mcp__sitemap__*` | ✅ | ✅ | ✅ |

---

## File editing tools

**Prefer editing tools over `write_file` for existing files.**

| Tool | When to use |
|---|---|
| `apply_diff` | Surgical edits to existing files — specific sections. Multiple SEARCH/REPLACE blocks in one call. |
| `search_and_replace` | Find-and-replace a pattern across a file, with optional line range. |
| `insert_content` | Add new lines at a specific position without modifying existing content. |
| `write_file` | Creating new files, or intentional full rewrites. Always provide COMPLETE content. |

---

## Execution tool

`execute_command` — run a CLI command. Available in Agent mode only.

- Use for builds, tests, git operations, system operations
- Prefer relative paths; avoid `cd` — use the `cwd` parameter instead
- Don't use for long-running servers or watchers — ask the user to run those
- Chain dependent commands with `&&`; use `;` only when failure of earlier commands doesn't matter

---

## Subagent tool

`spawn_subagent` — create an independent agent with its own context.

Use only when ALL of these apply:
- The task is clearly self-contained
- It would add significant irrelevant content to current context
- You cannot accomplish it with 1-2 direct tool calls

Types: `"explore"` (read tools, explorer model), `"general"` (inherits current mode tools).

Set `fork_context=true` when the subagent needs to understand prior conversation.

---

## Documentation search

`search_bob_docs` — semantic search over Bob's documentation. Use when the user
asks about Bob's features, configuration, tools, modes, or capabilities.

---

## Todo tracking

`update_todo_list` — replace the current todo list with an updated checklist.
Use for complex multi-step tasks. Mark items `[x]` completed, `[-]` in progress,
`[ ]` pending. Only available in Agent mode.

---

## Sources

Bob application documentation and tool descriptions. Accessed 2026-08.
