# muse sessions

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse --help` + `muse exec --help` subcommand list.

## Session lifecycle

- Start: `muse "{prompt}"` (interactive) or `muse exec "{prompt}"` (headless).
- Resume: `muse resume --last` or `muse resume <session-ref>`.
- Pin an id headlessly: `muse exec --session-id <UUID> "{prompt}"`.
- Logs: persisted per session unless `--no-session-log` is passed.

## Inspection and messaging

- `muse export` — export a session transcript to a file.
- `muse trace` — inspect a recorded session or run trace.
- `muse session-message` — list or send cross-session messages.

## Compaction (headless flags)

- `--context-compaction-strategy summary-preserved-suffix/v1 |`
  `prefix-extension-summary/v1 | prefix-extension-inventory-summary/v1`
- `--context-compaction-soft-threshold <FRAC>`
- `--context-compaction-hard-threshold <FRAC>`

## Fleet notes

Headless argv: `["muse", "exec", "{prompt}"]`. Mailbox injection rides
`UserPromptSubmit` (fire-proven); `--session-id` gives a stable handle for
follow-up `exec` calls. Cross-session messaging via `session-message send`.
