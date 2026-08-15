# Memory

Bob uses the same two memory systems as Claude Code: **AGENTS.md** (you write it)
and **auto-memory** (Bob writes it when it learns something worth keeping).

---

## AGENTS.md

The primary memory file. Bob reads it at session start via `InstructionsLoaded`.

- Location: `<project-root>/AGENTS.md`
- You write and maintain it
- Put: project architecture, coding conventions, recurring constraints, context Bob should always have
- Bob will suggest additions during sessions when it learns something new

---

## Auto-memory

Bob can write to `~/.config/bob/AGENTS.md` (user-level) or `<project>/.agents/memory/` (project-level) during a session when it determines something is worth persisting.

Auto-memory is triggered when Bob:
- Learns a user preference that should persist
- Discovers a project fact that will be relevant in future sessions
- Completes a task where the approach should be remembered

---

## Session continuity

Bob does not have persistent memory across sessions by default — each session
starts fresh. AGENTS.md is the bridge: anything Bob needs to know next session
should be in AGENTS.md.

When cli-enforcement is deployed, the session init hook (`session_init.py`)
reads `.agents/.session_lessons_summary.md` and injects it as additional
context at session start — giving Bob a summary of lessons from previous sessions.

---

## Hunt memory (security skills)

The security skills (`bug-bounty`, `bb-methodology`) maintain their own
hunt-memory JSONL files:

| File | Contents |
|---|---|
| `.agents/memory/audit.jsonl` | Audit log of findings and actions |
| `.agents/memory/patterns.jsonl` | Vulnerability patterns discovered |
| `.agents/memory/journal.jsonl` | Session journal entries |

Use the `source-command-memory-gc` skill to inspect or rotate these files.

---

## Sources

Bob application documentation. Accessed 2026-08.
