# Sandboxing

Sandboxing is **OS-level filesystem and network isolation for the Bash tool and its child processes**. It complements [permissions](./permissions.md) — permissions decide *whether Claude can call a tool*, sandboxing decides *what that Bash subprocess can actually access at the kernel level*.

---

## Why it matters

- A `Read(./.env)` deny rule blocks the Read tool — but `cat .env` from Bash bypasses it. The sandbox catches it at the OS layer.
- Prompt injection that tricks Claude into running something dangerous is bounded by what the sandbox allows.
- Reduces approval fatigue — safe ops within the sandbox don't need a per-command prompt.

> Effective sandboxing requires **both** filesystem AND network isolation. Without network isolation a compromised agent could exfiltrate `~/.ssh/id_rsa`. Without filesystem isolation it could backdoor things to gain network access.

---

## Platforms & enforcement

| Platform | Mechanism |
|---|---|
| macOS | Seatbelt (built-in) |
| Linux | [bubblewrap](https://github.com/containers/bubblewrap) |
| WSL2 | bubblewrap (same as Linux) |
| WSL1 | Not supported |
| Windows native | Planned |

### Linux/WSL2 deps

```bash
# Ubuntu/Debian
sudo apt-get install bubblewrap socat

# Fedora
sudo dnf install bubblewrap socat
```

Enable in-session: `/sandbox`. The menu shows install instructions if dependencies are missing.

### Default behavior on missing deps

If the sandbox can't start, Claude Code shows a warning and runs commands without sandboxing. To make this a *hard failure*:

```json
{ "sandbox": { "failIfUnavailable": true } }
```

---

## Two sandbox modes

| Mode | Bash inside the sandbox |
|---|---|
| **Auto-allow** | Auto-approved without prompts (commands needing non-allowed network fall back to the regular permission flow) |
| **Regular permissions** | Goes through standard permission flow, even when sandboxed |

In both modes, the sandbox enforces the same filesystem/network boundaries. The difference is whether sandboxed Bash is auto-approved.

`autoAllowBashIfSandboxed: true` (default) makes auto-allow the active mode.

> Even with auto-allow on, `rm`/`rmdir` targeting `/`, your home dir, or critical system paths still trigger a prompt. Explicit deny rules are always respected.

---

## Filesystem isolation

**Defaults:**
- Write access: cwd + subdirs only
- Read access: entire computer, except denied dirs

OS-level enforcement: **all** sandboxed subprocesses respect this, including `kubectl`, `terraform`, `npm`, etc.

### Granting subprocess writes

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

When defined in multiple settings scopes, arrays **merge** (combine, not replace). Project + user + managed all stack.

### Path prefixes (different from permissions!)

| Prefix | Means |
|---|---|
| `/path` | Absolute path |
| `~/path` | Home dir |
| `./path` or no prefix | Project root (project settings) or `~/.claude` (user settings) |

> ⚠️ This differs from the [Read/Edit permission rules](./permissions.md#path-patterns), which use `//path` for absolute and `/path` for project-relative. Sandbox uses normal POSIX conventions.
> The older `//path` prefix still works for absolute. If you previously used `/path` expecting project-relative, switch to `./path`.

### Denying reads/writes

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead":  ["~/"],
      "allowRead": ["."],            // re-allow within denied region
      "denyWrite": ["/etc"]
    }
  }
}
```

`denyRead` merges with `Read(...)` permission deny rules. `allowRead` takes precedence over `denyRead`.

### Managed `allowManagedReadPathsOnly`

When set in managed settings, only managed `allowRead` entries are respected. User/project/local `allowRead` are ignored. `denyRead` still merges from all sources.

---

## Network isolation

A proxy server outside the sandbox controls outbound connections. Default is **Trusted** — the [allowlisted domains](https://code.claude.com/docs/en/claude-code-on-the-web#default-allowed-domains) (package registries, GitHub, cloud SDKs).

```json
{
  "sandbox": {
    "network": {
      "allowedDomains":  ["github.com", "*.npmjs.org"],
      "deniedDomains":   ["bad.example.com"]
    }
  }
}
```

`deniedDomains` blocks specific domains even when a broader `allowedDomains` wildcard would otherwise permit them.

### Unix sockets (macOS) and local binding

```json
{
  "sandbox": {
    "network": {
      "allowUnixSockets":    ["/var/run/postgres.sock"],
      "allowAllUnixSockets": false,
      "allowLocalBinding":   true,
      "allowMachLookup":     ["com.apple.cfprefsd.daemon"]
    }
  }
}
```

> ⚠️ Don't allow `/var/run/docker.sock` casually — it grants effective host access via Docker.

### Custom proxy

```json
{
  "sandbox": {
    "network": {
      "httpProxyPort":  8080,
      "socksProxyPort": 8081
    }
  }
}
```

For organizations needing TLS-inspection / custom filtering / centralized logging.

---

## Excluding commands from the sandbox

```json
{
  "sandbox": {
    "excludedCommands": ["docker *", "watchman *"]
  }
}
```

Some tools genuinely don't work sandboxed:
- `watchman` is incompatible — for `jest`, use `jest --no-watchman`.
- `docker` is incompatible — exclude or run via `docker compose` outside the sandbox.

---

## The `dangerouslyDisableSandbox` escape hatch

When a command fails inside the sandbox (network unreachable, incompatible tool), Claude can retry with `dangerouslyDisableSandbox`. Such commands go through the **normal permission flow** — you must approve them.

Disable the escape hatch entirely:

```json
{ "sandbox": { "allowUnsandboxedCommands": false } }
```

Now `dangerouslyDisableSandbox` is ignored — all commands must run sandboxed or be in `excludedCommands`.

---

## Weakened modes

```json
{
  "sandbox": {
    "enableWeakerNestedSandbox":      true,   // Linux: works inside Docker without privileged namespaces
    "enableWeakerNetworkIsolation":   true    // macOS: allow TLS trust service access
  }
}
```

Both reduce security. Use only when you have *external* isolation enforcing things.

---

## Security limitations to know

- **Network filtering is domain-only.** It doesn't inspect traffic. Allowing `github.com` may still allow data exfiltration. **[Domain fronting](https://en.wikipedia.org/wiki/Domain_fronting)** can bypass.
- **Privilege escalation via Unix sockets** — see Docker socket warning above.
- **Filesystem privilege escalation** — overly broad write access to `$PATH` dirs, system config, or shell rc files (`.bashrc`, `.zshrc`) can escalate when other users/processes touch those files.
- **`enableWeakerNestedSandbox` significantly weakens Linux security.** Only use in additional-isolation contexts.

---

## What sandboxing does NOT cover

- **Built-in file tools** (Read, Edit, Write) — they use the [permission system](./permissions.md), not the sandbox.
- **Computer use** — when Claude opens apps and controls your screen, that runs on your actual desktop. Per-app prompts gate each app.

---

## Open source

The sandbox runtime is on npm:

```bash
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Source: [github.com/anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime). You can sandbox arbitrary programs (e.g. an MCP server) with it.

---

## Best practices

1. **Start restrictive.** Open up as needed.
2. **Combine with permissions** for defense-in-depth.
3. **Different rules per environment** (dev vs prod contexts).
4. **Monitor sandbox violation logs** to learn what Claude actually needs.
5. **Review allowed domains** regularly — broad domains like `github.com` permit broad data exfil paths.

---

## See also

- [permissions.md](./permissions.md) — `Read`/`Edit` rules merge into sandbox filesystem
- [permission-modes.md](./permission-modes.md) — `auto` mode and the classifier
- [settings.md](./settings.md) — full `sandbox.*` key list
