# Built-in tools

Gemini CLI ships with a set of built-in **tools** that let the model act on your
local environment: read and write files, run shell commands, search code, fetch
web pages, and more. Tools extend the model beyond text generation.

Most tools run automatically when the model decides it needs one. Tools that
modify your system (file writes, edits, shell commands) are **mutators** and
require your confirmation before they execute — the CLI shows a diff or the exact
command first. Read-only tools (search, list, read) typically run without a
prompt.

## How tools are invoked

- **Automatic:** The model emits a tool call; Gemini CLI checks it against the
  active security policy, prompts for confirmation if needed, then runs it.
- **`@` (file access):** `@path/to/file` in your prompt injects file content by
  triggering `read_many_files`.
- **`!` (shell):** `!ls -la` runs a command directly via `run_shell_command`.

### Confirmation, sandboxing, trusted folders

- **User confirmation** is required for mutators. Review the diff or command
  carefully before approving.
- **Sandboxing** can isolate tool execution in a container. See the Sandboxing
  guide.
- **Trusted folders** gate whether the model may use system tools in a given
  directory. See the Trusted folders guide.

## Managing and inspecting tools

Use the `/tools` slash command in an interactive session:

| Command | Effect |
| :------ | :----- |
| `/tools` | Lists all registered tools with their display names. |
| `/tools desc` | Lists all tools with their full descriptions. |

This is the quickest way to verify that [MCP servers](./mcp.md) and custom tools
loaded correctly. You can enable, disable, or configure individual tools through
`settings.json` (see [configuration.md](./configuration.md)).

## Tool summary

| Tool | Kind | Category | Confirmation | Summary |
| :--- | :--- | :------- | :----------- | :------ |
| `run_shell_command` | Execute | Execution | Yes | Runs arbitrary shell commands; supports interactive and background processes. |
| `glob` | Search | File system | No | Finds files matching glob patterns. |
| `grep_search` | Search | File system | No | Regex search within file contents (legacy alias `search_file_content`). |
| `list_directory` | Read | File system | No | Lists files and subdirectories in a path. |
| `read_file` | Read | File system | No | Reads one file (text, image, audio, PDF). |
| `read_many_files` | Read | File system | No | Reads and concatenates multiple files; triggered by `@`. |
| `replace` | Edit | File system | Yes | Precise text replacement within a file. |
| `write_file` | Edit | File system | Yes | Creates or overwrites a file. |
| `web_fetch` | Fetch | Web | Yes | Retrieves and processes content from URLs. |
| `google_web_search` | Search | Web | No | Google Search for up-to-date information. |
| `ask_user` | Communicate | Interaction | Yes | Asks you one or more interactive questions. |
| `write_todos` | Other | Interaction | No | Maintains the agent's internal subtask list. |
| `save_memory` | Other | Memory | — | Persists durable facts to Markdown memory files. |
| `activate_skill` | Other | Memory | Yes | Loads an Agent Skill's procedural expertise. |
| `get_internal_docs` | Think | Memory | No | Reads Gemini CLI's own docs for self-questions. |
| `enter_plan_mode` | Plan | Planning | Yes | Switches to read-only Plan Mode. |
| `exit_plan_mode` | Plan | Planning | Yes | Finalizes a plan and requests approval to implement. |
| `list_mcp_resources` | Search | MCP | No | Lists resources from connected MCP servers. |
| `read_mcp_resource` | Read | MCP | No | Reads a specific MCP resource. |

The `Kind` column reflects the internal classification Gemini CLI assigns each
tool (`Execute`, `Read`, `Edit`, `Search`, `Fetch`, `Plan`, `Communicate`,
`Think`, `Other`). Confirmation marked "—" means the docs do not specify a
prompt for that tool.

> **Note:** An experimental **Task Tracker** family
> (`tracker_create_task`, `tracker_update_task`, `tracker_get_task`,
> `tracker_list_tasks`, `tracker_add_dependency`, `tracker_visualize`) and
> `update_topic` exist for progress tracking. They are gated behind
> `experimental.taskTracker` and are out of scope here. The internal
> `complete_task` tool finalizes a subagent's mission and is not user-callable.

## Tool names and the registry

Each built-in tool has a stable **tool name** (used in policy rules and API
calls, e.g. `read_file`) and a human-friendly **display name** shown in the UI
(e.g. `ReadFile`, `FindFiles`, `SearchText`, `Edit`). The `ToolRegistry` class
manages every available tool. You can extend the registry with custom tools via
`tools.discoveryCommand` in settings or by connecting [MCP servers](./mcp.md).
For a deep dive into the internal Tool API, see `packages/core/src/tools/` in the
Gemini CLI repository.

