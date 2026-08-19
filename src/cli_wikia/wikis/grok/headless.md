# Headless Mode

`grok -p "prompt"` / `grok --prompt "prompt"` processes a single prompt non-interactively
and exits. This is the scripting/CI entry point of `@vibe-kit/grok-cli` 0.0.34 (note:
`grok --version` misreports a hardcoded `1.0.1`). There is no separate "exec" subcommand —
headless is a flag on the main binary.

## Usage

```bash
grok -p "fix the failing test in app.py"
grok --prompt "summarize recent changes" -d /path/to/repo
```

---

## Auto-approval: everything runs, no flag needed

Headless mode **auto-approves all tool use**. Before processing the prompt, the CLI sets
the confirmation service's session flag `allOperations` to `true`
(`confirmationService.setSessionFlag("allOperations", true)`, `dist/index.js:181-182`).
Every file write and every bash command the model requests executes without confirmation.

- There is **no yolo / `--dangerously-skip-permissions` flag** — none exists, and none is
  needed: `-p` already implies full auto-approval.
- Conversely, interactive mode has **no flag to pre-approve** operations; approval
  prompts (with per-session "approve all" toggles) are interactive-only.

> **Treat every `grok -p` invocation as fully trusted.** Sandbox at the OS level if the
> prompt or the repo content is untrusted.

---

## Output format: NDJSON

Headless output is newline-delimited JSON — **one OpenAI-style chat message object per
line** on stdout (`dist/index.js:224-227`). Roles are `user`, `assistant`, and `tool`;
assistant messages include `tool_calls`, and tool results carry `tool_call_id`:

```json
{"role":"user","content":"fix the failing test in app.py"}
{"role":"assistant","content":"I'll look at the test first.","tool_calls":[{"id":"call_1","type":"function","function":{"name":"view_file","arguments":"{\"path\":\"app.py\"}"}}]}
{"role":"tool","tool_call_id":"call_1","content":"..."}
{"role":"assistant","content":"Fixed. The assertion was inverted."}
```

### Error shape

On failure the CLI emits a single assistant message and exits **1**
(`dist/index.js:229-236`):

```json
{"role":"assistant","content":"Error: <message>"}
```

So: check the exit code, then parse stdout line-by-line as JSON. MCP-server connection
noise, when present, goes to **stderr** (it is only suppressed in interactive mode —
`dist/mcp/mcp-protocol-client.js:16-17`), so parse stdout only.

---

## Useful flag combinations

| Flag | Description |
|------|-------------|
| `-d, --directory <dir>` | Change working directory before running (per-repo targeting) |
| `-m, --model <model>` | Model for this run (see [models.md](models.md)) |
| `--max-tool-rounds <N>` | Cap on tool-execution rounds — default **400** (`dist/index.js:248,264`) |
| `-u, --base-url <url>` | API endpoint override (any OpenAI-compatible provider) |
| `-k, --api-key <key>` | API key for this run — **see caution below** |

> **Caution:** `-k` and `-u` are **persisted** to `~/.grok/user-settings.json`
> (`saveCommandLineSettings`, `dist/index.js:59-75`). They are not per-invocation
> overrides. For ephemeral credentials use the `GROK_API_KEY` / `GROK_BASE_URL`
> environment variables instead.

```bash
# One-shot against a specific repo with a bigger output budget
GROK_MAX_TOKENS=8192 grok -p "refactor the config loader" -d ~/src/myrepo -m grok-4-latest

# Bounded run for CI
grok -p "run the test suite and fix trivial failures" --max-tool-rounds 50
```

`GROK_MAX_TOKENS` matters more than you'd expect: the default `max_tokens` is only
**1536** — see [models.md](models.md).

---

## Interactive alternative: positional message

A bare positional argument is **not** headless — `grok "do the thing"` starts the
interactive TUI with that string as the initial message (variadic `[message...]`,
`dist/index.js:242,282-286`). Only `-p/--prompt` exits after one turn.

---

## Second headless entry point: `grok git commit-and-push`

```bash
grok git commit-and-push
```

Stages all changes, generates a commit message via the model, commits, and pushes
(`dist/index.js:93-175`). It is the only other non-interactive command (also available
as `/commit-and-push` inside the TUI). It calls the paid API to write the message.

---

## Orchestration notes

- **Fleet-style spawning works.** One `grok -p` process per task, `-d` per repo,
  NDJSON on stdout, exit code 0/1 — easy to supervise from a parent orchestrator.
- **No mid-session injection.** This CLI has **no lifecycle hook system** (no
  PreToolUse/PostToolUse, no shell-on-event mechanism anywhere in `dist/`), so an
  orchestrator cannot gate or observe individual tool calls in flight. Control is
  limited to: the prompt itself, per-project custom instructions in `.grok/GROK.md`
  (loaded from the working directory, `~/.grok/GROK.md` fallback), `--max-tool-rounds`,
  and killing the process.
- **Side effect:** running grok in a directory **creates `.grok/settings.json` in the
  cwd** if missing (`loadProjectSettings`, `dist/utils/settings-manager.js:164-180`).
  Expect stray `.grok/` directories in orchestrated repos.
- `.env` in the cwd is loaded via `dotenv` (`dist/index.js:12`), so per-repo env
  configuration is possible.

## Sources

Verified 2026-07-23 against the installed package (no real prompts were run — help output
and source inspection only):

- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/index.js` —
  `processPromptHeadless` lines 176-237 (auto-approve 181-182, NDJSON loop 224-227,
  error+exit 229-236), `loadModel` 77-91, `git commit-and-push` 93-175,
  `saveCommandLineSettings` 59-75, positional message 242/282-286, `--max-tool-rounds`
  default 248/264, dotenv line 12.
- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/mcp/mcp-protocol-client.js`
  lines 16-17 (stderr suppression is interactive-only).
- `grok --help` (2026-07-23) — flag list and defaults reproduced above; `grok git --help`
  for `commit-and-push`.
- `grep -rn -i hook dist/` — only React/Ink UI input hooks exist; no lifecycle hook
  system (hence no hooks page in this wiki).
- npm README for @vibe-kit/grok-cli 0.0.34 (via npm registry API, 2026-07-23) — confirms
  headless flags and the absence of any permissions-skip flag.
