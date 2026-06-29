# Architecture: Clawspring

DeepSeek Code is the CLI; **Clawspring** is the agent runtime underneath it. Clawspring
is what loads instructions, runs the hook events, enforces permissions, manages memory,
and spawns subagents. Its design is closely adapted from Claude Code — the directory
names and concepts (CLAWSPRING.md ≈ CLAUDE.md, `~/.clawspring/` ≈ `~/.claude/`) map
almost one-to-one. This page explains how the pieces fit.

---

## The dual-layer system

Clawspring keeps two completely separate configuration/memory layers:

```
┌──────────────────────────── GLOBAL LAYER — ~/.clawspring/ ───────────────────────┐
│  CLAWSPRING.md       loaded into EVERY session, all projects                      │
│  settings.json       master runtime settings                                      │
│  hooks.json          28 hook events → scripts                                     │
│  permissions.json    allow / ask / deny rules                                     │
│  config.json         harness ceilings (max_tokens, depth, concurrency, …)         │
│  agents/             global subagents (advisor, code-reviewer, researcher, tester)│
│  skills/             global skills                                                │
│  hooks/              hook scripts                                                  │
│  rules/              global-hard-rules.md (path-scoped)                           │
│  memory/             GLOBAL memory (cross-project facts, project index)           │
│  sessions/           session logs                                                 │
│  *_TEMPLATE.md       AGENT / SKILL / PLUGIN specs; ARCHITECTURE / STACKING docs   │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────── PROJECT LAYER — .clawspring/ (per project) ──────────────┐
│  CLAWSPRING.md       project instructions (imports global via @~/.clawspring/…)   │
│  settings.local.json project overrides                                            │
│  hooks/ agents/ skills/   project-specific extensions (merged with global)        │
│  memory/             PROJECT memory (isolated per project)                        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Project isolation is a hard rule:** each project gets its own `.clawspring/`, and
contexts are never mixed between projects — even if paths look similar.

---

## Dual memory

There are two memory stores with strict scope discipline:

| | Global memory (`~/.clawspring/memory/`) | Project memory (`.clawspring/memory/`) |
|---|---|---|
| Stores | Cross-project patterns, tool quirks, a **project index** (paths only) | Project-specific architecture, conventions, decisions |
| Never stores | Project-specific code/architecture | Global rules; other projects' info |
| Scope flag | `user` | `project` |

**The litmus test:** if you moved the project to another machine, would the memory
still apply? Yes → project scope. Applies across all projects → global scope.

Memory is read/written by the `Memory*` tools (`MemorySave`, `MemorySearch`,
`MemoryList`, `MemoryDelete`). Each store has a `MEMORY.md` index that is rebuilt after
every save/delete; the first ~200 lines load into context at session start. Global
memory may record *where* projects live (`projects-index.md`) but not their contents.

---

## Loading order (every session)

```
1. ~/.clawspring/CLAWSPRING.md             global instructions
2. ~/.clawspring/rules/global-hard-rules.md  hard rules
3. .clawspring/CLAWSPRING.md               project instructions (imports global)
4. ~/.clawspring/memory/MEMORY.md          global memory index (first 200 lines)
5. .clawspring/memory/MEMORY.md            project memory index (first 200 lines)
6. .clawspring/settings.local.json         project overrides
7. ~/.clawspring/settings.json             global settings
8. ~/.clawspring/hooks.json                global hooks
9. .clawspring/hooks/                       project hooks (merged with global)
```

`@import` references (e.g. `@~/.clawspring/CLAWSPRING.md`) are resolved recursively,
up to a small hop limit, to pull shared docs into a project's instructions.

---

## Bootstrapping a new project

When the agent enters a directory that looks like a project (has `.git/`,
`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, a `Makefile`, etc.) but has
no `.clawspring/`, the `CwdChanged` / `SessionStart` hook bootstraps one:

```
CwdChanged → cwd-changed.sh
  ├─ .clawspring/ exists?  → load project CLAWSPRING.md + memory
  └─ missing & is a project → create:
        .clawspring/CLAWSPRING.md      (imports global)
        .clawspring/memory/MEMORY.md   (empty project index)
        .clawspring/{hooks,agents,skills}/   (empty)
     and append the project path to ~/.clawspring/memory/projects-index.md
```

