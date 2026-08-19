# Custom Instructions — `.grok/GROK.md`

Grok CLI (`@vibe-kit/grok-cli` 0.0.34) supports exactly one custom-instructions
mechanism: a markdown file at `.grok/GROK.md`. The loader is
23 lines of code (`dist/utils/custom-instructions.js`) and its behavior is simple and
strict — one file is found, read whole, and injected into the system prompt.

---

## Lookup order

| Priority | Path | Scope |
|----------|------|-------|
| 1 | `.grok/GROK.md` | Project — resolved from the working directory |
| 2 | `~/.grok/GROK.md` | Global fallback — user home |

**First match wins. The two files are NOT merged.** If a project `.grok/GROK.md`
exists, `~/.grok/GROK.md` is never read for that session. If neither exists, no
custom-instructions section is added at all.

The project lookup follows the *effective* working directory: with
`grok -d /path/to/repo`, the CLI changes directory first, so
`/path/to/repo/.grok/GROK.md` is the file that gets picked up.

---

## What it does NOT read

Verified against the entire loader source — there is no other code path:

- **A bare `GROK.md` at the project root is ignored.** The file must live inside the
  `.grok/` directory. Only `.grok/GROK.md` (project) and `~/.grok/GROK.md` (global)
  are ever checked.
- **No directory walking.** It does not search parent directories or the git root —
  only the cwd's `.grok/` and the home `.grok/`.
- **No other tools' instruction files.** Grok CLI reads no instruction file from any
  other CLI's convention; `.grok/GROK.md` is the only instruction filename it knows.
- **No config knob.** Neither `.grok/settings.json` nor `~/.grok/user-settings.json`
  has a key to point at a different instructions file.

A read error (e.g. permissions) prints a `console.warn` and behaves as if the file
were absent — it never aborts the session.

---

## How it is injected

The file is loaded **once, at agent construction**, whitespace-trimmed, and prepended
into the system prompt as a `CUSTOM INSTRUCTIONS:` section **above** the standard
instructions (`dist/agent/grok-agent.js:40-43`):

```
CUSTOM INSTRUCTIONS:
<your .grok/GROK.md content>

The above custom instructions should be followed alongside the standard instructions below.
```

Because loading happens at construction, editing `.grok/GROK.md` mid-session has no
effect — restart the CLI to pick up changes.

---

## Example `.grok/GROK.md`

```markdown
# Project instructions

- This is a Python 3.11 project managed with uv; run tests with `uv run pytest`.
- Never edit files under `migrations/` — generate new ones instead.
- Match the existing 4-space indent and ruff formatting.
- Prefer `str_replace_editor` for edits; do not rewrite whole files.
- Ask before running any command that installs packages.
```

Create it with:

```bash
mkdir -p .grok
$EDITOR .grok/GROK.md
```

---

## The only Level-1 integration point

`.grok/GROK.md` is the **only** channel external tooling has into this CLI. The
installed 0.0.34 line has **no lifecycle hook system** — no pre/post-tool events, no
`hooks` key in either settings file, no shell-command-on-event mechanism anywhere in
`dist/`. Enforcement or policy layers can therefore only reach Grok CLI at Level 1:
by writing rules into `.grok/GROK.md` (project) or `~/.grok/GROK.md` (global) and
trusting the model to follow them. The successor package adds a real hook system —
see [grok-dev.md](grok-dev.md).

---

## Sources

Verified against the installed package on this machine on 2026-07-23
(`/home/phantomcore/.npm-global/lib/node_modules/@vibe-kit/grok-cli/`):

- `dist/utils/custom-instructions.js` (entire file, 23 lines) — project lookup
  resolving `.grok/GROK.md` from the working directory at line 6, home fallback
  `~/.grok/GROK.md` at line 11, first-match return (no merge), `console.warn` on
  error.
- `dist/agent/grok-agent.js:40-48` — `loadCustomInstructions()` called in the
  constructor; `CUSTOM INSTRUCTIONS:` section string and its placement above the
  standard system prompt.
- `dist/index.js` — `-d/--directory` changes directory before the agent is
  constructed, so the project lookup follows the target directory.
- npm README for `@vibe-kit/grok-cli` 0.0.34 (retrieved via npm registry API,
  2026-07-23) — documents the same project-overrides-global (not merged) behavior.
