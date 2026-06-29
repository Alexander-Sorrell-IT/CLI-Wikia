# Antigravity Python SDK

Beyond the interactive CLI, Antigravity exposes a **public Python SDK** for
spawning, configuring, and orchestrating agents programmatically — inside
scripts, data pipelines, CI/CD, or automated test suites. The agent primitives
(code execution, file management, web browsing, reasoning, subagents) run in
Google's secure Linux sandbox.

- Package: **`google-antigravity`** on PyPI
- Source: <https://github.com/google-antigravity/antigravity-sdk-python>

---

## Installation

```sh
pip install google-antigravity
```

> The SDK relies on a compiled runtime binary shipped inside the platform-specific
> PyPI wheels. Always install via `pip` so you get the correct binary for your OS.

---

## Quickstart

The `Agent` class manages the full lifecycle — binary discovery, tool wiring,
hook registration, and policy defaults — behind a single async context manager.
By default an agent runs **read-only** for safety; pass a `CapabilitiesConfig`
to enable write tools (`run_command`, `edit_file`, …).

```python
import asyncio
import sys
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

async def main():
    config = LocalAgentConfig(
        system_instructions="You are an expert assistant for codebase navigation.",
        capabilities=CapabilitiesConfig(),   # enable write tools
    )

    async with Agent(config) as agent:
        response = await agent.chat("Write a short python script to list files.")

        # stream response tokens as they arrive
        async for token in response:
            sys.stdout.write(token)
            sys.stdout.flush()
        print()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Core types

| Type | Role |
|------|------|
| `Agent` | Async context manager that owns an agent's lifecycle |
| `LocalAgentConfig` | Agent configuration: `system_instructions`, `capabilities`, … |
| `CapabilitiesConfig` | Which tools the agent may use; omit for read-only |

`agent.chat(...)` returns a response object **immediately** (non-blocking) that
you iterate to stream output.

---

## Streaming thoughts & tool calls

For agentic workflows you can observe the agent's internal reasoning and
intercept its tool executions:

```python
# stream reasoning / thinking deltas
async for thought in response.thoughts:
    print(f"[Thinking] {thought}")

# stream strongly-typed tool-call events
async for call in response.tool_calls:
    print(f"[Executing Tool] {call.name} with args: {call.args}")
```

---

## Interactive loop helper

Spin up a terminal chat loop against an agent in a few lines:

```python
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
from google.antigravity.utils.interactive import run_interactive_loop

config = LocalAgentConfig(capabilities=CapabilitiesConfig())
async with Agent(config) as agent:
    await run_interactive_loop(agent)
```

---

## When to use the SDK vs the CLI

| | SDK | CLI (`agy`) |
|--|-----|-------------|
| Driver | Your Python code | A person at a terminal |
| Best for | Pipelines, tests, custom orchestration, embedding agents | Interactive coding, one-shot `-p` runs |
| Output | Python objects / streamed tokens | TUI chat, edits, artifacts |

> The examples above come from Antigravity's bundled SDK reference. For the full
> API surface (orchestration APIs, custom tool exposure, hook registration),
> see the GitHub repo and `https://antigravity.google/docs`.

---

## See also

- [cli-vs-api.md](./cli-vs-api.md) — `agy`/SDK vs the underlying model APIs
- [agentic-model.md](./agentic-model.md) — the agent loop the SDK drives
