# Overview: What Bob Is

**Bob** is a highly skilled AI software engineer assistant — a configured,
mode-switched Claude instance delivered through the Bob application by
matrixbuilderops. It is not a standalone CLI binary; it runs as a Claude session
with a custom role definition, a fixed tool set per mode, and an extensible skill
system.

---

## How Bob differs from raw Claude Code

| Aspect | Raw Claude Code (`claude`) | Bob |
|---|---|---|
| Role | General assistant | Software engineer persona with strict engineering discipline |
| Modes | No mode concept | Agent, Plan, Ask — each with different tool sets |
| Skills | SKILL.md files in `.claude/skills/` | SKILL.md files in `.agents/skills/` — same format |
| Instruction file | `CLAUDE.md` | `AGENTS.md` or mode frontmatter |
| Hook system | Full Claude hooks (30 events) | Inherits full Claude hooks unchanged |
| MCP servers | Configured per project | filelens + sitemap bundled; others addable |
| Enforcement | Optional cli-enforcement | cli-enforcement deployable via `cli-enforcement deploy bob` |

---

## The engineering discipline

Bob follows hard rules baked into its role definition:

- **Never speculate about code it has not opened.** Read files before answering questions about them.
- **Produce the minimal change that solves the problem.** No unrequested features, refactors, or abstractions.
- **No error handling for scenarios that cannot happen.**
- **Do not clean up surrounding code unrelated to the task.**
- **Every changed line must trace directly to the user's request.**
- **Validate before reporting completion** — run lint, tests, typecheck, build, or whatever applies.

These are enforced by the role definition, not by hooks. For hard enforcement
(blocking edits below a points threshold, anti-hallucination checks, KB gates)
deploy cli-enforcement: `cli-enforcement deploy bob --write`.

---

## What Bob can do

The full tool set depends on the active mode (see [modes.md](./modes.md)), but
across all modes Bob can:

- Read, write, search, and edit files
- Execute shell commands (Agent mode only)
- Search the Bob documentation (`search_bob_docs`)
- Browse websites via the sitemap MCP server
- Read file structure via the filelens MCP server
- Activate skills on demand
- Spawn independent subagents for focused side work
- Switch modes mid-session

---

## What Bob cannot do

- **No standalone CLI.** There is no `bob` binary — you interact through the Bob application UI or API.
- **No version flag.** Bob's version is tied to the application release.
- **No `--headless` or `-p` mode.** Bob is interactive-first.

---

## Sources

Bob application documentation, the Bob system role definition, and the installed skill files at `.agents/skills/`. Accessed 2026-08.
