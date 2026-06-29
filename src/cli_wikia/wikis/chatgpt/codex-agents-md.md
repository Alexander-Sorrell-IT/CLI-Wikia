# AGENTS.md — Project Instructions

`AGENTS.md` is Codex's always-loaded instruction file — the equivalent of Claude Code's `CLAUDE.md`. Codex reads it **before doing any work**. From OpenAI's [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) guide.

> **Not locally verified** — sourced from official docs. Confirm discovery behavior with `/init` and a test repo after installing Codex.

---

## What it is

A plain Markdown file describing how an agent should work in this project: build/test commands, the package manager, coding conventions, lint rules, do/don't lists, approval expectations. Generate a starter file with the `/init` slash command.

---

## Discovery & precedence

Codex builds an **instruction chain** with strict precedence, then concatenates the pieces.

**1. Global scope (`~/.codex`)** — checked first, but lowest priority in the merged prompt:
- `AGENTS.override.md`, then `AGENTS.md` — only the **first non-empty** file loads.

**2. Project scope (git root → current directory)** — walking *downward* from the repo root, in each directory Codex looks for, in order:
- `AGENTS.override.md`
- `AGENTS.md`
- any configured fallback filename (e.g. `TEAM_GUIDE.md`, `.agents.md`)
- **At most one file per directory** loads.

**Stops at the current working directory** — it does not descend into directories below your cwd.

### How they merge

Files concatenate from **root downward**, separated by blank lines. Because files closer to your cwd appear **later** in the combined prompt, they **override** earlier (higher-level) guidance.

```
~/.codex/AGENTS.md            ← global defaults (loaded first, weakest)
<repo>/AGENTS.md              ← repo-wide norms
<repo>/services/api/AGENTS.md ← service-specific overrides (loaded last, strongest)
```

The combined content is capped at `project_doc_max_bytes` (**32 KiB** default). When the cap is hit, remaining files are skipped — so place the most specific overrides closest to the work.

---

## Configuration

In `~/.codex/config.toml` (see [codex-config.md](./codex-config.md)):

```toml
project_doc_max_bytes = 65536                                 # raise the 32 KiB cap
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
```

`CODEX_HOME` changes where the global `~/.codex/AGENTS.md` is read from.

---

## What to put where

| Level | Typical content |
|---|---|
| Global (`~/.codex/AGENTS.md`) | Personal working agreements: preferred package managers, test commands, approval habits across all your repos |
| Project root | Repo norms: how to build/test/lint, architecture notes, conventions, "never touch X" |
| Nested directory | Team- or service-specific rules that refine (not replace) parent guidance |

### Example

```markdown
# AGENTS.md

## Commands
- Install: `pnpm install`
- Test: `pnpm test` (run before claiming done)
- Lint: `pnpm lint --fix`

## Conventions
- TypeScript strict mode; no `any`.
- Prefer named exports.
- Don't edit files under `generated/`.

## Approvals
- Ask before deleting files or running migrations.
```

---

## See also

- [codex-config.md](./codex-config.md) — `project_doc_max_bytes`, `project_doc_fallback_filenames`
- [codex-slash-commands.md](./codex-slash-commands.md) — `/init` scaffolds an `AGENTS.md`
- [codex-overview.md](./codex-overview.md) — where AGENTS.md sits in the model
