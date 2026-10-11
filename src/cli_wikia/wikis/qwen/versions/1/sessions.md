# qwen sessions

> wiki-version: 1 | cli-version: 0.24.7 | verified: 2026-10-10
> source: `qwen --help` + observed `~/.qwen/sessions/`.

## Lifecycle

- One-shot: `qwen "{prompt}"` (positional; default mode).
- Interactive continue: `qwen -i "{prompt}"`.
- History: `--chat-recording` persists chat to disk; without it,
  `--continue/--resume` cannot work.
- Session stores: `~/.qwen/sessions/`, `~/.qwen/projects/`.

## Fleet notes

Headless argv: `["qwen", "-y", "{prompt}"]` (positional prompt + yolo).
Requires `OPENAI_API_KEY` (or provider envKey) to be SET even for local
servers, else the run cancels. Mailbox injection rides `UserPromptSubmit`.
Worktrees (`--worktree`) land under `<repo>/.qwen/worktrees/<slug>/`.