Bootstrap never blocks (always exits 0).

---

## The hook-event flow

A representative pass through a session (full list in [hooks.md](hooks.md)):

```
SessionStart        → startup.sh: init session, detect project
UserPromptSubmit    → log prompt, block dangerous intents
PreToolUse(Bash)    → pre-bash.sh: BLOCK sudo / rm -rf / / fork bombs / curl|sh
PreToolUse(Write)   → pre-write.sh: BLOCK secret files / outside workspace
PreToolUse(WebFetch)→ pre-web.sh: BLOCK internal IPs / localhost
PostToolUse(commit) → post-commit.sh: suggest a code review
Stop                → stop-check.sh: require advisor before substantive completion
SubagentStop        → can BLOCK to keep a subagent working
CwdChanged          → bootstrap a new .clawspring/ if missing
```

---

## Permission resolution

```
Layer precedence:  CLI flags > .clawspring/settings.local.json
                   > .clawspring/settings.json > ~/.clawspring/settings.json
Merge:             allow ∪ allow; a deny at ANY level wins; ask combines
Per-call:          deny? → DENY · allow? → ALLOW · ask? → ASK · else → ASK
```

See [permissions.md](permissions.md) for the rule syntax and the shipped policy.

---

## The layered extensibility model (stacking)

Each layer does one thing well; the leverage is in composing them.

```
   Plugins                       ← bundle everything
   Hooks (deterministic)         ← the only thing that can hard-block
   Permissions (allow/ask/deny)
   Rules (path-scoped)
   Subagents (isolated context)  ← model-driven
   Skills (on-demand prompts)
   Advisor (second opinion)
   CLAWSPRING.md + auto-memory   ← always-loaded
   Settings
   Core REPL / agent loop
```

**The one rule that governs the whole stack:** the model can ignore *prompts*
(CLAWSPRING.md, skills) but cannot ignore *hooks or permissions*, which run outside the
model in the harness.

### Composition patterns

- **Skill as a friendly door to a subagent** — a skill with `context: fork` +
  `agent: code-reviewer` gives users a `/review` command whose work runs in isolated
  context.
- **Hook enforces what a skill only suggests** — CLAWSPRING.md says "run tests before
  committing"; a `PreToolUse(Bash(git commit *))` hook makes skipping tests impossible.
- **Subagent with preloaded skills** — an agent declares `skills: [api-conventions,
  validation]` so a specialist has its domain knowledge without polluting the main
  context.
- **Advisor + Stop hook = quality gate** — call `/advisor` before declaring done; the
  `Stop` hook blocks completion until it has been consulted.

### Decision tree

```
Need behavior to happen for sure?      → Hook
Want to suggest it?
  always-on                            → CLAWSPRING.md
  on demand                            → Skill
  in its own context                   → Subagent
Need a second opinion?                 → Advisor
Need to package & share?               → Plugin
Need to react to outside events?       → Hook (Notification, FileChanged)
```

---

## How this maps to Claude Code

Clawspring is openly modeled on Claude Code; the parallels are exact in many places:

| Clawspring | Claude Code equivalent |
|------------|------------------------|
| `CLAWSPRING.md` | `CLAUDE.md` |
| `~/.clawspring/` | `~/.claude/` |
| `hooks.json` (28 events) | `settings.json` hooks (28+ events) |
| `permissions.json` (allow/ask/deny) | permissions rules |
| AGENT.md / SKILL.md frontmatter | the same field set |
| advisor subagent + Stop gate | advisor / second-opinion patterns |

Where this matters: most Claude Code mental models transfer, but the **model** is
DeepSeek V4 and the **CLI is `deepseek-code`**, not `claude`. Treat Claude-Code
behaviors as a strong prior, but trust what *this* tool reports.

---

## Related

- [hooks.md](hooks.md) · [permissions.md](permissions.md) · [agents.md](agents.md)
  · [skills.md](skills.md) · [configuration.md](configuration.md)
