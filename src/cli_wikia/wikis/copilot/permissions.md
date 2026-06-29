# Permissions

Copilot CLI gates everything the agent does behind a permission system with three axes — **tools**, **paths**, and **URLs** — plus a layer that decides which tools the model can even *see*. By default it restricts risky actions and prompts you for confirmation; flags and settings let you pre-approve or forbid things.

Reference: `copilot help permissions`.

---

## Two distinct layers

1. **Visibility** — which tools exist for the model at all:
   - `--available-tools[=…]` — a whitelist; disables every other tool.
   - `--excluded-tools[=…]` — a blacklist; hides just those tools.
2. **Approval** — for visible tools, whether they run without a prompt:
   - `--allow-tool`, `--deny-tool`, `--allow-all-tools`.

> Approval flags never expose a tool that visibility filters removed. **Deny always beats allow**, including over `--allow-all-tools`.

---

## Tool permission patterns

`--allow-tool` / `--deny-tool` take a pattern of the form `kind(argument)`; the argument is optional and depends on the kind.

| Pattern | Matches |
|---|---|
| `shell(command)` | An exact shell command. Omit the argument to match all shell commands |
| `shell(git:*)` | A command prefix — the `:*` suffix matches by command *stem*. `shell(git:*)` matches `git push` but **not** `gitea` |
| `write` | All file-creating/modifying tools (except shell). Shell redirections need `--allow-all-tools` |
| `<mcp-server>(tool)` | One tool from an MCP server; omit `(tool)` for all tools of that server |
| `url(domain-or-url)` | URL access by the shell and web-fetch tools; omit for all URLs |

`git` and `gh` are approved on a first-level-subcommand basis (e.g. `git push`, `gh pr create`).

```bash
# Investigate read-only-ish: allow shell, forbid writes
copilot --allow-tool=shell --deny-tool=write -p "investigate the bug"

# All git except push
copilot --allow-tool='shell(git:*)' --deny-tool='shell(git push)'

# All tools from MyMCP except one
copilot --deny-tool='MyMCP(denied_tool)' --allow-tool='MyMCP'
```

---

## URL permissions

`--allow-url` / `--deny-url` (and the `allowedUrls` / `deniedUrls` settings) accept exact URLs or protocol+domain patterns, applied to the shell and web-fetch tools.

- **Protocol-aware:** approving `https://example.com` does **not** allow `http://example.com`.
- Patterns without a protocol default to `https://`.
- Wildcard subdomains: `*.github.com`.
- **Deny takes precedence** over allow.

```bash
copilot --allow-url=github.com                 # https://github.com
copilot --allow-url=http://example.com          # explicit http
copilot --deny-url=https://malicious-site.com
copilot --allow-all-urls
```

---

## Path permissions

By default file access is limited to the **current working directory and its subdirectories**, plus the **system temp directory**.

| Flag | Effect |
|---|---|
| `--add-dir <dir>` | Extend access to another directory (repeatable; also `/add-dir`, `/list-dirs`) |
| `--allow-all-paths` | Disable path verification — any path on the filesystem |
| `--disallow-temp-dir` | Remove the automatic temp-dir grant |

Trusted folders (where you've granted read/execute on first use) persist in `settings.json` (`trustedFolders`).

---

## "Allow everything" switches

| Flag | Equivalent to |
|---|---|
| `--allow-all` / `--yolo` | `--allow-all-tools --allow-all-paths --allow-all-urls` |
| `--allow-all-tools` (env `COPILOT_ALLOW_ALL`) | Auto-run all tools — **required for non-interactive (`-p`) mode** |
| `--allow-all-paths` | Any path |
| `--allow-all-urls` | Any URL |

Inside a session, `/allow-all` does the same; `/reset-allowed-tools` clears session grants.

---

## Autonomy & secrets

- `--no-ask-user` disables the `ask_user` tool, so the agent never pauses to ask clarifying questions — pair with autopilot for unattended runs.
- `--secret-env-vars=KEY,OTHER` strips those env vars from shell/MCP environments and redacts their values from output.

---

## Interactive approvals

In an interactive session, when the agent wants to do something not pre-approved, you can: allow it once, allow it for the rest of the session, or reject with an alternative instruction. Approvals are saved to `~/.copilot/permissions-config.json`.

> GitHub notes the permission patterns are expected to gain richer wildcard matching in future versions.

---

## See also

- [modes.md](modes.md) — autopilot pairs with broad permissions
- [configuration.md](configuration.md) — `allowedUrls`/`deniedUrls`/`trustedFolders`
- [custom-agents.md](custom-agents.md) — per-agent tool restrictions
