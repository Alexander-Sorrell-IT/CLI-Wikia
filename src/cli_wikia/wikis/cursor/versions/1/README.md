# Cursor (cursor-agent)

> wiki-version: 0 | status: UNVERIFIED — cursor-agent is NOT installed on the
> maintainer machine. Every fact below is a best-effort assumption awaiting
> confirmation. Do not treat as ground truth.

Cursor is an AI code editor (VS Code family) plus a terminal agent
(`cursor-agent`; bare `cursor` launches the IDE).

Assumed (confirm on install):

- Headless: `cursor-agent -p "{prompt}"` (assumed print-mode flag).
- Interactive: `cursor-agent "{prompt}"`.
- Project dir: `.cursor/` (rules/hooks live here in the IDE).
- Settings: `~/.cursor/settings.json` (assumed path).
- Instructions: `AGENTS.md` (converged default; Cursor also has `.cursor`
  rules in the IDE — confirm which the agent reads).
- Hooks: treated as NONE until confirmed — enforcement is 16/16 artificial,
  upgradeable via `cli-enforcement sync cursor --write` once hooks.md exists.

See: cli-reference.md, configuration.md.
