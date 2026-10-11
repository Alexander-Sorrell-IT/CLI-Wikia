# muse configuration

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: observed `~/.config/muse/*.json` + `muse init --dry-run`.

## User config dir: ~/.config/muse/

| File | Contents (observed keys) |
|------|--------------------------|
| `settings.json` | `schema_version`, `provider`, `model`, `model_reasoning_efforts`, `tui`, `mcpServers` (streamable-HTTP entries) |
| `auth.json` | Provider API credentials (managed by `muse auth|login`) |
| `trust.json` | Per-project trust decisions (`projects: {path: {decision}}`) |

Enforcement stages its engine/docs under a `.muse/` dir of our own, with
the project hook plugin nested at `.muse/plugin/` (nesting fire-proven).
No other project dot-directory is used by the CLI itself.

## Project rules: AGENTS.md

`muse init` scaffolds `AGENTS.md` in the workspace root. Muse Code reads it
as project rules when it runs in that directory. `--dry-run` prints the
generated file without writing; `--force` overwrites.

## Enterprise planes

`muse config validate --plane <defaults|policy> --file <path>` checks an
enterprise plane document (`{"schema_version":1,"settings":{...}}`), not the
user's flat settings.json. `muse config status` shows plane state.

## Environment / overrides

- Per-run: `-c KEY=VALUE` (unknown or clashing keys refuse the run).
- No documented config-dir env var found in `--help`; wikia falls back to
  the generic `WIKIA_CONFIG_DIR` for this model.
