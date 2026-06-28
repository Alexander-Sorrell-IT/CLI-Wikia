# Sessions, Agents, Skills & Hooks (DeepSeek Code)

DeepSeek Code persists sessions and supports configurable agents, skills, and
hooks. This page covers their listing subcommands and related flags.

## Sessions

### Listing sessions

```bash
deepseek-code sessions
```

### Starting, continuing, and resuming

| Action | Command |
|--------|---------|
| New REPL | `deepseek-code` |
| New REPL with prompt | `deepseek-code "query"` |
| Continue most recent | `deepseek-code -c` |
| Resume specific session | `deepseek-code -r <id> "query"` |

### Session flags

| Flag | Description |
|------|-------------|
| `--name, -n <name>` | Set display name for session |
| `--continue, -c` | Resume most recent session in cwd |
| `--resume, -r <id>` | Resume specific session |
| `--print, -p [query]` | Print mode — non-interactive |
| `--session-id <uuid>` | Use a specific session ID |

Session persistence is controlled by the `sessionPersistence` config field —
see [configuration.md](configuration.md).

## Agents

List configured agents:

```bash
deepseek-code agents
```

Run or define agents at launch:

| Flag | Description |
|------|-------------|
| `--agent <name>` | Run the main thread as a named agent |
| `--agents <json>` | Define subagents from JSON |

## Skills

List available skills:

```bash
deepseek-code skills
```

## Hooks

List configured hooks:

```bash
deepseek-code hooks
```

## Skipping discovery

To skip discovery of hooks, skills, plugins, and `CLAUDE.md`:

```bash
deepseek-code --bare "just answer directly"
```

| Flag | Description |
|------|-------------|
| `--bare` | Skip discovery (hooks, skills, plugins, CLAUDE.md) |

> Verify exact values in the official docs / run `deepseek-code --help`.
