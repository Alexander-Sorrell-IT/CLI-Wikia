# muse troubleshooting

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: observed commands + probe diagnostics.

- `muse doctor` (via doctor skill) diagnoses install/runtime issues from
  binary evidence.
- `muse trace` inspects a recorded session/run trace; `muse export`
  writes transcripts to files.
- Session logs: `~/.local/share/muse/sessions/YYYY/MM/DD/<id>/session.jsonl`
  (+ `session-index.db`, `local-tracing/`).
- `muse: Hooks: N runnable · M warnings` names bad hook rows
  (`UnsupportedEvent`, `D66` matcher errors); unknown settings members are
  named at startup (`tbh: ignoring unknown top-level member`).
- `tui-history.jsonl` (+`.lock`) records interactive input.
- Stuck installs: `.lock` files under plugin cache; never delete while a
  run holds them.
