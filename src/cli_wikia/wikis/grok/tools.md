# Tools

Grok CLI (`@vibe-kit/grok-cli` 0.0.34) exposes **8 internal tools** to the model in
OpenAI function-calling format, defined in `dist/grok/tools.js` (`BASE_GROK_TOOLS`)
and dispatched by the switch in `dist/agent/grok-agent.js:521-544`. Seven are always
present; the eighth (`edit_file`) is conditional. MCP server tools are appended to
the same list dynamically at runtime.

---

## Core tools

| Tool | Parameters | Purpose |
|------|------------|---------|
| `view_file` | `path`, optional `start_line`/`end_line` | View file contents or list a directory |
| `create_file` | `path`, `content` | Create a **new** file (not for editing existing ones) |
| `str_replace_editor` | `path`, `old_str`, `new_str`, `replace_all` | Replace text in an existing file; fuzzy matching for multi-line strings |
| `bash` | `command` | Execute a bash command |
| `search` | `query`, `search_type` (`text`\|`files`\|`both`), glob include/exclude, regex flags | Unified ripgrep-backed text/file search (via `ripgrep-node`) |
| `create_todo_list` | array of `{id, content, status, priority}` items | Create a visual todo list for planning |
| `update_todo_list` | todo updates | Update existing todos |
| `edit_file` | `target_file`, `instructions`, `code_edit` | **Conditional** — Morph Fast Apply abbreviated-edit format (see below) |

Tool name definitions in `dist/grok/tools.js`: `view_file` (line 7), `create_file`
(32), `str_replace_editor` (53), `bash` (82), `search` (99), `create_todo_list`
(154), `update_todo_list` (195), `edit_file` (238).

---

## Conditional tool: `edit_file` (Morph Fast Apply)

`edit_file` is only registered when the **`MORPH_API_KEY`** environment variable is
set. `buildGrokTools()` (`tools.js:261-268`) splices `MORPH_EDIT_TOOL` into the
array right after `str_replace_editor` when the key is present; otherwise the model
never sees it. It sends abbreviated edits to Morph's Fast Apply service (the npm
README advertises "4,500+ tokens/sec with 98% accuracy"). Without `MORPH_API_KEY`,
all edits go through `str_replace_editor`.

```bash
export MORPH_API_KEY=...   # enables the edit_file tool for this session
```

---

## MCP tools

Tools from configured MCP servers are **appended dynamically** to the same tool list
(`addMCPToolsToGrokTools`, `tools.js:333-340`) under their own names, so the model
calls them exactly like internal tools. Servers are configured per-project in
`.grok/settings.json` under `mcpServers` and initialize lazily in the background at
agent construction (`grok-agent.js:108-124`); set `MCP_DEBUG=1` to see connection
logs.

---

## The confirmation system

File operations and bash commands prompt the user interactively before running
(`dist/utils/confirmation-service.js`). The prompt offers "don't ask again" choices
that set **per-session approve-all flags**:

| Session flag | Effect |
|--------------|--------|
| `fileOperations` | Auto-approve all further file creates/edits this session |
| `bashCommands` | Auto-approve all further bash commands this session |
| `allOperations` | Auto-approve everything this session |

Key properties:

- Flags live in memory only (`confirmation-service.js:12-14`, checked at 27-29) —
  they reset every session and are **not scriptable from any config file**. There is
  no permission-rules system, allowlist, or lifecycle hook layer around tool calls in
  this version (see [grok-dev.md](grok-dev.md) for the successor that adds one).
- **Headless mode auto-approves everything**: `grok -p "..."` sets
  `setSessionFlag("allOperations", true)` before processing (`dist/index.js:181-182`),
  so all file writes and bash commands run without confirmation. There is no separate
  yolo/skip-permissions flag — headless *is* that flag.
- A `ConfirmationTool` class exists internally (`dist/tools/confirmation-tool.js`)
  but is **not** exposed as a model-callable tool.

---

## Built-in web / X search (not a tool)

The system prompt claims "real-time web search and X (Twitter) data", but there is no
search tool for the web — it is implemented at the **request level** via x.ai's
`search_parameters` field on the chat-completions payload
(`dist/grok/client.js:35-37` non-streaming, `56-58` streaming).

Whether a request gets `search_parameters` is decided by a keyword heuristic,
`shouldUseSearchFor()` (`grok-agent.js:130-157`): the user message triggers live
search if it contains any of `today`, `latest`, `news`, `trending`, `breaking`,
`current`, `now`, `recent`, `x.com`, `twitter`, `tweet`, `what happened`, `as of`,
`update on`, `release notes`, `changelog`, `price` — or matches a year pattern
(`/(20\d{2})/`). This only works against the real x.ai endpoint; other
OpenAI-compatible providers ignore or reject the field.

---

## Sources

Verified against the installed package on this machine on 2026-07-23
(`/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/`):

- `dist/grok/tools.js` — `BASE_GROK_TOOLS` (lines 3-233) with tool names at the line
  numbers listed above; `MORPH_EDIT_TOOL` at 238; `buildGrokTools()` with the
  `process.env.MORPH_API_KEY` conditional splice at 261-268;
  `addMCPToolsToGrokTools` at 333-340.
- `dist/agent/grok-agent.js` — tool dispatch switch (521-544), tool list in the
  system prompt (47-56), `shouldUseSearchFor()` keyword list (130-157), lazy MCP
  init (108-124).
- `dist/utils/confirmation-service.js` — session flags (12-14), skip check (27-29),
  per-tool "don't ask again" (54-57), `setSessionFlag` (106).
- `dist/index.js:176-227` — headless `processPromptHeadless` sets
  `allOperations = true` at 181-182.
- `dist/grok/client.js` — `search_parameters` attached to the request payload
  (35-37, 56-58); fixed `temperature: 0.7` and default `max_tokens` (26-33).
- npm README for `@vibe-kit/grok-cli` 0.0.34 (npm registry API, 2026-07-23) — Morph
  Fast Apply description and the `MORPH_API_KEY` → `edit_file` behavior.
