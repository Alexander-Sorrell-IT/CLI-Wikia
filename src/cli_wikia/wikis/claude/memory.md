# Memory: CLAUDE.md and Auto-Memory

Claude Code has **two** memory systems that work together but are written by different parties: `CLAUDE.md` (you write it) and **auto-memory** (Claude writes it).

---

## CLAUDE.md — you write this

Plain markdown that loads at session start. It's *context*, not *enforced rules* — Claude tries to follow it but isn't required to.

### Hierarchy (highest → lowest precedence)

| Scope | Path | Shared via git? | Enforced? |
|---|---|---|---|
| Managed (org policy) | `/etc/claude-code/CLAUDE.md` (Linux), `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `C:\Program Files\ClaudeCode\CLAUDE.md` | Yes (IT) | Yes |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Yes | No |
| User | `~/.claude/CLAUDE.md` | No | No |
| Local | `./CLAUDE.local.md` | No (gitignored) | No |

### Loading order

1. Walk up the directory tree from cwd, loading every `CLAUDE.md` and `CLAUDE.local.md` found.
2. Within each dir, `CLAUDE.md` is loaded first, then `CLAUDE.local.md` is appended (so local conflicts win).
3. Nested `CLAUDE.md` files in subdirectories load lazily when Claude reads files there.
4. All files are concatenated into context — they don't override each other.

### Imports

```markdown
See @README.md for overview, @docs/architecture.md for design.
@~/.claude/global-rules.md
```

- Relative paths resolve relative to the importing file.
- Max 5 import hops.
- `@~/path` references your home dir.

### Path-scoped rules

Put files in `.claude/rules/*.md` with frontmatter `paths: ["src/**/*.ts"]`. They only load when Claude opens matching files. Reduces noise.

```markdown
---
paths: ["src/api/**/*.ts"]
---
API handlers always validate input with Zod before processing.
```

### `--add-dir` and CLAUDE.md

CLAUDE.md files in `--add-dir` directories are **not loaded by default**. To load them, set:
```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

### Sizing

- Keep CLAUDE.md under ~200 lines. More tokens = less adherence.
- Use specific instructions ("Use 2-space indentation, never tabs") not vague ones ("Format code nicely").
- Block comments `<!-- maintainer note -->` are stripped before injection (no token cost).

### Example

```markdown
# Project: MyApp

Build: `npm run build`
Test:  `npm test`

## Code style
- 2-space indent (never tabs)
- async/await, not callbacks
- JSDoc for all public functions

## Architecture
- API handlers: src/api/handlers/
- Migrations:    migrations/
- Tests must pass before commit

## Workflows
- Use /code-review before PRs
- Use /test-debug when tests fail
```

---

## Auto-Memory — Claude writes this

Claude automatically saves discovered facts (build commands, conventions, your preferences) to `~/.claude/projects/<project>/memory/`. This is per-project and **machine-local** — not synced.

### Layout

```
~/.claude/projects/<project>/memory/
├── MEMORY.md              # Index — first ~200 lines load at startup
├── debugging.md           # On-demand topic file
├── api-conventions.md     # On-demand topic file
└── …
```

### Memory types

The auto-memory system organizes notes into four types:

| Type | What it stores | Example |
|---|---|---|
| **user** | Role, expertise, preferences | "User is a senior Go engineer, new to React" |
| **feedback** | Corrections + validated approaches you've given | "Don't mock the database — past incident with mocks passing while migrations failed" |
| **project** | What's currently happening | "Merge freeze 2026-03-05; mobile cutting release" |
| **reference** | Pointers to external systems | "Pipeline bugs tracked in Linear project INGEST" |

### Settings

```json
{
  "autoMemoryEnabled": true,
  "autoMemoryDirectory": "~/custom-memory-dir"
}
```

### How it works

1. Claude reads the first ~200 lines of `MEMORY.md` at session start.
2. During the session, Claude reads/writes topic files on demand.
3. `MEMORY.md` stays a concise index; details live in topic files.
4. `/memory` shows everything — both CLAUDE.md and auto-memory — and lets you browse/edit/delete.

### Subagent memory

Subagents can have their own auto-memory by setting:

```yaml
---
memory: project   # or 'user' or 'local'
---
```

Stored at `~/.claude/projects/<project>/memory/agents/<agent-name>/`.

### What NOT to save

- Code patterns/conventions — readable from the codebase.
- Git history / who changed what — `git log` is authoritative.
- Debugging fix recipes — the fix is in the code; the commit message has the why.
- Anything in CLAUDE.md.
- Ephemeral task state — use TaskCreate, not memory.

### Auto-memory vs CLAUDE.md

| | CLAUDE.md | Auto-Memory |
|---|---|---|
| Author | You | Claude |
| When | Known conventions | Discovered patterns |
| Scope | Per dir / project | Per project (machine-local) |
| Load | Full content | First ~200 lines + on-demand |
| Use for | Standards, build commands, architecture | Build details Claude figured out, your stated preferences, who-does-what |

---

## The `/memory` command

In the REPL:

```
/memory          # Show all memory sources (CLAUDE.md + auto-memory)
```

You can browse, edit, and delete entries through this UI.

---

## The `/remember` skill (some plugins)

Some plugin setups (notably the included `remember` skill) save session state in `.remember/` directories within projects:

```
.remember/
├── now.md             # Current session buffer
├── today-2026-04-26.md   # Daily snapshots
├── recent.md          # Last 7 days
├── archive.md         # Historical
└── core-memories.md   # Key moments
```

This is separate from auto-memory. The `/remember` skill writes here so the next session can pick up where you left off.

---

## See also

- [skills.md](./skills.md) — `disable-model-invocation` for skills that should only fire on `/`
- [settings.md](./settings.md) — `autoMemoryEnabled`, `autoMemoryDirectory`
- [permissions.md](./permissions.md) — `additionalDirectories`
