# Billing & Usage

Copilot CLI usage is metered in **AI credits** against your Copilot budget. (On the legacy billing platform you'll instead see **premium requests**.) The CLI surfaces usage in several places so you can keep spend in view.

Reference: `copilot help billing`.

---

## Where usage appears

| Surface | What it shows |
|---|---|
| **Footer / status bar** | Remaining AI-credit budget, continuously (or remaining premium requests on legacy billing) |
| `/statusline` | Add `ai-credits` (monthly usage) and `ai-used` (this session). Legacy: `quota` for remaining premium requests |
| `/model` picker | Per-token cost for each model — input, cached input, and output (legacy: a request multiplier) |
| `/context` | Context-window token usage by source (system prompt, tools, messages; finer per-source breakdown in `/experimental`) |
| `/usage` | AI-credit usage for the session, token breakdown (input/output/cached), and usage-limit progress |
| `/exit` | An exit summary reporting the session's usage |

---

## Controlling spend

- **Pick a cheaper model** — the `/model` picker shows relative cost before you switch.
- **Reasoning effort** — lower `--effort` costs less (see [models.md](models.md)).
- **Autopilot cap** — in autopilot mode the agent pauses after a number of automatic continuations so unattended usage doesn't run away. Default is **5**; change it with `--max-autopilot-continues <count>`.
- **Context tier** — `long_context` is priced higher than `default` for tiered models.

---

## BYOK

When using a [custom model provider (BYOK)](providers-byok.md), inference is billed by **your** provider, not GitHub — these requests don't consume AI credits and don't participate in the `continueOnAutoMode` auto-switch on rate limits.

---

## Learn more

- AI credits: <https://docs.github.com/en/copilot/concepts/billing>
- Legacy premium requests: <https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy>

---

## See also

- [models.md](models.md) — cost vs capability
- [modes.md](modes.md) — autopilot continuation cap
- [monitoring.md](monitoring.md) — token/cost data via OTel
