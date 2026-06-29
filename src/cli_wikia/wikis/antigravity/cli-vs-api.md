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

> Rule of thumb: **API for programs, CLI for people.** Antigravity is firmly a
> people-facing agent; verify whether it exposes any programmatic API in the
> official Google docs.
