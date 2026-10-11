# Muse Code (muse)

> wiki-version: 2 | cli-version: 1.4.4 (1.4.4-R5419.1) | verified: 2026-10-10
> source: `muse --help` + MSP schema export + session taxonomy + fire probes
> (offline). No official docs URL used.

Muse Code is an interactive terminal coding agent (`muse`). Model observed:
`muse-spark-1.3-contributor` at `max` reasoning effort (provider `meta`).

- Headless: `muse exec "{prompt}"` (add `--json` for machine-readable JSONL).
- Interactive: `muse "{prompt}"` (starts a session / the TUI).
- Project rules: `AGENTS.md` at the workspace root (scaffolded by `muse init`).
- User config: `~/.config/muse/settings.json` (+ `auth.json`, `trust.json`).
- Hooks: REAL — 20 events, user route (`settings.json` key) + project route
  (workspace plugin). Both fire-proven. See hooks.md.
- Skills: project/user/plugin skills with enable/disable/validate/install;
  can import from Claude Code or Codex (`muse skills import --from claude|codex`).
- MCP: streamable-HTTP entries under `mcpServers` in settings.json
  (`muse mcp login|logout` for OAuth).

See: cli-reference.md, configuration.md, sessions.md.
