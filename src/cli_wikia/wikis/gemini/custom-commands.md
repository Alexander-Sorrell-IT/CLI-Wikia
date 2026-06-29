# Custom Commands

Custom commands let you save frequently used prompts as reusable slash commands. Define them as TOML files, scope them to a project or globally, and enrich them with arguments, shell output, and file content.

## File locations and precedence

Commands are discovered from two directories:

| Scope | Location | Availability |
|---|---|---|
| **User (global)** | `~/.gemini/commands/` | Every project |
| **Project (local)** | `<project-root>/.gemini/commands/` | The current project (can be committed and shared) |

If a project command has the same name as a user command, the **project command wins**, letting projects override global commands.

## Naming and namespacing

A command's name comes from its file path relative to the `commands/` directory. Subdirectories create namespaces, with the path separator (`/` or `\`) converted to a colon (`:`).

| File | Command |
|---|---|
| `~/.gemini/commands/test.toml` | `/test` |
| `<project>/.gemini/commands/git/commit.toml` | `/git:commit` |

## Managing commands

| Command | Action |
|---|---|
| `/commands list` | List all available command files |
| `/commands reload` | Reload `.toml` files after creating or editing them, without restarting the CLI |

## TOML schema (v1)

Definition files use the `.toml` extension and TOML format.

| Field | Required | Description |
|---|---|---|
| `prompt` | Yes | The prompt sent to the model. Single- or multi-line string. |
| `description` | No | One-line description shown in the `/help` menu. If omitted, a generic description is generated from the filename. |

```toml
description = "Asks the model to refactor the current context into a pure function."
prompt = """
Please analyze the code I've provided in the current context.
Refactor it into a pure function.

Your response should include:
1. The refactored, pure function code block.
2. A brief explanation of the key changes you made and why.
"""
```

## Argument injection: `{{args}}`

If the prompt contains `{{args}}`, the CLI replaces it with the text typed after the command name. Behavior depends on context:

- **Raw injection** (in the prompt body): arguments are inserted exactly as typed.
- **Shell-escaped injection** (inside a `!{...}` block): arguments are automatically shell-escaped to prevent command injection.

```toml
# Invoked via: /git:fix "Button is misaligned"
description = "Generates a fix for a given issue."
prompt = "Please provide a code fix for the issue described here: {{args}}."
```

### Default argument handling (no `{{args}}`)

If the prompt does **not** contain `{{args}}`:

- With arguments (e.g. `/mycommand arg1`), the CLI appends the full command you typed to the end of the prompt, separated by two newlines — so the model sees both the instructions and the input.
- Without arguments, the prompt is sent unchanged.

This pattern works well when the prompt instructs the model how to parse the appended raw command:

```toml
# Invoked via: /changelog 1.2.0 added "Support for default argument parsing."
description = "Adds a new entry to the project's CHANGELOG.md file."
prompt = """
# Task: Update Changelog
You are an expert maintainer of this project. The user's raw command is appended
below your instructions. Parse the <version>, <change_type>, and <message> from
their input and use the write_file tool to update CHANGELOG.md.
"""
```

## Shell injection: `!{...}`

Execute a shell command and inject its output into the prompt — ideal for pulling in live context such as a git diff.

```toml
# Invoked via: /git:commit
description = "Generates a Git commit message based on staged changes."
prompt = """
Please generate a Conventional Commit message based on the following git diff:

```diff
!{git diff --staged}
```
"""
```

How it works:

1. Use the `!{...}` syntax to inject command output.
2. Any `{{args}}` inside the block is shell-escaped before substitution.
3. The parser requires **balanced braces** inside `!{...}`. For commands with unbalanced braces, wrap them in an external script and call that script.
4. The CLI runs a **security check** on the final resolved command and shows a confirmation dialog before executing it.
5. On failure, injected output includes stderr followed by a status line such as `[Shell command exited with code 1]`, so the model understands the failure context.

Example combining raw and escaped `{{args}}`:

```toml
prompt = """
Please summarize the findings for the pattern `{{args}}`.

Search Results:
!{grep -r {{args}} .}
"""
```

Running `/grep-code It's complicated` injects the raw arguments in the body and the escaped form inside the shell block, executing `grep -r "It's complicated" .` after confirmation.

## File injection: `@{...}`

Embed file content or a directory listing directly into the prompt.

```toml
# Invoked via: /review FileCommandLoader.ts
description = "Reviews the provided context using a best practice guide."
prompt = """
You are an expert code reviewer.

Your task is to review {{args}}.

Use the following best practices when providing your review:

@{docs/best-practices.md}
"""
```

Details:

- **File:** `@{path/to/file.txt}` is replaced by the file's content.
- **Multimodal:** supported images (PNG, JPEG), PDF, audio, and video are encoded and injected as multimodal input. Other binary files are skipped gracefully.
- **Directory:** `@{path/to/dir}` inserts each file within the directory and its subdirectories, respecting `.gitignore` and `.geminiignore` when enabled.
- **Workspace-aware:** paths are searched in the current directory and other workspace directories. Absolute paths are allowed only within the workspace.
- **Processing order:** `@{...}` is resolved **before** shell commands (`!{...}`) and argument substitution (`{{args}}`).
- **Parsing:** the path inside `@{...}` must have balanced braces.

## Example: create and run a command

```bash
mkdir -p ~/.gemini/commands/refactor
touch ~/.gemini/commands/refactor/pure.toml
# add the TOML content, then in the CLI:
```

```
> @my-messy-function.js
> /refactor:pure
```

The first line adds a file to context; the second invokes the `/refactor:pure` command defined in `~/.gemini/commands/refactor/pure.toml`.

## See also

- [configuration.md](./configuration.md) — settings and `.gemini` directory layout
- [commands.md](./commands.md) — built-in slash command reference
- [mcp.md](./mcp.md) — extending the CLI with MCP tools
