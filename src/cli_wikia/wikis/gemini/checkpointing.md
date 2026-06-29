# Checkpointing & Rewind

Gemini CLI can automatically snapshot your project before the model modifies any files, so you can instantly revert to the state before a tool ran. Two related features cover this:

- **Checkpointing** — automatic, per-modification snapshots you restore with `/restore`.
- **Rewind** — an interactive way to jump back to an earlier point in the conversation and optionally undo the file changes made since.

---

## Checkpointing

When you approve a tool that modifies the filesystem (such as `write_file` or `replace`), the CLI automatically creates a **checkpoint** capturing three things:

1. **A Git snapshot** — a commit in a separate *shadow* Git repository at `~/.gemini/history/<project_hash>`. It captures the full state of your project files at that moment and does **not** interfere with your own project's Git repo.
2. **Conversation history** — the entire conversation up to that point.
3. **The tool call** — the specific call that was about to execute.

Restoring a checkpoint reverts all project files to the snapshot, restores the conversation history, and re-proposes the original tool call so you can run it again, modify it, or ignore it.

### Storage locations

| Data | Location |
|---|---|
| Git snapshot | `~/.gemini/history/<project_hash>` (shadow repo) |
| Conversation history + tool calls | `~/.gemini/tmp/<project_hash>/checkpoints` (JSON) |

All checkpoint data is stored locally on your machine.

### Enabling checkpointing

Checkpointing is **disabled by default**. Enable it in `settings.json`:

```json
{
  "general": {
    "checkpointing": {
      "enabled": true
    }
  }
}
```

> The `--checkpointing` command-line flag was **removed in v0.11.0**. Checkpointing can now only be enabled through `settings.json`.

### Using `/restore`

Once enabled, checkpoints are created automatically. Manage them with `/restore`.

List all checkpoints for the current project:

```
/restore
```

Checkpoint file names combine a timestamp, the modified file, and the tool, e.g. `2025-06-22T10-00-00_000Z-my-file.txt-write_file`.

Restore a specific checkpoint by passing its file name (also shown in docs as `/restore [tool_call_id]`):

```
/restore 2025-06-22T10-00-00_000Z-my-file.txt-write_file
```

Your files and conversation are immediately restored to the checkpoint's state, and the original tool prompt reappears.

---

## Rewind

`/rewind` lets you go back to a previous point in the conversation and, optionally, revert any file changes the AI made during those interactions — useful for undoing mistakes, exploring alternatives, or cleaning up session history.

### Triggering rewind

- Type `/rewind` and press **Enter**, or
- Press **`Esc` twice**.

### Interface

An interactive list of your previous interactions appears (most recent at the bottom). Navigate with the **Up/Down arrows**; each entry previews the user prompt and the number of files changed at that step. Press **Enter** on the target interaction, then choose an action:

| Option | Effect |
|---|---|
| Rewind conversation and revert code changes | Reverts **both** chat history and file modifications to before the selected interaction |
| Rewind conversation | Reverts **only** the chat history; file changes are kept |
| Revert code changes | Reverts **only** the file modifications; chat history is kept |
| Do nothing (`Esc`) | Cancels the rewind |

If no code changes were made since the selected point, the code-reverting options are hidden.

### Key considerations

- **Destructive:** rewinding permanently changes your session history and possibly your files — use with care.
- **Agent awareness:** rewinding the conversation makes the model lose all memory of the removed interactions. If you *only* revert code, you may need to tell the model the files changed.
- **Scope:** rewind only affects file changes made by the AI's edit tools. It does **not** undo your manual edits or changes from the shell tool (`!`).
- **Compression:** rewind works across chat compression points by reconstructing history from stored session data.

---

## See also

- [sessions.md](./sessions.md) — session saving, `/resume`, and retention
- [permissions.md](./permissions.md) — approval modes that gate the modifying tools
- [settings.md](./settings.md) — `general.checkpointing.enabled`
- [commands.md](./commands.md) — `/restore`, `/rewind`
- [configuration.md](./configuration.md) — storage paths under `~/.gemini`
