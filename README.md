# CLI Wikia

An **offline, pip-installable reference wiki** for AI coding CLIs —
Claude Code, DeepSeek, GitHub Copilot, ChatGPT/OpenAI, and Gemini —
with a single command to browse, search, read and edit the docs.

It's more than a wiki: the bundled docs can also be used as **grounding
context for a local model** (`wikia ask`), so the same content works as a
reference *and* as a knowledge base you fully control and can edit.

## Install

```bash
pip install cli-wikia
```

## Usage

```bash
wikia models                       # list models + topic counts
wikia list claude                  # list Claude topics
wikia read claude hooks            # print a topic
wikia search "permission"          # search across all models
wikia search "mcp" --model claude  # search one model
wikia path claude                  # show where the files live (to edit them)
wikia ask claude "how do hooks work?"   # answer from the docs via a local model
```

## How it's organized

```
src/cli_wikia/wikis/
├── claude/     # populated (Claude Code docs)
├── deepseek/   # skeleton
├── copilot/    # skeleton
├── chatgpt/    # skeleton
└── gemini/     # skeleton
```

Each topic is a plain Markdown file. Add or edit files in a model's folder
and reinstall (`pip install -e .`) to update your local copy. Because the
repo is git-backed, **every revision of every doc is kept** in history.

## Status

- **Claude** wiki is fully populated.
- DeepSeek / Copilot / ChatGPT / Gemini are skeletons to be filled from each
  tool's CLI (you have `deepseek-code`, `copilot`, `gemini`, `ollama`
  installed) or official documentation.

## License

MIT — see [LICENSE](LICENSE).
