# muse CLI reference

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse --help` output on maintainer machine.

## Usage

```
muse [OPTIONS] [PROMPT]
muse [OPTIONS] <COMMAND>
muse exec [OPTIONS] [PROMPT]     # headless, non-interactive
```

## Commands

| Command | Purpose |
|---------|---------|
| `resume` | Resume a previous session (`--last` or session ref) |
| `exec` | Run one prompt non-interactively (headless) |
| `config` | Validate enterprise configuration documents |
| `export` | Export a session transcript to a file |
| `trace` | Inspect a recorded session or run trace |
| `model-profile` | Show model resolution per knob and effort tier |
| `skills` | List, inspect, enable, disable skills |
| `voice` | Transcribe an audio clip into text |
| `plugins` | Validate and manage plugin bundles |
| `sandbox` | Check or set up the OS sandbox |
| `schema` | Export the MSP wire schema (JSON Schema / TypeScript) |
| `serve` | Serve an MSP session host over stdio |
| `session-message` | List or send cross-session messages |
| `mcp` | Log in/out of an MCP server (OAuth) |
| `auth` / `login` / `logout` | Manage provider API credentials |
| `init` | Scaffold agent config (`AGENTS.md`) in the workspace |

## Notable options

- `--provider echo|meta|local` (default: meta)
- `--model <MODEL>` model id for non-echo providers
- `--reasoning-effort none|minimal|low|medium|high|xhigh|max|ultra` (default: high)
- `--approval-mode untrusted|on-request|never` (default: on-request)
- `--permission-profile <ID>` named permission profile
- `--workspace <PATH>` policy-gated workspace tools rooted at PATH
- `-w/--worktree [off|create|existing]` session git worktree
- `--parallel-tool-calls` / `--no-parallel-tool-calls`
- `-c/--config KEY=VALUE` one setting for this run (repeatable, JSON values)
- `--image <PATH>` attach a local image; `--base-url` override provider URL
- `--no-session-log` do not persist session event logs

## exec options (headless extras)

`--json` (JSONL events on stdout), `--prompt-file`, `--api-key-stdin`,
`--output-schema FILE` (meta provider only), `--max-model-steps N`,
`--max-tool-output-bytes N`, `--session-id UUID`, `--allow-workspace-switch`,
`--context-compaction-strategy`, `--context-compaction-soft/hard-threshold`.
