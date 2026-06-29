# Agents

A **subagent** is a separate Clawspring session with its own context window, system
prompt, tool set, and (optionally) memory. Use subagents to push heavy research or
parallel work out of the main conversation so the main context stays clean. The
subagent model mirrors Claude Code's.

```bash
deepseek-code agents              # list configured agents
deepseek-code --agent researcher  # run the main thread AS a named agent
deepseek-code --agents '<json>'   # define subagents inline
```

---

## Built-in agents

The global install ships four agents in `~/.clawspring/agents/`:

| Agent | Purpose | Tools | maxTurns |
|-------|---------|-------|----------|
| `advisor` | Second-opinion reviewer for mid-task validation | `Read, Glob, Grep, Bash(git *)` | 10 |
| `code-reviewer` | Reviews code for quality, security, best practices | `Read, Glob, Grep, Bash(git *)` | 15 |
| `researcher` | Deep research / exploration producing large intermediate output | `Read, Glob, Grep, WebSearch, WebFetch, Bash(git *)` | 30 |
| `tester` | Runs tests, analyzes failures, finds root causes | `Bash, Read, Glob, Grep` | 20 |

Each is a markdown file with YAML frontmatter and a system-prompt body. For example,
`code-reviewer.md` defines a CRITICAL/WARNING/SUGGESTION output format and a
bug-first review checklist.

---

## AGENT.md frontmatter — 16 fields

A subagent definition is a `<name>.md` file. The body becomes the system prompt; the
frontmatter configures the session.

```markdown
---
name: my-agent
description: When to delegate to this subagent
tools: Read, Glob, Grep
disallowedTools: Write, Edit
model: inherit
permissionMode: acceptEdits
maxTurns: 25
skills: [api-conventions, error-patterns]
mcpServers:
  - github
hooks:
  PreToolUse: [...]
memory: project
background: false
effort: high
isolation: worktree
color: blue
initialPrompt: |
  Auto-submitted as the first user turn when this agent is the main session.
---

You are a [role]. When invoked, [instructions].
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique, lowercase + hyphens |
| `description` | Yes | When the agent should be delegated to |
| `tools` | No | Allowlist. Inherits all parent tools if omitted |
| `disallowedTools` | No | Denylist, removed from the inherited/specified set |
| `model` | No | `pro`, `flash`, full ID, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Max agentic turns (default 25) |
| `skills` | No | Skills injected into context at startup (full content) |
| `mcpServers` | No | MCP servers — strings reuse configured ones, objects define inline |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | `user`, `project`, or `local` — cross-session learning |
| `background` | No | `true` = always run as a background task |
| `effort` | No | `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | No | `worktree` — run in a temp git worktree, auto-cleaned |
| `color` | No | UI color (`red`, `blue`, `green`, …) |
| `initialPrompt` | No | Auto-submitted when this agent is the main session |

> The built-in agents use a small subset (`name`, `description`, `tools`, `maxTurns`,
> `permissionMode`). The full 16-field spec is documented in the install's
> `AGENT_TEMPLATE.md`; fields beyond that subset are *verify in the tool* for your
> version.

---

## Where subagents live (precedence)

| Source | Path | Precedence |
|--------|------|------------|
| `--agents` JSON | CLI flag | 1 (highest) |
| `--agent <name>` | CLI flag | 2 |
| Project | `.clawspring/agents/<name>.md` | 3 |
| User (global) | `~/.clawspring/agents/<name>.md` | 4 |
| Plugin | `<plugin>/agents/<name>.md` | 5 (lowest) |

**Plugin subagents do not support** `hooks`, `mcpServers`, or `permissionMode`.

---

## Tool restriction

```yaml
tools: Read, Grep, Glob, Bash          # allowlist — only these
disallowedTools: Write, Edit           # denylist — everything except these
# With both: disallowedTools is applied first, then tools is resolved
```

## Model resolution order

1. `CLAUDE_CODE_SUBAGENT_MODEL` env var (overrides everything)
2. The per-invocation `model` parameter
3. The subagent definition's `model` frontmatter
4. The main conversation's model

So `model: inherit` follows the parent — unless the env var overrides it.

## Parent-override rules

A parent running in `bypassPermissions` or `acceptEdits` mode **cannot** have that
relaxed by a stricter subagent `permissionMode` — the parent's posture wins.

---

## Concurrency limits

The harness config caps how subagents fan out (see [configuration.md](configuration.md)):

- `max_agent_depth: 3` — nesting depth
- `max_concurrent_agents: 3` — parallel subagents

A subagent cannot itself spawn further subagents beyond the depth limit.

---

## Skills vs subagents

| | Skill | Subagent |
|---|---|---|
| Entry point | SKILL.md | AGENT.md |
| System prompt | Appended to the main prompt | **Replaces** it |
| Context window | Shared with the parent | **Isolated** |
| Tools | `allowed-tools` (additive) | `tools` / `disallowedTools` (restrictive) |
| Best for | Repeatable workflows | Heavy research, parallel work |
| Cost | Cheap | A full extra session |

A common pattern is a **skill with `context: fork` + `agent: <name>`** so a `/command`
delegates straight into a subagent. See [skills.md](skills.md) and
[architecture.md](architecture.md).

---

## The advisor

The **advisor** is a second-opinion mechanism implemented as a specialized subagent
(`~/.clawspring/agents/advisor.md`) plus a `Stop`-hook gate. It is the headline
quality feature of this install.

### What it does

When invoked, the advisor receives the task description, the tool calls and results,
and the current approach, then returns exactly one verdict:

| Verdict | Meaning |
|---------|---------|
| **PROCEED** | The approach is sound; no changes needed |
| **ADJUST: \<changes\>** | Mostly right, but make these specific changes |
| **BLOCK: \<reason\>** | Fundamentally wrong/dangerous — use this alternative instead |

It is instructed to be concise, specific (name files/functions), and ruthless about
hidden assumptions — and to BLOCK immediately on a security risk.

### Two layers

1. **On-demand** — call `/advisor "should I proceed with X?"` at any decision point.
2. **Stop-hook enforcement** — `stop-check.sh` can block session completion (exit 2)
   until the advisor has been consulted, forcing a review before substantive work is
   declared done.

### When to call it

- **Before** committing to a substantive approach or interpretation.
- **Before** declaring a task complete (make the deliverable durable first).
- When stuck, or when considering a change of approach.
- When a subagent's findings contradict your plan.

### How to weight it

Give it serious weight, but: a failed empirical test beats theoretical advice, and
primary-source evidence beats the advisor's claim. A passing self-test is *not*
evidence the advice is wrong — it may just mean the test doesn't check what the
advisor checked.

---

## Related

- [skills.md](skills.md) — preloading skills into agents; fork pattern
- [hooks.md](hooks.md) — `SubagentStart`/`SubagentStop`, the `Stop` advisor gate
- [architecture.md](architecture.md) — isolation, memory, and composition
