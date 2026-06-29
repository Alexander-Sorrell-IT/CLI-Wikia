# Configuration & Sessions (Antigravity)

## First-time setup

```bash
agy install     # configure environment paths and shell settings
```

## Projects

Antigravity organizes work into **projects**:

| Flag | Description |
|------|-------------|
| `--new-project` | Create a new project for this session |
| `--project <id>` | Use a specific project ID for the session |

```bash
agy --new-project -i "scaffold a FastAPI service"
agy --project <id> -p "add tests for the user module"
```

## Sessions / conversations

| Flag | Description |
|------|-------------|
| `-c`, `--continue` | Continue the most recent conversation |
| `--conversation <id>` | Resume a specific conversation by ID |

## Workspace & sandbox

| Flag | Description |
|------|-------------|
| `--add-dir <dir>` | Add a directory to the workspace (repeatable) |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled |

## Permissions

By default Antigravity prompts before running tools. To auto-approve everything
(risky):

```bash
agy --dangerously-skip-permissions -p "..."
```

## Logging & timeouts

| Flag | Description |
|------|-------------|
| `--log-file <path>` | Override the CLI log file path |
| `--print-timeout <dur>` | Timeout for print-mode wait (default `5m0s`) |

## Updates

```bash
agy update         # update the CLI
agy changelog      # see what changed
```

> Verified from `agy --help` (v1.0.12).
