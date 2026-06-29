# Codex Models & Reasoning Effort

The models Codex CLI can drive, from OpenAI's [Models](https://developers.openai.com/codex/models) page. These are the **agentic coding** GPT-5.x models, distinct from the general API model list in [models.md](./models.md).

> **Not locally verified** and **fast-moving.** OpenAI's coding-model lineup changes often; treat specific ids as a snapshot from the docs. Confirm with `/model` in the TUI after installing, and check the live [Models](https://developers.openai.com/codex/models) and [Changelog](https://developers.openai.com/codex/changelog) pages.

---

## Recommended models

| Model | Description (per docs) | Best for |
|---|---|---|
| `gpt-5.5` | Newest frontier model for complex coding, computer use, knowledge work, and research workflows | The strongest default for hard, long-horizon coding |
| `gpt-5.4` | Flagship frontier model with strong coding, reasoning, tool use, and agentic capabilities | All-purpose professional development |
| `gpt-5.4-mini` | Fast, efficient mini model for responsive tasks and subagents | Speed-sensitive or lighter work, subagents |
| `gpt-5.3-codex-spark` | Text-only **research preview**, optimized for near-instant real-time iteration (ChatGPT Pro) | Rapid edit/iterate loops |

## Older / specialized (still referenced)

| Model | Notes |
|---|---|
| `gpt-5.2-codex` | Advanced agentic coding model — context compaction, large refactors, Windows support, cybersecurity |
| `gpt-5.1-codex-max` | Extended reasoning for long-running, project-scale work; supports `xhigh` |
| `gpt-5.1-codex-mini` | Smaller, cost-effective model for routine tasks |
| `gpt-5.1-codex` | Legacy — present in the API catalog but not routed to by default |

> The docs note `gpt-5.2` and `gpt-5.3-codex` are **deprecated for ChatGPT sign-in**; update references to current recommended models.

---

## Reasoning effort

Most GPT-5.x models accept a reasoning-effort setting that trades speed for depth:

```
none · minimal · low · medium · high · xhigh
```

- `xhigh` is available on `gpt-5.1-codex-max` and newer families that support it.
- Set it persistently in config, or pick it together with the model via `/model`.

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
```

Related output controls (see [codex-config.md](./codex-config.md)):

| Key | Values |
|---|---|
| `model_reasoning_summary` | `auto` \| `concise` \| `detailed` \| `none` |
| `model_verbosity` | `low` \| `medium` \| `high` |

---

## Switching models

| Method | How |
|---|---|
| Config | `model = "gpt-5.5"` in `config.toml` |
| Flag | `codex --model gpt-5.5` (or `-m`) for a new session |
| In-session | `/model` — choose model **and** reasoning effort mid-thread |
| IDE | Model selector below the input box |

```bash
codex -m gpt-5.4-mini -c model_reasoning_effort=low   # fast, cheap session
codex -m gpt-5.5 -c model_reasoning_effort=xhigh      # deepest reasoning
```

---

## Local / open-source models

`codex --oss` points Codex at a local open-source model provider, and custom providers can be defined under `[model_providers]` in config (see [codex-config.md](./codex-config.md#authentication--providers)) — including OpenAI-compatible proxies and third parties like Mistral.

---

## See also

- [codex-config.md](./codex-config.md) — `model`, `model_reasoning_effort`, providers
- [codex-slash-commands.md](./codex-slash-commands.md) — `/model`, `/fast`
- [models.md](./models.md) — the separate **API** model list for the `openai` CLI
