# Sessions, Memory & Remote Control

Every Copilot CLI conversation is a **session** with an ID, saved to disk so you can resume, rename, share, rewind, or drive it from elsewhere.

---

## Resuming

| Command | Effect |
|---|---|
| `copilot --continue` | Resume the most recent session |
| `copilot --resume` | Open a session picker |
| `copilot --resume=<value>` | Resume by session ID, task ID, ID prefix (7+ hex), or exact name |
| `copilot --session-id=<id>` | Resume by ID, or set the UUID for a **new** session |
| `copilot --name="my feature"` | Name a new session (resume later with `--resume="my feature"`) |

```bash
copilot --allow-all-tools --resume          # resume last, auto-approving
copilot --resume=0cb916d                     # by ID prefix
```

Inside a session: `/resume` (switch), `/rename` (rename or auto-name), `/new` (start fresh), `/session` (manage), `/clear` (abandon and restart), `/restart` (restart preserving the session).

Sessions persist under `~/.copilot/session-state/` and `~/.copilot/session-store.db`.

---

## Context management

Long sessions fill the model's context window. Tools to manage it:

| Command | Effect |
|---|---|
| `/context` | Show context-window token usage, broken down by system prompt, tools, and messages |
| `/compact [focus]` | Summarize history to reclaim space (optionally focused on a topic) |
| `/usage` | Session usage metrics and token breakdown |

---

## Memory

Beyond a single session, Copilot can keep **cross-session memory** — durable facts it recalls later. It's controlled by the `memory` setting (default `true`) and stored in `~/.copilot/memories/`.

| How | Effect |
|---|---|
| `/memory` | Show status, or enable/disable memory |
| `--enable-memory` | Enable memory in **prompt mode** (it's off by default for `-p` runs) |

---

## Sharing & exporting

| Command / flag | Effect |
|---|---|
| `/share` | Save the session (or a research report) to markdown, HTML, or a GitHub gist |
| `/copy` | Copy the last response to the clipboard |
| `--share[=path]` | After a non-interactive run, write markdown (default `./copilot-session-<id>.md`) |
| `--share-gist` | After a non-interactive run, write a secret GitHub gist |

---

## Rewind

Made a mess? `/rewind` (alias `/undo`) rewinds the last turn **and reverts the file changes** it made — handy for backing out an edit the agent got wrong.

---

## Remote control from web & mobile

You can bridge a local session to GitHub's web and mobile apps:

| Flag / command | Effect |
|---|---|
| `--remote` / `/remote` | Allow GitHub web and mobile to **control** this local session |
| `--remote-export` | **Export** the session read-only (view, no control) |
| `--no-remote` / `--no-remote-export` | Disable control / disable export (also disables control) |
| `--connect[=sessionId]` | Attach directly to a remote session or task |

This is distinct from `/delegate`, which hands the whole task to GitHub's cloud coding agent to finish and open a PR (see [modes.md](modes.md)).

---

## Keeping the machine awake

`/keep-alive [on|off|busy|<duration>]` (or the `keepAlive` setting) prevents the system from sleeping while a session runs — `busy` keeps it awake only while the agent is actively working.

---

## See also

- [modes.md](modes.md) — delegate, autopilot, fleet
- [slash-commands.md](slash-commands.md) — every session command
- [billing.md](billing.md) — usage shown on exit
