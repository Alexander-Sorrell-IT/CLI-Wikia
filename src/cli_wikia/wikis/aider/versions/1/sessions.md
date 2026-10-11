# aider sessions

> wiki-version: 1 | cli-version: 0.86.2 | verified: 2026-10-10
> source: observed `~/.aider.*` files + `--help`.

## History files (home dir)

- `.aider.chat.history.md` — chat transcripts
- `.aider.input.history` — readline history
- `.aider.model.metadata.json`, `.aider.model.settings.yml` — model data

## Fleet notes

Headless argv: `["aider", "--yes-always", "--message", "{prompt}", "--exit"]`.
No mailbox hook event (no hook system) — spawn-only until hooks land.
Use `--dry-run` to validate argv without spending model calls. Git repo
presence changes behavior (`--git/--no-git`, auto-commits); fleet workdirs
should init a repo or pass `--no-git` explicitly.
