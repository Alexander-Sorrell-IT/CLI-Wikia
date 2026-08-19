# Models

How `@vibe-kit/grok-cli` 0.0.34 picks a model, what it ships with, and — separately —
what the live xAI API actually serves today. The two have diverged: the bundled list
predates xAI's 2026-05-15 model retirements (see the last section).

## Default model

**`grok-code-fast-1`** — hardcoded as both the user-settings default and the project
default (`dist/utils/settings-manager.js:14,39`; also `dist/agent/grok-agent.js:27`).

## Resolution chain

Highest priority first:

1. `--model` / `-m` CLI flag
2. `GROK_MODEL` environment variable (`dist/index.js:77-91`)
3. Project setting `model` in `.grok/settings.json`
4. User setting `defaultModel` in `~/.grok/user-settings.json`
5. Hardcoded fallback `grok-code-fast-1`

Steps 3-5 are `getCurrentModel()` (`dist/utils/settings-manager.js:228-238`).

## Bundled model list

`DEFAULT_USER_SETTINGS.models` (`dist/utils/settings-manager.js:15-33`), shown by the
`/models` slash command in the TUI. Context notes are the source's own comments:

| Model | Source comment |
|-------|----------------|
| `grok-4-1-fast-reasoning` | Grok 4.1 Fast (2M context, "latest - November 2025") |
| `grok-4-1-fast-non-reasoning` | Grok 4.1 Fast (2M context) |
| `grok-4-fast-reasoning` | Grok 4 Fast (2M context) |
| `grok-4-fast-non-reasoning` | Grok 4 Fast (2M context) |
| `grok-4` | Grok 4 flagship (256K context) |
| `grok-4-latest` | Grok 4 flagship alias |
| `grok-code-fast-1` | Grok Code (coding-optimized, 256K context) — **default** |
| `grok-3` | Grok 3 (131K context) |
| `grok-3-latest` | Grok 3 alias |
| `grok-3-fast` | Grok 3 |
| `grok-3-mini` | Grok 3 |
| `grok-3-mini-fast` | Grok 3 |

The list is **user-editable**: edit the `models` array in `~/.grok/user-settings.json`
(auto-created with the defaults above on first interactive run, auto-migrated across
versions). Because the API client is plain OpenAI chat-completions, you can point
`baseURL` at any OpenAI-compatible provider and list its model names here.

## Request parameters — the `GROK_MAX_TOKENS` gotcha

From `dist/grok/client.js` (lines 9-12, 26-33):

| Parameter | Value | Notes |
|-----------|-------|-------|
| `max_tokens` | **1536** default | Surprisingly low — long answers get truncated. Override with the `GROK_MAX_TOKENS` env var (no flag or settings key exists for it). |
| `temperature` | **0.7 fixed** | Not configurable anywhere |
| timeout | **360s** | Per-request client timeout |
| base URL | `https://api.x.ai/v1` | Override via `GROK_BASE_URL`, `-u`, or `baseURL` in `~/.grok/user-settings.json` |

```bash
GROK_MAX_TOKENS=8192 grok -p "write the full migration script"
```

---

## Current xAI lineup (live API) — separate from the bundled list

> **This section describes the live xAI API as of 2026-07-23 (docs.x.ai), not the CLI.**
> The bundled list above was frozen in late 2025 and predates the retirements below.

Per docs.x.ai/developers/models ($/1M tokens: input / cached input / output; two pricing
tiers by prompt size):

| Model | Context | <200k tokens | ≥200k tokens |
|-------|---------|--------------|--------------|
| `grok-4.5` | 500k | $2.00 / $0.30 / $6.00 | $4.00 / $0.60 / $12.00 |
| `grok-4.3` | 1M | $1.25 / $0.20 / $2.50 | $2.50 / $0.40 / $5.00 |
| `grok-4.20-0309-reasoning` | 1M | $1.25 / $0.20 / $2.50 | $2.50 / $0.40 / $5.00 |
| `grok-4.20-0309-non-reasoning` | 1M | $1.25 / $0.20 / $2.50 | $2.50 / $0.40 / $5.00 |
| `grok-4.20-multi-agent-0309` | 1M | $1.25 / $0.20 / $2.50 | $2.50 / $0.40 / $5.00 |
| `grok-build-0.1` | 256k | $1.00 / $0.20 / $2.00 | $2.00 / $0.40 / $4.00 |

### The 2026-05-15 retirement — what happens to the bundled names

xAI retired most of the CLI's bundled models on **2026-05-15**
(docs.x.ai/developers/migration/may-15-retirement). Retired slugs **keep resolving** —
requests are redirected server-side and **billed at the redirect target's pricing**:

| Retired slug (in the bundled list) | Now routes to |
|-----------------------------------|---------------|
| `grok-code-fast-1` (the CLI default) | `grok-build-0.1` |
| `grok-4-0709`, `grok-3` | `grok-4.3` |
| `grok-4-fast-reasoning`, `grok-4-fast-non-reasoning` | `grok-4.3` |
| `grok-4-1-fast-reasoning`, `grok-4-1-fast-non-reasoning` | `grok-4.3` (low/none reasoning effort) |

Practical consequences for this CLI:

- Out of the box it silently runs on `grok-build-0.1` (the model behind xAI's official
  "Grok Build" CLI) at grok-build pricing, while displaying `grok-code-fast-1`.
- Nearly every other bundled Grok name is billed as `grok-4.3`.
- **Fix:** add the current names (`grok-4.3`, `grok-4.5`, `grok-build-0.1`, ...) to the
  `models` array in `~/.grok/user-settings.json` and set `defaultModel` accordingly, or
  set `model` in the project's `.grok/settings.json`.
- UNVERIFIED: today's status of the `grok-4-latest` / `grok-3-latest` aliases (not shown
  on the fetched docs page), and secondary-source claims of a final hard cutoff for
  retired slugs on 2026-08-15.

## Sources

- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/utils/settings-manager.js`
  — defaults and model list lines 12-33, project default 38-40, `getCurrentModel()`
  228-238 (inspected 2026-07-23).
- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/index.js` —
  `loadModel()` lines 77-91 (flag/env precedence).
- `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/dist/grok/client.js`
  — base URL line 9, 360s timeout line 10, `GROK_MAX_TOKENS` line 12, request params
  (temperature 0.7, max_tokens) lines 26-33.
- `grok --help` (2026-07-23) — `-m/--model` flag and `GROK_MODEL` env var.
- docs.x.ai — developers/models and developers/migration/may-15-retirement (fetched
  2026-07-23): live lineup, pricing, and the retirement/redirect table. Conflicting
  secondary-source pricing was discarded in favor of docs.x.ai.
- No API calls were made; live-lineup facts are from web research only and the two
  UNVERIFIED items are flagged inline.
