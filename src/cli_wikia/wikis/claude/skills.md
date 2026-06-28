# Skills

Skills extend what Claude can do. Each skill is a directory with a `SKILL.md` file. Claude either invokes one automatically when it matches the task, or you invoke it manually with `/skill-name`.

Custom slash commands (`.claude/commands/foo.md`) and skills are *the same thing now*. A skill at `.claude/skills/foo/SKILL.md` and a command at `.claude/commands/foo.md` both create `/foo` and work the same way. Skills add features: a directory for supporting files, full frontmatter, and automatic invocation when the description matches.

Skills follow the [Agent Skills](https://agentskills.io) open standard. Claude Code extends it with invocation control, subagent execution, and dynamic context injection.

---

## Bundled skills

Ship with Claude Code, available in every session — invoked with `/`:

```
/simplify     /batch     /debug     /loop     /claude-api
```

Plus `/init`, `/review`, `/security-review` are also available through the Skill tool. Most other built-ins (`/compact`, `/help`, etc.) are commands, not skills.

---

## Where skills live

| Location | Path | Scope |
|---|---|---|
| Enterprise (managed) | See [managed settings](./settings.md) | All users in your org |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled (namespaced `/plugin:name`) |

**Precedence:** Enterprise > Personal > Project. Plugin skills use `plugin-name:skill-name` namespace, so they can't conflict.

If a skill and a command share a name, the **skill takes precedence**.

### Live change detection

Claude Code watches skill dirs. Adding/editing/removing a skill takes effect within the current session — no restart. *Creating a brand-new top-level skills dir* requires restart so the watcher picks it up.

### Nested discovery (monorepos)

When working with files in subdirs, Claude also discovers skills from nested `.claude/skills/`. Edit a file in `packages/frontend/` and Claude looks in `packages/frontend/.claude/skills/` too.

### Skills from `--add-dir`

`--add-dir` grants file access only — but `.claude/skills/` inside an added dir **is** loaded automatically. (Other config like agents/commands/output-styles is not.)

---

## Skill directory structure

```
my-skill/
├── SKILL.md              # required — frontmatter + body
├── reference.md          # detailed docs, loaded on demand
├── examples.md           # example outputs
├── template.md           # template Claude fills in
└── scripts/
    └── helper.sh         # something Claude can execute
```

Reference supporting files from `SKILL.md` so Claude knows what each contains:

```markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

Keep `SKILL.md` under 500 lines. Move detail into linked files.

---

## Frontmatter — every field

```yaml
---
name: my-skill
description: What it does and when to use it
when_to_use: Extra trigger phrases, examples
argument-hint: "[issue-number] [format]"
arguments: [issue, format]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Edit, Bash(gh *)
model: claude-sonnet-4-6
effort: high
context: fork
agent: Explore
hooks:
  PreToolUse: [...]
paths: ["src/**/*.ts"]
shell: bash
---
```

| Field | Required | Description |
|---|---|---|
| `name` | No | Display name. If omitted, uses dir name. Lowercase + hyphens, max 64 chars |
| `description` | Recommended | What the skill does + when to use. Claude uses this to decide when to load. If omitted, uses first markdown paragraph. **Truncated at 1,536 chars** in the listing |
| `when_to_use` | No | Extra trigger context, appended to description in listing. Counts toward 1,536-char cap |
| `argument-hint` | No | Hint shown during autocomplete: `[issue-number]` |
| `arguments` | No | Named positional args for `$name` substitution. Space-separated string or YAML list |
| `disable-model-invocation` | No | `true` = only **you** can invoke (also blocks subagent preload). Default `false` |
| `user-invocable` | No | `false` = hide from `/` menu (only Claude can invoke). Default `true` |
| `allowed-tools` | No | Pre-approve these tools while skill is active. Space-separated or YAML list |
| `model` | No | `sonnet`, `opus`, `haiku`, full ID, or `inherit`. Override applies for the rest of the turn only |
| `effort` | No | `low`, `medium`, `high`, `xhigh`, `max`. Overrides session effort |
| `context` | No | `fork` = run in a forked subagent context |
| `agent` | No | Which subagent type to use when `context: fork`. Built-ins: `Explore`, `Plan`, `general-purpose`. Or any custom from `.claude/agents/` |
| `hooks` | No | Hooks scoped to this skill's lifecycle (same format as [settings hooks](./hooks.md)) |
| `paths` | No | Glob patterns. When set, Claude auto-loads only when working with matching files. Comma-separated string or YAML list |
| `shell` | No | `bash` (default) or `powershell`. PowerShell requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` |

All fields optional except `description` is recommended.

---

## String substitutions in skill content

| Variable | Description |
|---|---|
| `$ARGUMENTS` | All args as a string. If absent from content, args are appended as `ARGUMENTS: <value>` |
| `$ARGUMENTS[N]` | Specific arg by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` (so `$0`, `$1`, ...) |
| `$name` | Named arg from the `arguments` frontmatter list (positions map in order) |
| `${CLAUDE_SESSION_ID}` | Current session ID — useful for logging, session-keyed files |
| `${CLAUDE_SKILL_DIR}` | The skill's directory — use in scripts to reference bundled files regardless of cwd |

Indexed args use shell-style quoting. `/my-skill "hello world" second` → `$0` = `hello world`, `$1` = `second`. `$ARGUMENTS` always has the full string as typed.

```yaml
---
name: session-logger
description: Log activity for this session
---
Log to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

---

## Shell injection — dynamic context

The `` !`<command>` `` syntax runs shell commands **before** the skill content reaches Claude. The output replaces the placeholder.

```yaml
---
name: pr-summary
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---
## PR context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this PR…
```

This is **preprocessing** — Claude only sees the rendered prompt with actual data, not the command itself.

### Multi-line shell blocks

For multi-line, use a fenced block opened with ` ```! `:

````markdown
## Environment
```!
node --version
npm --version
git status --short
```
````

### Disabling shell execution by policy

```json
{ "disableSkillShellExecution": true }
```

Each command is replaced with `[shell command execution disabled by policy]` instead of running. Bundled and managed skills are unaffected. Useful in managed settings where users can't override.

---

## Auto-invocation, manual, and `disable-model-invocation`

| Frontmatter | You can invoke | Claude can invoke | Loaded into context |
|---|---|---|---|
| (default) | Yes | Yes | Description always in context, full body loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description NOT in context, full body loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full body loads when invoked |

Use `disable-model-invocation: true` for things Claude shouldn't trigger autonomously (e.g. `/deploy`).

---

## Skill content lifecycle

When invoked, the rendered `SKILL.md` enters the conversation **as a single message** and stays there for the rest of the session. Claude doesn't re-read the file on later turns.

### Auto-compaction

Auto-compaction carries invoked skills forward within a token budget:
- After summarization, Claude re-attaches the most recent invocation of each skill.
- Keeps the **first 5,000 tokens** of each skill.
- Combined budget across re-attached skills: **25,000 tokens**.
- Filled from most recent → oldest. Older skills can be dropped after compaction.

If a skill seems to stop influencing behavior, the content is usually still there but the model is choosing other approaches. Either strengthen the description, or use [hooks](./hooks.md) for deterministic enforcement. For large skills you've drifted from, just `/skill-name` again to reload.

---

## Pre-approving tools

`allowed-tools` grants permission *only* for the listed tools while the skill is active. It doesn't restrict — every tool remains callable, and your normal permissions still govern unlisted tools.

To **block** a skill from using a tool, add a deny rule in your [permission settings](./permissions.md).

```yaml
---
name: commit
description: Stage and commit current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

---

## Run a skill in a subagent (`context: fork`)

The skill content becomes the prompt that drives the subagent. It won't have your conversation history.

> `context: fork` only makes sense for skills with explicit instructions. Pure reference content gives the subagent guidelines but no actionable task.

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

When invoked:

1. New isolated context.
2. Subagent receives the rendered skill content as its prompt.
3. The `agent` field determines execution environment (model, tools, permissions).
4. Results return to your main conversation.

`agent` defaults to `general-purpose` if omitted.

### Skill-with-fork vs. subagent-with-skills (the inverse)

| | Skill with `context: fork` | Subagent with `skills: [...]` |
|---|---|---|
| System prompt | From the agent type (Explore, Plan, …) | The subagent's markdown body |
| Task | The SKILL.md content | Claude's delegation message |
| Loads in addition | CLAUDE.md | Preloaded skills + CLAUDE.md |

See [agents.md](./agents.md#preload-skills-into-subagents) for the inverse pattern.

---

## Restricting which skills Claude can invoke

```text
# Disable all skills
Skill                 # add to deny

# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Syntax: `Skill(name)` for exact, `Skill(name *)` for prefix + args.

`user-invocable` controls *menu visibility*, not Skill-tool access. Use `disable-model-invocation: true` to truly block programmatic invocation.

---

## Description budget & truncation

Skill descriptions sit in context so Claude knows what's available. With many skills, descriptions get shortened to fit a budget — which can strip the keywords Claude needs.

- Budget: **1% of the context window**, fallback **8,000 chars**.
- Each entry's combined description+when_to_use is capped at **1,536 chars** regardless.

Raise the budget:

```bash
export SLASH_COMMAND_TOOL_CHAR_BUDGET=20000
```

Or front-load the key use case in your description.

---

## Extended thinking

To enable extended thinking in a skill, include the word **`ultrathink`** anywhere in the body.

---

## Sharing

- **Project**: commit `.claude/skills/` to git.
- **Plugins**: ship via a `skills/` dir in your [plugin](./plugins.md).
- **Managed**: deploy org-wide via [managed settings](./settings.md).

---

## Troubleshooting

- **Not triggering** → check description has the keywords, verify it appears in `What skills are available?`, try rephrasing the request to match, or `/skill-name` directly.
- **Triggers too often** → make description more specific, or set `disable-model-invocation: true`.
- **Description cut off** → set `SLASH_COMMAND_TOOL_CHAR_BUDGET` higher, or trim text.

---

## See also

- [agents.md](./agents.md) — when to use a subagent instead
- [hooks.md](./hooks.md) — deterministic enforcement when skills aren't enough
- [plugins.md](./plugins.md) — packaging skills for distribution
- [stacking.md](./stacking.md) — composing skills + agents + hooks
