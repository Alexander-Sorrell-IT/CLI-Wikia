# The Successor: `grok-dev` (and the Grok CLI Ecosystem)

This wiki documents the **installed** `@vibe-kit/grok-cli` **0.0.34** — a frozen
legacy line, last published 2025-11-27. As of mid-2026 there are **three** distinct
"Grok CLI" tools in circulation, two of which share the same binary name. This page
disambiguates them and lists exactly which facts elsewhere in this wiki stop being
true if you upgrade.

| | Installed: `@vibe-kit/grok-cli` | Successor: `grok-dev` | Official: Grok Build |
|---|---|---|---|
| Publisher | superagent-ai (community) | superagent-ai (same repo, renamed) | xAI |
| npm package | `@vibe-kit/grok-cli` 0.0.34 (2025-11-27, frozen) | `grok-dev` 1.1.7 (2026-05-15) | not on npm (curl installer) |
| Binary | `grok` | **`grok`** (same name — collision) | `grok-build` |
| Config dir | `.grok/` + `~/.grok/` | `.grok/` + `~/.grok/` (extended schema) | `~/.grok-build/` |
| Auth | `GROK_API_KEY` (pay-per-token API) | `GROK_API_KEY` (API) | `grok-build login` (subscription OAuth) |
| Instructions | `.grok/GROK.md` | merged instruction files (see below) | see below |
| Lifecycle hooks | **none** | **17 events** | UNVERIFIED |
| Runtime | Node >= 18, Ink/React TUI | Bun + OpenTUI | native installer |

---

## 1. The installed line is frozen

The `superagent-ai/grok-cli` GitHub repo (3,329 stars, MIT, still active — last push
2026-07-06) renamed its npm package to **`grok-dev`** around March 2026 and rewrote
the tool. `@vibe-kit/grok-cli` has had **no release since 0.0.34 (2025-11-27)** and
is not marked deprecated on npm, but the repo's current README no longer documents
anything about it — the 0.0.34 npm README is the last authoritative doc for the
installed line, and this wiki is written from the installed package source itself.

---

## 2. `grok-dev` — the successor (same repo, new tool)

npm package `grok-dev`, first published 2026-03-20, latest **1.1.7** (2026-05-15,
25 versions). Built with **Bun and OpenTUI**. **The binary is still `grok`** —
installing `grok-dev` globally replaces the command behind the same name, and
installing both lines collides.

Everything below exists in `grok-dev` and does **NOT** exist in the installed
0.0.34:

- **Lifecycle hooks — 17 events.** Configured in `~/.grok/user-settings.json` under
  a `"hooks"` key, Claude-Code-style shape (`matcher` + `{type: "command", command,
  timeout}`), JSON on stdin/stdout, **exit code 2 = block**. Events: `PreToolUse`,
  `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `SessionStart`,
  `SessionEnd`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`,
  `TaskCreated`, `TaskCompleted`, `PreCompact`, `PostCompact`, `Notification`,
  `InstructionsLoaded`, `CwdChanged`.
- **New instruction convention.** Custom instructions move to `AGENTS.md`, merged
  from the git root down to the cwd, with per-directory `AGENTS.override.md`
  overrides. **The `.grok/GROK.md` mechanism is gone.**
- **Sub-agents** (`task`, `delegate` tools), **sandbox mode** (macOS 14+ Apple
  Silicon only), **skills** at `.agents/skills/<name>/SKILL.md`, Telegram remote
  control.
- **Extra model tools:** `search_x`, `search_web`, `generate_image`,
  `generate_video`, `computer`. Morph Fast Apply (`edit_file`) is no longer
  mentioned.
