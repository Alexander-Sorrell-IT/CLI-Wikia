# Sandbox

To protect your machine from destructive commands or unauthorized network access
during autonomous agent runs, Antigravity ships a **native OS-level sandbox** for
terminal execution. Where [permissions](./permissions.md) decide *whether* a tool
runs, the sandbox bounds *what that process can actually do* at the OS layer.

---

## Enabling the sandbox

Two ways:

```bash
agy --sandbox -p "build and run the test suite"   # per-session
```

```json
// settings.json — persistent
{ "enableTerminalSandbox": true }
```

When enabled, terminal commands the agent runs execute inside a **restricted
sandbox environment** instead of directly on your host.

---

## Pairing the sandbox with permissions

The cleanest autonomous setup combines the sandbox with the
`proceed-in-sandbox` [tool-permission mode](./permissions.md#tool-permission-modes-toolpermission):

```json
{
  "enableTerminalSandbox": true,
  "toolPermission": "proceed-in-sandbox"
}
```

This lets the agent run commands **without prompting**, but only because they are
**contained** in the sandbox. Commands that would need to escape the sandbox
(e.g. unreachable network, host-only tools) fall back to the normal permission
flow.

---

## File-access boundary

The sandbox works together with the workspace boundary:

| Setting | Effect |
|---------|--------|
| `allowNonWorkspaceAccess: false` *(default)* | The agent reads/writes only inside the project root |
| `allowNonWorkspaceAccess: true` | The agent may touch files outside the workspace |

In the desktop app this is the **Non-Workspace File Access** policy
(`allow` / `ask` / `deny`), overridable per project.

Combined with the sandbox, this means: even if the agent is tricked into running
something destructive, it is bounded to the workspace and the sandbox's view of
the filesystem and network.

---

## Network containment

Internet access during sandboxed runs is bounded by the **Internet Access
Policy** (`allow` / `ask` / `deny`) and the **Browser Allowlist** (which domains
the browser tools may reach). See [permissions.md](./permissions.md#network--file-access-policy).

---

## What the sandbox does and doesn't cover

- **Covers:** terminal commands the agent runs (and their child processes).
- **Bounded by policy, not the sandbox:** built-in file read/write and network
  reach are gated by the permission policies above.

> The sandbox is described as a "native operating system sandbox layer." The
> exact mechanism per platform (and any Linux/macOS dependencies) is documented
> at `https://antigravity.google/docs/agent-permissions` — verify there. This is
> a different implementation from the older Gemini CLI's container-based sandbox.

---

## See also

- [permissions.md](./permissions.md) — `proceed-in-sandbox`, internet/browser policy
- [configuration.md](./configuration.md) — `enableTerminalSandbox`, `allowNonWorkspaceAccess`
- [cli-reference.md](./cli-reference.md) — the `--sandbox` launch flag
