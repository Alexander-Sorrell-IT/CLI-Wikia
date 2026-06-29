# ChatGPT (Codex / OpenAI) Wiki

OpenAI's command-line tooling. The **primary** tool here — the peer to Claude
Code, Gemini CLI, Antigravity and Copilot CLI — is **Codex**, OpenAI's terminal
**coding agent** (`codex`). A second, API-focused tool, the **`openai` CLI**, is
also documented.

> **Tool status on this machine:**
> - **Codex CLI (`codex`)** — the coding agent. **Not installed here**, so its
>   pages are sourced from official docs and clearly marked. Start at
>   [codex-cli.md](./codex-cli.md).
> - **`openai` CLI (v2.24.0)** — installed; API calls (chat, images, audio,
>   files, fine-tuning). Verified from `openai --help`.

## Quick start

```bash
# Codex (coding agent) — after installing it
codex "fix the failing test in app.py"

# openai CLI (API calls) — installed
export OPENAI_API_KEY=sk-...
openai api chat.completions.create -m gpt-4o -g user "Explain async/await"
```

## Topics

| File | What it covers |
|------|----------------|
| [codex-cli.md](./codex-cli.md) | **Codex** — the OpenAI coding agent (primary; from docs) |
| [cli-reference.md](./cli-reference.md) | `openai` CLI flags + `api` / `tools` subcommands (verified) |
| [models.md](./models.md) | Choosing a model (`-m`), listing models |
| [configuration.md](./configuration.md) | API key, base URL, organization, Azure |

> `openai` CLI sections verified from `openai --help`. Codex and model names
> come from official OpenAI docs — verify after installing `codex` and with
> `openai api models.list`.
