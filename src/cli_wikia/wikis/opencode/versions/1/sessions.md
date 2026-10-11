# opencode sessions

> wiki-version: 1 | cli-version: v2.0.22 | verified: 2026-10-10
> source: `--help` + live `opencode run` probe.

## Lifecycle

- Headless: `opencode run --format json "{msg}"` — creates a session id
  (`ses_...`), streams JSON events (`message`, `error`, ...).
- Resume/fork: `-s/--session ID`, `-c/--continue`, `--fork`.
- Manage: `opencode session ...`; title via `--title`.

## Fleet notes

Headless argv: `["opencode", "run", "--format", "json", "{prompt}"]`.
No mailbox hook event (no JSON hooks surface) — spawn-only; correlate
follow-ups with `-s <sessionID>` from the first run's JSON.
Caveat (2026-10-10): default model `exo-free` deprecated server-side —
fleet runs need `-m <live-model>` in the template if the user's default
is dead. Auth via `opencode auth` (integrations/credentials).
