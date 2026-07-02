# CLI Wikia

An **offline, pip-installable reference wiki** for AI coding CLIs —
Claude Code, DeepSeek, GitHub Copilot, ChatGPT/OpenAI, Gemini, and
Google Antigravity — with a single command to browse, search, read and
edit the docs.

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
├── claude/       # populated (Claude Code docs)
├── deepseek/     # skeleton
├── copilot/      # skeleton
├── chatgpt/      # skeleton
├── gemini/       # skeleton
└── antigravity/  # skeleton
```

Each topic is a plain Markdown file. Add or edit files in a model's folder
and reinstall (`pip install -e .`) to update your local copy. Because the
repo is git-backed, **every revision of every doc is kept** in history.

## Status

- **Claude** wiki is fully populated.
- DeepSeek / Copilot / ChatGPT / Gemini / Antigravity are skeletons to be
  filled from each tool's CLI or official documentation.

## Keeping the docs fresh, hooks, and scheduling

```bash
# update — diff each model's sources (--help/--version, official docs, and the
# model's own self-report) against the last snapshot; --write accepts a new baseline
wikia update gemini
wikia update --all --write

# hooks — integrate the wiki into a tool
wikia hooks status                 # per-model integration status
wikia hooks enable claude --write  # Level 1: awareness block in the instructions file
wikia hooks manifest claude        # Level 2: generate an editable hook manifest
wikia hooks apply claude --write   # merge the manifest into the tool's settings
                                   # (existing hooks are preserved; a .bak-cli-wikia
                                   # backup is written first)
wikia hooks remove claude --write  # remove exactly the hooks apply installed

# schedule — auto-run `wikia update --all` on a systemd user timer
wikia schedule config --write      # create the config (interval, upgrade, enabled)
wikia schedule apply --write       # install/remove the timer to match the config
wikia schedule status
```

All mutating commands are dry-run by default; pass `--write` to apply.

## License

MIT — see [LICENSE](LICENSE).
