# aider configuration

> wiki-version: 1 | cli-version: 0.86.2 | verified: 2026-10-10
> source: observed `~/.aider.conf.yml` + `--help` config-file paragraph.

## Config files

Any `--flag` can be set in YAML. Search order: `./.aider.conf.yml`,
then `~/.aider.conf.yml`, or `-c FILE`.

| File | Role |
|------|------|
| `.aider.conf.yml` | Project config (root, not a dot-dir) |
| `~/.aider.conf.yml` | Global config (observed: models, aliases, read list) |
| `CONVENTIONS.md` | Instruction file (x10 refs in installed package) |
| `read:` entries | Extra always-loaded files (e.g. global conventions) |

## Observed global keys

`model`, `weak-model`, `edit-format`, `env-file`, `model-metadata-file`,
`model-settings-file`, `read: [...]`, `map-tokens`, `auto-commits`,
`show-diffs`, `suggest-shell-commands`, `detect-urls`, `dark-mode`, `alias:`.

## Enforcement staging

Aider reads no dot-dir, so enforcement stages engine+docs+artificial wiring
under a `.aider/` dir of our own (same pattern as `.muse/`). The CLI does
not read it. No config-dir env var found; wikia falls back to
`WIKIA_CONFIG_DIR`.
