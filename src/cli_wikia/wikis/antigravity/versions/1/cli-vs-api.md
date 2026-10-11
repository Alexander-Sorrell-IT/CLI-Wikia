# CLI vs API (Antigravity)

## The two shapes

| | CLI — Antigravity (`agy`) | API |
|--|---------------------------|-----|
| **What it is** | A terminal agent you run | The model APIs it calls underneath |
| **Who uses it** | A person, interactively | Your application, programmatically |
| **Invocation** | `agy`, `agy -p "..."` | The provider API of the chosen model |
| **Output** | Chats, edits files, runs tools | JSON your code parses |

## How they relate

Antigravity is an **agent product**, not itself a public model API. It
orchestrates models from several providers (its `agy models` list includes
Gemini, Claude and an open GPT model) and calls *their* APIs underneath.

So the split here is:
- **`agy` (CLI/agent)** — the interactive tool you drive in the terminal.
- **The model APIs** (Gemini API, Anthropic API, etc.) — the programmatic
  interfaces to the underlying models, used directly when you build software.

## When to use which

- **API** — building software → call the underlying model's API directly
  (see the [gemini](../gemini/cli-vs-api.md) and [chatgpt](../chatgpt/cli-vs-api.md) pages).
- **CLI (`agy`)** — hands-on, multi-model agentic coding in the terminal.

> Rule of thumb: **API for programs, CLI for people.** Antigravity is primarily a
> people-facing agent, but it *also* ships a programmatic surface — the public
> **Antigravity Python SDK** (`pip install google-antigravity`) — for embedding
> agents in code. See [sdk.md](./sdk.md). The SDK orchestrates the same agents;
> the underlying *model* APIs (Gemini, Anthropic, …) remain separate.

## Sources

- Antigravity official docs: `https://antigravity.google/docs` (hooks: `/docs/hooks`, CLI features: `/docs/cli-features`, usage: `/docs/cli-using`) (Accessed 2026-07-02)
- Google Developers Blog, "An important update: Transitioning Gemini CLI to Antigravity CLI": `https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/` (Accessed 2026-07-02)
- GitHub — google-antigravity/antigravity-cli: `https://github.com/google-antigravity/antigravity-cli` (Accessed 2026-07-02)
- Verified against the installed CLI on 2026-07-02: `agy` v1.0.13 (`agy --help`; binary strings confirm `.agents/` workspace root incl. `.agents/skills` and `.agents/agents`, `AGENTS.md` and `GEMINI.md` recognition, `~/.gemini/antigravity-cli/settings.json`, and `hooks.json` discovery) and on-disk state under `~/.gemini/antigravity-cli/` and `~/.gemini/config/`.
