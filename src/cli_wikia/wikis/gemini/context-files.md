# Context files (GEMINI.md)

Context files — named `GEMINI.md` by default — provide persistent, instructional
context to the model. Use them for project-specific instructions, a persona, or
a coding style guide instead of repeating yourself in every prompt. The CLI
concatenates all loaded context files and sends them with every prompt.

## Context hierarchy

The CLI sources context from several locations and loads them in this order:

1. **Global context file** — `~/.gemini/GEMINI.md` in your home directory.
   Default instructions applied across all your projects.
2. **Environment / workspace context files** — `GEMINI.md` files found in your
   configured workspace directories and their **parent** directories. Context
   relevant to the project you are currently working on.
3. **Just-in-time (JIT) context files** — when a tool accesses a file or
   directory, the CLI scans that directory and its **ancestors** (up to a trusted
   root) for `GEMINI.md`. Lets the model discover instructions for specific
   components only when needed.

The CLI footer shows the number of loaded context files, a quick visual cue of
the active instructional context.

### Example `GEMINI.md`

```markdown
# Project: My TypeScript Library

## General Instructions

- When you generate new TypeScript code, follow the existing coding style.
- Ensure all new functions and classes have JSDoc comments.
- Prefer functional programming paradigms where appropriate.

## Coding Style

- Use 2 spaces for indentation.
- Prefix interface names with `I` (for example, `IUserService`).
- Always use strict equality (`===` and `!==`).
```

## The `/memory` command

Inspect and manage the loaded context with `/memory`:

| Command            | Action                                                                       |
| ------------------ | ---------------------------------------------------------------------------- |
| `/memory show`     | Display the full, concatenated hierarchical memory sent to the model.        |
| `/memory reload`   | Force a re-scan and reload of all `GEMINI.md` files from every location.     |
| `/memory inbox`    | Open the Auto Memory review inbox (experimental; see below).                 |

> The CLI footer's context-file count updates after a reload. (If your build
> exposes a `/memory refresh` or `/memory list` variant, verify in official docs.)

## Customize the context file name

`GEMINI.md` is the default, but you can configure one or more names with the
`context.fileName` setting. The CLI looks for each name in the hierarchy.

```json
{
  "context": {
    "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]
  }
}
```

## Imports (Memory Import Processor)

Break large context files into reusable pieces using the `@path` syntax. An `@`
followed by a path inlines that file's content where the directive appears.

```markdown
# Main GEMINI.md file

This is the main content.

@./components/instructions.md

More content here.

@../shared/style-guide.md
```

### Supported paths

| Form                       | Meaning                          |
| -------------------------- | -------------------------------- |
| `@./file.md`               | Same directory.                  |
| `@../file.md`              | Parent directory.                |
| `@./components/file.md`    | Subdirectory.                    |
| `@/absolute/path/file.md`  | Absolute path.                   |

### Rules and safety

- **Nested imports** — imported files may themselves import others.
- **Circular imports** are detected and prevented.
- **Maximum depth** — recursion is capped (default: 5 levels).
- **Path validation** — imports are only allowed from permitted directories
  (`validateImportPath`), blocking access to sensitive files outside the scope.
- **Code regions ignored** — `@` references inside code blocks or inline code
  spans are not treated as imports (detected via the `marked` library).
- **Missing or unreadable files** fail gracefully, leaving an error comment in
  the output rather than aborting.

The processor returns an **import tree** showing which files were read and their
relationships, useful for debugging:

```
Memory Files
 L project: GEMINI.md
            L a.md
              L b.md
            L included.md
```

## Auto Memory (experimental)

Auto Memory mines your past, idle Gemini CLI sessions in the background and
proposes durable memory updates and reusable [Agent Skills](./subagents.md). It
is **off by default** and never applies anything without your approval.

Enable it in `~/.gemini/settings.json` (or a project's `.gemini/settings.json`)
and restart:

```json
{ "experimental": { "autoMemory": true } }
```

How it works:

- On session startup a background task scans recent transcripts in
  `~/.gemini/tmp/<project>/chats/`. A session is eligible only if it has been
  **idle ≥ 3 hours** and contains **≥ 10 user messages**; active, trivial, and
  sub-agent sessions are ignored.
- An extraction agent (a preview Gemini Flash model) drafts candidates: memory
  updates as unified-diff `.patch` files and procedures as `SKILL.md` files. It
  defaults to producing nothing unless evidence is strong, so many runs yield no
  items.
- Candidates land in a project-local **review inbox**. Auto Memory cannot
  directly edit active memory, settings, credentials, or project `GEMINI.md`
  files. When new candidates appear, the CLI shows an inline notice.

Review with `/memory inbox`. From the dialog you can read a `SKILL.md`, **promote**
a skill to user scope (`~/.gemini/skills/`) or workspace scope
(`.gemini/skills/`), **apply** or reject skill patches, and **apply** or dismiss
private (project) or global (`~/.gemini/GEMINI.md`) memory patches. Memory patches
are target-allowlisted and applied atomically, then memory reloads for the
current session.

> Auto Memory does not extract from the current session or from shared project
> `GEMINI.md` files; it proposes only private project memory, global personal
> memory, and skills. Disable by setting `autoMemory` back to `false` and
> restarting.

## Ignoring files (.geminiignore)

A `.geminiignore` file in your project root excludes paths from tools that
respect it — for example, files matched here are dropped when you share files
with the `@` command. Ignored files remain visible to other services like Git.

Syntax mostly follows `.gitignore`:

- Blank lines and `#` comments are ignored.
- Standard globs (`*`, `?`, `[]`) are supported.
- A trailing `/` matches directories only.
- A leading `/` anchors the pattern to the `.geminiignore` location.
- `!` negates (re-includes) a pattern.

```
# Exclude the /packages/ directory and all subdirectories
/packages/

# Exclude a specific file
apikeys.txt

# Exclude all .md files except README.md
*.md
!README.md
```

> Edits to `.geminiignore` take effect only after you **restart** the Gemini CLI
> session.

## See also

- [configuration.md](./configuration.md) — `context.fileName`, settings scopes
- [settings.md](./settings.md) — `experimental.autoMemory`
- [commands.md](./commands.md) — `/memory`, `@` file references
- [subagents.md](./subagents.md) — Agent Skills promoted by Auto Memory