## File system tools

All file system tools operate within a `rootDirectory` (the workspace root) for
security.

### `read_file` (ReadFile)

Reads and returns one file's content. Supports text, images, audio, and PDF.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `file_path` | string | Yes | Path to the file. |
| `offset` | number | No | Start line for text files (0-based). |
| `limit` | number | No | Maximum lines to read. |

(The policy-engine JSON keys are `file_path`, `start_line`, `end_line`; verify in
official docs which form your version uses.)

### `read_many_files` (ReadManyFiles)

Reads and concatenates content from multiple files. Often triggered by the `@`
symbol in your prompt.

| Argument | Type | Description |
| :------- | :--- | :---------- |
| `include` | array/glob | Paths or glob patterns to include. |
| `exclude` | array/glob | Patterns to exclude. |
| `recursive` | boolean | Recurse into subdirectories. |
| `useDefaultExcludes` | boolean | Apply default ignore patterns. |

### `write_file` (WriteFile)

Writes content to a file, overwriting if it exists or creating it if not.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `file_path` | string | Yes | Path to the file. |
| `content` | string | Yes | Data to write. |

**Confirmation:** required. The CLI shows a diff before writing.

### `replace` (Edit)

Precise, targeted text replacement within a file. By default it expects to find
and replace exactly **one** occurrence of `old_string`; provide enough
surrounding context to uniquely identify the location.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `file_path` | string | Yes | Path to the file. |
| `instruction` | string | Yes | Semantic description of the change. |
| `old_string` | string | Yes | Exact literal text to find. |
| `new_string` | string | Yes | Exact literal text to replace it with. |
| `allow_multiple` | boolean | No | If `true`, replace all occurrences; default `false` (exactly one). |

**Confirmation:** required.

### `glob` (FindFiles)

Finds files matching a glob pattern across the workspace.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `pattern` | string | Yes | Glob to match, e.g. `"*.py"`, `"src/**/*.js"`. |
| `path` | string | No | Directory to search within; defaults to root directory. |
| `case_sensitive` | boolean | No | Default `false`. |
| `respect_git_ignore` | boolean | No | Default `true`. |

Returns absolute paths sorted by modification time (newest first) and ignores
nuisance dirs like `node_modules` and `.git` by default. No confirmation.

### `grep_search` (SearchText)

Searches for a regex pattern within file contents. Legacy alias:
`search_file_content`.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `pattern` | string | Yes | Regex to search for, e.g. `"function\s+myFunction"`. |
| `path` | string | No | Directory to search; defaults to the cwd. |
| `include` | string | No | Glob filtering which files are searched, e.g. `"src/**/*.{ts,tsx}"`. |

Uses `git grep` when available for speed, falling back to system `grep` or a
JavaScript search. Returns matching lines prefixed with file path and line
number. No confirmation. Additional policy-engine keys include `exclude_pattern`,
`names_only`, `case_sensitive`, `fixed_strings`, `context`, `after`, `before`,
`no_ignore`, `max_matches_per_file`, and `total_max_matches`.

### `list_directory` (ReadFolder)

Lists names of files and subdirectories directly within a path.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `dir_path` | string | Yes | Absolute or relative directory path. |
| `ignore` | array | No | Glob patterns to exclude. |
| `file_filtering_options` | object | No | `.gitignore` / `.geminiignore` compliance config. |

## Shell tool

### `run_shell_command` (Shell)

Executes commands on your system shell — the primary way the agent interacts with
your environment beyond file edits. On Windows commands run with
`powershell.exe -NoProfile -Command`; elsewhere with `bash -c`.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `command` | string | Yes | The exact shell command. |
| `description` | string | No | Short description shown at confirmation. |
| `dir_path` | string | No | Where the command runs (absolute or relative to root). |
| `is_background` | boolean | No | Move the process to the background immediately. |

**Confirmation:** required. **Return value** is a JSON object with `Command`,
`Directory`, `Stdout`, `Stderr`, `Exit Code`, and `Background PIDs`.

When executing a command, Gemini CLI sets `GEMINI_CLI=1` in the subprocess
environment so scripts can detect they run inside the CLI.

**Interactive commands:** set `tools.shell.enableInteractiveShell` to `true` to
use a pseudo-terminal (`node-pty`), enabling `vim`, `nano`, `htop`,
`git rebase -i`, etc. Press `Tab` to focus the interactive shell. Falls back to
`child_process` (non-interactive) when `node-pty` is unavailable. Related
settings: `tools.shell.showColor` and `tools.shell.pager` (default `cat`),
which apply only when interactive shell is enabled, and
`tools.shell.inactivityTimeout` (seconds before a stalled process is killed).

