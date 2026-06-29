# Models

Unlike the older Gemini CLI, Antigravity is **multi-vendor**: it can route a
session to Google's Gemini models, Anthropic's Claude models, or an open-weight
GPT model. The **reasoning/effort tier is baked into the model name** you select.

## Listing models

```bash
agy models
```

On this machine (v1.0.13) that returns:

| Model | Vendor | Tier / notes |
|-------|--------|--------------|
| Gemini 3.5 Flash (Low) | Google | Fast tier, low effort |
| Gemini 3.5 Flash (Medium) | Google | Fast tier, default balance |
| Gemini 3.5 Flash (High) | Google | Fast tier, higher effort |
| Gemini 3.1 Pro (Low) | Google | Pro tier, low effort |
| Gemini 3.1 Pro (High) | Google | Pro tier, deep reasoning |
| Claude Sonnet 4.6 (Thinking) | Anthropic | Extended thinking |
| Claude Opus 4.6 (Thinking) | Anthropic | Extended thinking |
| GPT-OSS 120B (Medium) | Open-weight | Open GPT model |

The **default model** is **Gemini 3.5 Flash** (config key `model` defaults to
`gemini-3.5-flash`). Flash powers local agents with speed and large context;
Pro is for complex planning, architecture, and hard debugging.

> The exact roster depends on your account/plan and changes over time. Always run
> `agy models` for the current set. Availability of higher tiers and Pro models
> can depend on your Google AI subscription (e.g. Google AI Pro vs Ultra) —
> verify entitlements in official docs.

---

## Reasoning / effort tiers

The parenthesized tier (**Low / Medium / High**, plus an internal **Minimal**)
controls how much the model "thinks" — its computational depth and planning
budget — before acting:

| Tier | Behavior | Best for |
|------|----------|----------|
| **Low** (and Minimal) | Fewer reasoning steps, faster, cheaper | Boilerplate, simple edits, straightforward commands |
| **Medium** | Balanced reasoning | Everyday coding, most tasks |
| **High** | Extra reasoning, validation traces, self-correction, more tool calls | Debugging complex failures, system design, ambiguous bugs |

The Claude models expose this as a **(Thinking)** variant (extended
chain-of-thought) rather than discrete Low/Medium/High labels.

**Tip:** start at a lower tier and step up only when a task needs it — this
conserves quota and reduces the chance of hitting rate limits.

---

## Selecting a model

### At launch

```bash
agy --model "Gemini 3.1 Pro (High)" -p "design a migration plan for the DB layer"
```

Use the exact display name from `agy models` (it includes the tier in
parentheses).

### Mid-session

```
/model        # opens the interactive model picker
```

### As a default

Set it in `settings.json` (see [configuration.md](./configuration.md)):

```json
{ "model": "gemini-3.5-flash" }
```

> The `settings.json` `model` key uses the internal identifier
> (`gemini-3.5-flash`), whereas `--model` and `/model` accept the human display
> name with the tier. When in doubt, pick from `agy models` / `/model`.

---

## See also

- [agentic-model.md](./agentic-model.md) — how the model is used in the agent loop
- [cli-reference.md](./cli-reference.md) — the `--model` flag and `/model` command
- [cli-vs-api.md](./cli-vs-api.md) — `agy` vs calling these vendors' APIs directly
