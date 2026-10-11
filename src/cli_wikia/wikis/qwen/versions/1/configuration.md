# qwen configuration

> wiki-version: 1 | cli-version: 0.24.7 | verified: 2026-10-10
> source: observed `~/.qwen/settings.json` keys + `--help` + dist refs
> (`.qwen/settings.json` x192, `QWEN.md` x196 in dist).

## Config files

| File | Role |
|------|------|
| `~/.qwen/settings.json` | Global settings (`$version`, `modelProviders`, `security`, `model`, `tools`, `memory`, `env`, `ui`, `telemetry`, `proxy`, ...) |
| `.qwen/settings.json` | Per-project settings (same schema) |
| `QWEN.md` | Project instruction file (primary) |
| `AGENTS.md` | Also recognized as instruction file |

## Observed global dir (~/.qwen/)

`settings.json`, `extensions/`, `extension-store/`, `skills/`, `memories/`,
`sessions/`, `projects/`, `tmp/`, `usage/`, `output-language.md`. Backup
copies (`settings.json.bak`, `settings.json.before-retention-guard`) appear
after qwen's own retention guard runs — do not treat as config sources.

## Models / auth (observed)

`modelProviders.openai[]` entries point at `http://localhost:11434/v1`
(ollama) with `envKey: OPENAI_API_KEY`. Any key value works against local
ollama; headless runs in this workbench use a dummy value. `security.auth`
selects the provider type.

## Environment

- `OPENAI_API_KEY` (or per-provider `envKey`) must be SET (value can be dummy
  for local servers) or headless runs cancel with "Operation cancelled".
- `QWEN_TLS_INSECURE=1` equals `--insecure` (lab only).
- No config-dir relocation var found; wikia falls back to `WIKIA_CONFIG_DIR`.