**Command restrictions** are covered under [Policy and allowlisting](#policy-and-allowlisting).

## Web tools

### `google_web_search` (GoogleSearch)

Performs a Google Search for up-to-date information.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `query` | string | Yes | The search query. |

Returns a grounded summary with source URIs and titles. The Gemini API processes
the results before returning a synthesized response. No confirmation.

### `web_fetch` (WebFetch)

Retrieves and processes content from URLs in your prompt.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `prompt` | string | Yes | A request containing up to 20 `http(s)` URLs plus instructions for processing them. |

**Confirmation:** triggers a dialog showing the converted URLs. Uses the Gemini
API's `urlContext` for retrieval, falling back to a direct local fetch if API
access fails, and returns a synthesized response with source attribution.

> **Warning:** `web_fetch` can reach local and private network addresses (e.g.
> `localhost`), a risk with untrusted prompts. In Plan Mode it always requires
> explicit user confirmation.

## Interaction tools

### `ask_user` (Ask User)

Asks you 1–4 questions to gather preferences or clarify requirements. Pauses
execution until you answer or dismiss the dialog, then returns answers as a JSON
string indexed by question position.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `questions` | array | Yes | 1–4 question objects (see below). |

Each question object: `question` (full text), `header` (≤16-char chip label),
`type` (`choice` default, `text`, or `yesno`), `options` (2–4 objects with
`label` and `description`, required for `choice`), `multiSelect`, `placeholder`.

```json
{
  "questions": [
    {
      "header": "Database",
      "question": "Which database would you like to use?",
      "type": "choice",
      "options": [
        { "label": "PostgreSQL", "description": "Object-relational database." },
        { "label": "SQLite", "description": "Embedded SQL engine." }
      ]
    }
  ]
}
```

**Confirmation:** inherent — the tool is interactive.

### `write_todos` (TodoWrite)

Maintains the agent's internal subtask list for multi-step requests, updating the
progress indicator above the input prompt.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `todos` | array | Yes | Full task list; each item has `description` and `status`. |

`status` is one of `pending`, `in_progress`, `completed`, `cancelled`, or
`blocked`. Only one task may be `in_progress` at a time. State is session-scoped;
toggle the full list view with **Ctrl+T**. No confirmation.

## Memory tools

### `save_memory`

Persists durable facts, user preferences, and project details by editing
Markdown memory files directly (using `write_file` or `replace` under the hood).
Project-wide instructions go in repository `GEMINI.md` files, private project
notes in the per-project private memory folder, and personal cross-project
preferences in the global `~/.gemini/GEMINI.md`. Saved facts load automatically
into the hierarchical context system for future sessions. See the
[Project context (GEMINI.md)](./configuration.md) system for how this loads.

### `activate_skill` (Activate Skill)

Loads a discovered [Agent Skill](./skills.md)'s instructions and bundled
resources into context.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `name` | enum | Yes | Name of the skill to activate, e.g. `code-reviewer`. |

Used exclusively by the agent — you cannot call it manually. Activation prompts
you for consent and grants the agent read access to the skill's directory. See
[skills.md](./skills.md).

### `get_internal_docs`

Reads Gemini CLI's own documentation (`path` argument) so the agent can answer
questions about its own capabilities accurately. No confirmation.

## Planning tools

### `enter_plan_mode` (Enter Plan Mode)

Switches the CLI into a safe, read-only **Plan Mode** for researching complex
changes. Typically called when you ask the agent to "start a plan."

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `reason` | string | No | Short reason for entering Plan Mode. |

Switches the approval mode to `PLAN` and notifies you. **Confirmation:** yes.
Not available in YOLO mode.

### `exit_plan_mode` (Exit Plan Mode)

Signals that planning is complete, presents the finalized plan, and requests
approval to implement. The agent must reach informal agreement with you in chat
before calling it.

| Argument | Type | Required | Description |
| :------- | :--- | :------- | :---------- |
| `plan_path` | string | Yes | Path to the finalized Markdown plan; must live in the project's temporary plans dir, e.g. `~/.gemini/tmp/<project>/plans/`. |

On approval the CLI switches to the chosen approval mode (`DEFAULT` or
`AUTO_EDIT`) and marks the plan approved; on rejection it stays in Plan Mode and
returns your feedback to the model. **Confirmation:** yes.

## MCP tools

When you connect [MCP servers](./mcp.md), their tools are registered alongside
the built-ins and appear in `/tools`. Two built-in tools work with MCP servers
directly:

- **`list_mcp_resources`** — lists all resources exposed by connected MCP
  servers (Search, no confirmation).
- **`read_mcp_resource`** — reads a specific MCP resource (Read, no
  confirmation).

MCP tools are named after the server and the remote tool; confirmation behavior
follows the server's trust configuration. See [mcp.md](./mcp.md).

## `.geminiignore` and `.gitignore`

File-discovery tools honor ignore files so the agent does not surface excluded
paths:

- `glob` accepts `respect_git_ignore` (default `true`) and
  `respect_gemini_ignore`.
- `list_directory` accepts `file_filtering_options` to configure `.gitignore`
  and `.geminiignore` compliance.
- `grep_search` exposes `no_ignore` to bypass ignore rules when needed.

Add a `.geminiignore` file at the workspace root (same syntax as `.gitignore`) to
keep files out of tool results regardless of git status.

## Policy and allowlisting

Tool execution is governed by the **policy engine** and a few settings.

### Allowlisting built-in tools (`tools.core`)

> **Warning:** `tools.core` is an allowlist for **all** built-in tools, not just
> shell. When set to any value, only the listed tools are enabled — including
> `read_file`, `write_file`, `glob`, `grep_search`, etc.

Restrict `run_shell_command` to specific command prefixes by adding entries in
the form `run_shell_command(<prefix>)`:

```json
{
  "tools": {
    "core": ["run_shell_command(git)", "run_shell_command(npm)"]
  }
}
```

`git status` and `npm install` are allowed; `ls -l` is blocked. Including the
bare `run_shell_command` acts as a wildcard. `tools.exclude` is a blocklist
(checked first, takes precedence) but is **deprecated** — use the policy engine
to block commands instead:

```json
{
  "tools": {
    "core": ["run_shell_command"],
    "exclude": ["run_shell_command(rm)"]
  }
}
```

Validation rules: commands chained with `&&`, `||`, or `;` are split and each
part validated separately (any disallowed part blocks the whole chain); matching
is by prefix (`git` allows `git status`); the blocklist always wins.

### Policy engine and `--allowed-tools`

The policy engine matches tool calls by `toolName` and an `argsPattern` (a regex
over the JSON arguments) to `allow`, `deny`, or `ask`. Knowing each tool's JSON
argument keys is essential — for example, deny writes to `.env` files:

```toml
[[rule]]
toolName = "write_file"
argsPattern = '"file_path":".*\.env"'
decision = "deny"
priority = 100
denyMessage = "Writing to .env files is not allowed."
```

For shell rules the policy engine offers `commandPrefix` and `commandRegex`
shorthands (sugar over `toolName = "run_shell_command"` + `argsPattern`; they are
not arguments of the tool itself). The `--allowed-tools` flag and related policy
controls let you pre-approve specific tools so they run without prompting; see
[configuration.md](./configuration.md) and the policy engine reference (verify in
official docs for the exact `--allowed-tools` syntax in your version).

### Argument keys for policy rules

| Tool | JSON argument keys |
| :--- | :----------------- |
| `run_shell_command` | `command`, `description`, `dir_path`, `is_background` |
| `glob` | `pattern`, `dir_path`, `case_sensitive`, `respect_git_ignore`, `respect_gemini_ignore` |
| `grep_search` | `pattern`, `dir_path`, `include_pattern`, `exclude_pattern`, `names_only`, `case_sensitive`, `fixed_strings`, `context`, `after`, `before`, `no_ignore`, `max_matches_per_file`, `total_max_matches` |
| `list_directory` | `dir_path`, `ignore`, `file_filtering_options` |
| `read_file` | `file_path`, `start_line`, `end_line` |
| `read_many_files` | `include`, `exclude`, `recursive`, `useDefaultExcludes` |
| `write_file` | `file_path`, `content` |
| `replace` | `file_path`, `old_string`, `new_string`, `instruction`, `allow_multiple` |
| `ask_user` | `questions` |
| `write_todos` | `todos` |
| `activate_skill` | `name` |
| `get_internal_docs` | `path` |
| `enter_plan_mode` | `reason` |
| `exit_plan_mode` | `plan_path` |
| `google_web_search` | `query` |
| `web_fetch` | `prompt` |

## See also

- [skills.md](./skills.md) — Agent Skills and the `activate_skill` tool
- [mcp.md](./mcp.md) — connecting MCP servers and their tools
- [configuration.md](./configuration.md) — settings, `tools.*`, and policy
- [extensions.md](./extensions.md) — bundling tools and skills
- [cli-reference.md](./cli-reference.md) — slash commands and flags
