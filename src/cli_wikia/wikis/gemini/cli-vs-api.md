# CLI vs API (Gemini)

## The two shapes

| | CLI — Gemini CLI | API — Gemini API |
|--|------------------|------------------|
| **What it is** | A terminal program you run (`gemini`) | An HTTP endpoint your code calls |
| **Who uses it** | A person, interactively | Your application, programmatically |
| **Invocation** | `gemini`, `gemini -p "..."` | Google's Generative Language API via SDK |
| **Auth** | Account login or API key | API key |
| **Output** | Chats, edits files, runs tools | JSON your code parses |

## How they relate

The Gemini CLI is an **agent built on the Gemini API**: it adds a terminal UI,
tools, MCP and extensions on top of raw model calls. The API is what you call
directly from code.

## When to use which

- **API** — building software that uses Gemini models.
- **CLI** — interactive coding/help in the terminal.

> Rule of thumb: **API for programs, CLI for people.** Note Google is steering
> long-term toward [Antigravity](../antigravity/README.md) as the agent tool —
> but the underlying Gemini **API** remains the programmatic interface.
> Verify current API details in the official Google AI docs.
