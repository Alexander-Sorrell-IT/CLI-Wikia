# Stacking — How to Compose Skills, Agents, Hooks, and Everything Else

This file is about **composition**. Each layer of Claude Code is good at one thing; the leverage comes from stacking them. Below: which combinations work, which don't, and the patterns that show up in real plugins.

---

## The composition matrix

Read each row as: "**Row** can do *this* with **Column**."

|  | Skill | Subagent | Hook | MCP server | Plugin |
|---|---|---|---|---|---|
| **Skill** | Skills can `/invoke other skills`; `context: fork` makes a skill run *as* a subagent. Skills can chain via Bash. | A skill with `context: fork` + `agent: Explore` (or a custom agent) delegates to a subagent. The skill body becomes the subagent's prompt. | Skills can declare `hooks:` in frontmatter — those fire only while the skill is active. | Skills can pre-approve MCP tools via `allowed-tools: mcp__github__*`. Skills are the natural way for Claude to choose when to use an MCP tool. | Skills are the most common plugin component. Bundle 5 skills + 1 MCP + 2 hooks → one install. |
| **Subagent** | Subagents preload skills with `skills: [...]` (full content injected at startup). They don't inherit skills from parent — list them. | Cannot spawn subagents from inside a subagent. The Agent tool only works from the main thread. | Subagents can declare `hooks:` in frontmatter — fire only while subagent is active. **Plugin subagents do NOT support hooks** (security). | Subagents can scope MCP servers with `mcpServers:` — inline (subagent-only) or by name (shared with parent). Use to keep big tool sets out of the parent context. | Plugin subagents are the easiest way to ship reusable specialists. |
| **Hook** | A hook can run before/after skill invocation (`UserPromptExpansion`, `PreToolUse` matching `Skill(...)`). It can inject `additionalContext` Claude reads. | `SubagentStart` and `SubagentStop` hooks gate subagent lifecycle. Block `SubagentStop` (exit 2) to keep the subagent working. | Hooks chain naturally — `PostToolUse` of one tool can trigger work that fires `PreToolUse` of another. Each hook event is independent. | `mcp__server__tool` matchers let hooks intercept MCP calls — for validation, rate-limiting, audit logging. | Plugin hooks fire only while the plugin is enabled. Use for plugin-specific safety. |
| **MCP server** | MCP tools surface in the toolkit; skills with `allowed-tools: mcp__*` enable them in context. MCP **prompts** appear as `/server:prompt` slash commands. | Subagents with `mcpServers:` can have private MCP servers the parent never sees. | MCP servers can hook by being called from a `mcp_tool` handler. They can also be the *source* of `Notification` events via the `claude/channel` capability. | Multiple MCP servers can collaborate by being called in sequence by Claude. | Plugins ship MCP servers in `.mcp.json`; they auto-start when plugin enabled. |
| **Plugin** | A plugin can ship N skills (namespaced `/plugin:skill`). | A plugin can ship N agents — but **subagent `hooks`/`mcpServers`/`permissionMode` fields are ignored** in plugin agents (security). | Plugins ship hooks in `hooks/hooks.json`. Active while plugin is enabled. | Plugins bundle MCP servers in `.mcp.json` or inline. | Plugins can declare `dependencies: [...]` on other plugins. |

---

## The five most useful patterns

### Pattern 1 — Skill as a friendly entry to a subagent

The skill becomes the *user-facing command*; the subagent is where the heavy work happens in isolated context.

```yaml
---
name: review
description: Deep code review of recent changes
context: fork
agent: code-reviewer
allowed-tools: Bash(git *)
---
Review the diff and provide actionable feedback. Focus on bugs first, style second.

PR diff:
!`git diff main...HEAD`
```

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Reviews diffs for bugs and best practices
model: claude-opus-4-7
tools: Read, Glob, Grep, Bash(git *)
---
You are a senior reviewer. Always:
1. Identify bugs first.
2. Flag security issues.
3. Suggest improvements with file:line refs.
```

**Why it works:** the user gets a `/review` slash command, but the actual work runs in an isolated context where the reviewer has its own tool set. The main session stays light.

---

### Pattern 2 — Hook enforces what skills only suggest

CLAUDE.md and skills are *suggestions*. Hooks are *enforcement*. Combine them so Claude *prefers* the right path AND can't deviate.

```markdown
# CLAUDE.md
Always run `npm run lint` before committing.
```

```yaml
# .claude/skills/commit/SKILL.md
---
name: commit
description: Stage and commit current changes
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(npm run lint)
---
Run `npm run lint` first. If it passes, stage and commit:

