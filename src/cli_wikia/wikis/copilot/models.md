# Models

Copilot CLI routes your prompts to a model from GitHub's model catalog (or to a custom provider — see [providers-byok.md](providers-byok.md)). The set of models you can pick depends on your subscription, org policy, and the CLI version.

---

## Picking a model

```bash
copilot --model gpt-5.4 -p "refactor the logging module" --allow-all-tools
copilot --model auto                # let Copilot choose per task
```

Inside a session use `/model` — the picker shows each model's relative cost (per-token input / cached-input / output, or a request multiplier on legacy billing) so you can weigh it before switching. The default can also be set with `COPILOT_MODEL` or the `model` key in `settings.json`.

`auto` is special: Copilot selects a model for you and can switch to it automatically when you hit eligible rate limits (if `continueOnAutoMode` is on).

---

## Available models

The catalog evolves; the model picker is the source of truth. As of CLI 1.0.65 the `model` setting accepts these well-known IDs:

| Family | IDs |
|---|---|
| Anthropic Claude | `claude-opus-4.8`, `claude-opus-4.7`, `claude-opus-4.6`, `claude-opus-4.6-fast`, `claude-opus-4.5`, `claude-sonnet-4.6`, `claude-sonnet-4.5`, `claude-haiku-4.5`, `claude-fable-5` |
| OpenAI GPT | `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex`, `gpt-5-mini` |
| Google Gemini | `gemini-3.1-pro-preview`, `gemini-3.5-flash` |

> Availability varies by plan and org. Verify the live list with `/model`; treat this table as a snapshot, not a contract.

---

## Context window tier

Some models offer a larger, separately priced context window. Choose the tier with:

```bash
copilot --context long_context -p "review this very large file"
```

| Flag / setting | Values | Notes |
|---|---|---|
| `--context <tier>` | `default`, `long_context` | Overrides the persisted setting |
| `contextTier` (settings.json) | `default`, `long_context` | For tiered-pricing models |

For eligible models a context-tier picker also appears inside `/model`.

---

## Reasoning effort

Controls how much the model "thinks" before answering — higher effort costs more.

```bash
copilot --effort high -p "design a migration plan"
```

| Flag | Values |
|---|---|
| `--effort`, `--reasoning-effort` | `none`, `low`, `medium`, `high`, `xhigh`, `max` |

Per-subagent effort can be set via `subagents.agents.<name>.effortLevel` (or `inherit`). For OpenAI models, `--enable-reasoning-summaries` surfaces the model's reasoning summary.

---

## Cost & usage

The `/model` picker, the footer/status bar, and `/usage` all surface cost. Usage is metered in **AI credits** (or premium requests on legacy billing). See [billing.md](billing.md).

---

## See also

- [providers-byok.md](providers-byok.md) — point the CLI at your own provider
- [billing.md](billing.md) — AI credits, quotas, autopilot caps
- [cli-vs-api.md](cli-vs-api.md) — model access via the CLI vs an API
