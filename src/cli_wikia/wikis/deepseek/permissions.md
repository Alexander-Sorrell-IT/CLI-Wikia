# Permissions

Permissions decide what DeepSeek Code may do without asking you. There are two
moving parts: a **permission mode** (the overall posture) and a set of
**allow / ask / deny rules** (per-tool, per-pattern). Together with hooks, this is
the layer that is enforced by the harness rather than suggested to the model.

---

## Permission modes

The `--permission-mode` flag advertises four modes, but the runtime
(`~/.clawspring/permissions.json`) defines **six**. The full set:

| Mode | Behavior |
|------|----------|
| `default` | Standard prompts for each tool use |
| `acceptEdits` | Auto-accept file edits + filesystem ops in the cwd; still prompts for Bash |
| `plan` | Read-only exploration — no edits or commands |
| `auto` | A background classifier reviews each command and auto-approves safe ones within guardrails |
| `dontAsk` | Auto-deny anything not explicitly allowed (allow rules still work) |
| `bypassPermissions` | Skip all permission prompts (full autonomy) |

```bash
deepseek-code --permission-mode plan "outline the change first"
deepseek-code --permission-mode acceptEdits "apply the refactor"
```

The default mode in the shipped config is **`acceptEdits`** (set via `permissionMode`
in the CLI config and `permissions.defaultMode` in Clawspring settings).

Two guardrail switches exist in the settings:

| Setting | Effect |
|---------|--------|
| `disableBypassPermissionsMode` | When `true`, `bypassPermissions` cannot be selected |
| `disableAutoMode` | When `true`, `auto` mode is unavailable |

---

## Allow / ask / deny rules

Rules use the same syntax as Claude Code: `Tool` or `Tool(pattern)`, where the pattern
is a glob (for Bash, matched against the command) or a gitignore-style path (for
Read/Edit). They live in `~/.clawspring/permissions.json` and in the `permissions`
block of `settings.json`.

### Rule syntax examples

| Rule | Matches |
|------|---------|
| `Read` | The Read tool, unconditionally |
| `Bash(git *)` | Any `git` command |
| `Bash(git push *)` | Just `git push …` |
| `Read(**/.env)` | Reading any `.env` file |
| `Read(**/*.pem)` | Reading any PEM file |
| `Agent(researcher)` | Delegating to the `researcher` subagent |
| `Skill(commit)` | Invoking the `commit` skill |

### What the shipped config allows / asks / denies

The default policy is deliberately broad-but-guarded:

- **allow** — common dev tooling and read/write/search tools without prompting:
  `Bash(git *)`, `Bash(npm *)`, `Bash(python *)`, `Bash(pip *)`, `Bash(cargo *)`,
  `Bash(go *)`, `Bash(node *)`, plus safe shell utilities (`cat`, `ls`, `find`,
  `grep`, `mkdir`, `cp`, `mv`, `head`, `tail`, …) and the tool primitives `Read`,
  `Edit`, `Write`, `Glob`, `Grep`, `WebSearch`, `WebFetch`, the `Memory*` and `Task*`
  tools, `Agent`, `Skill`.
- **ask** — operations that change shared state or touch the system:
  `Bash(git push *)`, `Bash(git commit --amend *)`, `Bash(git rebase *)`,
  `Bash(git reset --hard *)`, `Bash(git branch -D *)`, `Bash(docker *)`,
  `Bash(systemctl *)`, `Bash(shutdown *)`, `Bash(reboot *)`, `Bash(kill *)`,
  `Bash(pkill *)`, publish commands, `ssh`/`scp`/`rsync`, mounts.
- **deny** — destructive or secret-exposing operations, blocked outright:
  `Bash(rm -rf /*)`, `Bash(rm -rf ~)`, `Bash(sudo *)`, `Bash(chmod 777 *)`, fork
  bombs, `curl … | sh`, `wget … | sh`, `mkfs.*`, `dd if=*`, `shred *`, writes to
  `/dev/sda`, and reads of `**/.env`, `**/credentials*`, `**/.aws/credentials`,
  `**/id_rsa*`, `**/*.pem`, `**/*.key`, `**/secrets/**`, `**/.git-credentials`,
  `**/.netrc`.

There are also dedicated `agentPermissions` and `skillPermissions` maps — e.g.
`Skill(commit): ask`, `Skill(deploy *): ask`, `Agent(researcher): allow`.

---

## Resolution order

Settings merge across layers (most specific first), then rules are evaluated in a
fixed order for each tool call:

```
Layer precedence:
  1. CLI flags
  2. .clawspring/settings.local.json   (project, local)
  3. .clawspring/settings.json         (project, shared)
  4. ~/.clawspring/settings.json       (global)

Rule merge:
  - allow + allow            = combined allowlist
  - a deny at ANY level      = denied everywhere (cannot be re-allowed)
  - ask rules combine across levels

Per-call check order:
  1. deny rule matches   → DENY immediately
  2. allow rule matches  → ALLOW without prompt
  3. ask rule matches    → ASK the user
  4. otherwise           → ASK (or mode-dependent behavior)
```

The key safety property: **a deny rule is absolute** — no lower-precedence allow can
override it.

---

## Per-tool flags

Beyond rules and modes, two CLI flags adjust the tool surface for a single run:

| Flag | Description |
|------|-------------|
| `--allowed-tools <list>` | Pre-approve these tools (no prompt) |
| `--disallowed-tools <list>` | Remove these tools from the model entirely |

```bash
deepseek-code --allowed-tools "Read,Edit" "fix the bug"
deepseek-code --disallowed-tools "Bash" "review this code without running anything"
```

`--disallowed-tools` is stronger than a deny rule: the tool simply does not exist for
that session.

---

## Bypassing prompts

```bash
deepseek-code --dangerously-skip-permissions "run the whole workflow"
```

This disables every approval prompt for the run. Even so, **deny rules and
`PreToolUse` hooks still fire** — those are the harness-level guards that the bypass
flag does not turn off. Use sparingly; pair with `--max-turns` / `--max-budget-usd`.

---

## How hooks reinforce permissions

Permissions answer "is this allowed?"; hooks can answer "is this allowed *and* does it
pass my custom check?". The shipped `PreToolUse` hooks (`pre-bash.sh`, `pre-write.sh`,
`pre-web.sh`) block fork bombs, secret-file writes, and internal-network fetches even
when the permission layer would allow them. See [hooks.md](hooks.md).

---

## Related

- [hooks.md](hooks.md) — deterministic enforcement, the `PreToolUse` gates
- [configuration.md](configuration.md) — where the `permissions` block lives
- [architecture.md](architecture.md) — the full layer/merge picture
