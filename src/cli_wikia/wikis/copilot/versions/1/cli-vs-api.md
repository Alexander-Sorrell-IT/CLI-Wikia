# CLI vs API (GitHub Copilot)

## The two shapes

| | CLI — Copilot CLI | API |
|--|-------------------|-----|
| **What it is** | A terminal agent you run (`copilot`) | Programmatic model access |
| **Who uses it** | A person, interactively | Your application, programmatically |
| **Invocation** | `copilot`, `copilot -p "..."` | GitHub Models API / provider API (BYOK) |
| **Output** | Chats, edits files, runs tools | JSON your code parses |

## How they relate

The Copilot CLI is an **agent** that runs models behind the scenes. Copilot is
primarily delivered as a *product* (IDE, CLI) rather than a single public chat
API, but:

- The CLI can use a **`--model`** and supports **BYOK ("bring your own key")
  custom model providers** (see the `providers` help topic), so it can be
  pointed at provider APIs.
- For pure programmatic use, the **GitHub Models API** and the underlying
  provider APIs are the API-shaped surface.

## When to use which

- **API** — building software / automation → use the provider or GitHub Models API.
- **CLI (Copilot)** — interactive coding help in the terminal, with permissions
  and MCP.

> Rule of thumb: **API for programs, CLI for people.** Copilot's exact API
> offerings change — verify in the official GitHub Copilot docs and the
> `copilot help providers` topic.

## Sources

- GitHub Copilot CLI official docs: <https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli> and <https://github.com/github/copilot-cli> (Accessed 2026-07-02)
- Core pages of this wiki (hooks, configuration, cli-reference, custom-instructions, mcp, permissions) were re-verified against the official docs and the installed `copilot` CLI 1.0.68 on 2026-07-02; this page has not been individually re-verified since — confirm details against the official docs above.
