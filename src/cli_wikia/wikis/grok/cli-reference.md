# CLI Reference

The `grok` command starts an interactive Ink/React TUI by default, runs one-shot
headless with `-p`, and has two subcommand groups: `git` and `mcp`. This page is
the complete surface as reported by `grok --help`, `grok git --help`,
`grok git commit-and-push --help`, `grok mcp --help` and `grok mcp add --help`
(@vibe-kit/grok-cli 0.0.34 — note `--version` misreports `1.0.1`, a hardcoded
string).

## Usage

```
grok [options] [command] [message...]
```

The variadic positional `[message...]` is an **initial message**: `grok "do the
thing"` opens the interactive TUI with that message already sent. For a
non-interactive run use `-p` instead.

---

## Global options

| Flag | Description |
|------|-------------|
| `-V, --version` | Print the version number — **prints the stale hardcoded `1.0.1`**, not the real npm version 0.0.34 |
| `-d, --directory <dir>` | Set the working directory (chdirs before doing anything; default: cwd) |
| `-k, --api-key <key>` | Grok API key (or set `GROK_API_KEY`) — **see caution below** |
| `-u, --base-url <url>` | API base URL (or set `GROK_BASE_URL`; default `https://api.x.ai/v1`) — **see caution below** |
| `-m, --model <model>` | Model to use (or set `GROK_MODEL`); highest priority in the model resolution chain |
| `-p, --prompt <prompt>` | Headless mode: process a single prompt, emit NDJSON, exit — **auto-approves all tool use**, see [headless.md](headless.md) |
| `--max-tool-rounds <rounds>` | Maximum tool execution rounds (default: `400`) |
| `-h, --help` | Display help |

> **CAUTION — `-k` / `-u` persist.** Passing `--api-key` or `--base-url` on the
> command line does not just apply for that run: the values are **written to
> `~/.grok/user-settings.json`** (`saveCommandLineSettings`, `dist/index.js`
> lines 59-75). A one-off `-u http://localhost:8080/v1` silently becomes your
> default endpoint. `-m` and env vars do not persist.

---

## Subcommand: `git`

```
grok git commit-and-push [options]
```

Stages all changes, generates a commit message with the model, commits, and
pushes to the remote (`dist/index.js` lines 93-175). This is a second headless
entry point — it makes API calls and mutates your repo without a TUI.

Options: `-d, --directory <dir>`, `-k, --api-key <key>`, `-u, --base-url <url>`,
`-m, --model <model>`, `--max-tool-rounds <rounds>` (default `400`) — same
semantics (and the same `-k`/`-u` persistence caution) as the global flags.

## Subcommand: `mcp`

Manages MCP servers in the **project** `.grok/settings.json` under `mcpServers`.
See [mcp.md](mcp.md) for config shape and transports.

| Command | What it does |
|---------|--------------|
| `grok mcp add [options] <name>` | Add an MCP server |
| `grok mcp add-json <name> <json>` | Add a server from a JSON config string |
| `grok mcp remove <name>` | Remove a server |
| `grok mcp list` | List configured servers *(read-only, safe)* |
| `grok mcp test <name>` | Test the connection to a server |

`grok mcp add` options:

| Flag | Description |
|------|-------------|
| `-t, --transport <type>` | `stdio`, `http`, `sse`, `streamable_http` (default: `stdio`) |
| `-c, --command <command>` | Command to run the server (stdio) |
| `-a, --args [args...]` | Arguments for the server command (stdio; default: `[]`) |
| `-u, --url <url>` | URL for HTTP/SSE transports |
| `-h, --headers [headers...]` | HTTP headers, `key=value` format (default: `[]`) |
| `-e, --env [env...]` | Environment variables, `key=value` format (default: `[]`) |
| `--help` | Display help — note `-h` is taken by `--headers` here |

---

## Interactive slash commands

Inside the TUI (`dist/hooks/use-input-handler.js` lines 153-157):

| Command | Action |
|---------|--------|
| `/help` | Show available commands |
| `/clear` | Clear the conversation |
| `/models` | Open the model picker |
| `/commit-and-push` | Same as `grok git commit-and-push` |
| `/exit` | Exit the TUI |

---

## Environment variables

Complete list (from `grep process.env` over `dist/`):

| Variable | Description |
|----------|-------------|
| `GROK_API_KEY` | API key — checked before the `apiKey` in `~/.grok/user-settings.json` |
| `GROK_BASE_URL` | API endpoint override (default `https://api.x.ai/v1`) |
| `GROK_MODEL` | Model override — beats project/user settings, loses to `-m` |
| `GROK_MAX_TOKENS` | `max_tokens` override (default is a surprisingly low **1536**) |
| `MORPH_API_KEY` | Enables the extra `edit_file` Morph Fast Apply tool (see [tools.md](tools.md)) |
| `MCP_DEBUG` | Un-suppresses MCP transport/connection logs |

A `.env` file in the cwd is **auto-loaded** via `dotenv.config()`
(`dist/index.js` line 12) — a project `.env` with `GROK_API_KEY` works with no
shell exports.

---

## Examples

```bash
grok                                       # interactive TUI
grok "review src/ for bugs"                # TUI with an initial message
grok -m grok-4.3 -p "add type hints"       # headless, explicit model
grok -p "run the tests and fix failures" \
     -d ~/proj --max-tool-rounds 50        # headless, bounded, other dir
grok git commit-and-push                   # AI commit + push
grok mcp add linear -t sse \
     -u "https://mcp.linear.app/sse"       # add an SSE MCP server
grok mcp list                              # safe read-only listing
```

## Sources

- `grok --help`, `grok git --help`, `grok git commit-and-push --help`, `grok mcp --help`, `grok mcp add --help` — all output reproduced here verbatim (run 2026-07-23 against `/home/phantomcore/.npm-global/bin/grok`).
- `grok --version` → `1.0.1`; real version: `package.json` line 3 = `0.0.34`; hardcoded string at `dist/index.js` line 241.
- `-k`/`-u` persistence: `dist/index.js` lines 59-75 (`saveCommandLineSettings`). Headless auto-approval: `dist/index.js` lines 181-182. `git commit-and-push` implementation: `dist/index.js` lines 93-175. Positional `[message...]`: `dist/index.js` lines 242, 282-286. `.env` autoload: `dist/index.js` line 12.
- Slash commands: `dist/hooks/use-input-handler.js` lines 153-157. Env vars: `grep -rn 'process.env' dist/` over the installed package; `GROK_MAX_TOKENS` default 1536 at `dist/grok/client.js` lines 26-33.
- npm README for 0.0.34 (npm registry API, 2026-07-23) corroborates the flag list and the Linear MCP example.
