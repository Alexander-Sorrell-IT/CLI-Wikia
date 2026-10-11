# OpenCode (opencode)

> wiki-version: 1 | cli-version: v2.0.22 (native binary) | verified: 2026-10-10
> source: `opencode --help`, `opencode run --help`, binary strings, live run.

OpenCode is a server-backed coding agent: CLI talks to a background service
(`opencode service`) or a private `--standalone` server per invocation.

- Headless: `opencode run --format json "{prompt}"` (message last; `--agent`,
  `-m provider/model`, `-s` session, `-f` attach file available).
- Interactive: `opencode --prompt "{prompt}"` (TUI; `mini` for minimal UI).
- Config: `opencode.json(c)` at project root or `~/.config/opencode/`;
  observed global dir holds only `service.json` (server state).
- Instructions: `AGENTS.md` (verified in binary strings).
- Hooks: NO deployable JSON surface. Plugin API + event bus exist
  (`hook.before/after`, `permission.asked/rejected/replied`, `session.*`)
  but take JS plugins, not shell commands — enforcement is 16/16 artificial.
- Live probe: `run` creates a session and streams JSON events; default model
  `exo-free` was deprecated server-side (410) at probe time — pass `-m` with
  a live model if spawns fail on model, not on argv.

See: cli-reference.md, configuration.md, sessions.md.
