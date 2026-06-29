# Sessions & the REPL

DeepSeek Code is session-based: each conversation is persisted (when
`sessionPersistence` is on) so you can pause and resume it later. This page covers
starting, continuing, and resuming sessions; the interactive REPL; and print mode for
scripting.

---

## Starting a session

| Action | Command |
|--------|---------|
| New interactive REPL | `deepseek-code` |
| REPL with an opening prompt | `deepseek-code "explain this repo"` |
| Named session | `deepseek-code -n "auth-refactor"` |
| Specific session ID | `deepseek-code --session-id <uuid>` |
| One-shot, non-interactive | `deepseek-code -p "fix the bug"` |

A bare REPL starts on the **Flash** model by default; add `--model pro` to start on
Pro.

## Continuing and resuming

| Action | Command |
|--------|---------|
| Continue the most recent session in the cwd | `deepseek-code -c` |
| Continue it non-interactively | `deepseek-code -c -p "keep going"` |
| Resume a specific session by ID | `deepseek-code -r <id> "next step"` |
| List saved sessions | `deepseek-code sessions` |

`-c` is scoped to the current working directory — it picks up the latest session you
ran *there*. Use `-r <id>` to jump to any session regardless of directory.

### Session flags

| Flag | Description |
|------|-------------|
| `--name`, `-n <name>` | Set a display name |
| `--continue`, `-c` | Resume the most recent session in the cwd |
| `--resume`, `-r <id>` | Resume a specific session |
| `--print`, `-p [query]` | Print mode (non-interactive) |
| `--session-id <uuid>` | Use a specific session ID |

---

## Where sessions live

Sessions are stored under `~/.deepseek-code/sessions/`. Persistence is controlled by
the `sessionPersistence` field in `~/.deepseek-code/config.json`; with it off, runs
are ephemeral and `deepseek-code sessions` shows nothing.

The Clawspring harness config bounds session usage (see
[configuration.md](configuration.md)):

- `session_daily_limit: 10` — sessions per day
- `session_history_limit: 200` — lines of history/memory loaded into context

---

## Print mode (`-p`)

Print mode runs a single turn (or an agentic loop bounded by `--max-turns`) and exits,
writing the result to stdout. It is the path for scripting and CI:

```bash
deepseek-code -p "summarize the diff"           # one-shot
cat logs.txt | deepseek-code -p "explain this"  # piped stdin
deepseek-code --bare -p "lint and fix"          # no extension discovery
deepseek-code -p "do the task" \
  --output-format json --max-turns 8 --max-budget-usd 0.50
```

Pair `-p` with:

- `--output-format text|json|stream-json` — structured output for parsing
- `--max-turns <N>` and `--max-budget-usd <amount>` — hard bounds on an autonomous run
- `--bare` — skip hooks/skills/plugins/CLAUDE.md for a deterministic run

---

## The interactive REPL

Inside the REPL you drive the session with slash commands. The full set
(`deepseek-code help --all`):

| Command | Action |
|---------|--------|
| `/help` | Show available commands |
| `/model [pro\|flash]` | Switch model |
| `/effort [level]` | Set effort (low/medium/high/max) |
| `/compact [focus]` | Compress conversation history (optionally around a focus) |
| `/init` | Generate a CLAUDE.md for the current project |
| `/memory` | View/edit project memory |
| `/hooks` | List active hooks |
| `/agents` | List subagents |
| `/skills` | List skills |
| `/permissions` | View/edit permission rules |
| `/config` | Show current configuration |
| `/cost` | Show token usage & cost for the session |
| `/status` | Show session status |
| `/resume` | Open the session picker |
| `/rename <name>` | Rename the current session |
| `/export` | Export the session to a file |
| `/tasks` | Manage the task list |
| `/feedback` | Send feedback |
| `/exit` | Exit the REPL |

`/compact` is worth knowing: it summarizes the conversation so a long session stays
within the context window. A `PreCompact` hook can run before it to preserve anything
important (see [hooks.md](hooks.md)).

---

## Tasks

The session carries a task list, surfaced with `/tasks` and managed by the `Task*`
tools (`TaskCreate`, `TaskUpdate`, `TaskGet`, `TaskList`). `TaskCreated` and
`TaskCompleted` are hook events, so task creation/completion can be gated or logged.

---

## Related

- [models.md](models.md) — `/model`, `/effort`, switching mid-session
- [cli-reference.md](cli-reference.md) — every flag and subcommand
- [hooks.md](hooks.md) — `SessionStart`, `SessionEnd`, `PreCompact`, `Stop`
- [architecture.md](architecture.md) — what loads into a session at startup
