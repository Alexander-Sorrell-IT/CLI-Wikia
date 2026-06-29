# Google Antigravity (`agy`) Wiki

Reference for **Google Antigravity** — Google's agentic coding CLI, invoked as
`agy`. Documented against **v1.0.12**.

> **Why this exists alongside the Gemini CLI wiki:** Antigravity is Google's
> newer, long-term agentic tool. Google is steering toward Antigravity and
> winding down investment in the older Gemini CLI, so both are documented here
> during the transition. See the [gemini](../gemini/README.md) wiki for the
> older tool.

## Quick start

```bash
agy                          # interactive agentic session
agy -p "explain this repo"   # one-shot, print the response and exit
agy -c                       # continue the most recent conversation
agy models                   # list available models
```

## Topics

| File | What it covers |
|------|----------------|
| [cli-reference.md](./cli-reference.md) | All flags and subcommands |
| [models.md](./models.md) | Available models (`agy models`) |
| [plugins.md](./plugins.md) | Plugin system, importing from gemini/claude |
| [configuration.md](./configuration.md) | Projects, sessions, sandbox, logs |

> Verified from `agy --help` and `agy models` (v1.0.12). Run `agy help` and
> `agy <subcommand> help` for the latest.
