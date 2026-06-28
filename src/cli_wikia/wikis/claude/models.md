# Models

Claude Code runs on Anthropic's Claude family. As of 2026-04-26 the latest models are:

| Model | ID | Context | Notes |
|---|---|---|---|
| **Claude Opus 4.7** | `claude-opus-4-7` | up to **1M tokens** | Latest flagship; this guide was written by Opus 4.7 (1M context) |
| Claude Opus 4.6 | `claude-opus-4-6` | 200K | Previous Opus; **Fast mode** runs on this variant |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K | Workhorse model — high quality, faster, cheaper than Opus |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K | Fast and cheap; best for simple subagents and small workflows |

When you're building agents/skills/SDK apps, **default to the latest and most capable**: Opus 4.7 for hard reasoning, Sonnet 4.6 for everyday work, Haiku 4.5 for high-volume cheap tasks.

---

## Aliases

The CLI and frontmatter accept short aliases that always resolve to the latest in that family:

| Alias | Currently resolves to |
|---|---|
| `opus` | Latest Opus (4.7) |
| `sonnet` | Latest Sonnet (4.6) |
| `haiku` | Latest Haiku (4.5) |
| `inherit` | Whatever the parent session is using (subagent default) |

Full IDs always work too: `--model claude-opus-4-7`, `--model claude-sonnet-4-6`, etc.

---

## Selecting a model

### From the CLI

```bash
claude --model opus           # latest Opus
claude --model claude-opus-4-7
claude --model sonnet
claude -p "query" --model haiku
```

### Mid-session

```
/model           # interactive picker
/model opus      # switch immediately
```

### As a default

```json
// settings.json
{ "model": "claude-opus-4-7" }
```

### Per-skill or per-subagent

```yaml
# SKILL.md or AGENT.md
---
model: claude-haiku-4-5-20251001   # only for this skill/subagent
---
```

`model: inherit` keeps the parent's model.

### Restrict which models are pickable

```json
// settings.json (organization-friendly)
{ "availableModels": ["claude-opus-4-7", "claude-sonnet-4-6"] }
```

### Map to provider-specific IDs (Bedrock / Vertex / Foundry)

```json
{
  "modelOverrides": {
    "claude-opus-4-7": "anthropic.claude-opus-4-7-v1:0"
  }
}
```

---

## Effort level

Some models accept an *effort level* that increases internal reasoning depth (and tokens). Five levels:

```
low → medium → high → xhigh → max
```

Available levels depend on the model. Set per-session:

```bash
claude --effort high
```

Set persistently:

```json
{ "effortLevel": "xhigh" }
```

Override per-skill or per-subagent:

```yaml
---
effort: high
---
```

In the REPL: `/effort high`. The session value resumes after a per-skill override.

---

## Extended thinking

To use **extended thinking** (long chain-of-thought) in a skill, just include the word **`ultrathink`** anywhere in the skill body. To enable it by default:

```json
{ "alwaysThinkingEnabled": true, "showThinkingSummaries": false }
```

---

## Fast mode (Opus 4.6 only)

`/fast` toggles **Fast mode**, which uses Claude Opus 4.6 with faster output. It does *not* downgrade to a smaller model — it's a faster variant of Opus 4.6. Fast mode is **only available on Opus 4.6**, not 4.7.

Per-session opt-in can be required:

```json
{ "fastModePerSessionOptIn": true }
```

---

## Auto mode (model gating)

The [auto permission mode](./permission-modes.md#auto) requires one of these models — other models, including Haiku, are not supported:

- **Team / Enterprise / API plans:** Sonnet 4.6, Opus 4.6, or **Opus 4.7**
- **Max plan:** **Opus 4.7 only**
- **Pro plan:** auto mode is unavailable

If your model isn't supported, auto mode is reported as unavailable (not a transient outage).

---

## Model resolution order in subagents

When a subagent runs, Claude Code resolves the model in this order (first match wins):

1. `CLAUDE_CODE_SUBAGENT_MODEL` env var
2. The per-invocation `model` parameter (passed via the Agent tool)
3. The subagent definition's `model` frontmatter
4. The main conversation's model

So a subagent declared with `model: inherit` follows the parent — but `CLAUDE_CODE_SUBAGENT_MODEL` overrides everything.

---

## Fallback model (print mode)

For headless `claude -p` runs, if your default model is overloaded you can fall back automatically:

```bash
claude -p --fallback-model sonnet "query"
```

---

## See also

- [cli-reference.md](./cli-reference.md) — `--model`, `--effort`, `--fallback-model`, `--betas`
- [permission-modes.md](./permission-modes.md) — auto-mode model requirements
- [environment-variables.md](./environment-variables.md) — `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CODE_USE_BEDROCK`, etc.
