# Custom Instructions

Custom instructions are natural-language Markdown files that Copilot automatically folds into your prompts, so it follows your project's conventions without being told each time. Copilot CLI reads several kinds, with a clear precedence.

Reference: [Adding custom instructions for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions).

---

## The file types

### `AGENTS.md` — primary instructions

One or more `AGENTS.md` files, searched in:

- the **repository root**,
- the **current working directory**, and
- any directory listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` (comma-separated).

The `AGENTS.md` at the **repo root** is treated as the **primary** instructions and carries the most weight. Tool-specific alternatives at the repo root are also recognized: `CLAUDE.md` (Claude models) and `GEMINI.md` (Gemini models).

A personal, machine-wide file is read from `$HOME/.copilot/copilot-instructions.md`.

### `.github/copilot-instructions.md` — repository-wide

Applies to all requests in the repo. This is the file `copilot init` generates after scanning your codebase.

### `.github/instructions/**/*.instructions.md` — path-scoped

Apply only to files matching a glob, via frontmatter:

```markdown
---
applyTo: "app/models/**/*.rb"
---

Use ActiveRecord scopes instead of raw SQL in model methods.
```

Multiple patterns are comma-separated, e.g. `applyTo: "**/*.ts,**/*.tsx"`. These files are searched within or below `.github/instructions` at the repo root, or below a `.github/instructions` directory in the current working directory.

---

## Precedence & interaction

- Root `AGENTS.md` = **primary**, more influential than instructions found elsewhere.
- If both `.github/copilot-instructions.md` and path-scoped `*.instructions.md` apply, **both are used**.
- If an `AGENTS.md` and a `.github/copilot-instructions.md` both exist at the root, **both** are used.
- Copilot's choice between *conflicting* instructions is **non-deterministic** — avoid contradictions.

---

## Restricting where instructions apply

Add an `excludeAgent` key to an instruction file's frontmatter to stop a given agent from using it. Valid values: `"code-review"` or `"cloud-agent"`.

```markdown
---
applyTo: "**/*.py"
excludeAgent: "code-review"
---
```

---

## Generating and managing

```bash
copilot init                 # write .github/copilot-instructions.md from a repo scan
copilot --no-custom-instructions   # ignore all instruction files this run
```

Inside a session:

- `/init` — same as `copilot init`.
- `/instructions` — view and toggle which instruction files are active.
- `/env` — confirm which instruction files (and MCP servers, skills, agents, hooks…) loaded.

Add extra search directories with the `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` env var (comma-separated). Copilot looks for an `AGENTS.md` and any `.github/instructions/**/*.instructions.md` in each.

---

## How this differs from agents and skills

| Mechanism | Scope | Loaded |
|---|---|---|
| Custom instructions | Always-on guidance for a repo/path | Automatically into every prompt |
| [Custom agents](custom-agents.md) | A whole persona (instructions + tools + model) | When you pick the agent |
| [Skills](skills.md) | A narrow, callable capability | On demand when relevant |

---

## See also

- [custom-agents.md](custom-agents.md)
- [skills.md](skills.md)
- [configuration.md](configuration.md)
