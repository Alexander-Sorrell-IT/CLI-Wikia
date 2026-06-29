# Permissions

Antigravity gates what an agent is allowed to *do* — run commands, touch files,
reach the network, drive the browser — through a **tool-permission policy** plus
explicit **allow/deny rules**. This is the layer that decides whether a tool call
proceeds, prompts you, or is blocked.

---

## Tool-permission modes (`toolPermission`)

The headline setting. It controls the confirmation behavior for tool execution:

| Mode | Behavior |
|------|----------|
| `request-review` *(default)* | The agent asks for approval before running tools that change things |
| `always-proceed` | No prompts — auto-approve everything (risky) |
| `strict` | Prompt for **all** non-read tools |
| `proceed-in-sandbox` | Auto-proceed, but only inside the terminal [sandbox](./sandbox.md) |

Set it in `settings.json`:

```json
{ "toolPermission": "request-review" }
```

or interactively via `/permissions` and `/config`. `proceed-in-sandbox` is the
sweet spot for autonomy with a safety net: the agent runs freely, but contained.

### The launch-flag escape hatch

```bash
agy --dangerously-skip-permissions -p "..."
```

This auto-approves **every** permission request for the session — equivalent to
`always-proceed`. Reserve it for throwaway or already-sandboxed environments.

---

## Allow / deny / ask rules (`permissions`)

Beyond the global mode, you define fine-grained rules for **files, commands, and
URLs** under the `permissions` object (global) or per-project. Conceptually:

- **Command allowlist / denylist** — terminal commands that are always permitted
  or always blocked.
- **File rules** — allow/ask/deny reading or writing specific paths.
- **URL / Browser allowlist** — restrict which domains the agent's web and
  browser tools may visit.

### "Always Approve" matching is strict by default

As of v1.0.13, command-permission "Always Approve" rules match **literally
(non-regex)** by default. To use a regular expression, **prefix the rule with
`regex:`**:

```
# literal match (default)
npm test

# regex match (opt-in)
regex:^npm (test|run build)$
```

Redirection checks were also relaxed so that safe commands with output
redirection (e.g. `tool > file`) can match an approval rule without requiring
full-command approval.

> The precise schema of the `permissions` object (field names, glob syntax) is
> documented at `https://antigravity.google/docs/agent-permissions`. The behavior
> above is confirmed from the changelog and bundled docs; verify the exact JSON
> shape in official docs.

---

## Workspace trust (`trustedWorkspaces`)

The agent only gets execution rights in directories you trust. Trusted paths are
recorded in:

```json
{ "trustedWorkspaces": ["/home/me/projects/app", "/home/me/work"] }
```

Opening an untrusted directory restricts what the agent may run until you grant
trust.

---

## Network & file-access policy

Two coarse policies bound the agent's reach (exposed in the desktop app as
dropdowns, and via config keys in the CLI):

| Policy | Values | Setting |
|--------|--------|---------|
| **Non-workspace file access** | `allow` / `ask` / `deny` | `allowNonWorkspaceAccess` (bool in CLI) — see [sandbox.md](./sandbox.md) |
| **Internet access** | `allow` / `ask` / `deny` | governs whether the agent can make network requests |
| **Browser allowlist** | list of domains | restricts the agent's browser navigation |

Project-level settings can override these for a single workspace.

---

## How the layers fit together

```
agent wants to run a tool
        │
        ▼
trustedWorkspaces? ── no ──► restricted / prompt
        │ yes
        ▼
allow/deny rule match? ── deny ──► blocked
        │ (regex: opt-in)
        ▼
toolPermission mode ──► proceed | prompt | proceed-in-sandbox
        │
        ▼
sandbox + hooks enforce at execution time
```

Permissions decide *whether* a tool runs; the [sandbox](./sandbox.md) decides
*what that process can touch*; [hooks](./hooks.md) can deterministically block at
lifecycle points. Use them together for defense in depth.

---

## See also

- [sandbox.md](./sandbox.md) — OS-level terminal isolation
- [hooks.md](./hooks.md) — deterministic lifecycle enforcement
- [configuration.md](./configuration.md) — where these keys live and precedence
