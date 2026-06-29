# Codex CLI Reference — subcommands & flags

Every `codex` subcommand and the global flags, from the official [Command line options](https://developers.openai.com/codex/cli/reference) reference.

> **Not locally verified** — Codex isn't installed on this machine. Confirm exact spellings with `codex --help` and `codex <subcommand> --help` after installing. Items flagged "verify" were ambiguous in the docs.

---

## Subcommands

### Run & execute

| Command | What it does |
|---|---|
| `codex` | Launch the interactive terminal UI in the current directory |
| `codex "<prompt>"` | Launch the TUI seeded with an initial prompt |
| `codex exec` (alias `codex e`) | Non-interactive / scripted run that finishes without human input — see [codex-exec.md](./codex-exec.md) |
| `codex resume` | Continue a previous session (resume by id, or `--last`) |
| `codex fork` | Branch an existing session into a new thread |

### Session management

| Command | What it does |
|---|---|
| `codex archive` | Hide a session from active lists |
| `codex unarchive` | Restore an archived session |
| `codex delete` | Permanently remove a session |
| `codex apply` | Apply a Codex **Cloud** task's diff to your local working tree |

### Authentication

| Command | What it does |
|---|---|
| `codex login` | Authenticate — Sign in with ChatGPT (default), API key, device auth, or access token |
| `codex login status` | Show current auth state (verify exact form) |
| `codex logout` | Remove cached credentials |

See [codex-auth.md](./codex-auth.md).

### MCP & tools

| Command | What it does |
|---|---|
| `codex mcp` | Manage MCP servers (`codex mcp add`, `list`, `remove`) — see [codex-mcp.md](./codex-mcp.md) |
| `codex mcp-server` | Run Codex itself as an MCP server so other agents can call it |
| `codex plugin` | Install / manage plugins |
| `codex features` | Enable / disable feature flags (`[features]` table) |
| `codex cloud` | Launch and manage Codex Cloud tasks from the terminal |
| `codex sandbox` | Run an arbitrary command inside Codex's sandbox |
| `codex execpolicy` | Validate / inspect execution policy rules |

### Utilities

| Command | What it does |
|---|---|
| `codex doctor` | Generate a diagnostic report (auth, sandbox, config) |
| `codex completion` | Generate shell completions |
| `codex update` | Check for and install CLI updates |
| `codex app` / `codex app-server` | Launch the desktop app / run the local app server (verify) |

---

## Global flags

These apply to `codex` (interactive) and generally to `codex exec`.

| Flag | Short | Values / arg | Purpose |
|---|---|---|---|
| `--model` | `-m` | model id | Override the configured model (e.g. `gpt-5.5`) — see [codex-models.md](./codex-models.md) |
| `--sandbox` | `-s` | `read-only` \| `workspace-write` \| `danger-full-access` | Set the sandbox policy for this run |
| `--ask-for-approval` | `-a` | `untrusted` \| `on-request` \| `never` | Set the approval policy for this run |
| `--full-auto` | — | — | Convenience preset: `workspace-write` + low-friction approvals |
| `--dangerously-bypass-approvals-and-sandbox` | `--yolo` | — | **No sandbox, no approvals.** Highest risk — only in a disposable/isolated environment |
| `--config` | `-c` | `key=value` | Override any `config.toml` key inline (repeatable; dotted keys allowed) |
| `--cd` | `-C` | path | Set the working directory Codex operates in |
| `--profile` | `-p` | profile name | Activate a named [profile](./codex-config.md#profiles) |
| `--image` | `-i` | file(s) | Attach image file(s) (screenshots, design specs) to the prompt |
| `--search` | — | — | Enable live web search for the session |
| `--oss` | — | — | Use a local open-source model provider |
| `--enable` / `--disable` | — | feature | Toggle a feature flag for this run |
| `--remote` | — | — | Connect to a remote app-server (verify) |

> ⚠️ `--profile`'s short form is documented as `-p`, but `-p` is also a common "print" alias in other CLIs — verify against `codex --help`.

---

## `codex exec` flags

In addition to the global flags above, `exec` adds automation-oriented options:

| Flag | Short | Purpose |
|---|---|---|
| `--json` | — | Emit newline-delimited JSON events on stdout |
| `--output-last-message` | `-o` | Write only the final assistant message to a file |
| `--output-schema` | — | Validate structured output against a JSON schema file |
| `--ephemeral` | — | Don't persist session files to disk |
| `--ignore-rules` | — | Skip `execpolicy` rule files |
| `--skip-git-repo-check` | — | Allow running outside a git repository |

See [codex-exec.md](./codex-exec.md) for usage patterns.

---

## Common usage patterns

```bash
# Interactive session, pick model + reasoning effort inline
codex --model gpt-5.5 -c model_reasoning_effort=high

# Read-only "ask me anything about this repo" session
codex --sandbox read-only --ask-for-approval on-request

# Hands-off local automation (edits + commands inside the workspace)
codex --full-auto "refactor the auth module and run the tests"

# One-shot headless run for CI, JSON output, final message to a file
codex exec --json -o result.txt "bump the version and update the changelog"

# Pipe context in from another command
git diff | codex exec "write a conventional-commit message for this diff"

# Run in a specific directory with a named profile
codex --cd ~/work/api --profile deep-review

# Attach a screenshot
codex -i bug.png "the layout is broken like this — fix the CSS"
```

---

## See also

- [codex-overview.md](./codex-overview.md) — install, auth, modes
- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — what `--sandbox` / `--ask-for-approval` mean
- [codex-config.md](./codex-config.md) — keys you can set with `-c key=value`
- [codex-exec.md](./codex-exec.md) — non-interactive runs
