# Agent Modes (GitHub Copilot CLI)

GitHub Copilot CLI can start in different agent modes that control how much it
plans versus acts.

## Setting the mode

```bash
copilot --mode plan -i "outline the refactor"
```

| Flag | Values | Description |
|------|--------|-------------|
| `--mode <mode>` | `interactive`, `plan`, `autopilot` | Initial agent mode |

There are also dedicated shortcut flags:

| Flag | Equivalent |
|------|------------|
| `--plan` | Start in plan mode |
| `--autopilot` | Start in autopilot mode |

## The modes

| Mode | Description |
|------|-------------|
| `interactive` | Standard interactive session — Copilot asks before acting |
| `plan` | Plan mode — focuses on producing a plan |
| `autopilot` | Autopilot mode — runs more autonomously |

```bash
# Plan first
copilot --plan -i "design the migration"

# Autopilot
copilot --autopilot -p "implement the migration"
```

## Combining with permissions

Autopilot and non-interactive runs usually need broader permissions. Recall
that `--allow-all-tools` (or `COPILOT_ALLOW_ALL`) is required for
non-interactive mode. See [permissions.md](permissions.md).

```bash
copilot --autopilot --allow-all -p "build and test the project"
```

## Related

- `--no-ask-user` makes a session more autonomous by disabling the
  `ask_user` tool — see [permissions.md](permissions.md).

> Verify exact values in the official docs / run `copilot --help`.
