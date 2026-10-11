# Aider (aider)

> wiki-version: 1 | cli-version: 0.86.2 (uv tool) | verified: 2026-10-10
> source: `aider --help` + installed package + observed `~/.aider.conf.yml`.

Aider is a terminal pair-programmer: you add files to the chat, it edits them
via diff/edit formats, with git integration (auto-commits, diffs, history).

- Headless: `aider --yes-always --message "{prompt}" --exit`
  (flags from --help; live model call did not complete in this sandbox).
- Interactive: `aider --message "{prompt}"` (no `--exit` stays in chat).
- Positionals are FILES, not prompts — never append a bare prompt.
- Config: `.aider.conf.yml` (project root) or `~/.aider.conf.yml`, `-c` to
  pick, `--env-file` for keys. Aliases via `--alias ALIAS:MODEL`.
- Conventions: `CONVENTIONS.md` (verified in package; no AGENTS.md support
  found) plus `read:` list in yml.
- Hooks: NONE. Enforcement deploys fully artificial (16/16).
- Useful: `--dry-run`, `--map-tokens`, `--lint-cmd/--test-cmd` with
  `--auto-lint/--auto-test`, `--model/--weak-model/--editor-model`.

See: cli-reference.md, configuration.md, sessions.md.
