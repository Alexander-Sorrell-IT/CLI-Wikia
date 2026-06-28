# Sessions (Gemini CLI)

Gemini CLI persists sessions per project, so you can resume, list, and delete
previous conversations.

## Resuming a session

```bash
# Resume the most recent session
gemini --resume latest

# Resume by index number
gemini --resume 5
```

| Flag | Description |
|------|-------------|
| `-r, --resume` | Resume a previous session. Use `latest` for most recent or an index number (e.g. `--resume 5`) |

## Listing sessions

List available sessions for the current project and exit:

```bash
gemini --list-sessions
```

| Flag | Description |
|------|-------------|
| `--list-sessions` | List available sessions for the current project and exit |

## Deleting a session

Delete a session by its index number:

```bash
gemini --delete-session 5
```

| Flag | Description |
|------|-------------|
| `--delete-session` | Delete a session by index number |

## Tips

- Use `--list-sessions` to find the index of a session before resuming or
  deleting it.
- `--resume latest` is the quickest way to continue where you left off.

> Verify exact values in the official docs / run `gemini --help`.
