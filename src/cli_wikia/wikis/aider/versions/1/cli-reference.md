# aider CLI reference

> wiki-version: 1 | cli-version: 0.86.2 | verified: 2026-10-10
> source: `aider --help` output on maintainer machine.

## Usage

```
aider [OPTIONS] [FILES...]     # positionals are files to add to chat
aider --message "{p}" --exit   # headless one-shot (+ --yes-always)
```

## Notable options

- `--message COMMAND`, `--message-file MESSAGE_FILE` — headless prompt in
- `--exit` — quit after `--message` (one-shot); omit to stay interactive
- `--yes-always` — skip all confirmations
- `--dry-run` — show what would happen without calling the model
- `--model MODEL`, `--weak-model`, `--editor-model`, `--editor-edit-format`
- `--alias ALIAS:MODEL` (repeatable), `--list-models`, `--model-settings-file`,
  `--model-metadata-file`, `--reasoning-effort`, `--thinking-tokens`
- `--api-key PROVIDER=KEY`, `--set-env VAR=value`, `--env-file ENV_FILE`
- `-c/--config CONFIG_FILE` (default search: `./.aider.conf.yml`, then home)
- `--read FILE` (repeatable read-only file), `--map-tokens`, `--map-refresh`
- `--git/--no-git`, `--auto-commits/--no-auto-commits`,
  `--dirty-commits`, `--attribute-author/committer`, `--commit-prompt`
- `--lint/--auto-lint/--lint-cmd`, `--test/--auto-test/--test-cmd`
- `--watch-files`, `--suggest-shell-commands`, `--show-diffs`, `--dark-mode`
