# Projects, Sessions & Conversations

Antigravity separates three concepts that are easy to conflate: **projects**
(where work happens), **sessions** (a running instance of the CLI), and
**conversations** (the durable record of an interaction). Understanding the split
explains how resume, fork, and rewind behave.

```
Project (workspace)
   ├── Session  (one live `agy` run — ephemeral)
   └── Conversation history (durable, one UUID per thread)
         └── Subagent threads (async children)
```

---

## Projects (workspaces)

A **project** is the directory tree of source code the agent works on. It defines
the file-system boundary and security scope.

| Flag | Description |
|------|-------------|
| `--new-project` | Create a new project for this session |
| `--project <id>` | Use a specific project ID |
| `--add-dir <dir>` | Add extra directories to the workspace (repeatable) |

```bash
agy --new-project -i "scaffold a FastAPI service"
agy --project <id> -p "add tests for the user module"
```

Key properties:

- **Boundary enforcement.** By default the agent reads/writes only within the
  project root. Crossing that boundary is governed by `allowNonWorkspaceAccess`
  (see [sandbox.md](./sandbox.md)).
- **Trust.** A workspace must be trusted to grant execution rights; trusted paths
  are listed in `trustedWorkspaces` (see [permissions.md](./permissions.md)).
- **Per-project config & customizations.** Projects can override global settings
  (config under `~/.gemini/config/projects/`) and carry workspace-scoped rules
  and skills in `<project-root>/.agents/` (see [customization.md](./customization.md)).

Per-project configuration is resolved with **higher priority than the global
`settings.json`**.

---

## Sessions

A **session** is one live run of the `agy` TUI (or a one-shot `-p` invocation).
It is the *runtime* layer — ephemeral.

- **Lifecycle:** begins when you launch `agy`, ends at `/exit`, `/quit`,
  `Ctrl+D` (double, empty prompt), or process close.
- **Holds transient state:** which subagents are running (`/agents`), background
  task status (`/tasks`), context contents (`/context`), and token/quota usage
  (`/usage`).
- **Launch flags apply only to this session** — e.g. `--sandbox`, `--model`,
  `--add-dir` don't persist to config.
- **In-session controls** (slash commands) let you reshape the session live:
  `/add-dir`, `/clear`, `/model`, `/fast`, etc. (full list in
  [cli-reference.md](./cli-reference.md)).

---

## Conversations

A **conversation** is the **durable** record of prompts, agent reasoning, tool
calls, and responses. Unlike a session it survives restarts and is saved to disk.

- **Identity:** every conversation gets a UUID (e.g.
  `0dc79202-f007-48c4-8339-bd65fc6e9363`).
- **Storage:** metadata/index under `~/.gemini/antigravity-cli/conversations/<id>`
  and working memory + transcripts under
  `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/`
  (`transcript.jsonl` token-efficient, `transcript_full.jsonl` untruncated). See
  [configuration.md](./configuration.md) for the full layout.

### Resuming

| Method | Effect |
|--------|--------|
| `agy -c` / `agy --continue` | Resume the most recent conversation in this workspace |
| `agy --conversation <id>` | Resume a specific conversation |
| `/resume`, `/switch`, `/conversation` | In-session picker to jump to a past thread |

### Forking & rewinding

| Command | Effect |
|---------|--------|
| `/fork` or `/branch` | Duplicate the current conversation state into a new thread — explore an alternative from a checkpoint without touching the original |
| `/rewind` or `/undo` | Roll the current conversation back to an earlier checkpoint |
| `/rename` | Give the conversation a human-readable name |

Forking is useful for "try approach B" without losing approach A; rewinding is
useful for backing out of a wrong turn.

### Subagent threads

Invoking a subagent creates a **child conversation thread** that runs
asynchronously and reports back to the parent — see
[agentic-model.md](./agentic-model.md#subagents).

---

## See also

- [configuration.md](./configuration.md) — exact on-disk layout and config precedence
- [cli-reference.md](./cli-reference.md) — every resume/fork/rewind command and flag
- [agentic-model.md](./agentic-model.md) — subagents and background/scheduled tasks
