# Configuration

Grok CLI is configured across **two JSON files** — a user file in `~/.grok/` and
a project file in `.grok/` — plus environment variables and CLI flags on top.
Both files are managed by `dist/utils/settings-manager.js`; this page documents
each as it exists on disk in @vibe-kit/grok-cli 0.0.34.

---

## 1. User settings — `~/.grok/user-settings.json`

Path built at `settings-manager.js` line 50
(`path.join(os.homedir(), ".grok", "user-settings.json")`).

```json
{
  "apiKey": "xai-...",
  "baseURL": "https://api.x.ai/v1",
  "defaultModel": "grok-code-fast-1",
  "models": [
    "grok-4-1-fast-reasoning", "grok-4-1-fast-non-reasoning",
    "grok-4-fast-reasoning", "grok-4-fast-non-reasoning",
    "grok-4", "grok-4-latest", "grok-code-fast-1",
    "grok-3", "grok-3-latest", "grok-3-fast",
    "grok-3-mini", "grok-3-mini-fast"
  ],
  "settingsVersion": 2
}
```

| Field | Description |
|-------|-------------|
| `apiKey` | xAI API key. `GROK_API_KEY` env var is checked first |
| `baseURL` | API endpoint; change it to use any OpenAI-compatible provider |
| `defaultModel` | User-level default model |
| `models` | The list shown by the `/models` picker — user-editable |
| `settingsVersion` | Schema version for auto-migration (current: `2`) |

Behavior:

- **Auto-created** with defaults on first interactive run
  (`ensureUserSettingsDirectory()`, `dist/index.js` lines 38-47).
- **Permissions:** file written mode `0600`, directory `0700`
  (settings-manager.js lines 69, 139) — it holds your API key.
- **Auto-migrated:** when `settingsVersion` is behind `SETTINGS_VERSION` (2),
  migration prepends newer models to `models`.
- **Silently written by flags:** passing `-k`/`--api-key` or `-u`/`--base-url`
  on any run **persists those values into this file**
  (`saveCommandLineSettings`, `dist/index.js` lines 59-75).

## 2. Project settings — `.grok/settings.json`

Path: `.grok/settings.json` in the **cwd** (settings-manager.js line 52).

```json
{
  "model": "grok-4.3",
  "mcpServers": {
    "linear": { "transport": "sse", "url": "https://mcp.linear.app/sse" }
  }
}
```

| Field | Description |
|-------|-------------|
| `model` | Project-level model override (beats user `defaultModel`) |
| `mcpServers` | MCP server definitions, keyed by name — the **only** MCP config location; there is no global MCP config. See [mcp.md](mcp.md) |

Behavior:

- **Auto-created in the cwd if missing** whenever grok actually runs
  (`loadProjectSettings()`, settings-manager.js lines 164-180) — running grok in
  a directory leaves a `.grok/` behind. `--help`/`--version` exit before this
  and create nothing (verified).
- Managed for you by `grok mcp add` / `remove` / `add-json`.

---

## Model resolution chain

From `dist/index.js` lines 77-91 plus `getCurrentModel()`
(settings-manager.js lines 228-238), highest priority first:

```
--model flag  >  GROK_MODEL env  >  project .grok/settings.json "model"
              >  user defaultModel  >  hardcoded "grok-code-fast-1"
```

Note the hardcoded fallback `grok-code-fast-1` was **retired by xAI on
2026-05-15** and now routes to `grok-build-0.1` — see [models.md](models.md).

---

## The `.grok/` directory layout

| Path | Scope | Purpose |
|------|-------|---------|
| `.grok/settings.json` | project (cwd) | Model override + `mcpServers` (auto-created) |
| `.grok/GROK.md` | project (cwd) | Custom instructions — **checked first** |
| `~/.grok/user-settings.json` | user | API key, base URL, default model, model list |
| `~/.grok/GROK.md` | user | Custom instructions — fallback if the project file is absent |

The instruction file lookup is first-match-wins: the project `.grok/GROK.md`
completely **replaces** the home fallback — they are never merged. No other
filename or location is read. See
[custom-instructions.md](custom-instructions.md).

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `GROK_API_KEY` | API key (beats the `apiKey` in `~/.grok/user-settings.json`) |
| `GROK_BASE_URL` | API endpoint override |
| `GROK_MODEL` | Model override (slot 2 in the resolution chain) |
| `GROK_MAX_TOKENS` | Override the fixed `max_tokens` default of **1536** |
| `MORPH_API_KEY` | Enables the `edit_file` Morph tool ([tools.md](tools.md)) |
| `MCP_DEBUG` | Verbose MCP transport logging |

A `.env` in the cwd is auto-loaded on startup (`dotenv.config()`,
`dist/index.js` line 12), so these can live per-project.

Fixed request parameters you **cannot** configure (`dist/grok/client.js` lines
26-33): `temperature: 0.7`, 360s timeout. Only `max_tokens` is overridable, via
`GROK_MAX_TOKENS`.

---

## Related

- [cli-reference.md](cli-reference.md) — the flags that feed this chain
- [models.md](models.md) — bundled model list vs what xAI still serves
- [mcp.md](mcp.md) — the `mcpServers` block in detail
- [custom-instructions.md](custom-instructions.md) — `.grok/GROK.md`

## Sources

Everything verified against the installed package
`/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/` on
2026-07-23 (version: `package.json` line 3 = 0.0.34):

- `dist/utils/settings-manager.js`: lines 50/52 (both file paths), 14-33/39 (defaults + bundled model list, `SETTINGS_VERSION = 2`), 69/139 (0600/0700 modes), 164-180 (`loadProjectSettings` auto-create), 228-238 (`getCurrentModel` fallback); field set confirmed by `settings-manager.d.ts` types.
- `dist/index.js`: lines 38-47 (user-settings auto-create), 59-75 (`-k`/`-u` persistence), 77-91 (flag/env model priority), 12 (dotenv autoload).
- `dist/utils/custom-instructions.js` (all 23 lines): project-first `.grok/GROK.md` → `~/.grok/GROK.md` fallback, no merge.
- `dist/grok/client.js` lines 9, 26-33: default base URL `https://api.x.ai/v1`, temperature 0.7, max_tokens 1536, 360s timeout.
- On this machine `~/.grok/` does not exist and running `grok --help`/`--version` created no `.grok/` in the cwd (verified 2026-07-23) — confirming help/version exit before settings load.
- `grok-code-fast-1` retirement (2026-05-15, routes to `grok-build-0.1`): docs.x.ai migration page, fetched 2026-07-23.
