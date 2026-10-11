# muse permissions

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: MSP schema + `--help` + launcher env.

## Profiles and toolsets

`--permission-profile <ID>` selects a named profile. The toolset domain
(`AgentToolsetName`) includes `shell_ro`, `shell_rw`, `read`, `edit`,
`full`, `plan`, `explore`, `apply_patch`, `browser`, `memory_lite`,
`memory_full`, `notes`, `unstable_subagents`. `PermissionGate` /
`PermissionGateDecision` enforce per-tool; `ToolPermissionRequirements` and
`ToolPermissionSpec` declare what each tool needs.

## Sandbox and workspace

`muse sandbox` checks/sets up the OS sandbox (Linux: Bubblewrap, needs
user namespaces). `--workspace <PATH>` roots policy-gated tools;
`--allow-workspace-switch` permits leaving it. `--worktree
off|create|existing` isolates the session in a git worktree
(`.muse/worktrees/`); `--subagent-worktree-isolation` extends that to
children. Untrusted workspaces degrade: delegation auto → unavailable,
approval judge → never, project plugins blocked.

## Secrets and redaction

`--secret-redaction strict|relaxed|off` (default strict),
`--redact-tools <names>` (repeatable), `--api-key-stdin` (never argv).
`--tls-ca` / `--tls-insecure` (lab only) control transport trust.
