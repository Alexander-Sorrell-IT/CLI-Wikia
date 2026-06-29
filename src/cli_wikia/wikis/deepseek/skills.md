# Skills

A **skill** is an on-demand prompt template — a named, parameterized piece of guidance
the model can invoke when a task matches, or that you invoke explicitly with
`/skill-name`. Skills are *suggestions*: the model can follow or ignore them. For
behavior that must happen, use a [hook](hooks.md) instead.

```bash
deepseek-code skills    # list available skills
```

By default the install ships **no skills** — you add them as `.md` files under
`~/.clawspring/skills/` (global) or `.clawspring/skills/` (project). The format and
spec below come from the install's `SKILL_TEMPLATE.md`.

---

## Directory structure

Each skill is a directory containing a `SKILL.md`, plus optional supporting files
loaded on demand:

```
my-skill/
├── SKILL.md          # required — frontmatter + body
├── reference.md      # detailed docs, loaded on demand
├── examples.md       # example outputs
└── scripts/
    └── helper.sh     # something the model can execute
```

Keep `SKILL.md` under ~500 lines; move detail into linked files.

---

## SKILL.md frontmatter — 15 fields

```yaml
---
name: my-skill                    # lowercase + hyphens, max 64 chars
description: What it does and when to use it   # used for auto-invocation matching
when_to_use: Extra trigger phrases / examples  # appended to the description
argument-hint: "[issue-number] [format]"       # autocomplete hint
arguments: [issue, format]        # named positional args for $name substitution
disable-model-invocation: false   # true = only the user can invoke it
user-invocable: true              # false = hide from the / menu (model-only)
allowed-tools: Read, Edit, Bash(gh *)   # pre-approve these tools while active
model: pro                        # model override for this turn only
effort: high                      # effort override for this turn
context: fork                     # fork = run in an isolated subagent context
agent: researcher                 # which subagent type when context: fork
hooks:                            # hooks scoped to this skill's lifecycle
  PreToolUse: [...]
paths: ["src/**/*.ts"]            # globs — auto-load only when matching files present
shell: bash                       # bash (default) or powershell
---
[Body — the actual prompt content]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name; defaults to the directory name |
| `description` | Recommended | What it does + when to use it. **Truncated at 1,536 chars** |
| `when_to_use` | No | Extra trigger context |
| `argument-hint` | No | Autocomplete hint |
| `arguments` | No | Named positional args |
| `disable-model-invocation` | No | `true` = user-only invocation (also drops it from context) |
| `user-invocable` | No | `false` = model-only invocation |
| `allowed-tools` | No | Pre-approve tools (additive, not restrictive) |
| `model` | No | Model override for this turn |
| `effort` | No | Effort override |
| `context` | No | `fork` = run as an isolated subagent |
| `agent` | No | Subagent type when `context: fork` |
| `hooks` | No | Lifecycle hooks |
| `paths` | No | File glob patterns that trigger auto-load |
| `shell` | No | `bash` (default) or `powershell` |

---

## Invocation matrix

| Frontmatter | User can invoke | Model can invoke | In context? |
|-------------|-----------------|------------------|-------------|
| (default) | Yes | Yes | Always |
| `disable-model-invocation: true` | Yes | **No** | Not in context |
| `user-invocable: false` | **No** | Yes | Always |

`allowed-tools` is **additive** (it pre-approves tools while the skill is active) — it
does not restrict the toolset the way a subagent's `tools` field does.

---

## String substitutions

Inside the body, these are replaced before the model sees the prompt:

| Variable | Expands to |
|----------|-----------|
| `$ARGUMENTS` | All args as a single string |
| `$ARGUMENTS[N]` | A specific arg, 0-based |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `$name` | A named arg from the `arguments` list |
| `${CLAWSPRING_SESSION_ID}` | The current session ID |
| `${CLAWSPRING_SKILL_DIR}` | The skill's directory |

---

## Shell injection — dynamic context

A skill body can run shell commands at load time and embed their output. This is
**preprocessing**: the model only ever sees the rendered prompt with real data, never
the raw commands.

Inline:

```markdown
## PR context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
```

Multi-line:

````markdown
```!
node --version
npm --version
git status --short
```
````

---

## Where skills live (precedence)

| Location | Path | Scope |
|----------|------|-------|
| Personal (global) | `~/.clawspring/skills/<name>/SKILL.md` | All your projects |
| Project | `.clawspring/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Wherever the plugin is enabled |

Precedence: **Personal > Project**. Plugin skills are namespaced as `plugin:skill`.

The Clawspring settings cap how much skill metadata loads into context via
`skills.descriptionBudget` (8000 chars in the shipped config) and can auto-compact it
(`skills.autoCompactionEnabled`).

---

## Example: a commit skill

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
Stage and commit changes:

!`git status --short`

Ask for a commit message, then commit.
```

Because `disable-model-invocation: true`, only the user can run `/commit`. (The
shipped permission policy also gates `Skill(commit)` with `ask`.)

---

## Skills vs subagents

See the comparison table in [agents.md](agents.md#skills-vs-subagents). In short:
skills append to the current context and are cheap; subagents replace the context and
isolate it. Combine them with `context: fork` + `agent:` to get a `/command` that runs
in an isolated subagent.

---

## Related

- [agents.md](agents.md) — subagents and the fork pattern
- [hooks.md](hooks.md) — when to enforce instead of suggest
- [architecture.md](architecture.md) — composition / stacking patterns
