# Qwen Code (qwen)

> wiki-version: 1 | cli-version: 0.24.7 (@qwen-code/qwen-code, npm) | verified: 2026-10-10
> source: installed dist JS + `qwen --help` + observed `~/.qwen/`.
> No official docs URL used; this page is sourced from the installed binary.

Qwen Code is an agentic coding CLI (Gemini-CLI family). Local models observed
via ollama (`localhost:11434`): qwen2.5-coder 7b/14b, qwen3-coder 30b.

- Headless: `qwen "{prompt}"` (positional; `-p/--prompt` works but is
  deprecated upstream). Add `-y` / `--approval-mode yolo` for fleet runs.
- Interactive: `qwen -i "{prompt}"` (executes then continues interactively).
- Project rules: `QWEN.md` (primary; `AGENTS.md` also recognized).
- Config: `~/.qwen/settings.json` global, `.qwen/settings.json` per project.
- Hooks: REAL, Claude-compatible (permission decisions, deny/block), fired
  via internal messageBus. 8 events verified in dist. See hooks.md.
- MCP: `qwen mcp add|remove|list|reconnect|approve|reject`, or `--mcp-config`.
- Sandbox: `qwen sandbox [cmd]`, `-s/--sandbox` flag.
- Safety: `--safe-mode` disables hooks/extensions/skills/MCP (never use under
  enforcement); `--approval-mode plan|default|auto-edit|auto|yolo`.

See: cli-reference.md, configuration.md, hooks.md, sessions.md.
