# Git Worktrees (experimental 🔬)

When you're juggling several tasks at once, Git worktrees give each Gemini CLI
session its own working directory and branch while sharing the same repository
history — so changes in one session never collide with another. This is an
experimental feature under active development.

> Available in newer releases than the installed v0.22.4. Verify availability
> with `gemini --help`.

---

## Enable it

Worktrees are gated behind a setting. Turn it on via `/settings` ("Enable Git
Worktrees") or in [settings.json](./settings.md):

```json
{
  "experimental": {
    "worktrees": true
  }
}
```

## Create and enter a worktree

Use `--worktree` (`-w`). The name you pass becomes both the directory (under
`.gemini/worktrees/`) and the branch name:

```bash
gemini --worktree feature-search   # named worktree + branch
gemini --worktree                  # random name, e.g. worktree-a1b2c3d4
```

> Initialize each new worktree for your stack (e.g. `npm install`, create a
> virtualenv, run your build) — a fresh worktree is a clean checkout.

## Exit and resume

Exiting (`/quit` or Ctrl+C) **leaves the worktree intact** — uncommitted
changes, staged files, untracked files, and new commits are all preserved.
Gemini never auto-deletes a worktree or branch; cleanup is up to you. On exit it
prints instructions for resuming or removing the worktree.

Resume by navigating into the worktree and passing the session ID:

```bash
cd .gemini/worktrees/feature-search
gemini --resume <session_id>
```

## Manage worktrees manually

```bash
# Remove a preserved worktree and its branch
git worktree remove .gemini/worktrees/feature-search --force
git branch -D worktree-feature-search

# Create a worktree yourself, then start Gemini in it
git worktree add ../project-feature-search -b feature-search
cd ../project-feature-search && gemini
```

See the [official git-worktree docs](https://git-scm.com/docs/git-worktree) for
the underlying Git mechanics.

---

## See also

- [sessions.md](./sessions.md) — resuming and managing sessions
- [cli-reference.md](./cli-reference.md) — the `-w/--worktree` flag
- [settings.md](./settings.md) — `experimental.worktrees`
