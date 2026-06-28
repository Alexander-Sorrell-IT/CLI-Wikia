# Permissions

Permission rules control which tools Claude can use without asking. They sit on top of [permission modes](./permission-modes.md) — the mode sets the default ("ask for X kind of thing"), rules pre-approve or block specific tool uses.

---

## The tiered system

| Tool kind | Approval needed | "Yes, don't ask again" behavior |
|---|---|---|
| Read-only (Read, Grep, Glob, …) | No | n/a |
| Bash commands | Yes | Permanently per project + command |
| File modification (Edit, Write) | Yes | Until session end |

`/permissions` opens the UI showing all rules and which settings file each came from.

---

## Three rule kinds

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Read(./)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Bash(curl *)", "Read(./.env)", "WebFetch"]
  }
}
```

Evaluation order: **deny → ask → allow**. First match wins, so deny always beats allow.

If a tool is denied at any level (managed > local > project > user), no other level can allow it.

---

## Rule syntax

### Match all uses of a tool

Bare tool name, no parens:

| Rule | Effect |
|---|---|
| `Bash` | All Bash commands |
| `WebFetch` | All web fetches |
| `Read` | All file reads |
| `Edit` | All file edits |

`Bash(*)` is equivalent to `Bash`.

### With a specifier

| Rule | Effect |
|---|---|
| `Bash(npm run build)` | Exact command |
| `Bash(npm run *)` | Prefix wildcard |
| `Bash(* install)` | Suffix wildcard |
| `Bash(git * main)` | Mid wildcard |
| `Read(./.env)` | This file in cwd |
| `Edit(/src/**/*.ts)` | All TS files under project root |
| `WebFetch(domain:example.com)` | Fetches to domain |
| `Skill(deploy)` | Exact skill |
| `Skill(deploy *)` | Skill + args prefix |
| `Agent(Explore)` | Restrict subagent type |
| `mcp__github` | All tools from `github` MCP server |
| `mcp__github__*` | Same, wildcard syntax |
| `mcp__github__list_issues` | One specific MCP tool |

---

## Bash specifics

### Wildcards

A `*` matches any sequence including spaces, so one wildcard can span multiple args. `Bash(git *)` matches `git log --oneline --all`.

**The space before `*` matters:**
- `Bash(ls *)` matches `ls -la` but **not** `lsof` (word boundary).
- `Bash(ls*)` matches both (no boundary).

`Bash(ls:*)` is the same as `Bash(ls *)` — only at the end of a pattern.

### Compound commands

Claude Code is shell-aware, so `Bash(safe-cmd *)` will *not* allow `safe-cmd && other-cmd`. The recognized separators: `&&`, `||`, `;`, `|`, `|&`, `&`, newlines. Each subcommand must match independently.

When you approve a compound command with "Yes, don't ask again", a separate rule is saved per subcommand (up to 5).

### Process wrappers (auto-stripped before matching)

`timeout`, `time`, `nice`, `nohup`, `stdbuf` — and bare `xargs` (with no flags). So `Bash(npm test *)` matches `timeout 30 npm test`.

**Not** stripped: `direnv exec`, `devbox run`, `mise exec`, `npx`, `docker exec`. So `Bash(devbox run *)` matches *anything after `run`* including `devbox run rm -rf .`. Write per-inner-command rules: `Bash(devbox run npm test)`.

### Wrappers that always prompt

`watch`, `setsid`, `ionice`, `flock` cannot be auto-approved by prefix rules. `find` with `-exec` or `-delete` also always prompts.

### Read-only commands (always run, no prompt)

```
ls, cat, head, tail, grep, find, wc, diff, stat, du, cd
```

Plus read-only `git` forms. Unquoted globs are OK *only* for commands whose flags are all read-only.

### Don't try to constrain Bash arguments to specific URLs

`Bash(curl http://github.com/ *)` is fragile — it won't catch `curl https://...`, `curl -L http://bit.ly/...`, `URL=http://github.com && curl $URL`, etc. For URL filtering, instead:

- **Deny `curl`/`wget` in Bash**, then allow `WebFetch(domain:github.com)` for actual fetching.
- **Use a `PreToolUse` hook** that validates URLs.
- Use **sandboxing** (`allowedDomains`) for OS-level enforcement.

---

## Read & Edit specifics

`Edit` rules apply to all built-in file-editing tools. `Read` rules apply best-effort to all file-reading tools (Grep, Glob, etc.).

> **`Read(./.env)` deny does NOT block `cat .env` in Bash.** It blocks the Read tool only. For OS-level enforcement that catches all processes, use [sandboxing](./sandboxing.md).

### Path patterns (gitignore-style)

| Pattern | Means | Example |
|---|---|---|
| `//path` | **Absolute** path from filesystem root | `Read(//Users/alice/secrets/**)` |
| `~/path` | Path from **home** | `Read(~/Documents/*.pdf)` |
| `/path` | Path **relative to project root** | `Edit(/src/**/*.ts)` |
| `path` or `./path` | Path **relative to cwd** | `Read(*.env)` |

> `/Users/alice/file` is **not** absolute — it's project-relative. Use `//Users/alice/file` for absolute paths.

`*` matches files in one dir; `**` matches recursively. `Read` / `Edit` / `Write` with no parens allows everything.

### Symlinks

When Claude touches a symlink, both the symlink path and its target are checked:

- **Allow rules:** apply only when *both* paths match. A symlink inside an allowed dir pointing outside still prompts.
- **Deny rules:** apply when *either* matches. A symlink pointing to a denied file is denied.

### Windows

Paths are normalized to POSIX before matching. `C:\Users\alice` becomes `/c/Users/alice`. `//c/**/.env` matches `.env` files anywhere on C:. `//**/.env` matches across all drives.

---

## Working directories

Claude defaults to files in the cwd it was launched in. Extend access:

- **Startup:** `--add-dir <path>...`
- **Mid-session:** `/add-dir`
- **Persistent:** `permissions.additionalDirectories`

```json
{ "permissions": { "additionalDirectories": ["../docs", "../shared"] } }
```

Files in additional dirs follow the same rules as the original cwd: readable without prompts; edits follow the current mode.

### `--add-dir` exception: skills are loaded

`--add-dir` grants *file access*, not full configuration discovery. **Most** `.claude/` config (subagents, commands, output styles, hooks, settings) is *not* loaded from added dirs. Two exceptions:

- **Skills** in `.claude/skills/` — loaded with live reload.
- **Plugin settings:** only `enabledPlugins` and `extraKnownMarketplaces`.
- **CLAUDE.md / `.claude/rules/` / `CLAUDE.local.md`** — only if `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set.

To share configuration across projects: use `~/.claude/`, plugins, or launch Claude from the dir holding the `.claude/` you want.

---

## Hooks override permission decisions in one direction

A `PreToolUse` hook can return `"allow"`, `"deny"`, `"ask"`, or `"defer"`. **But:**

- A matching deny rule blocks the call regardless of what the hook returned.
- A matching ask rule still prompts even if the hook returned `"allow"`.
- A blocking hook (exit 2) **stops** the call before permission rules are evaluated, so it overrides allow rules.

This preserves the deny-first precedence including managed-settings denies.

Pattern: allow `Bash` broadly, then write a PreToolUse hook to reject specific dangerous commands.

---

## Managed settings (org-wide enforcement)

Admins deploy these via OS-level policies, managed-settings files, or [server-managed settings](https://code.claude.com/docs/en/server-managed-settings). User and project settings cannot override them.

### Managed-only keys

These have effect *only* when set in managed settings:

| Key | Effect |
|---|---|
| `allowManagedHooksOnly` | Only managed/SDK/force-enabled hooks load. User/project/most plugin hooks blocked |
| `allowManagedMcpServersOnly` | Only managed `allowedMcpServers` are respected. `deniedMcpServers` still merges |
| `allowManagedPermissionRulesOnly` | User/project cannot define allow/ask/deny rules. Only managed rules apply |
| `allowedMcpServers` | Allowlist of MCP servers |
| `deniedMcpServers` | Denylist of MCP servers |
| `allowedChannelPlugins` | Allowlist of channel plugins (replaces Anthropic default when set). Requires `channelsEnabled: true` |
| `channelsEnabled` | Master switch for [channels](./channels.md) on Team/Enterprise |
| `blockedMarketplaces` | Plugin marketplaces that cannot be added (checked before download) |
| `strictKnownMarketplaces` | Allowlist of plugin marketplaces |
| `forceRemoteSettingsRefresh` | Block CLI startup until remote managed settings fetched (fail-closed) |
| `pluginTrustMessage` | Custom message in the plugin trust warning |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Only managed `allowRead` paths respected; `denyRead` still merges from all sources |
| `sandbox.network.allowManagedDomainsOnly` | Only managed `allowedDomains` respected; non-allowed domains blocked silently |
| `wslInheritsWindowsSettings` | When `true` in HKLM or `C:\Program Files\ClaudeCode\managed-settings.json`, WSL reads Windows policy chain |

`disableBypassPermissionsMode` and `disableAutoMode` are typically in managed settings but work from any scope.

> Remote Control and web sessions are gated by an admin toggle in the [Claude Code admin console](https://claude.ai/admin-settings/claude-code), not a managed-settings key.

---

## Settings precedence

```
Managed   >   CLI flags   >   .claude/settings.local.json
              >   .claude/settings.json   >   ~/.claude/settings.json
```

Arrays merge across scopes (rules don't override each other; they combine).

---

## Restricting subagents

Use `Agent(name)` rules to control subagent invocation:

```json
{ "permissions": { "deny": ["Agent(Explore)"] } }
```

Disables the Explore subagent. Use without parens (`Agent`) to gate the Agent tool entirely.

---

## See also

- [permission-modes.md](./permission-modes.md) — what each mode auto-allows
- [sandboxing.md](./sandboxing.md) — OS-level enforcement for Bash
- [hooks.md](./hooks.md) — `PreToolUse` for custom validation
- [settings.md](./settings.md) — full settings hierarchy
