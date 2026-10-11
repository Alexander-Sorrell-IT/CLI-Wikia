# muse subagents

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `--help` flags + MSP hook events + observed delegation lines.

Children run under the parent's session with inherited tool grants;
per-call narrowing only. `SubagentStart` / `SubagentStop` hooks bracket
their lifetime. `--subagent-worktree-isolation` isolates writers (parallel
children must not share a checkout). Agent identities ship in the model
catalog (`workflow-subagent`, `general-purpose`, plugin agents).
Cross-session work uses `session-message send|list`.
Delegation degrades on untrusted workspaces (`auto unavailable`).
