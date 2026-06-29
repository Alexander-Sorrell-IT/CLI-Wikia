# CLI vs API (OpenAI / ChatGPT)

OpenAI is the clearest example of the difference, because here you can see
*both* shapes side by side.

## The two shapes

| | CLI | API |
|--|-----|-----|
| **What it is** | A program you run in a terminal | An HTTP endpoint your code calls |
| **Who uses it** | A person, interactively | Your application, programmatically |
| **OpenAI examples** | `codex` (coding agent), `openai` (API-wrapper CLI) | `https://api.openai.com/v1/...` via SDK |
| **Auth** | Account login or `OPENAI_API_KEY` | `OPENAI_API_KEY` (bearer token) |
| **Output** | Human-readable text / edits files | JSON your code parses |

## How they relate

The **API is the foundation**; the CLIs sit on top of it:

- **`openai` CLI** is essentially a thin command-line wrapper over the API —
  `openai api chat.completions.create ...` is the *same* call your code would
  make to `POST /v1/chat/completions`, just from the shell.
- **Codex** is an *agent* built on the API: it adds a loop, tools (edit files,
  run commands), and permissions on top of the raw model calls.

## When to use which

- **API** — you're building software: a backend, a script, a product feature.
  You want structured JSON, retries, streaming into your own UI.
- **CLI (`openai`)** — quick one-off API calls or testing from the terminal.
- **CLI (Codex agent)** — you want hands-on help coding in your repo.

> Rule of thumb: **API for programs, CLI for people.** An agent CLI (Codex) is
> "a person-style tool that acts on its own," still powered by the API underneath.
