# Bob: The Complete Wiki

A reference for **Bob** — the AI software engineering assistant built on top of
Claude, shipped as a custom mode system by matrixbuilderops. Bob runs inside the
Bob application (a desktop AI coding assistant) and is accessed through
mode-switching: each mode has its own tool set, role definition, and available
skills.

> Documented against the Bob system as of 2026-08. Bob is NOT a standalone CLI
> binary — it is a configured Claude instance. There is no `bob --help` or
> `bob --version`. All facts here are sourced from the Bob system itself and
> the `.agents/skills/` directory on this machine.

## Topics

- [overview.md](./overview.md) — what Bob is, modes, how it differs from raw Claude
- [modes.md](./modes.md) — Agent, Plan, Ask modes and when to use each
- [skills.md](./skills.md) — the skill system: activation, SKILL.md format, available skills
- [hooks.md](./hooks.md) — hook events Bob inherits from Claude Code
- [mcp.md](./mcp.md) — MCP servers available (filelens, sitemap, and others)
- [tools.md](./tools.md) — all tools available per mode
- [configuration.md](./configuration.md) — custom modes, profiles, workspace config
- [memory.md](./memory.md) — how Bob maintains context across sessions
- [enforcement.md](./enforcement.md) — the cli-enforcement point system deployed on Bob
- [cli-reference.md](./cli-reference.md) — Bob slash commands and interaction patterns

## Key facts

| Property | Value |
|---|---|
| Binary / entrypoint | No standalone binary — accessed through the Bob application |
| Underlying model | Claude (Anthropic) |
| Config dir | `.agents/` (workspace) / `~/.config/bob/` (user) |
| Hook system | Inherits Claude Code's full hook system (30 events) |
| Instruction file | `AGENTS.md` or mode-specific frontmatter |
| Skills dir | `.agents/skills/` |

## Sources

Bob system documentation and the installed skill files at `.agents/skills/` on this machine. Accessed 2026-08.
