# Models (Antigravity)

## Listing models

```bash
agy models
```

## Available models

As reported by `agy models` (v1.0.12) — note Antigravity offers **multiple
vendors' models** and exposes reasoning/effort tiers in the model name:

| Model | Notes |
|-------|-------|
| Gemini 3.5 Flash (Medium) | Google, fast tier |
| Gemini 3.5 Flash (High) | Google, fast tier, higher effort |
| Gemini 3.5 Flash (Low) | Google, fast tier, low effort |
| Gemini 3.1 Pro (Low) | Google, pro tier |
| Gemini 3.1 Pro (High) | Google, pro tier, higher effort |
| Claude Sonnet 4.6 (Thinking) | Anthropic, with extended thinking |
| Claude Opus 4.6 (Thinking) | Anthropic, with extended thinking |
| GPT-OSS 120B (Medium) | Open-weight GPT model |

## Selecting a model

```bash
agy --model "Gemini 3.1 Pro (High)" -p "..."
```

> This list is what `agy models` returned on this machine (v1.0.12). The exact
> roster changes over time — run `agy models` for the current set.
