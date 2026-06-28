# OpenAI Codex CLI (coding agent)

The peer to Claude Code, Gemini CLI and Copilot CLI on the OpenAI side is the
**Codex CLI** — a terminal coding agent that can read your repo, edit files and
run commands. It is **not installed on this machine**, so the content below is
from public documentation rather than captured `--help` output.

> ⚠️ **Not verified locally.** Treat everything here as approximate and confirm
> against the official Codex CLI docs and `codex --help` after installing.

## Installation (typical)

```bash
npm install -g @openai/codex      # or the documented install method
codex --version
```

## Typical usage (from docs)

```bash
codex                     # interactive coding session in the current repo
codex "fix the failing test in app.py"
```

Codex CLI generally supports:
- An **interactive TUI** plus a non-interactive/exec mode for scripting.
- **Approval / autonomy modes** controlling whether edits and shell commands
  run automatically or require confirmation.
- Authentication via your OpenAI account or `OPENAI_API_KEY`.
- Model selection and an `AGENTS.md`-style project instructions file.

## How it differs from the `openai` CLI

| | `openai` CLI | Codex CLI |
|--|--------------|-----------|
| Role | Direct API calls | Autonomous coding agent |
| Edits files / runs commands | No | Yes |
| Interactive TUI | No | Yes |
| Documented here from | Real `--help` | Public docs only |

## To populate this page properly

Install Codex CLI, then capture ground truth the same way the other wikis were
built:

```bash
codex --help > /tmp/codex-help.txt
```

…and turn that into accurate topic files (cli-reference, models, configuration,
permissions/approval-modes).
