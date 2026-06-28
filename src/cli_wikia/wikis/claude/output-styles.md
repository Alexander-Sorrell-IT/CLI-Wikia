# Output Styles

Output styles change how Claude **responds** (tone, role, format) — they don't change what Claude knows or what tools it has. They modify the system prompt while keeping core capabilities unchanged.

---

## Built-in styles

| Style | Behavior |
|---|---|
| `Default` | Standard software engineer mode |
| `Explanatory` | Adds `★ Insight ─────────────` blocks teaching patterns and architectural choices |
| `Learning` | Collaborative, learn-by-doing mode. Claude leaves `TODO(human)` markers for you to implement 5–10 lines of meaningful code |

---

## Selecting

```
/config        # interactive picker → "Output style"
```

Or in settings:

```json
{ "outputStyle": "Explanatory" }
```

Or per-session via `--output-style` (where supported by the CLI surface).

---

## Custom output styles

```markdown
# ~/.claude/output-styles/trainer/OUTPUT_STYLE.md

---
name: Technical Trainer
description: Teaches code patterns through guided discovery
keep-coding-instructions: true
---

You are a patient technical trainer. Help users learn, not just solve problems.

## How to teach

1. **Ask guiding questions** before revealing the answer.
2. **Explain the "why"** behind patterns, not just the "how".
3. **Show before/after** comparisons.
4. **Highlight edge cases** that test understanding.

## Specific behaviors

- When implementing features, ask "What would you try first?"
- After debugging, explain the root cause.
- Suggest exercises to reinforce concepts.
```

### Locations

| Scope | Path |
|---|---|
| Personal | `~/.claude/output-styles/<name>/OUTPUT_STYLE.md` |
| Project | `.claude/output-styles/<name>/OUTPUT_STYLE.md` |
| Plugin | `<plugin>/output-styles/<name>/OUTPUT_STYLE.md` |

### Frontmatter

| Field | Purpose |
|---|---|
| `name` | Display name in menu |
| `description` | Shown in `/config` picker |
| `keep-coding-instructions` | Boolean. Keep coding/testing instructions from Claude Code's default prompt. Default: `false` (i.e., they're removed unless you set this) |

---

## Output styles vs related features

| Feature | What it does |
|---|---|
| **Output style** | Modifies system prompt (role, tone, format). Removes coding instructions unless `keep-coding-instructions: true` |
| **CLAUDE.md** | Provides project context (facts, conventions). Added as a user message **after** the system prompt |
| **Subagents** | Custom system prompts for specific tasks; isolated context, tool restrictions |
| **Skills** | Task-specific workflows you invoke with `/skill-name`; load on demand |
| **`--append-system-prompt`** | Appends text to system prompt for one session; doesn't persist |

---

## Composition

- Output styles are mutually exclusive (only one active at a time).
- They're orthogonal to CLAUDE.md — both can exist; CLAUDE.md adds context, the style changes voice.
- They don't restrict tool access — that's the [permissions](./permissions.md) system.
- They affect how Claude *formats and explains* responses.

---

## Token cost considerations

- Adding an output style increases input tokens (but prompt caching reduces this after the first request in a session).
- `Explanatory` and `Learning` intentionally produce longer responses (more output tokens).

---

## See also

- [skills.md](./skills.md) — for task-specific behavior
- [memory.md](./memory.md) — for project context (CLAUDE.md)
- [cli-reference.md](./cli-reference.md) — `--append-system-prompt`, `--system-prompt`