!`git diff --cached --name-only`
```

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "if": "Bash(git commit *)",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/require-lint.sh"
      }]
    }]
  }
}
```

```bash
#!/bin/bash
# .claude/hooks/require-lint.sh
if ! npm run lint --silent 2>&1 >/dev/null; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Lint failed — fix before committing"
    }
  }'
  exit 2
fi
exit 0
```

**Why it works:** the skill makes the right path easy; the hook makes the wrong path impossible.

---

### Pattern 3 — Subagent with preloaded skills as a domain expert

Define a subagent that always has the right knowledge loaded, so the parent doesn't pay the context cost.

```yaml
# .claude/agents/api-developer.md
---
name: api-developer
description: Implement API endpoints following team conventions
model: claude-sonnet-4-6
skills:
  - api-conventions       # full content injected at startup
  - error-handling-patterns
  - validation-patterns
tools: Read, Edit, Write, Bash(npm test)
mcpServers:
  - openapi-validator:
      type: stdio
      command: npx
      args: ["-y", "@openapi/validator"]
---
You implement API endpoints. Apply preloaded conventions strictly.
```

The skills are full content (not just descriptions), the MCP server is inline so the *parent* never sees the openapi-validator tools, and the subagent runs in isolation.

**Why it works:** the parent context stays clean; the specialist has all its knowledge and tools without polluting the main session.

---

### Pattern 4 — Channel + Notification hook + skill = ambient awareness

External event arrives → hook decides if it matters → skill kicks in.

