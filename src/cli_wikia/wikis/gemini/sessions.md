# Session management

Gemini CLI saves your conversation history automatically so you can resume work where you left off, review past interactions, and manage history across projects. Sessions are **project-specific**: switching directories switches to that project's history.

---

## Automatic saving

Session history is recorded in the background as you interact, so your work is preserved even if you interrupt a session. Each session stores:

- Your prompts and the model's responses.
- All tool executions (inputs and outputs).
- Token usage statistics (input, output, cached, etc.).
- Assistant thoughts and reasoning summaries (when available).

**Storage location:** `~/.gemini/tmp/<project_hash>/chats/`, where `<project_hash>` is a unique identifier derived from the project's root directory.

---

## Resuming sessions

### From the command line

Use `--resume` (or `-r`) when launching the CLI:

| Command | Effect |
|---|---|
| `gemini --resume` | Resume the most recent session (`latest`) |
| `gemini --resume 1` | Resume by index (see [listing sessions](#listing-sessions)) |
| `gemini --resume a1b2c3d4-…` | Resume by full session UUID |

```bash
gemini --resume
gemini -r 1
gemini --resume a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### From the interactive interface

Inside a running session, use `/resume` to open the **Session Browser**:

```text
/resume
```

In slash completion, `/resume` (and its alias `/chat`) commands are grouped under titled separators:

- `-- auto --` — the session browser (`list` opens it).
- `-- checkpoints --` — manual tagged checkpoint commands.

Unique prefixes such as `/resum` and `/cha` resolve to the same grouped menu.

The Session Browser lets you:

- **Browse** past sessions and **preview** each (date, message count, first prompt).
- **Search** — press `/` then type to filter by ID or content.
- **Select** — press **Enter** to resume.
- **Delete** — press **x** on a session.
- **Exit** — press **Esc**.

### Manual chat checkpoints

For named branch points *inside* a session, use chat checkpoints via `/resume` (or the `/chat` alias):

```text
/resume save decision-point
/resume list
/resume resume decision-point
/resume delete decision-point
```

Compatibility aliases: `/chat …` works for the same commands, and `/resume checkpoints …` remains supported during migration. (A `share` subcommand for sessions/checkpoints should be verified in official docs.)

### Parallel sessions with Git worktrees

To work on multiple tasks at once, give each session its own copy of the codebase with [Git worktrees](./git-worktrees.md), so changes in one session don't collide with another.

---

## Managing sessions

### Listing sessions

```bash
gemini --list-sessions
```

```text
Available sessions for this project (3):

  1. Fix bug in auth (2 days ago) [a1b2c3d4]
  2. Refactor database schema (5 hours ago) [e5f67890]
  3. Update documentation (Just now) [abcd1234]
```

### Deleting sessions

Deleting a session also removes all associated data — implementation plans, task trackers, tool outputs, and activity logs.

**From the command line** (by index or ID):

```bash
gemini --delete-session 2
```

**From the Session Browser:** open it with `/resume`, navigate to the session, and press **x**.

The `/quit --delete` command (deleting the current session on exit) should be verified in official docs.

---

## Configuration

### Session retention

By default Gemini CLI cleans up old session data automatically to keep history from growing indefinitely. The default policy retains sessions for **30 days**.

```json
{
  "general": {
    "sessionRetention": {
      "enabled": true,
      "maxAge": "30d",
      "maxCount": 50
    }
  }
}
```

| Key | Type | Meaning | Default |
|---|---|---|---|
| `enabled` | boolean | Master switch for session cleanup | `true` |
| `maxAge` | string | Keep sessions for this duration (e.g. `"24h"`, `"7d"`, `"4w"`); older ones are deleted | `"30d"` |
| `maxCount` | number | Maximum sessions to retain; oldest beyond this are deleted | unlimited |
| `minRetention` | string | Safety limit — sessions newer than this are never auto-deleted | `"1d"` |

You can also adjust these via the `/settings` command.

### Session limits

Cap the length of individual sessions to keep context windows manageable:

```json
{
  "model": {
    "maxSessionTurns": 100
  }
}
```

- **`maxSessionTurns`** (number) — maximum user/model exchanges in one session; `-1` means unlimited (default). When reached, interactive mode shows a message and stops sending requests (start a new session manually); non-interactive mode exits with an error.

---

## See also

- [checkpointing.md](./checkpointing.md) — automatic snapshots and `/rewind`
- [settings.md](./settings.md) — `general.sessionRetention.*`, `model.maxSessionTurns`
- [commands.md](./commands.md) — `/resume`, `/chat`, `/settings`
- [configuration.md](./configuration.md) — storage under `~/.gemini/tmp/<project_hash>/`
- [cli-reference.md](./cli-reference.md) — `--resume`/`-r`, `--list-sessions`, `--delete-session`
