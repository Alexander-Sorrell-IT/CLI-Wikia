# Headless Mode and the Agent SDK

Two ways to run Claude Code programmatically:

1. **Headless `claude -p`** — the CLI in print mode for shell scripts, CI/CD, pipes.
2. **Agent SDK** (Python or TypeScript) — when you're embedding Claude Code's agent loop in another application.

---

## Headless via the CLI

```bash
claude -p "Find and fix the bug"

# Process piped content
cat logs.txt | claude -p "explain"

# Resume a specific session
claude -p "Focus on errors" --resume "$session_id"

# CI / fast / deterministic
claude --bare -p "lint" --allowedTools "Bash,Read"
```

### `--bare` mode

Skips auto-discovery of hooks, skills, plugins, MCP servers, auto-memory, and CLAUDE.md. Has Bash + file Read + file Edit tools. Sets `CLAUDE_CODE_SIMPLE`. Fastest, most deterministic — ideal for CI.

### Output formats

```bash
# Plain text (default)
claude -p "query"

# JSON: { result, session_id, usage, ... }
claude -p "query" --output-format json

# Streaming: newline-delimited JSON
claude -p "Write a poem" \
  --output-format stream-json \
  --verbose --include-partial-messages \
| jq -rj 'select(.type=="stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

### Structured output via JSON Schema

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{
    "type":"object",
    "properties":{"functions":{"type":"array","items":{"type":"string"}}}
  }' \
| jq '.structured_output'
```

### Multi-turn

```bash
session_id=$(claude -p "Review this" --output-format json | jq -r '.session_id')
claude -p "Focus on X" --resume "$session_id"
```

---

## Useful headless flags

| Flag | Purpose |
|---|---|
| `--output-format text\|json\|stream-json` | Output mode |
| `--input-format text\|stream-json` | Input mode |
| `--include-partial-messages` | Token-level streaming events |
| `--include-hook-events` | Include hook lifecycle events in output |
| `--replay-user-messages` | Re-emit user messages back on stdout for ack (with stream-json input) |
| `--max-turns <N>` | Limit agentic turns; exits with error when reached |
| `--max-budget-usd <amount>` | Cap dollar spend |
| `--no-session-persistence` | Don't save session to disk |
| `--fork-session` | New session ID instead of reusing original (with `--resume`) |
| `--fallback-model <name>` | Auto-fallback when default model is overloaded |
| `--exclude-dynamic-system-prompt-sections` | Move per-machine sections (cwd, env, memory paths, git status) into first user message — improves prompt-cache reuse across users |
| `--bare` | Skip discovery (see above) |
| `--permission-prompt-tool <mcp-tool>` | MCP tool to handle permission prompts non-interactively |

---

## Continuous integration patterns

### Lint + auto-fix

```bash
claude --bare -p "Run npm test, fix any failures, commit when green" \
  --allowedTools "Bash(npm *),Edit,Bash(git *)" \
  --max-turns 10 \
  --max-budget-usd 0.50 \
  --output-format json
```

### Structured extraction

```bash
RESULT=$(claude -p "List exported symbols from src/api.ts" \
  --output-format json \
  --json-schema "$(cat schema.json)" \
| jq -r '.structured_output')
```

### Streaming UI

```bash
claude -p "explain this codebase" \
  --output-format stream-json --include-partial-messages --verbose \
| my-streaming-renderer
```

### Pre-approved MCP permission prompts

For non-interactive sessions where MCP needs OAuth, use:

```bash
claude -p --permission-prompt-tool mcp_auth_tool "do work"
```

---

## The Agent SDK

When `claude -p` isn't enough — when you're embedding the agentic loop into your own application.

Two packages:
- **Python**: `pip install anthropic` (general SDK) — see [agent-sdk overview](https://code.claude.com/docs/en/agent-sdk/overview)
- **TypeScript**: `@anthropic-ai/sdk`

What the Agent SDK adds over `claude -p`:

- **Validated structured outputs** (JSON Schema enforcement at the SDK level)
- **Tool approval callbacks** — write your own approve/deny logic
- **Programmatic subagent spawning**
- **Session persistence** with custom storage backends
- **Real-time streaming with callbacks**
- **Cost tracking** — token usage breakdowns
- **Programmatic hook registration**

### Minimal Python example

```python
from anthropic import Anthropic

client = Anthropic(api_key="…")

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[...],
    messages=[{"role": "user", "content": "Fix the bug"}],
)
print(response.content[0].text)
```

### Minimal TypeScript example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const response = await client.messages.create({
  model: 'claude-opus-4-7',
  max_tokens: 1024,
  tools: [...],
  messages: [{ role: 'user', content: 'Fix the bug' }],
});

console.log(response.content[0].type === 'text' ? response.content[0].text : '');
```

### Always include prompt caching

When building Agent SDK apps, **always include prompt caching** (`cache_control` on stable system prompts and tools). Major cost reduction — every session-start CLAUDE.md and tool-list is a cache hit after the first request.

### Migrating between Claude versions

The `/claude-api` bundled skill handles migrations between Claude API versions (4.5 → 4.6, 4.6 → 4.7, retired model replacements). Invoke it on existing Anthropic-SDK code to update.

---

## When to use what

| Use case | Tool |
|---|---|
| One-off shell query | `claude -p` |
| Multi-turn shell conversation | `claude --continue` + `--resume` |
| CI/CD workflow | `claude --bare -p` |
| Structured output | `--output-format json` + `--json-schema` |
| Real-time token streaming | `--output-format stream-json` |
| Python app | Agent SDK (Python) |
| TypeScript app | Agent SDK (TypeScript) |
| Complex programmatic tool use with custom approval | Agent SDK with hooks/callbacks |

---

## See also

- [cli-reference.md](./cli-reference.md) — every flag
- [hooks.md](./hooks.md) — hooks work in headless mode too
- [models.md](./models.md) — `--fallback-model`, `availableModels`
- Agent SDK documentation: <https://code.claude.com/docs/en/agent-sdk/overview>
