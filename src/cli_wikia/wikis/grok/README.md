# Grok CLI Wiki

**Grok CLI** (`grok`) is an open-source, community-built terminal coding agent for
xAI's Grok models, published on npm as **`@vibe-kit/grok-cli`** by the
superagent-ai / vibe-kit project. It is an agentic loop with file-editing tools,
bash execution, ripgrep search and MCP support, speaking the **OpenAI-compatible
chat-completions API** against `https://api.x.ai/v1` (any OpenAI-compatible
provider works by changing the base URL).

> **This wiki documents the installed line: `@vibe-kit/grok-cli` 0.0.34.**
> The upstream repo has since renamed its npm package to **`grok-dev`** and
> rewritten the tool (same `grok` binary name — a collision hazard). The installed
> 0.0.34 line is frozen (last published 2025-11-27). See
> [grok-dev.md](grok-dev.md) for the successor.

---

## Identity & version discrepancy

Two version numbers exist for the same install, and only one is real:

| Where | Reports | Truth |
|---|---|---|
| npm registry / `package.json` | **0.0.34** | The actual published version |
| `grok --version` / `-V` | `1.0.1` | A **hardcoded string** in `dist/index.js` (line 241), out of sync with `package.json` |

Do not trust `grok --version` for anything. When checking what is installed, read
`package.json` in the package directory or use `npm ls -g @vibe-kit/grok-cli`.

Also disambiguate from **Grok Build** (`grok-build`), xAI's *official*
subscription-gated CLI launched 2026-05-14 with config under `~/.grok-build/`. It
is a completely different product from this community CLI.

---

## Install

```bash
npm install -g @vibe-kit/grok-cli    # requires Node >= 18
```

Installs the `grok` binary (on this machine:
`/home/phantomcore/.npm-global/bin/grok` →
`../lib/node_modules/@vibe-kit/grok-cli/dist/index.js`).

## Quick start

```bash
export GROK_API_KEY=xai-...              # or -k / ~/.grok/user-settings.json

grok                                     # interactive TUI (Ink/React)
grok "explain this repo"                 # interactive, with an initial message
grok -p "fix the failing test" -d ~/app  # headless: one prompt, NDJSON out, exit
grok git commit-and-push                 # AI commit message, commit, push
grok mcp list                            # list configured MCP servers
```

**Cost warning:** every real prompt is a paid xAI API call, and headless mode
(`-p`) auto-approves *all* file writes and bash commands. Only `--help`,
`--version` and `grok mcp list` are free/safe.

**Default model caution:** the built-in default is `grok-code-fast-1`, which xAI
**retired on 2026-05-15** — requests to that slug now route (and bill) as
`grok-build-0.1`. See [models.md](models.md).

---

## Topic index

| File | What it covers |
|---|---|
| [README.md](README.md) | **Start here** — what Grok CLI is, install, quick start |
| [cli-reference.md](cli-reference.md) | Every flag, subcommand, slash command and env var |
| [configuration.md](configuration.md) | `~/.grok/user-settings.json`, project `.grok/settings.json`, model resolution |
| [custom-instructions.md](custom-instructions.md) | The `.grok/GROK.md` instruction file (project-first, home fallback) |
| [headless.md](headless.md) | `grok -p` — NDJSON output, auto-approval, scripting/CI |
| [mcp.md](mcp.md) | MCP servers — `grok mcp` management, transports, `mcpServers` config |
| [models.md](models.md) | Bundled model list, resolution order, the 2026-05-15 xAI retirements |
| [tools.md](tools.md) | The 8 built-in agent tools, incl. the Morph `edit_file` conditional |
| [grok-dev.md](grok-dev.md) | The successor package `grok-dev` — what changed |

---

## No lifecycle hooks

The installed `@vibe-kit/grok-cli` 0.0.34 has **no lifecycle hook system of any
kind**: no PreToolUse/PostToolUse or session events, no `hooks` key in either
settings file's schema, and no shell-command-on-event mechanism anywhere in
`dist/`. (A `grep -rn -i hook dist/` matches only React/Ink *UI* input hooks.)
The only interception point is the interactive confirmation prompt for file ops
and bash, which is not scriptable from config — and which headless mode bypasses
entirely. The successor `grok-dev` package *does* add a 17-event hook system; see
[grok-dev.md](grok-dev.md).

## Where things live

| Path | Purpose |
|---|---|
| `~/.grok/user-settings.json` | User settings: API key, base URL, default model, model list |
| `~/.grok/GROK.md` | Global custom instructions (fallback) |
| `.grok/settings.json` | Project settings: model, MCP servers (auto-created in cwd) |
| `.grok/GROK.md` | Project custom instructions (wins over the home fallback; not merged) |
| `.env` in cwd | Auto-loaded via dotenv on startup |

## Sources

- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/package.json` line 3 (`"version": "0.0.34"`, engines Node >= 18); `dist/index.js` line 241 (hardcoded `.version("1.0.1")`); `grok --version` output → `1.0.1` (run 2026-07-23).
- `grok --help` output (run 2026-07-23) — binary description, flags, subcommands.
- `dist/utils/settings-manager.js` lines 50-52 (settings paths), 228-238 (model fallback); `dist/utils/custom-instructions.js` (instruction-file lookup); `dist/grok/tools.js` (tool list); `dist/agent/grok-agent.js` line 27 + `client.js` line 9 (default model, `https://api.x.ai/v1`).
- No hooks: `grep -rn -i hook dist/` over the installed package matches only `dist/hooks/use-*.js` UI input hooks; no hooks key in `settings-manager.d.ts` types.
- npm registry API (2026-07-23): `@vibe-kit/grok-cli` latest 0.0.34 published 2025-11-27, bin `grok`, not deprecated; successor `grok-dev` first published 2026-03-20 (same repo, superagent-ai/grok-cli, 3,329 stars).
- xAI model retirements: docs.x.ai migration page (2026-07-23) — `grok-code-fast-1` retired 2026-05-15, routes to `grok-build-0.1`. Grok Build official CLI (launched 2026-05-14, binary `grok-build`, config `~/.grok-build/`): Wikipedia + news sources, 2026-07-23.
