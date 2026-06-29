# CLI vs API (DeepSeek)

## The two shapes

| | CLI — DeepSeek Code | API — DeepSeek API |
|--|---------------------|--------------------|
| **What it is** | A terminal coding agent (`deepseek-code`) | An HTTP endpoint your code calls |
| **Who uses it** | A person, interactively | Your application, programmatically |
| **Invocation** | `deepseek-code`, `deepseek-code -p "..."` | DeepSeek API via HTTP/SDK |
| **Auth** | `deepseek-code auth login` / `DEEPSEEK_API_KEY` | `DEEPSEEK_API_KEY` |
| **Output** | Chats, edits files, runs tools | JSON your code parses |

## How they relate

DeepSeek Code (the CLI) is an **agent built on the DeepSeek API**: it wraps the
model (V4 Pro / Flash) in a loop with tools, sessions, agents, skills and hooks.
The API is what you call directly from your own code.

Both share the same key: `DEEPSEEK_API_KEY` authenticates the CLI *and* direct
API calls.

## When to use which

- **API** — building software that uses DeepSeek models.
- **CLI (DeepSeek Code)** — interactive agentic coding in your repo.

> Rule of thumb: **API for programs, CLI for people.** Verify current API
> endpoints and model IDs in the official DeepSeek API docs.