- **Headless upgrades:** `--batch-api` (xAI Batch API), `--format json` (ndjson
  *event* stream, replacing 0.0.34's message-per-line output), `--verify`, sessions
  via `--session latest`.
- **Config extensions:** `~/.grok/user-settings.json` gains hooks / sub-agents /
  Telegram / sandbox keys; new `~/.grok/workspace-trust.json`; project
  `.grok/settings.json` gains a sandbox block, plus `.grok/computer/` and
  `.grok/generated-media/` directories.
- Models referenced: `grok-4.3`, `grok-4.20-non-reasoning`,
  `grok-4.20-multi-agent-0309`; `grok models` lists the current menu.

---

## 3. Grok Build — xAI's separate official CLI (do not confuse)

xAI ships its own terminal coding agent, **Grok Build** — a distinct product, not
related to either community line:

- Launched **2026-05-14** (early beta, SuperGrok Heavy), expanded **2026-05-25** to
  all SuperGrok ($30/mo) and X Premium+ ($40/mo) subscribers. SuperGrok Heavy
  $299/mo (promo "SuperHeavy" $99/mo for 6 months).
- Install: `curl -fsSL https://x.ai/cli/install.sh | bash` (macOS/Linux);
  `irm https://x.ai/cli/install.ps1 | iex` (Windows, added 2026-05-25).
- Binary **`grok-build`**, config dir **`~/.grok-build/`**, auth via
  **`grok-build login`** (browser OAuth against the subscription — no API key).
- Runs **`grok-build-0.1`** (256K context, 70.8% SWE-Bench Verified; also on the
  API since ~2026-05-20).
- Features: plan-first execution (reviewable plan + diff preview), up to **8
  parallel sub-agents in git worktrees**, native MCP, headless `-p` flag.
- One third-party guide claims the binary is `grok` with `grok auth login` and a
  `.grok/hooks.json` hook file — contradicted by other sources; **UNVERIFIED**,
  treat with caution.
- July 2026: a researcher reported Grok Build uploaded users' entire source repos
  (including secrets and excluded files) to company cloud storage; the company
  subsequently released Grok Build under the Apache License. (Wikipedia names the
  company "SpaceXAI"; other sources say "xAI" — naming **UNVERIFIED**.)

**Rule of thumb:** `grok-build` binary + `~/.grok-build/` + subscription login =
official xAI tool. `grok` binary + `.grok/` + `GROK_API_KEY` = the community lines
documented in this wiki.

---

## 4. Migration: what stops being true if you upgrade

`npm install -g grok-dev` swaps the `grok` command's entire behavior. After that,
these facts from the other pages of this wiki **no longer hold**:

| Wiki fact (installed 0.0.34) | After upgrading to `grok-dev` 1.1.7 |
|---|---|
| `.grok/GROK.md` (project) / `~/.grok/GROK.md` (global) custom instructions, first match wins | Not read at all — replaced by the merged instruction-file convention above |
| No lifecycle hooks; `.grok/GROK.md` is the only Level-1 integration point | 17 hook events with block support (exit 2) in `~/.grok/user-settings.json` |
| 8 internal tools; `edit_file` only with `MORPH_API_KEY` | Different tool set (`search_x`, `search_web`, `generate_image`, `generate_video`, `task`, `delegate`, `computer`, ...); Morph no longer mentioned |
| Web/X search via `search_parameters` keyword heuristic | Explicit `search_web` / `search_x` tools |
| Headless `grok -p` emits one OpenAI-style message object per line | `--format json` event stream; plus `--batch-api`, `--verify`, `--session latest` |
| No sub-agents, no sandbox, no skills | Sub-agents, sandbox (macOS 14+ Apple Silicon), skills, Telegram |
| `~/.grok/user-settings.json` holds only `apiKey`/`baseURL`/`defaultModel`/`models`/`settingsVersion` | Schema extended (hooks, sub-agents, Telegram, sandbox) + `workspace-trust.json` |
| `grok --version` misreports `1.0.1` (hardcoded) | Reports the real `grok-dev` version |
| Node >= 18 runtime | Bun + OpenTUI |

**True regardless of upgrading:** the installed CLI's default model
`grok-code-fast-1` was **retired 2026-05-15** — the slug still resolves but routes
(and bills) as `grok-build-0.1`; the rest of the bundled 0.0.34 model list
(`grok-3*`, `grok-4-fast-*`, `grok-4-1-fast-*`, `grok-4-0709`) routes to
`grok-4.3`. Status of the `grok-4-latest` / `grok-3-latest` aliases: UNVERIFIED.

---

## Sources

- Local install verified 2026-07-23:
  `/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/package.json`
  line 3 (`"version": "0.0.34"`); `dist/index.js:241` (hardcoded `.version("1.0.1")`);
  `bin/grok` symlink via `readlink -f`.
- npm registry API (npmjs.com returned 403), 2026-07-23: `@vibe-kit/grok-cli` latest
  0.0.34 published 2025-11-27, bin `grok`, not deprecated; `grok-dev` first published
  2026-03-20, latest 1.1.7 (2026-05-15), 25 versions, bin `grok`.
- GitHub `superagent-ai/grok-cli` (API + raw README.md/package.json on main, accessed
  2026-07-23): stars/license/last-push; grok-dev feature set, hook events, config
  paths, instruction convention, headless flags, model references.
- docs.x.ai — developers/models and developers/migration/may-15-retirement (fetched
  2026-07-23): `grok-code-fast-1` → `grok-build-0.1` routing, `grok-3*`/`grok-4-fast*`
  → `grok-4.3`, `grok-build-0.1` context/pricing.
- Grok Build launch/expansion dates, tiers, installers, features: Wikipedia + multiple
  news/review sources (x.ai pages returned 403); conflicting third-party claims and
  the "SpaceXAI" naming flagged UNVERIFIED above.
