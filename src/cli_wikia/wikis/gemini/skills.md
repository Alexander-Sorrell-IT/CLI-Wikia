# Agent Skills

Agent Skills extend Gemini CLI with specialized, **on-demand expertise** —
procedural workflows, conventions, and bundled resources for tasks like security
auditing, cloud deployments, or codebase migrations. A skill is a self-contained
directory packaging instructions and assets into a discoverable capability,
following the [Agent Skills](https://agentskills.io) open standard.

Unlike [GEMINI.md](./configuration.md) context files, which provide persistent
workspace-wide background, Skills load only when relevant. This keeps the model's
context window uncluttered while still giving it access to a large library of
capabilities.

> **Note:** Agent Skills are a newer, evolving feature. Details such as exact CLI
> flags and discovery aliases may change between releases — verify against the
> official docs for your version (installed CLI is v0.22.4; this page documents
> the current docs, which may be ahead).

## How it works

The lifecycle is **discovery → activation → consent → injection → execution**:

1. **Discovery:** At session start, Gemini CLI scans the discovery tiers and
   injects the **name and description** of each enabled skill into the system
   prompt (progressive disclosure — full instructions are not loaded yet).
2. **Activation:** When the model finds a task matching a skill's description, it
   calls the [`activate_skill`](./tools.md) tool.
3. **Consent:** You see a confirmation prompt showing the skill's name, purpose,
   and the directory path it will gain access to.
4. **Injection:** On approval, the `SKILL.md` body and folder structure are added
   to the conversation, and the skill's directory is added to the agent's allowed
   file paths (so it can read bundled assets).
5. **Execution:** The model proceeds with the specialized expertise active,
   prioritizing the skill's procedural guidance.

Activation is driven entirely by the agent — `activate_skill` takes a single
`name` argument and cannot be invoked manually.

## Discovery tiers

Skills are discovered from several locations, in increasing order of precedence
(lowest to highest):

| Tier | Location | Scope |
| :--- | :------- | :---- |
| Built-in | Shipped with Gemini CLI (pre-approved) | Always available |
| Extension | Bundled inside installed [extensions](./extensions.md) | Where the extension is enabled |
| User | `~/.gemini/skills/` or the `~/.agents/skills/` alias | All your projects |
| Workspace | `.gemini/skills/` or the `.agents/skills/` alias | This project (shared via version control) |

**Precedence and aliases:** If multiple skills share a name, the version from the
higher-precedence tier wins. Within the same tier, the `.agents/skills/` alias
takes precedence over `.gemini/skills/`. The `.agents/skills/` path is an
interoperable convention compatible with other AI tools that follow the Agent
Skills standard.

## SKILL.md format

A skill directory needs only a `SKILL.md` file, but the recommended structure
bundles supporting resources:

```text
my-skill/
├── SKILL.md       (Required) Instructions and metadata
├── scripts/       (Optional) Executable scripts
├── references/    (Optional) Static documentation
└── assets/        (Optional) Templates and other resources
```

When a skill activates, the model is granted access to this **entire directory**
and can be instructed to use the files within it.

### Frontmatter

`SKILL.md` opens with YAML frontmatter, followed by Markdown instructions:

```markdown
---
name: code-reviewer
description:
  Expertise in reviewing code changes for correctness, security, and style. Use
  when the user asks to "review" their code or a PR.
---

# Code Reviewer Instructions

You act as a senior software engineer specialized in code quality. When this
skill is active, you MUST:

1. **Analyze**: Review the code for logical errors, security issues, and style.
2. **Review**: Use the bundled `scripts/review.js` utility for an automated check.
3. **Feedback**: Distinguish critical issues from minor improvements.
```

| Field | Required | Description |
| :---- | :------- | :---------- |
| `name` | Yes | Unique identifier; should match the directory name. |
| `description` | Yes | **Critical** — how Gemini decides when to use the skill. Be specific about the tasks it handles and the keywords that should trigger it. |

Reference bundled scripts and files from the instructions so the model knows what
each contains and when to use it.

## Activating and using skills

You don't activate skills yourself — phrase a request that matches a skill's
description and Gemini proposes activation. For the `code-reviewer` example above:

1. Ask something matching the description, e.g. *"Can you review index.js?"*
2. Gemini matches the request to the skill and asks permission to activate it.
3. After you approve, it runs the bundled logic, e.g.
   `node .gemini/skills/code-reviewer/scripts/review.js index.js`.

Confirm a skill loaded with `/skills list` (or `/skills`).

## Managing skills

### `/skills` slash command (interactive)

| Command | Effect |
| :------ | :----- |
| `/skills list [all] [nodesc]` | Show discovered skills. `all` includes built-in skills; `nodesc` hides descriptions. |
| `/skills link <path> [--scope user\|workspace]` | Link a local skill directory for immediate use. |
| `/skills enable <name>` | Re-enable a disabled skill. |
| `/skills disable <name>` | Prevent a skill from being triggered. |
| `/skills reload` (or `refresh`) | Re-scan all tiers without restarting. |

> **Note:** `/skills enable` and `/skills disable` default to the **user** scope.
> Pass `--scope workspace` to manage workspace-specific settings.

### `gemini skills` subcommands (terminal)

```bash
# List all discovered skills (--all includes built-in skills)
gemini skills list --all

# Install a skill from a Git repo, URL, or local .skill package
# --consent skips the security confirmation prompt
gemini skills install https://github.com/user/repo.git --consent

# Link a local directory for development
gemini skills link ./path/to/my-skill

# Uninstall an installed or linked skill
gemini skills uninstall my-skill --scope workspace
```

| Option | Description |
| :----- | :---------- |
| `--scope` | `user` (global, default) or `workspace` (current project). |
| `--path` | Sub-directory within a Git repo that contains the skill. |
| `--consent` | Acknowledge security risks and skip the interactive install confirmation. |
| `--all` | (for `list`) Include built-in skills. |

`install` defaults to the user profile; add `--scope workspace` to install only
for the current project.

## Creating a skill

### With the `skill-creator` meta-skill

The fastest path is to ask Gemini CLI to build one, e.g. *"Create a new skill
called 'code-reviewer' that analyzes local files for common errors and style
violations."* It scaffolds a directory, a `SKILL.md` with `name`/`description`
frontmatter, and the standard `scripts/`, `references/`, and `assets/` folders.

### Manually

```bash
# macOS/Linux
mkdir -p .gemini/skills/code-reviewer/scripts
```

Then create `.gemini/skills/code-reviewer/SKILL.md` with frontmatter and
instructions (see [SKILL.md format](#skillmd-format)), and add any scripts under
`scripts/`. Gemini CLI auto-discovers skills in `.gemini/skills`; start a new
session (or `/skills reload`) and trigger it to test.

### Development scripts

The core package ships helper scripts used by the built-in tooling:

- **Initialize:** `node scripts/init_skill.cjs <name> --path <dir>`
- **Validate:** `node scripts/validate_skill.cjs <path/to/skill>`
- **Package:** `node scripts/package_skill.cjs <path/to/skill>` (creates a
  `.skill` zip)

While developing in a separate directory, link it into your user skills for
testing with `gemini skills link .`.

## Sharing skills

- **Workspace:** commit `.gemini/skills/` to your project repository.
- **Extensions:** bundle skills inside a Gemini CLI [extension](./extensions.md).
- **Git repositories:** share a skill directory as a standalone repo and install
  with `gemini skills install <url>`.

## Security and consent

Skills can execute scripts and access your files, so consent is enforced at two
points:

1. **Installation consent:** Installing from a remote URL asks you to confirm the
   source (skip with `--consent`).
2. **Activation consent:** Each time a skill is triggered in a session, the agent
   must ask permission to activate it and gain access to its resources.

Built-in skills are pre-approved. Disabled skills (`/skills disable`) are never
triggered.

## Best practices

- **Write a specific `description`.** It is the sole signal Gemini uses to decide
  when to activate the skill — name the tasks and trigger keywords explicitly.
- **Keep `name` matched to the directory** for predictable precedence.
- **Bundle deterministic logic as scripts** under `scripts/` rather than relying
  on the model to reproduce steps, and reference them from `SKILL.md`.
- **Use progressive disclosure:** keep `SKILL.md` focused; put long reference
  material in `references/` so it loads only when needed.
- **Scope appropriately:** workspace skills for team/project conventions, user
  skills for personal cross-project expertise.

## See also

- [tools.md](./tools.md) — the `activate_skill` tool and built-in tools
- [extensions.md](./extensions.md) — bundling skills inside extensions
- [configuration.md](./configuration.md) — GEMINI.md context and settings
- [mcp.md](./mcp.md) — another way to extend the agent's capabilities
- [cli-reference.md](./cli-reference.md) — full command and flag reference
