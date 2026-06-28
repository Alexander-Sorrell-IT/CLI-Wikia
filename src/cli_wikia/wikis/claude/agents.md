# Subagents

A subagent is a separate Claude session with its own context window, system prompt, tool set, and (optionally) memory. The parent dispatches a task → the subagent works in isolation → it returns a summary. The parent context never sees the subagent's intermediate work.

**Why this matters:** research and exploration produce huge tool outputs that flood your main context. Push that work into a subagent, and your main session stays small.

For multi-Claude coordination *across sessions* with direct teammate-to-teammate messaging, see [agent-teams.md](./agent-teams.md).

---

## Where subagents live

| Source | Path | Precedence | When loaded |
|---|---|---|---|
| `--agents` JSON | CLI flag, ephemeral | 1 (highest) | At startup |
| `--agent <name>` | CLI flag | 2 | At startup (sets the main thread to *be* this agent) |
| Project | `.claude/agents/<name>.md` | 3 | Discovered by walking up from cwd |
| User | `~/.claude/agents/<name>.md` | 4 | All your projects |
| Plugin | `<plugin>/agents/<name>.md` | 5 (lowest) | When plugin enabled |
| Managed | `.claude/agents/` in [managed settings](./settings.md) | Highest, takes precedence over project/user with same name | All users in org |

Subagents are loaded at session start. After manually adding a file, restart or run `/agents` to load it immediately.

> Project subagents are discovered by walking up from cwd. Subagents are **not** loaded from `--add-dir` directories. To share across projects: use `~/.claude/agents/` or a plugin.

---

## File format

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Body = the system prompt. Subagents receive **only** this system prompt (plus basic env details), not the full Claude Code system prompt.

A subagent starts in the parent's cwd. `cd` inside a subagent does not persist between Bash calls and doesn't affect the main session. To give the subagent an isolated copy of the repo, use `isolation: worktree`.

---

## Frontmatter — every field

```yaml
---
name: my-agent
description: When Claude should delegate to this subagent
tools: Read, Glob, Grep
disallowedTools: Write, Edit
model: claude-opus-4-7
permissionMode: acceptEdits
maxTurns: 25
skills: [api-conventions, error-patterns]
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github
hooks:
  PreToolUse: [...]
memory: project
background: false
effort: high
isolation: worktree
color: blue
initialPrompt: |
  Auto-submitted as the first user turn when this agent is the main session
  agent (via --agent or the agent setting). Commands and skills are processed.
---
```

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique, lowercase + hyphens |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Allowlist. Inherits all tools from parent if omitted |
| `disallowedTools` | No | Denylist. Removed from inherited or specified list |
| `model` | No | `sonnet`, `opus`, `haiku`, full ID, or `inherit`. Default `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Max agentic turns before stopping |
| `skills` | No | Skills to **inject into context at startup** (full content, not just descriptions). Subagents don't inherit skills from the parent — list them explicitly |
| `mcpServers` | No | MCP servers available. Strings reference already-configured servers; objects define inline |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | `user`, `project`, or `local` — enables cross-session learning |
| `background` | No | `true` to always run as a background task |
| `effort` | No | `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | No | `worktree` — runs in a temporary git worktree (auto-cleaned if no changes) |
| `color` | No | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | No | Auto-submitted as first user turn when this agent is the *main session* agent. Commands and skills are processed. Prepended to user-provided prompt |

> **Plugin subagents do NOT support `hooks`, `mcpServers`, or `permissionMode`** — those fields are ignored when loading from plugins. To use them, copy the agent file to `.claude/agents/` or `~/.claude/agents/`.

---

## CLI-defined subagents (`--agents` JSON)

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, provide fixes."
  }
}'
```

`prompt` = the system prompt (equivalent to the markdown body). All the same frontmatter fields work — plus `disallowedTools`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`.

These exist only for the session and aren't saved to disk. Useful for testing and automation scripts.

---

## How dispatch works

Two paths:

### 1. As a subagent (parent delegates)

The parent's Claude encounters a task that matches a subagent's description, decides to delegate, and calls the **Agent tool** with the task. The subagent receives its system prompt + the task, runs in its own context, returns a summary. Parent continues.

### 2. As the main thread (`--agent`)

Run with `claude --agent <name>` and the named agent *replaces* Claude Code's default system prompt for the entire session. `initialPrompt` is auto-submitted as the first turn.

### Restricting which subagents can be spawned

Use `Agent(agent_type)` syntax in the `tools` field of an agent that runs as the main thread:

