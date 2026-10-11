# ChatGPT / OpenAI CLI Wiki

OpenAI's command-line tooling. There are **two distinct binaries**, and this wiki covers both:

1. **Codex CLI (`codex`)** — OpenAI's terminal **coding agent**, the peer to Claude Code, Gemini CLI and Copilot CLI. Reads your repo, edits files, runs commands in an agentic loop. Open source, written in Rust. **This is the primary tool here.**
2. **`openai` CLI (v2.24.0)** — a thin command-line **wrapper over the OpenAI API** (chat, images, audio, files, fine-tuning). Not an agent.

> **Tool status on this machine**
> - **Codex (`codex`) — NOT installed.** Every `codex-*.md` page is sourced from OpenAI's official docs at <https://developers.openai.com/codex/> and the [openai/codex](https://github.com/openai/codex) repo, and is **clearly marked as not locally verified.** Confirm flag/key spellings with `codex --help` / `codex doctor` after installing. Items the docs left ambiguous are flagged "verify."
> - **`openai` CLI (v2.24.0) — installed.** Its pages were confirmed against real `openai --help` output.
>
> These are unrelated tools that happen to share a vendor — see [cli-vs-api.md](./cli-vs-api.md).

---

## Quick start

```bash
# Codex — coding agent (after installing it)
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex "fix the failing test in app.py"           # interactive TUI
codex exec --json "summarize recent changes"      # headless / CI

# openai CLI — direct API calls (installed)
export OPENAI_API_KEY=sk-...
openai api chat.completions.create -m gpt-4o -g user "Explain async/await"
```

---

## Codex CLI (coding agent) — from official docs

| File | What it covers |
|---|---|
| [codex-overview.md](./codex-overview.md) | **Start here** — install, first run, the two modes, mental model, capabilities |
| [codex-cli-reference.md](./codex-cli-reference.md) | Every `codex` subcommand and global flag |
| [codex-config.md](./codex-config.md) | Every `config.toml` key — model, sandbox, providers, history, profiles, features |
| [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) | The safety model — sandbox modes × approval policies, presets, OS enforcement |
| [codex-models.md](./codex-models.md) | The GPT-5.x coding-model lineup and reasoning effort (`minimal`…`xhigh`) |
| [codex-agents-md.md](./codex-agents-md.md) | `AGENTS.md` — discovery order, merging, and what to put where |
| [codex-mcp.md](./codex-mcp.md) | MCP servers — stdio & HTTP transports, all keys, Codex-as-MCP-server |
| [codex-slash-commands.md](./codex-slash-commands.md) | In-TUI commands (`/model`, `/approvals`, `/diff`, `/review`, `/init`, …) |
| [hooks.md](./hooks.md) | Lifecycle hooks — events, `hooks.json` / `[hooks]` config, trust, `/hooks` |
| [codex-auth.md](./codex-auth.md) | Sign in with ChatGPT vs API key, device auth, headless/SSH, access tokens |
| [codex-exec.md](./codex-exec.md) | Non-interactive `codex exec` for scripting and CI |

## `openai` CLI (API wrapper) — verified from `--help`

| File | What it covers |
|---|---|
| [cli-reference.md](./cli-reference.md) | `openai` global flags + `api` / `tools` subcommands |
| [models.md](./models.md) | Choosing an **API** model (`-m`), listing models with `models.list` |
| [configuration.md](./configuration.md) | API key, base URL, organization, Azure backend |

## Concepts

| File | What it covers |
|---|---|
| [cli-vs-api.md](./cli-vs-api.md) | How the CLI and the API relate, and when to use each |

---

## Which tool do I want?

| You want to… | Use | Page |
|---|---|---|
| Have an agent edit code in your repo | **Codex** | [codex-overview.md](./codex-overview.md) |
| Run a hands-off coding task in CI | **Codex** `exec` | [codex-exec.md](./codex-exec.md) |
| Lock down what the agent can touch | **Codex** sandbox/approvals | [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) |
| Give the agent project rules | **Codex** `AGENTS.md` | [codex-agents-md.md](./codex-agents-md.md) |
| Make a one-off chat/completion call | **`openai`** CLI | [cli-reference.md](./cli-reference.md) |
| Generate images / transcribe audio / manage files | **`openai`** CLI | [cli-reference.md](./cli-reference.md) |
| Understand CLI vs API conceptually | — | [cli-vs-api.md](./cli-vs-api.md) |

---

## Reference URLs

- Codex docs: <https://developers.openai.com/codex/>
- Codex source: <https://github.com/openai/codex>
- OpenAI API & models: <https://platform.openai.com/docs/>

## Sources

- OpenAI Developers — Codex CLI: <https://developers.openai.com/codex/cli> (Accessed 2026-07-02)
- OpenAI Developers — Configuration Reference: <https://developers.openai.com/codex/config-reference> (Accessed 2026-07-02)
- OpenAI Developers — Hooks: <https://developers.openai.com/codex/hooks> (Accessed 2026-07-02)
- GitHub — openai/codex: <https://github.com/openai/codex> (Accessed 2026-07-02)
- Not locally verified: Codex CLI is not installed on this machine as of 2026-07-02; facts are from the official docs above.
