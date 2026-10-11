# muse worktrees

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `--help` + binary strings (`.muse/worktrees`).

`--worktree off|create|existing` isolates the session in a git worktree
(`.muse/worktrees/`). `--subagent-worktree-isolation` extends isolation to
child agents (parallel writers must never share a checkout). Fleet teams
map naturally onto one worktree per agent.
