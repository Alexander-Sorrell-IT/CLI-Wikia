# DeepSeek Code: The Complete Wiki

A reference for **DeepSeek Code** (`deepseek-code`) — a terminal coding agent that
pairs the **DeepSeek V4** model family with the **Clawspring Agent Runtime**. The
tool self-describes as a "DeepSeek V4 × Claude Code Hybrid": its CLI surface,
extension model (hooks, agents, skills, permissions, plugins), and on-disk layout
are closely modeled on Claude Code, while the model behind it is DeepSeek V4
(Pro 1.6T / Flash 284B).

- **Command:** `deepseek-code`
- **Version referenced:** 2.0.0 (Clawspring `v3.05.5`)
- **Backend:** DeepSeek V4 — Pro 1.6T MoE / Flash 284B MoE, 1M context
- **Runtime:** Clawspring Agent Runtime

> **Sourcing & accuracy.** This wiki was assembled by interrogating the installed,
> authenticated tool directly (`deepseek-code -p`, `--help`, and its read-only
> `config`/`agents`/`skills`/`hooks` subcommands) and by reading its real on-disk
> configuration under `~/.deepseek-code/` and `~/.clawspring/`. DeepSeek V4 model
> facts (parameter counts, 1M context) are corroborated by public sources. The
> **Clawspring runtime and the `deepseek-code` CLI itself have no public
> documentation** — everything here is from the tool as installed on this machine.
> Where a detail is the harness's own behavior and could differ across versions, it
> is marked *verify in the tool*.

---

## The mental model

Clawspring uses a **layered extensibility model** borrowed from Claude Code. Each
layer plugs into the same agentic loop, but they differ in *who* controls them — the
model, the user, or the harness.

```
                 ┌──────────────────────────────────────────┐
                 │  Plugins                                 │  ← bundle everything
                 ├──────────────────────────────────────────┤
   Deterministic │  Hooks (28 events, command handlers)     │  ← only thing that hard-blocks
   ─────────────►├──────────────────────────────────────────┤
                 │  Permissions (allow / ask / deny rules)  │
                 ├──────────────────────────────────────────┤
                 │  Rules (path-scoped *.rules.md)          │
                 ├──────────────────────────────────────────┤
   Model-driven  │  Subagents (isolated context)            │
   ─────────────►├──────────────────────────────────────────┤
                 │  Skills (on-demand prompts)              │
                 ├──────────────────────────────────────────┤
                 │  Advisor (second opinion mid-task)       │
                 ├──────────────────────────────────────────┤
   Always-loaded │  CLAWSPRING.md + dual auto-memory        │
   ─────────────►├──────────────────────────────────────────┤
                 │  Settings (permissions, env, …)          │
                 ├──────────────────────────────────────────┤
                 │  Models (DeepSeek V4 Pro / Flash)        │
                 ├──────────────────────────────────────────┤
                 │  Core REPL / agent loop (deepseek-code)  │
                 └──────────────────────────────────────────┘
```

**The single most important rule** (stated verbatim in Clawspring's own docs): the
model can *ignore* prompts (CLAWSPRING.md, skills) but it **cannot ignore hooks or
permissions** — those run *outside* the model and are enforced by the harness.

- Need behavior to *happen for sure*? → write a **hook**.
- Want to *suggest* behavior? → write a **skill** or a CLAWSPRING.md entry.
- Want isolation? → use a **subagent**.
- Want to ship it to others? → wrap it in a **plugin**.

---

## Topics

### Core

| File | What it covers |
|------|----------------|
| [cli-reference.md](cli-reference.md) | Every subcommand and CLI flag; environment variables; on-disk files |
| [models.md](models.md) | Pro vs Flash, parameters/pricing, `--effort`, `--thinking`, `--fallback-model` |
| [configuration.md](configuration.md) | Both config files (`~/.deepseek-code/config.json`, `~/.clawspring/`), settings keys, env vars |
| [cli-vs-api.md](cli-vs-api.md) | How the `deepseek-code` agent relates to the raw DeepSeek API |

### Sessions & control

| File | What it covers |
|------|----------------|
| [sessions.md](sessions.md) | Sessions (new/continue/resume), the REPL, slash commands, print mode |
| [permissions.md](permissions.md) | The 6 permission modes, allow/ask/deny rules, resolution order, sandbox |

### Extensibility

| File | What it covers |
|------|----------------|
| [hooks.md](hooks.md) | All 28 hook events, the `hooks.json` schema, exit codes, the installed scripts |
| [agents.md](agents.md) | Subagents, full AGENT.md frontmatter (16 fields), built-in agents, the advisor |
| [skills.md](skills.md) | SKILL.md frontmatter (15 fields), substitutions, shell injection, invocation matrix |
| [plugins.md](plugins.md) | `plugin.json` schema, packaging skills/agents/hooks, plugin scopes |

### How it fits together

| File | What it covers |
|------|----------------|
| [architecture.md](architecture.md) | The Clawspring dual-layer design, dual memory, loading order, stacking patterns |

---

## Quick start

```bash
deepseek-code                          # interactive REPL (defaults to Flash)
deepseek-code "explain this repo"      # REPL with an initial prompt
deepseek-code -p "fix the bug in main.py"   # one-shot print mode, then exit
deepseek-code --model pro              # REPL on the Pro model
deepseek-code -c                       # continue the most recent session
deepseek-code -r <id> "keep going"     # resume a specific session
deepseek-code --bare -p "lint and fix" # skip all discovery (CI / deterministic)
cat logs.txt | deepseek-code -p "explain"   # piped stdin
```

Authenticate once with `deepseek-code auth login` (or set `DEEPSEEK_API_KEY`); check
with `deepseek-code auth status`.

---

## Decision tree

| You want to… | Go to |
|--------------|-------|
| Learn the flags and subcommands | [cli-reference.md](cli-reference.md) |
| Pick Pro vs Flash, set effort/thinking | [models.md](models.md) |
| Configure defaults | [configuration.md](configuration.md) |
| Resume work / use the REPL | [sessions.md](sessions.md) |
| Control what the agent may do | [permissions.md](permissions.md) |
| **Force** behavior deterministically | [hooks.md](hooks.md) |
| Isolate heavy research | [agents.md](agents.md) |
| Make a repeatable workflow | [skills.md](skills.md) |
| Get a second opinion mid-task | [agents.md](agents.md#the-advisor) |
| Package and share extensions | [plugins.md](plugins.md) |
| Understand the whole system | [architecture.md](architecture.md) |
