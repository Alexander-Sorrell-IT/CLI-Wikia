# Permissions (DeepSeek Code)

DeepSeek Code controls how much it can do without asking via a permission mode,
plus tool allow/deny lists.

## Permission modes

```bash
deepseek-code --permission-mode plan "outline the change first"
```

| Mode | Description |
|------|-------------|
| `default` | Prompt for approval before actions |
| `acceptEdits` | Auto-accept edit actions |
| `plan` | Plan-only mode |
| `auto` | Automatic mode |

The default permission mode can also be set in the config file via
`permissionMode` (see [configuration.md](configuration.md)).

## Tool allow / deny lists

| Flag | Description |
|------|-------------|
| `--allowed-tools <list>` | Tools allowed without prompting |
| `--disallowed-tools <list>` | Tools removed from the model |

```bash
deepseek-code --allowed-tools "Read,Edit" "fix the bug"
deepseek-code --disallowed-tools "Bash" "review this code"
```

## Bypassing prompts

```bash
deepseek-code --dangerously-skip-permissions "run the whole workflow"
```

| Flag | Description |
|------|-------------|
| `--dangerously-skip-permissions` | Bypass all permission prompts |

> Use `--dangerously-skip-permissions` with caution — it disables all
> approval prompts.

## Related

- Output limits like `--max-turns` and `--max-budget-usd` can bound an
  autonomous run — see [cli-reference.md](cli-reference.md).

> Verify exact values in the official docs / run `deepseek-code --help`.
