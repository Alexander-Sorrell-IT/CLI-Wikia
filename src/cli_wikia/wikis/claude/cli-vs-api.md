# CLI vs API (Claude)

## The two shapes

| | CLI — Claude Code | API — Anthropic Messages API |
|--|-------------------|------------------------------|
| **What it is** | A terminal coding agent you run | An HTTP endpoint your code calls |
| **Who uses it** | A person, interactively | Your application, programmatically |
| **Invocation** | `claude`, `claude -p "..."` | `POST /v1/messages` via the Anthropic SDK |
| **Auth** | Account login or `ANTHROPIC_API_KEY` | `ANTHROPIC_API_KEY` |
| **Output** | Edits files, runs tools, chats | JSON your code parses |

## How they relate

Claude Code (the CLI) is an **agent built on the Messages API**: it wraps the
raw model calls in a loop with tools (read/edit files, run commands, hooks,
permissions). The Claude Agent SDK lets you build your *own* agent on the same
API.

## When to use which

- **API / SDK** — building a product, backend, or automation that calls Claude.
- **CLI (Claude Code)** — hands-on coding in your repo with an autonomous agent.

> Rule of thumb: **API for programs, CLI for people.** See also
> [headless-sdk.md](./headless-sdk.md) for using Claude Code itself
> programmatically — a middle ground between the two.