```yaml
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Allowlist — only `worker` and `researcher` can be spawned. To allow any: `tools: Agent, Read, Bash`. To block all: omit `Agent` from `tools`.

Subagents cannot spawn other subagents, so `Agent(...)` has no effect inside a subagent definition.

> In v2.1.63 the `Task` tool was renamed to `Agent`. Existing `Task(...)` references still work.

To deny specific subagents while allowing others, use `permissions.deny`:

```json
{ "permissions": { "deny": ["Agent(Explore)"] } }
```

---

## Tool restriction — `tools` vs `disallowedTools`

Subagents **inherit all tools** from the parent (including MCP tools) by default.

```yaml
# Allowlist — exclusively allow these tools
tools: Read, Grep, Glob, Bash
```

```yaml
# Denylist — inherit everything except these
disallowedTools: Write, Edit
```

If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool. A tool listed in both is removed.

---

## Choosing a model

| Value | Means |
|---|---|
| `sonnet` / `opus` / `haiku` | Latest in family |
| `claude-opus-4-7` | Full ID |
| `inherit` (default) | Same as main conversation |

Resolution order at invocation:

1. `CLAUDE_CODE_SUBAGENT_MODEL` env var (overrides everything)
2. The per-invocation `model` parameter (passed via the Agent tool)
3. The subagent definition's `model` frontmatter
4. The main conversation's model

---

## MCP scoping

`mcpServers` gives a subagent access to MCP servers that aren't in the main conversation.

```yaml
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  - playwright:           # inline definition — scoped to THIS subagent
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github                # string — reuses already-configured server
---
```

Inline servers connect when the subagent starts and disconnect when it finishes. String references share the parent's connection.

> **Use this to keep MCP servers out of the main conversation.** If a server's tool descriptions are big and you only need them in one subagent, define it inline here rather than in `.mcp.json`. The parent doesn't pay the context cost.

Inline definitions use the same schema as `.mcp.json` server entries (`stdio`, `http`, `sse`, `ws`).

---

## Permission modes for subagents

| Mode | Behavior |
|---|---|
| `default` | Standard prompts |
| `acceptEdits` | Auto-accept file edits + filesystem cmds in cwd / `additionalDirectories` |
| `auto` | Background classifier reviews each command |
| `dontAsk` | Auto-deny prompts (allow rules still work) |
| `bypassPermissions` | Skip prompts |
| `plan` | Read-only exploration |

**Parent overrides:**
- If the parent uses `bypassPermissions` or `acceptEdits`, that takes precedence and **cannot** be overridden by the subagent.
- If the parent uses `auto`, the subagent inherits `auto` and any `permissionMode` in its frontmatter is **ignored**. The classifier evaluates the subagent's calls with the same rules as the parent.

---

## Preload skills into subagents

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

The **full content** of each skill is injected at startup, not just the description. Subagents do **not** inherit skills from the parent — list them explicitly.

You cannot preload skills with `disable-model-invocation: true`. If a listed skill is missing or disabled, Claude Code skips and logs a warning to the debug log.

This is the inverse of [running a skill in a subagent](./skills.md#run-a-skill-in-a-subagent-context-fork).

---

## Persistent memory

```yaml
memory: project
```

Stored at `~/.claude/projects/<project>/memory/agents/<agent-name>/`. Three scopes: `user`, `project`, `local`. Cross-session learning for the subagent specifically.

---

## Foreground vs background subagents

```yaml
background: true
```

Always runs as a background task — you'll be notified when it completes. Useful for long-running work where you don't need results to proceed.

You can also pass `run_in_background: true` per-invocation when calling the Agent tool.

---

## Isolation: worktree

```yaml
isolation: worktree
```

Subagent runs in a temporary [git worktree](https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), giving it an isolated copy of the repo. Auto-cleaned if no changes. Otherwise the path and branch are returned in the result.

---

## Hooks scoped to a subagent

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/check.sh"
```

Same format as [hooks in settings](./hooks.md). Active only while this subagent is running.

---

## Skills vs subagents — cheat sheet

| | **Skill** | **Subagent** |
|---|---|---|
| Entry point | `SKILL.md` | `AGENT.md` (or `<name>.md`) |
| System prompt | Appended to main prompt | Replaces it |
| Context window | Shared with parent | Isolated |
| Tools | `allowed-tools` (additive permission) | `tools` / `disallowedTools` (restrictive) |
| Memory | Shared CLAUDE.md / auto-memory | Can have its own (`memory: …`) |
| Cost | Cheap (no extra inference loop) | Full extra session |
| Best for | Repeatable workflows | Heavy research, parallel work |

A useful pattern: write a *skill* with `context: fork` + `agent: <name>` so you get a `/command` interface that delegates to a subagent in isolation.

---

## See also

- [agent-teams.md](./agent-teams.md) — multi-Claude coordination across sessions
- [skills.md](./skills.md) — `context: fork` and the inverse pattern
- [hooks.md](./hooks.md) — `SubagentStart` and `SubagentStop` events
- [cli-reference.md](./cli-reference.md) — `--agent`, `--agents`
