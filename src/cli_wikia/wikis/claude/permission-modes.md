# Permission Modes

Permission mode controls *how often Claude pauses to ask before doing something*. Six modes total; switch with `Shift+Tab` in the CLI, the mode indicator in VS Code, or `/config` / `--permission-mode`.

---

## The six modes

| Mode | What runs without asking | Best for |
|---|---|---|
| `default` | Reads only | Sensitive work, getting started |
| [`acceptEdits`](#acceptedits) | Reads, file edits, common filesystem cmds (`mkdir`, `touch`, `mv`, `cp`, `rm`, `rmdir`, `sed`) | Iterating on code you're reviewing |
| [`plan`](#plan) | Reads only — Claude proposes a plan, never edits | Exploring a codebase before changing it |
| [`auto`](#auto) | Everything — with background safety checks via classifier | Long autonomous tasks |
| [`dontAsk`](#dontask) | Only pre-approved tools; everything else auto-denied | Locked-down CI |
| [`bypassPermissions`](#bypasspermissions) | Everything except [protected paths](#protected-paths) | Isolated containers/VMs only |

The current mode appears in the status bar.

---

## How to switch

| Where | How |
|---|---|
| CLI | `Shift+Tab` to cycle `default → acceptEdits → plan` (and `auto` / `bypassPermissions` if enabled) |
| CLI startup | `--permission-mode <mode>` |
| Persistent default | `permissions.defaultMode` in [settings.json](./settings.md) |
| VS Code | Mode indicator at bottom of prompt box |
| Web / mobile | Dropdown next to prompt — modes available depend on cloud vs Remote Control |

---

## acceptEdits

Auto-approves file edits and these Bash commands within your working dir or `additionalDirectories`:

```
mkdir, touch, rm, rmdir, mv, cp, sed
```

Also auto-approves them when prefixed by safe env vars (`LANG=C`, `NO_COLOR=1`) or wrappers (`timeout`, `nice`, `nohup`).

Writes to [protected paths](#protected-paths) and other Bash commands still prompt.

```bash
claude --permission-mode acceptEdits
```

---

## plan

Claude *researches and proposes* changes without making them. Reads files, runs shell commands to explore, writes a plan — but never edits source.

Enter with `Shift+Tab` or `--permission-mode plan`. Prefix one prompt with `/plan` to use it for a single message.

When the plan is ready, Claude asks how to proceed. From the prompt you can:
- Approve and start in `auto` mode
- Approve and `acceptEdits`
- Approve and review each edit manually
- Keep planning with feedback
- Refine with [Ultraplan](https://code.claude.com/docs/en/ultraplan) (browser-based review)

Each "approve" option also offers to clear the planning context first.

---

## auto

Auto mode lets Claude execute without permission prompts. A separate **classifier model** reviews each action before it runs and blocks anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content.

> **Warning:** Auto mode is a research preview. It reduces prompts but does not guarantee safety.

### Requirements

All of:

- **Plan:** Max, Team, Enterprise, or API. **Not Pro**.
- **Admin gate:** On Team/Enterprise, an admin must enable it at [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).
- **Model:** Sonnet 4.6, Opus 4.6, or **Opus 4.7** on Team/Enterprise/API; **Opus 4.7 only** on Max. Haiku and claude-3 are not supported.
- **Provider:** Anthropic API only — not Bedrock, Vertex, or Foundry.

If unavailable, that's a *permanent* state for your account, not a transient outage. (A "cannot determine the safety of an action" message *is* a transient classifier outage.)

### What the classifier blocks by default

- Downloading and executing code (`curl | bash`)
- Sending sensitive data to external endpoints
- Production deploys and migrations
- Mass deletion on cloud storage
- Granting IAM or repo permissions
- Modifying shared infrastructure
- Irreversibly destroying files that existed before the session
- Force push, or pushing directly to `main`

### What it allows by default

- Local file ops in your working dir
- Installing dependencies declared in lock files / manifests
- Reading `.env` and sending credentials to their matching API
- Read-only HTTP requests
- Pushing to the branch you started on or one Claude created

`claude auto-mode defaults` prints the full rule sets. To customize what your org trusts, configure `autoMode.environment` in settings — see [the auto-mode config docs](https://code.claude.com/docs/en/auto-mode-config).

### Boundaries you state in conversation

If you say "don't push" or "wait until I review before deploying", the classifier treats that as a block signal. The boundary stays in force across messages until you lift it. **Caveat:** boundaries are *re-read from the transcript on each check*. If [context compaction](./memory.md) drops the message that stated the boundary, the boundary is lost. For a hard guarantee, add a [deny rule](./permissions.md).

### Fallback behavior

- Each denied action shows a notification and appears in `/permissions` under "Recently denied" (press `r` to retry with manual approval).
- If the classifier blocks 3 in a row or 20 total in a session, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode.
- In headless `-p` mode, repeated blocks abort the session.

### Inside auto mode, broad allow rules are dropped

When entering auto mode, these allow-rule patterns are temporarily dropped to prevent arbitrary code execution:

- Blanket `Bash(*)` or `PowerShell(*)`
- Wildcarded interpreters like `Bash(python*)`
- Package-manager run commands
- `Agent` allow rules (un-narrowed)

Narrow rules like `Bash(npm test)` carry over. Dropped rules are restored when you leave auto mode.

### Subagents in auto mode

The classifier checks subagent work at three points:

1. **Before spawn** — the delegated task description is evaluated.
2. **During execution** — each subagent action goes through the classifier; any `permissionMode` in the subagent's frontmatter is **ignored**.
3. **On finish** — the classifier reviews the subagent's full action history; any concern prepends a security warning to the results.

### Cost & latency

The classifier runs on a server-configured model independent of `/model`. Each check sends a portion of the transcript plus the pending action and counts toward your token usage. Reads and working-dir edits skip the classifier; the overhead comes mainly from shell commands and network ops.

### Disable from a higher scope

```json
{ "permissions": { "disableAutoMode": "disable" } }
```

---

## dontAsk

Auto-denies every tool call that would otherwise prompt. Only `permissions.allow` rules and built-in [read-only commands](#read-only-bash) execute; explicit `ask` rules are *denied* rather than prompted. Fully non-interactive — perfect for CI.

```bash
claude --permission-mode dontAsk
```

---

## bypassPermissions

Disables permission prompts and safety checks. Only writes to [protected paths](#protected-paths) still prompt. **Use only in containers/VMs/devcontainers** where Claude Code can't damage your host.

You cannot enter `bypassPermissions` from a session that wasn't started with one of these flags:

```bash
claude --permission-mode bypassPermissions
claude --dangerously-skip-permissions   # equivalent
```

`--allow-dangerously-skip-permissions` adds the mode to the `Shift+Tab` cycle without starting in it (so you can begin in `plan` and switch later).

> No protection against prompt injection. For background safety checks without prompts, use `auto` mode.

Disable from managed settings:

```json
{ "permissions": { "disableBypassPermissionsMode": "disable" } }
```

---

## Protected paths

Writes here are *never* auto-approved in any mode (they prompt in default/acceptEdits/plan/bypassPermissions, route to the classifier in auto, are denied in dontAsk):

**Directories:**
- `.git`
- `.vscode`, `.idea`, `.husky`
- `.claude` — **except** `.claude/commands`, `.claude/agents`, `.claude/skills`, `.claude/worktrees` (Claude routinely writes there)

**Files:**
- `.gitconfig`, `.gitmodules`
- `.bashrc`, `.bash_profile`, `.zshrc`, `.zprofile`, `.profile`
- `.ripgreprc`
- `.mcp.json`, `.claude.json`

---

## Read-only Bash

These Bash commands always run without a permission prompt in *every* mode (the set is not configurable):

```
ls, cat, head, tail, grep, find, wc, diff, stat, du, cd
```

Plus read-only forms of `git`. Unquoted globs are allowed only for commands whose every flag is read-only — `ls *.ts` and `wc -l src/*.py` skip the prompt; `find` / `sort` / `sed` / `git` with an unquoted glob still prompt.

A `cd` into a path inside your working dir or an `additionalDirectories` entry is read-only. `cd packages/api && ls` runs without a prompt; `cd ... && git ...` always prompts.

To force a prompt for one of these, add an `ask` or `deny` rule for it.

---

## See also

- [permissions.md](./permissions.md) — rule syntax, evaluation order, managed settings
- [hooks.md](./hooks.md) — PreToolUse hooks add custom permission logic
- [sandboxing.md](./sandboxing.md) — OS-level isolation (complements permissions)
- [models.md](./models.md) — auto-mode model gating
