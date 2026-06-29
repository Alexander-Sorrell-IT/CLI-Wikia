# Codex Approvals & Sandboxing

Codex's safety comes from **two independent layers** that combine. From OpenAI's [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security) and [Sandboxing](https://developers.openai.com/codex/concepts/sandboxing) docs.

> **Not locally verified** — Codex isn't installed here. Re-confirm preset mappings with `codex --help` and `/approvals` / `/permissions` after installing.

```
  Sandbox mode  →  WHAT Codex can technically do   (filesystem + network boundary)
  Approval policy → WHEN Codex must STOP and ask you (before crossing the boundary)
```

You can set both together for a session via flags (`--sandbox`, `--ask-for-approval`), config (`sandbox_mode`, `approval_policy`), or the `/approvals` and `/permissions` slash commands.

---

## Sandbox modes

The sandbox applies to **spawned commands too**, not just Codex's built-in file edits — so `git`, `npm`, `pip`, etc. inherit the boundary.

| Mode | Filesystem | Commands | Network |
|---|---|---|---|
| **`read-only`** | Read anywhere; **no writes** | Must be approved | Blocked |
| **`workspace-write`** | Read anywhere; **write inside the workspace** (+ `writable_roots`) | Routine local commands run inside the boundary | Off by default (`network_access`) |
| **`danger-full-access`** | Unrestricted | Unrestricted | Unrestricted |

> Even in writable modes, **protected paths stay read-only**: `.git`, `.agents`, `.codex`. This stops the agent from rewriting git history or its own config.

Extend the workspace boundary in config:

```toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true                    # allow outbound network
writable_roots = ["/tmp/build", "~/.cache/codex"]
```

### Enforcement mechanisms by OS

| Platform | Mechanism |
|---|---|
| macOS | Built-in **Seatbelt** sandbox |
| Linux / WSL2 | **bubblewrap** (`bwrap`) using user namespaces; falls back to a bundled helper needing unprivileged user namespaces. Ubuntu 25.04+ ships the needed AppArmor profile automatically |
| Windows | Native Windows sandbox in PowerShell; WSL2 uses the Linux path |

Codex searches `PATH` for `bwrap`. You can also run an arbitrary command inside the sandbox with `codex sandbox <cmd>`.

---

## Approval policies

| Policy | Behavior |
|---|---|
| **`untrusted`** | Auto-runs known-safe read operations; **asks** before any state-mutating or external command |
| **`on-request`** | Codex works inside the sandbox autonomously and **asks when it needs to escalate** (write outside the workspace, hit the network, etc.) |
| **`never`** | **Never prompts.** Codex operates strictly within sandbox limits; anything it can't do, it simply doesn't |
| **`granular`** | Independently toggle each approval category (see below) |

### Granular policy

```toml
approval_policy = { granular = {
  sandbox_approval    = true,   # escalations out of the sandbox
  rules               = true,   # execpolicy rule matches
  mcp_elicitations    = true,   # MCP server prompts
  request_permissions = false,  # permission-grant requests
  skill_approval      = false   # skill scripts
} }
```

### Auto-review

```toml
approvals_reviewer = "auto_review"
```

Routes eligible approval requests through an automatic reviewer agent. It only evaluates actions that already need approval; low/medium-risk actions can proceed when the policy allows them.

---

## Preset combinations

The TUI and flags expose these as friendly presets:

| Preset | Equivalent flags | What it means |
|---|---|---|
| **Auto** (default) | `--sandbox workspace-write --ask-for-approval on-request` | Reads files, makes edits, and runs commands in the workspace; asks to edit outside it or use the network |
| **Read Only** | `--sandbox read-only --ask-for-approval on-request` | Reads and answers questions; asks before any edit, command, or network access |
| **Read-Only CI** | `--sandbox read-only --ask-for-approval never` | Read-only with no prompts — for non-interactive/CI |
| **Full Auto** | `--full-auto` | Workspace-write with low-friction approvals — hands-off local work |
| **Full Access** | `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`) | **No sandbox, no approvals.** Highest risk |

The two "endpoints":

```bash
# Safest interactive: read, but ask before doing anything
codex --sandbox read-only --ask-for-approval on-request

# Most permissive: only in a disposable/isolated container
codex --yolo
```

Equivalent in config — full access:

```toml
sandbox_mode = "danger-full-access"
approval_policy = "never"
```

---

## Choosing a setup

| Situation | Sandbox | Approval |
|---|---|---|
| Exploring an unfamiliar repo | `read-only` | `on-request` |
| Normal local development | `workspace-write` | `on-request` (the **Auto** default) |
| Trusted hands-off task on local code | `workspace-write` | `never` (or `--full-auto`) |
| CI read-only analysis | `read-only` | `never` |
| Throwaway container, max autonomy | `danger-full-access` | `never` / `--yolo` |

---

## Security notes

- Network filtering / escalation gates are a boundary, not a guarantee — review what you grant via `writable_roots` and `network_access`.
- `danger-full-access` and `--yolo` remove all protection; reserve them for sandboxed/disposable environments where prompt-injection can't reach anything valuable.
- Protected paths (`.git`, `.agents`, `.codex`) remain read-only even in writable modes — don't rely on this as your only safeguard.

---

## See also

- [codex-config.md](./codex-config.md) — `sandbox_mode`, `approval_policy`, `sandbox_workspace_write.*` keys
- [codex-cli-reference.md](./codex-cli-reference.md) — `--sandbox`, `--ask-for-approval`, `--full-auto`, `--yolo`
- [codex-exec.md](./codex-exec.md) — how approvals behave in non-interactive runs
