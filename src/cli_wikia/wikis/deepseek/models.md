# Models

DeepSeek Code runs on the **DeepSeek V4** family. Two models are exposed through the
CLI, selected by the short names `pro` and `flash`. Both are Mixture-of-Experts (MoE)
models with a **1M-token context window**.

| Short name | Full ID | Architecture | Context | Price (in / out, per 1M tok) |
|------------|---------|--------------|---------|------------------------------|
| **`flash`** | `deepseek-v4-flash` | 284B MoE, 13B active | 1M | $0.14 / $0.28 |
| **`pro`** | `deepseek-v4-pro` | 1.6T MoE, 49B active | 1M | $0.145 / $1.74 |

> The parameter counts and 1M context are corroborated by public DeepSeek V4 sources.
> The prices are as printed by `deepseek-code --help`; *verify current pricing in the
> official DeepSeek pricing page before relying on it for budgeting.*

**When to use which:**

- **Flash** is the daily default — fast and cheap, ideal for quick fixes, simple
  edits, routine refactors, and high-volume work. It is the model a bare
  `deepseek-code` REPL starts on.
- **Pro** is for heavy lifting — complex reasoning, architecture and design work,
  tricky multi-step debugging, and anything where quality matters more than latency
  or cost.

---

## Selecting a model

### From the CLI

```bash
deepseek-code --model pro "refactor the logging module"
deepseek-code --model flash "quick fix for the typo"
deepseek-code --model deepseek-v4-flash "explicit full ID"
```

### Mid-session

```
/model            # interactive switch
/model pro        # switch immediately
```

### As a default

```bash
# environment
export DEEPSEEK_CODE_MODEL=deepseek-v4-pro
```

```json
// ~/.deepseek-code/config.json
{ "model": "deepseek-v4-flash" }
```

Note that the Clawspring layer also carries a default model in
`~/.clawspring/settings.json` (`"model": "deepseek-v4-pro"`). The CLI's own
`~/.deepseek-code/config.json` defaults to `deepseek-v4-flash`. When the two disagree,
the more specific source wins (CLI flag > env > CLI config > Clawspring settings) —
*verify the exact precedence in your install.* See [configuration.md](configuration.md).

---

## Reasoning effort

`--effort` controls how much reasoning the model invests, trading speed and cost for
depth. Four levels:

```
low → medium → high → max
```

| Level | Use it for |
|-------|------------|
| `low` | Trivial tasks — typos, quick greps, lookups |
| `medium` | Routine work — standard edits, moderate debugging |
| `high` | Complex work — refactors, architecture, multi-step plans (**default**) |
| `max` | Critical reasoning — security audits, migration plans, tricky edge cases |

```bash
deepseek-code --effort max "design a migration plan"
deepseek-code --effort low "fix the typo on line 42"
```

Set persistently with `DEEPSEEK_CODE_EFFORT`, the `effortLevel` config field, or per
skill/agent via `effort:` frontmatter. The default is `high`.

> Some agent/skill specs in this install accept an extended effort scale
> (`low/medium/high/xhigh/max`). The CLI `--effort` flag documents only the four
> levels above; `xhigh` appears in frontmatter contexts. *Verify which scale applies
> where in the tool.*

---

## Thinking (reasoning) mode

`--thinking` controls whether the model engages in extended chain-of-thought before
answering.

| Value | Behavior |
|-------|----------|
| `on` | Reasoning mode enabled (default in the shipped config) |
| `off` | Answer directly, no extended reasoning |
| `max` | Maximum extended thinking for the hardest problems |

```bash
deepseek-code --thinking max "trace this race condition"
deepseek-code --thinking off "what time is it"
```

The Clawspring settings expose a related toggle, `alwaysThinkingEnabled: true`, which
keeps thinking on across all interactions, and `~/.clawspring/config.json` carries a
`thinking_budget` (default `10000`) that caps thinking tokens. See
[configuration.md](configuration.md).

---

## Fallback model

Automatically fall back to a second model when the primary is overloaded:

```bash
deepseek-code --model pro --fallback-model flash "do the task"
```

This is most useful in headless `-p` runs where you do not want a transient overload
to abort the job.

---

## Relationship to the DeepSeek API

The same `deepseek-v4-pro` / `deepseek-v4-flash` model IDs are served by the public
DeepSeek API (OpenAI-compatible at `https://api.deepseek.com`, with an
Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`). DeepSeek Code
is an agent built on top of that API. See [cli-vs-api.md](cli-vs-api.md).
