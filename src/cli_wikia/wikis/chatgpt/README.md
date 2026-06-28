# ChatGPT / OpenAI CLI Wiki

Reference for OpenAI's command-line tooling. Documented against the official
**`openai` CLI v2.24.0** (installed), which ships with the OpenAI Python SDK
and makes direct API calls to ChatGPT/GPT models.

> **Two different "ChatGPT" command-line tools exist:**
> - **`openai` CLI** — official, API-focused (chat completions, images, audio,
>   files, fine-tuning). This is what's installed and documented here in detail.
> - **Codex CLI** — OpenAI's *coding agent* (the peer to Claude Code / Gemini
>   CLI / Copilot CLI). Not installed on this machine — see
>   [codex-cli.md](./codex-cli.md). Verify details in the official docs.

## Quick start

```bash
export OPENAI_API_KEY=sk-...
openai api chat.completions.create -m gpt-4o -g user "Explain async/await"
openai api models.list
```

## Topics

| File | What it covers |
|------|----------------|
| [cli-reference.md](./cli-reference.md) | `openai` flags + `api` / `tools` / `migrate` / `grit` subcommands |
| [models.md](./models.md) | Choosing a model (`-m`), listing models |
| [configuration.md](./configuration.md) | API key, base URL, organization, Azure |
| [codex-cli.md](./codex-cli.md) | OpenAI Codex CLI — the coding-agent peer (from docs) |

> CLI sections verified from `openai --help`. Model names and Codex details
> come from official OpenAI docs — verify with `openai api models.list` and the
> latest documentation.
