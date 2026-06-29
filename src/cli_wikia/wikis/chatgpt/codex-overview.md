# Codex CLI — Overview

**Codex CLI** (`codex`) is OpenAI's terminal coding agent — the peer to Claude Code, Gemini CLI and Copilot CLI. It reads your repository, edits files, runs commands, and iterates in an agentic loop. It is **open source and written in Rust**.

> **Source & verification status.** Everything on this page and the other `codex-*.md` files is sourced from OpenAI's official documentation at <https://developers.openai.com/codex/> and the [openai/codex](https://github.com/openai/codex) repo. **Codex is NOT installed on this machine**, so none of it was confirmed against a local `codex --help`. Treat flag/key spellings as authoritative-from-docs but re-verify with `codex --help` and `codex doctor` after installing. Anything marked "verify" was uncertain in the docs.
>
> The separate **`openai` CLI** (the API wrapper, v2.24.0) *is* installed and is documented in [cli-reference.md](./cli-reference.md), [models.md](./models.md), and [configuration.md](./configuration.md). The two tools are unrelated binaries — see [cli-vs-api.md](./cli-vs-api.md).

---

## The mental model

Codex layers two independent security controls on top of an agentic model loop:

```
   ┌─────────────────────────────────────────────┐
   │  Approval policy   "when must Codex ASK?"    │  untrusted / on-request / never / granular
   ├─────────────────────────────────────────────┤
   │  Sandbox mode      "what CAN Codex do?"      │  read-only / workspace-write / danger-full-access
   ├─────────────────────────────────────────────┤
   │  AGENTS.md         project/global prompts    │  always-loaded instructions
   ├─────────────────────────────────────────────┤
   │  config.toml + profiles + CLI flags          │  layered configuration
   ├─────────────────────────────────────────────┤
   │  Model + reasoning effort (GPT-5.x family)   │
   └─────────────────────────────────────────────┘
```

The two key safety layers are **orthogonal**: the *sandbox* defines what Codex is technically able to do (filesystem/network boundaries), while the *approval policy* defines when it must stop and ask you first. See [codex-approvals-sandbox.md](./codex-approvals-sandbox.md).

---

## Installation

| Platform | Command |
|---|---|
| macOS / Linux | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` |
| npm | `npm install -g @openai/codex` |
| Homebrew | `brew install codex` (verify formula name) |
| Windows | Native PowerShell installer, or run the Linux installer inside WSL2 |

For unattended/CI installs, set `CODEX_NON_INTERACTIVE=1` in the shell that runs the installer.

```bash
codex --version    # confirm install
codex doctor       # diagnostic report (auth, sandbox, config health)
codex update       # check for and install CLI updates
```

---

## First run & authentication

The first time you run `codex` you are prompted to sign in. Access requires a compatible plan — **ChatGPT Plus, Pro, Business, Edu, or Enterprise** — or an OpenAI API key.

```bash
codex                 # launches the interactive TUI; prompts sign-in on first run
codex login           # Sign in with ChatGPT (default) — opens a browser for OAuth
```

Two auth paths:

- **Sign in with ChatGPT** (default) — uses your subscription entitlements; full feature set.
- **API key** — usage-based billing; some features may be limited.

Credentials are cached at `~/.codex/auth.json`. Full detail (device-auth, headless/SSH, access tokens, env vars) is in [codex-auth.md](./codex-auth.md).

---

## The two operating modes

### Interactive (TUI)

```bash
codex                              # open an interactive session in the current repo
codex "fix the failing test in app.py"   # open the TUI seeded with an initial task
```

A full-screen terminal UI where you converse with the agent, watch diffs, approve commands, and drive it with [slash commands](./codex-slash-commands.md) (`/model`, `/approvals`, `/diff`, `/review`, `/init`, …).

### Non-interactive (`exec`)

```bash
codex exec "update the changelog for the latest release"
git log --oneline -20 | codex exec "summarize these commits"
codex exec --json "run the test suite and report failures"
```

`codex exec` (alias `codex e`) runs headless to completion — for scripting and CI. It exits non-zero on submission failure. See [codex-exec.md](./codex-exec.md).

---

## Key capabilities (from docs)

| Capability | Notes |
|---|---|
| Model switching | `/model` in the TUI, `--model/-m` flag, or `model` in config — see [codex-models.md](./codex-models.md) |
| Approval / sandbox modes | Per-session safety presets — see [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) |
| Project instructions | `AGENTS.md` files, global + per-repo + nested — see [codex-agents-md.md](./codex-agents-md.md) |
| MCP | Connect third-party tools via Model Context Protocol — see [codex-mcp.md](./codex-mcp.md) |
| Image inputs | Attach screenshots / design specs alongside a prompt (`--image/-i`) |
| Web search | Pull current information into a task (`--search`, or `web_search` config) |
| Code review | `/review` runs a local review agent over your working tree |
| Subagents | Parallelize complex work across agent threads (`/agent`) |
| Resume / fork | Continue or branch prior sessions (`codex resume`, `codex fork`, `/resume`, `/fork`) |
| Codex Cloud | Launch and apply cloud tasks from the terminal (`codex cloud`, `codex apply`) |
| IDE + integrations | VS Code/Cursor extension; GitHub, Slack, Linear connectors |

---

## Configuration at a glance

Codex is configured by `~/.codex/config.toml` (user) and `.codex/config.toml` (project), layered with profiles and CLI overrides. Minimal example:

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Full key reference: [codex-config.md](./codex-config.md).

---

## See also

- [codex-cli-reference.md](./codex-cli-reference.md) — every subcommand and flag
- [codex-config.md](./codex-config.md) — every `config.toml` key
- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — the safety model
- [codex-models.md](./codex-models.md) — GPT-5.x model lineup & reasoning effort
- [codex-agents-md.md](./codex-agents-md.md) — `AGENTS.md` project instructions
- [codex-mcp.md](./codex-mcp.md) — MCP servers
- [codex-slash-commands.md](./codex-slash-commands.md) — in-TUI commands
- [codex-auth.md](./codex-auth.md) — authentication
- [codex-exec.md](./codex-exec.md) — non-interactive automation
