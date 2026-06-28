# Environment Variables

Claude Code reads many environment variables. This is the consolidated list — settings can reach more configuration than env vars, but env vars are useful for CI, scripts, and per-shell overrides.

---

## Most commonly useful

| Variable | What it does |
|---|---|
| `ANTHROPIC_API_KEY` | API key for Anthropic API. Disables claude.ai-only features (Remote Control, web sessions) |
| `CLAUDE_CODE_OAUTH_TOKEN` | Long-lived OAuth token from `claude setup-token`. Inference-only — cannot establish Remote Control sessions |
| `CLAUDE_CODE_SIMPLE` | Set automatically by `--bare` — skip auto-discovery of hooks/skills/plugins/MCP/memory/CLAUDE.md |
| `CLAUDE_CODE_REMOTE` | `"true"` in remote/web environments. Use in hooks to gate cloud-only behavior |
| `CLAUDE_PROJECT_DIR` | Project root dir. Available to hooks. Quote when paths may contain spaces |
| `CLAUDE_PLUGIN_ROOT` | Plugin install dir. Available to plugin hooks/MCP/monitors. Changes on plugin update |
| `CLAUDE_PLUGIN_DATA` | Plugin's persistent data dir. Survives plugin updates |
| `CLAUDE_SESSION_ID` | Current session ID. Available in skills via `${CLAUDE_SESSION_ID}` |
| `CLAUDE_SKILL_DIR` | The skill's directory — use in skill scripts to reference bundled files regardless of cwd |
| `CLAUDE_ENV_FILE` | Only in `SessionStart`, `CwdChanged`, `FileChanged` command hooks: file you can `export VAR=val` into to persist env vars for subsequent Bash commands |

---

## Models & subagents

| Variable | What it does |
|---|---|
| `CLAUDE_CODE_SUBAGENT_MODEL` | Override the model for all subagents — takes precedence over per-invocation params and frontmatter |

---

## Auto-compaction

| Variable | What it does |
|---|---|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Trigger compaction earlier (e.g. `70` = at 70% capacity instead of default ~95%) |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | Effective context window for compaction calculations |

---

## Skills & commands

| Variable | What it does |
|---|---|
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Raise the character budget for skill descriptions in context. Default: 1% of context window or 8,000 |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | Set to `1` to allow `shell: powershell` in skills on Windows |

---

## MCP

| Variable | What it does |
|---|---|
| `MCP_TIMEOUT` | MCP server startup timeout in ms (e.g. `MCP_TIMEOUT=10000`) |
| `MAX_MCP_OUTPUT_TOKENS` | Raise the limit for MCP tool output (default warns at 10,000 tokens) |
| `MCP_CLIENT_SECRET` | OAuth client secret for `claude mcp add`/`add-json` (skip interactive prompt) |

---

## Cloud sessions / web

| Variable | What it does |
|---|---|
| `CCR_FORCE_BUNDLE` | Force `claude --remote` to bundle local repo even when GitHub access is available |
| `CLAUDE_CODE_REMOTE_SESSION_ID` | Available in cloud sessions — the session ID. Use to construct claude.ai/code/<id> links |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | `1` to load CLAUDE.md/`.claude/rules/`/CLAUDE.local.md from `--add-dir` directories |

---

## Remote Control

| Variable | What it does |
|---|---|
| `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` | Default prefix for auto-generated RC session names (default: machine hostname) |

---

## Agent teams

| Variable | What it does |
|---|---|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `1` to enable [agent teams](./agent-teams.md). Disabled by default |

---

## Provider selection

| Variable | What it does |
|---|---|
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock as the model provider |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI |
| `CLAUDE_CODE_USE_FOUNDRY` | Use Microsoft Foundry |

> Some features (Remote Control, auto-mode classifier) are Anthropic-API-only. Setting one of these disables them.

---

## Telemetry & observability

| Variable | What it does |
|---|---|
| `DISABLE_TELEMETRY` | Disable usage telemetry. **Disables auto-mode** because the eligibility check needs telemetry |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disable non-essential outbound. Same caveat as above |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Explicit opt-in to telemetry collection |

---

## Debug

| Variable | What it does |
|---|---|
| `CLAUDE_CODE_DEBUG_LOGS_DIR` | Directory for debug logs. Overridden by `--debug-file` |

---

## Status line / hook output

| Variable | What it does |
|---|---|
| (none specific to status line — it receives JSON on stdin) | |

---

## Common patterns

### Bare CI invocation

```bash
ANTHROPIC_API_KEY=$KEY \
CLAUDE_CODE_USE_BEDROCK= \
claude --bare -p "lint" --allowedTools "Bash(npm run lint),Read"
```

### Cloud-only logic in a hook

```bash
#!/bin/bash
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0   # skip locally
fi
# ...cloud-only setup...
```

### Persist env vars across Bash commands in a hook

```bash
#!/bin/bash
# In SessionStart / CwdChanged / FileChanged hooks
echo "export NODE_OPTIONS='--max-old-space-size=4096'" >> "$CLAUDE_ENV_FILE"
echo "export DEBUG=app:*"                              >> "$CLAUDE_ENV_FILE"
```

### Reference plugin scripts/data

```json
// plugin's hooks/hooks.json
{
  "PostToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/log.sh ${CLAUDE_PLUGIN_DATA}/log.txt"
    }]
  }]
}
```

---

## See also

- [settings.md](./settings.md) — `env` key sets vars for every session
- [hooks.md](./hooks.md) — `CLAUDE_ENV_FILE` and other hook-only env vars
- [skills.md](./skills.md) — substitutions like `${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}`
- [plugins.md](./plugins.md) — `${CLAUDE_PLUGIN_ROOT}` vs `${CLAUDE_PLUGIN_DATA}`
- Full env vars reference: <https://code.claude.com/docs/en/env-vars>
