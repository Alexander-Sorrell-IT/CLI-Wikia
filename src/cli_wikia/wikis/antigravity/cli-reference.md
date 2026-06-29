# Antigravity (`agy`) CLI Reference

Complete reference for the `agy` command, derived from `agy --help`
(version 1.0.12).

## Usage

```
agy [options]
agy <subcommand> [arguments]
```

`agy` launches an interactive agentic session by default. Use `-p`/`--print`
for one-shot, non-interactive runs.

## Options

| Option | Description |
|--------|-------------|
| `--add-dir <dir>` | Add a directory to the workspace (repeatable) |
| `-c`, `--continue` | Continue the most recent conversation |
| `--conversation <id>` | Resume a previous conversation by ID |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests without prompting |
| `-i`, `--prompt-interactive <prompt>` | Run an initial prompt, then continue interactively |
| `--log-file <path>` | Override the CLI log file path |
| `--model <model>` | Model for the current CLI session |
| `--new-project` | Create a new project for this session |
| `-p`, `--print` / `--prompt <text>` | Run a single prompt non-interactively and print the response |
| `--print-timeout <dur>` | Timeout for print-mode wait (default `5m0s`) |
| `--project <id>` | Project ID for the current CLI session |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled |

## Subcommands

| Command | Purpose |
|---------|---------|
| `agy changelog` | Show changelog and release notes |
| `agy help` | Show help for subcommands |
| `agy install` | Configure environment paths and shell settings |
| `agy models` | List available models — see [models.md](./models.md) |
| `agy plugin` (alias `plugins`) | Manage plugins — see [plugins.md](./plugins.md) |
| `agy update` | Update the CLI |

## Examples

```bash
# one-shot with a chosen model
agy --model "Gemini 3.1 Pro (High)" -p "review main.go for races"

# interactive, scoped to extra directories, in a sandbox
agy --add-dir ../shared --sandbox -i "start a refactor of the auth module"

# resume work
agy -c
agy --conversation <id>
```

> Verified from `agy --help`. The `--dangerously-skip-permissions` flag bypasses
> all approval prompts — use with care.
