# Customization: Rules & Skills

You steer an Antigravity agent with two complementary mechanisms:

- **Rules** (`AGENTS.md`) — constraints that are *always* applied. Use them for
  "always do it this way" facts and style.
- **Skills** (`SKILL.md`) — capabilities loaded *on demand* when relevant. Use
  them for "when the task is X, follow this procedure."

Both are *suggestions* the model follows — for hard enforcement use
[hooks](./hooks.md) or [permissions](./permissions.md).

Both can be defined **globally** or **per workspace**:

| Scope | Location |
|-------|----------|
| Global | `~/.gemini/config/` — `AGENTS.md`, `skills/<name>/SKILL.md` |
| Workspace | `<project-root>/.agents/` — `AGENTS.md`, `skills/` |

Workspace definitions override/extend the global ones for that project.

---

## Rules (`AGENTS.md`)

A **rule** is just a Markdown file of constraints you want the agent to obey —
coding style, project conventions, "never touch the generated/ folder," preferred
libraries, and so on. They are always loaded into the agent's context.

```markdown
# AGENTS.md

- Use TypeScript strict mode; never add `any`.
- All HTTP handlers go in `src/routes/`, one file per resource.
- Run `npm run lint` before declaring a task done.
```

- **Global** (`~/.gemini/config/AGENTS.md`) applies to every project.
- **Workspace** (`<project-root>/.agents/AGENTS.md`) applies to that repo and
  overrides/extends the global rules.

> Community/official sources describe individual rule files as capped at roughly
> **12,000 characters each**. Treat that limit as approximate and **verify in
> official docs** (`https://antigravity.google/docs/rules`). `AGENTS.md` is
> Antigravity's analog to the Gemini CLI's `GEMINI.md` and Claude's `CLAUDE.md`.

---

## Skills (`SKILL.md`)

A **skill** is a directory-based package — a `SKILL.md` definition plus optional
supporting assets (scripts, references, templates). Unlike a rule (always
loaded), a skill is **loaded into context only when the agent decides it's
relevant**, keeping the context window lean and avoiding distraction.

### Anatomy

```
skills/
└── analyze/
    └── SKILL.md
```

```markdown
---
name: analyze
description: Analyzes code changes on your current branch for common security vulnerabilities
---
You are a highly skilled senior security analyst. Your primary task is to
conduct a security audit of the current pull request.
...
```

The frontmatter has two key fields:

| Field | Purpose |
|-------|---------|
| `name` | The skill's identifier (and slash-command name) |
| `description` | When the agent should activate the skill — this is what drives on-demand loading |

The body is the prompt/procedure the agent follows once the skill activates. A
skill can include `references/` files (longer docs the skill tells the agent to
read) and helper scripts — for example, Antigravity's own bundled
`antigravity-guide` skill ships `references/cli.md`, `app.md`, `ide.md`, and
`sdk.md`.

### Listing & invoking

```
/skills        # list active skills in the TUI
```

Skills also surface as **slash commands** named after the skill. They can be
shipped inside [plugins](./plugins.md) (e.g. the `gemini-cli-security` plugin
bundles `analyze` and `analyze-github-pr`).

> The complete `SKILL.md` frontmatter field set, supporting-file conventions, and
> `skills.json` mapping are documented at
> `https://antigravity.google/docs/skills`. The two fields above are confirmed
> from real bundled skills; verify the full schema in official docs.

---

## Rules vs Skills vs Hooks — which to use

| You want… | Use |
|-----------|-----|
| A fact/convention applied to *everything* | **Rule** (`AGENTS.md`) |
| A procedure loaded *only when relevant* | **Skill** (`SKILL.md`) |
| Something to happen/never-happen *for sure* | **Hook** ([hooks.md](./hooks.md)) |
| To ship the above to others | **Plugin** ([plugins.md](./plugins.md)) |

---

## See also

- [plugins.md](./plugins.md) — bundle rules/skills/MCP/hooks for distribution
- [hooks.md](./hooks.md) — deterministic enforcement
- [configuration.md](./configuration.md) — where customization roots live
