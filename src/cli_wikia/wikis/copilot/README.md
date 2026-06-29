# GitHub Copilot CLI: The Complete Wiki

GitHub's coding agent in your terminal. The `copilot` binary can chat, read and edit files, run shell commands, search the codebase, plan and execute multi-step work, talk to MCP servers, and delegate tasks to GitHub's cloud coding agent — all behind a permission system you control.

> Sourced from <https://docs.github.com/en/copilot> (Copilot CLI sections) and the CLI's own `copilot help` topics. Reference build: **1.0.65**.

Each page is self-contained — read what you need.

---

## The mental model

Copilot CLI layers extensibility on top of one agentic loop. Roughly, from foundation to composition:

```
  Plugins ............ bundle agents + skills + hooks + MCP + LSP for distribution
  Hooks .............. event-driven logic around the agent
  Permissions ........ gate tools / paths / URLs (deny beats allow)
  MCP servers ........ external tools & data (built-in github-mcp-server + your own)
  Custom agents ...... reusable personas (.agent.md: instructions + tools + model + MCP)
  Skills ............. on-demand callable capabilities (SKILL.md)
  Custom instructions  always-on repo guidance (AGENTS.md, *.instructions.md)
  Modes .............. interactive / plan / autopilot / fleet / delegate
  Models ............. GitHub-routed catalog, or BYOK custom providers
  CLI / REPL ......... the copilot binary, sessions, config
```

The single switch that matters most for scripting: **`--allow-all-tools`** (or `COPILOT_ALLOW_ALL`) — required for non-interactive `-p` runs.

---

## Files in this wiki

### Start here

| File | What it covers |
|---|---|
| [getting-started.md](getting-started.md) | Install, subscription, auth (incl. headless tokens), first session, terminal setup |
| [cli-reference.md](cli-reference.md) | Every subcommand and every CLI flag |
| [slash-commands.md](slash-commands.md) | All interactive `/` commands |

### Configuration

| File | What it covers |
|---|---|
| [configuration.md](configuration.md) | `settings.json` keys, the `~/.copilot` layout, precedence |
| [environment-variables.md](environment-variables.md) | Every `COPILOT_*` and related env var |
| [logging.md](logging.md) | Log levels and directories, `/diagnose` |

### Models

| File | What it covers |
|---|---|
| [models.md](models.md) | Model catalog, context tier, reasoning effort |
| [providers-byok.md](providers-byok.md) | Custom model providers (OpenAI-compatible, Azure, Anthropic, Ollama) |

### Autonomy & control

| File | What it covers |
|---|---|
| [modes.md](modes.md) | interactive / plan / autopilot, fleet (parallel subagents), delegate to cloud |
| [permissions.md](permissions.md) | Tool / path / URL permission model and patterns |
| [sessions.md](sessions.md) | Resume, context, memory, share, rewind, remote control |

### Extending

| File | What it covers |
|---|---|
| [mcp.md](mcp.md) | MCP config sources, `copilot mcp` subcommands, built-in GitHub MCP toolsets |
| [custom-agents.md](custom-agents.md) | `.agent.md` frontmatter, locations, invocation |
| [custom-instructions.md](custom-instructions.md) | `AGENTS.md`, `copilot-instructions.md`, path-scoped `*.instructions.md` |
| [skills.md](skills.md) | `SKILL.md` skills and the `copilot skill` command |
| [plugins.md](plugins.md) | Bundle everything; marketplaces; install methods |
| [hooks.md](hooks.md) | Event hooks and `disableAllHooks` |

### Operations

| File | What it covers |
|---|---|
| [monitoring.md](monitoring.md) | OpenTelemetry traces and metrics (GenAI conventions) |
| [billing.md](billing.md) | AI credits, usage surfaces, spend controls |
| [cli-vs-api.md](cli-vs-api.md) | When to use the CLI vs a programmatic API |

---

## Quick decision tree

| You want to… | Go to |
|---|---|
| Install and sign in | [getting-started.md](getting-started.md) |
| Find a flag or subcommand | [cli-reference.md](cli-reference.md) |
| Run a `/` command in a session | [slash-commands.md](slash-commands.md) |
| Script it non-interactively | [cli-reference.md](cli-reference.md) + [permissions.md](permissions.md) (`--allow-all-tools`) |
| Use your own model / a local LLM | [providers-byok.md](providers-byok.md) |
| Plan first, then run unattended | [modes.md](modes.md) |
| Lock down what the agent may do | [permissions.md](permissions.md) |
| Tell Copilot about your project | [custom-instructions.md](custom-instructions.md) |
| Build a reusable persona | [custom-agents.md](custom-agents.md) |
| Connect external tools/data | [mcp.md](mcp.md) |
| Ship a toolkit to your team | [plugins.md](plugins.md) |
| See where the credits go | [billing.md](billing.md) |
| Export telemetry to a backend | [monitoring.md](monitoring.md) |

---

## Reference

Official docs: <https://docs.github.com/en/copilot/how-tos/copilot-cli>
Offline help: `copilot help <billing|commands|config|environment|logging|monitoring|permissions|providers>`