1. **Channel** (Telegram, CI webhook, log monitor) pushes a message into the session.
2. **`Notification` hook** parses it. If it matches a critical pattern, return `additionalContext` flagging it.
3. **Skill** (or CLAUDE.md instruction) tells Claude how to react when the flag is present.

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "permission_prompt|elicitation_dialog",
      "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/log-and-tag.sh" }]
    }]
  }
}
```

**Why it works:** Claude reacts to outside-world events without you having to ask.

---

### Pattern 5 — Plugin as the wrapper that ships everything

When you've built a useful workflow that touches multiple layers, package it. One install pulls in all the moving parts.

```
my-security-plugin/
├── .claude-plugin/plugin.json
├── .mcp.json                            # GitHub MCP server
├── skills/
│   ├── security-review/SKILL.md         # /my-security-plugin:security-review
│   ├── dependency-audit/SKILL.md
│   └── secret-scanner/SKILL.md
├── agents/
│   ├── security-reviewer.md             # subagent with strict tools
│   └── threat-modeler.md
├── hooks/hooks.json                     # PreToolUse blocks rm -rf, intercepts MCP calls
├── monitors/monitors.json               # tails auth.log → notifications
├── settings.json                        # default subagent + permission rules
└── README.md
```

What happens when a user runs `claude plugin install my-security-plugin`:

1. **`.mcp.json`** boots the GitHub MCP server. Tools surface as `mcp__github__*`.
2. **`settings.json`** registers default subagent + adds plugin's hook config to active hooks.
3. **PreToolUse hook** starts intercepting Bash and `mcp__github__*` calls.
4. **Monitor** starts tailing `auth.log`; lines arrive as Notifications.
5. **3 skills** appear as `/my-security-plugin:security-review`, etc.

User asks "review this code for vulnerabilities":
- Claude matches the request to the `security-review` skill description.
- Skill runs in main context. Calls `mcp__github__list_pull_requests` (allowed via skill's `allowed-tools`).
- Mid-skill Claude tries `rm -rf node_modules` for cleanup. Hook returns exit 2 — denied.
- Skill adapts and returns the review.

User asks "build a threat model":
- Claude delegates to the `threat-modeler` subagent.
- Subagent runs in isolated context. Returns summary to main conversation.
- Main context stays clean.

Auth log monitor fires:
- Notification arrives in the session: "Failed login burst on prod from 1.2.3.4".
- `Notification` hook tags it as urgent. Claude proactively investigates.

CI runs `claude --bare -p "audit deps" --plugin-dir ./my-security-plugin`:
- Bare mode skips global config but loads the plugin via `--plugin-dir`.
- `dependency-audit` skill runs end-to-end with no human in the loop.
- Output as structured JSON.

**Every layer is engaged.** And the user only had to install one thing.

---

## Anti-patterns

### ❌ Putting enforcement in CLAUDE.md alone
> "Don't run dangerous commands."

CLAUDE.md is a *suggestion*. The model can ignore it. If you need it enforced, it goes in a **hook**.

### ❌ Heavy skills in the main context instead of subagents
A skill that does deep research/analysis should use `context: fork`. Otherwise it floods your conversation with intermediate tool outputs you don't need.

### ❌ Plugin agents with hooks/MCP/permissionMode
Plugin subagents *don't support* `hooks`, `mcpServers`, or `permissionMode`. If you need those, the agent must live in `.claude/agents/` or `~/.claude/agents/`, not in the plugin.

### ❌ MCP servers everyone pays for
If a server's tool descriptions are big and only one subagent needs it, define it inline in that subagent's `mcpServers` instead of globally in `.mcp.json`. The parent doesn't pay the context cost.

### ❌ Skills with `disable-model-invocation: true` preloaded into a subagent
Doesn't work — preload draws from the same pool as model-invocable skills.

### ❌ Calling advisor at the end of a substantive task
Advisor's value peaks **before** you commit to an approach. Calling at the end gets you a critique you can't easily apply. Call early.

### ❌ Setting `bypassPermissions` on the parent and trying to override per-subagent
Parent's `bypassPermissions` and `acceptEdits` **cannot be overridden** by a subagent. Auto mode propagates and the subagent's `permissionMode` is ignored.

---

## Decision tree: which layer to use

```
Need behavior to happen for sure (deterministic)?
├─ Yes → Hook
└─ No  → Need it suggested?
         ├─ Yes (always-on)        → CLAUDE.md
         ├─ Yes (on demand)        → Skill
         ├─ Yes (in own context)   → Subagent (or skill with context: fork)
         └─ Yes (multi-Claude)     → Agent team

Need to call an external service?
└─ MCP server

Need to react to outside events?
├─ Continuous watching      → Monitor (in a plugin)
├─ Push from chat/CI/etc.   → Channel
└─ Lifecycle events         → Hook (Notification, FileChanged, etc.)

Need to package and share?
└─ Plugin (+ optionally publish to a marketplace)

Need OS-level isolation?
└─ Sandboxing

Need to run remotely?
├─ My machine, drive from phone → Remote Control
├─ Cloud VM, async              → Claude Code on the web
└─ Cloud VM, scheduled           → Routines / scheduled tasks
```

---

## When to call the advisor in a stack

The **advisor** sits orthogonally to all of this. Whenever a stack of skills/agents/hooks is making a decision that's hard to back out of:

- Before the orchestrating skill commits to an interpretation → `advisor()`.
- Before declaring a multi-component task done → `advisor()`.
- When a subagent's report contradicts your prior plan → `advisor()`.

See [advisor.md](./advisor.md).

---

## See also

- [skills.md](./skills.md) — skill frontmatter for `context: fork`, `agent`, `hooks`, `allowed-tools`
- [agents.md](./agents.md) — subagent frontmatter for `skills`, `mcpServers`, `hooks`
- [hooks.md](./hooks.md) — all 28 events
- [plugins.md](./plugins.md) — packaging skills + agents + hooks + MCP + monitors
- [advisor.md](./advisor.md) — second opinion mid-task
