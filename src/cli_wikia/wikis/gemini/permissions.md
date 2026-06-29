# Permissions

Gemini CLI gates tool execution through several layers: **approval modes** set the overall posture for a session, the **policy engine** evaluates fine-grained rules for each tool call, **trusted folders** decide whether a workspace's configuration is loaded at all, and **Plan Mode** enforces a strict read-only environment for research and design.

These layers complement [sandboxing](./sandboxing.md): permissions decide *whether* a tool runs; sandboxing limits *what* the resulting process can touch at the OS level.

---

## Approval modes

An approval mode sets the default posture for how tool calls are handled in a session.

| Mode | Behavior |
|---|---|
| `default` | Standard interactive mode; most write tools require confirmation |
| `autoEdit` (Auto-Edit) | Optimized for automated code editing; some write tools are auto-approved |
| `yolo` | All tools auto-approved — use with extreme caution |
| `plan` 🔬 | Strict, read-only mode for research and design (see [Plan Mode](#plan-mode-)) |

Set the mode at launch with the flag, or persistently in settings:

```bash
gemini --approval-mode=plan -p "Analyze telemetry and suggest improvements"
```

```json
{
  "general": {
    "defaultApprovalMode": "default"
  }
}
```

In an interactive session, press **`Shift+Tab`** to cycle through modes (`Default` → `Auto-Edit` → `Plan`). Plan Mode is automatically removed from the rotation while the CLI is actively processing or showing a confirmation dialog.

---

## The policy engine

The policy engine provides fine-grained control over tool execution. It evaluates a set of **rules** against each tool call and returns the highest-priority matching decision.

### Decisions

| Decision | Effect |
|---|---|
| `allow` | The tool call executes automatically, no interaction |
| `deny` | The tool call is blocked. For global rules (no `argsPattern`), denied tools are **completely excluded from the model's memory** — the model never sees them, which is more secure and saves context |
| `ask_user` | The user is prompted to approve or deny. In non-interactive mode this is treated as `deny` |

> `deny` is the recommended way to exclude tools. The legacy `tools.exclude` setting is deprecated in favor of policy rules with a `deny` decision.

### Rules

Each rule combines conditions with a decision and a priority. Rules live in `.toml` files; every `.toml` in a policy directory is loaded and combined.

```toml
[[rule]]
toolName = "run_shell_command"
commandPrefix = "rm -rf"
decision = "deny"
priority = 100
```

Key fields of the TOML schema:

| Field | Purpose |
|---|---|
| `toolName` | Tool name (or array of names) the rule targets. Wildcards: `*` (any tool), `mcp_server_*`, `mcp_*_toolName`, `mcp_*` |
| `mcpName` | Name of an MCP server — the recommended way to target MCP tools |
| `toolAnnotations` | Match tool metadata hints, e.g. `{ readOnlyHint = true }` |
| `argsPattern` | Regex tested against the tool's arguments (serialized to stable JSON) |
| `commandPrefix` | Shorthand for `run_shell_command`: command must start with this string (or array of strings) |
| `commandRegex` | Shorthand for `run_shell_command`: regex against the full command. Can't be combined with `commandPrefix` |
| `decision` | `allow`, `deny`, or `ask_user` |
| `priority` | `0`–`999` within a tier |
| `denyMessage` | Custom message shown when this rule denies a call |
| `modes` | Approval modes the rule applies to (omit = all modes) |
| `interactive` | Restrict to interactive (`true`) or non-interactive (`false`) environments |
| `subagent` | Apply only to calls made by a named subagent |
| `allowRedirection` | Permit shell redirection operators (`>`, `>>`, `<`, …) for this rule |

### Priority and tiers

Policies are organized into tiers; **the highest final priority wins**. Within a tier you set a `priority` from 0–999, and the engine computes:

```
final_priority = tier_base + (toml_priority / 1000)
```

| Tier | Base | Source |
|---|---|---|
| Default | 1 | Built-in policies shipped with Gemini CLI |
| Extension | 2 | Policies defined in extensions |
| Workspace | 3 | Project `.gemini/policies` — **currently disabled** ([issue #18186](https://github.com/google-gemini/gemini-cli/issues/18186)) |
| User | 4 | Your custom policies |
| Admin | 5 | Policies managed by an administrator |

So an Admin rule always beats a User rule, which beats Workspace and Default rules; the toml `priority` only orders rules *within* a tier.

> The **Workspace** tier is non-functional today — policies in a project's `.gemini/policies` directory have no effect. Use User or Admin policies instead.

### Policy file locations (`policyPaths` / `adminPolicyPaths`)

| Tier | Location |
|---|---|
| User | `~/.gemini/policies/*.toml` |
| Workspace (disabled) | `$WORKSPACE_ROOT/.gemini/policies/*.toml` |
| Admin (Linux) | `/etc/gemini-cli/policies` |
| Admin (macOS) | `/Library/Application Support/GeminiCli/policies` |
| Admin (Windows) | `C:\ProgramData\gemini-cli\policies` |

Administrators can add supplemental Admin-tier policies via the `--admin-policy` flag or the `adminPolicyPaths` setting in a system settings file. (A `policyPaths` setting for user policy locations should be verified in official docs.)

> **Security guard:** supplemental admin policies are ignored if any `.toml` files exist in the standard system location, preventing flag-based overrides of a central policy. Standard system policy directories must pass strict ownership checks (owned by `root`, not group/other writable on Linux/macOS; not writable by standard users on Windows) or they are ignored. Supplemental policies are exempt from these ownership checks.

### Mode-aware rules

A rule's `modes` array restricts when it is active. A rule with no `modes` is "always active" and applies in every mode, including Plan Mode. Persistent approvals are **context-aware**: choosing "Allow for all future sessions" includes the current mode and all *more permissive* modes in the hierarchy (`plan` < `default` < `autoEdit` < `yolo`). An approval granted in `default` applies to `default`, `autoEdit`, and `yolo`; one granted in `plan` deliberately applies to all modes.

### Default policies

Out of the box: read-only tools (`read_file`, `glob`, …) are generally **allowed**; write tools (`write_file`, `run_shell_command`, …) default to **`ask_user`**; agent delegation defaults to `ask_user`; `yolo` mode has a high-priority rule allowing all tools; `autoEdit` mode allows certain writes without prompting.

### Inspecting policies

Use `/policies list` inside the CLI to view the active rules. (Exact `/policies` subcommands should be verified in official docs.)

---

## Trusted folders

Trusted Folders is a security gate that decides whether a project's own configuration is loaded. It prevents potentially malicious project files from running until you approve the folder.

The feature is **disabled by default**. Enable it in your user `settings.json`:

```json
{
  "security": {
    "folderTrust": {
      "enabled": true
    }
  }
}
```

### The trust dialog

The first time you run the CLI from a folder, a dialog offers three choices:

- **Trust folder** — grants full trust to the current folder.
- **Trust parent folder** — trusts the parent directory and all of its subdirectories (handy if you keep safe projects under one root).
- **Don't trust** — marks the folder untrusted; the CLI runs in restricted "safe mode."

Before you choose, a **discovery phase** scans for custom commands, MCP servers, hooks, skills, and setting overrides, and flags security warnings (e.g. auto-approving tools or disabling the sandbox) so you can decide informedly. Your choice is saved in `~/.gemini/trustedFolders.json` and you're only asked once per folder.

### What "untrusted" disables

In safe mode the CLI does **not** load `.gemini/settings.json` or `.env` files, won't connect to MCP servers, won't load custom commands, disables automatic memory loading and tool auto-acceptance, and restricts extension install/update/uninstall.

### Managing trust

- `/permissions trust` (run `/permissions` from within the CLI) reopens the interactive dialog to change the current folder's trust level.
- Inspect `~/.gemini/trustedFolders.json` to see all trust rules.
- Override the trust file location with `GEMINI_CLI_TRUSTED_FOLDERS_PATH` (absolute path).

### Headless / CI environments

When prompts aren't possible and a folder is untrusted, the CLI throws `FatalUntrustedWorkspaceError` and exits. Bypass the check for the session with either:

- the `--skip-trust` flag, or
- the `GEMINI_CLI_TRUST_WORKSPACE=true` environment variable.

### Trust resolution order

1. **IDE trust signal** — if connected to an IDE, its answer takes highest priority.
2. **Local trust file** — otherwise the CLI consults `~/.gemini/trustedFolders.json`.

---

## Plan Mode 🔬

Plan Mode is a read-only environment for researching the codebase, evaluating trade-offs, and agreeing on an execution strategy *before* any code changes. It is enabled by default and managed via the `/settings` command.

### Entering and exiting

- **Launch in Plan Mode:** `gemini --approval-mode=plan`, or set **Default Approval Mode** to `Plan` via `/settings`.
- **During a session:** press `Shift+Tab` to cycle to Plan, or type `/plan [goal]` (the goal is optional — `/plan implement auth` switches mode and submits the prompt). You can also ask in natural language ("start a plan for…"), which calls the `enter_plan_mode` tool (unavailable in YOLO mode).
- **Exit:** approve a finalized plan (auto-exits and starts implementation), press `Shift+Tab` to cycle out, or ask to "exit plan mode." Cancel a plan with `Esc`.

### Workflow

You describe a goal; the CLI researches in read-only mode, discusses strategy (it stops and waits for your confirmation via `ask_user` before drafting), then writes a detailed plan as a Markdown file. Press **`Ctrl+X`** to edit the plan in your external editor — modify steps or leave inline comments, save, and the CLI refines the plan. Approve it ("automatically accept edits" or "manually accept edits") to begin implementation. `/plan copy` copies the approved plan to your clipboard.

### Tool restrictions

Plan Mode allows only read and research tools: `read_file`, `list_directory`, `glob`, `grep_search`, `google_web_search`, `web_fetch` (needs explicit confirmation), research subagents (`codebase_investigator`, `cli_help`), `ask_user`, read-only MCP tools, and `activate_skill`. `write_file`/`replace` are permitted **only** for `.md` files in the plans directory: `~/.gemini/tmp/<project>/<session-id>/plans/` (or a custom plans directory).

### Customization

Plan Mode's restrictions are enforced by the built-in `plan.toml` policy (Tier 1). Add your own Tier-2 rules in `~/.gemini/policies/` scoped with `modes = ["plan"]`:

```toml
# Allow git status/diff while planning
[[rule]]
toolName = "run_shell_command"
commandPrefix = ["git status", "git diff"]
decision = "allow"
priority = 100
modes = ["plan"]
```

Set a custom plans directory (restricted to the project root for safety):

```json
{
  "general": {
    "plan": {
      "directory": ".gemini/plans"
    }
  }
}
```

A custom directory also needs a policy rule allowing `write_file`/`replace` there in `plan` mode.

### Model routing

With an `auto` model, Plan Mode routes the **planning** phase to a high-reasoning Pro model and switches to a high-speed Flash model for **implementation** once a plan is approved. Disable this with:

```json
{
  "general": {
    "plan": {
      "modelRouting": false
    }
  }
}
```

### Non-interactive Plan Mode

In headless runs the policy engine auto-approves `enter_plan_mode`/`exit_plan_mode`, and on exit the CLI switches to YOLO mode so implementation steps run without hanging on tool approvals.

---

## See also

- [sandboxing.md](./sandboxing.md) — OS-level isolation that complements these permission layers
- [settings.md](./settings.md) — `general.defaultApprovalMode`, `security.folderTrust`, `general.plan.*`
- [configuration.md](./configuration.md) — environment variables and policy file locations
- [commands.md](./commands.md) — `/plan`, `/permissions`, `/policies`, `/settings`
- [cli-reference.md](./cli-reference.md) — `--approval-mode`, `--skip-trust`, `--admin-policy`
