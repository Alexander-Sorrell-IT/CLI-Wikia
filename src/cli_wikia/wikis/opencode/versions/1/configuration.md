# opencode configuration

> wiki-version: 1 | cli-version: v2.0.22 | verified: 2026-10-10
> source: `--help` + binary strings + observed `~/.config/opencode/`.

## Config files

| File | Role |
|------|------|
| `opencode.json` / `opencode.jsonc` | Project config (root) or global (`~/.config/opencode/`) |
| `AGENTS.md` | Instruction file (binary-verified) |
| `~/.config/opencode/service.json` | Background-service state (not config) |

## Server model

CLI commands talk to a background service (`opencode service`) unless
`--standalone` (private server) or `--server URL` is passed. `reload`
re-reads config without restart. Fleet headless runs should prefer
`--standalone` semantics or accept the shared service.

## Enforcement staging

opencode reads no dot-dir, so enforcement stages engine+docs+artificial
wiring under a `.opencode/` dir of our own. The CLI does not read it.
No config-dir env var found; wikia falls back to `WIKIA_CONFIG_DIR`.
