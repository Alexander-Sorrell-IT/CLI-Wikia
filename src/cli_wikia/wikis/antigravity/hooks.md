# Hooks

**Hooks** are Antigravity's mechanism for **deterministic execution boundaries**.
They represent a shift away from relying on the model's judgment toward
**programmatically enforced rules** that fire at key points in the agent's
lifecycle — so destructive or unwanted actions are *prevented*, not merely
*discouraged*.

This is the same distinction that runs through the whole platform:

- **Rules and skills** ([customization.md](./customization.md)) *suggest* behavior
  — the model can ignore them.
- **Hooks** *enforce* behavior — they run outside the model and can hard-block.

> **Status (verified 2026-07-02).** Hooks are a real, shipping feature of the
> Antigravity CLI (`agy`): the bundled CLI reference lists `/hooks` ("Lists all
> registered lifecycle hooks") and the official docs page
> `https://antigravity.google/docs/hooks` documents them. The **event names**
> and **config file location** below are well corroborated across sources. The
> exact handler **input/output JSON schema** still varies between community
> write-ups (see caveat at the bottom) — treat the field names as illustrative
> and confirm against the official docs for your version.

---

## What hooks are for

Typical uses:

- Block a class of commands or file writes regardless of what the model decides.
- Run a validation/formatter/test step automatically at a lifecycle point.
- Gate an action behind an external check before it is allowed to proceed.

Because hooks are deterministic, they are the right tool when you need something
to happen (or *never* happen) **for sure**, rather than asking the agent nicely.

---

## Lifecycle events

Antigravity fires hooks at five lifecycle points:

| Event | Fires |
|-------|-------|
| `PreToolUse` | Before a tool call runs — can allow, deny, or ask. |
| `PostToolUse` | After a tool call completes. |
| `PreInvocation` | Before an agent turn/invocation begins (startup or resume). |
| `PostInvocation` | After an agent turn/invocation finishes. |
| `Stop` | When the agent terminates the session. |

For `PreToolUse` / `PostToolUse` you scope the hook with a **`matcher`**
(a regular expression over the tool name): `"*"` or `""` matches every tool,
`"run_command"` matches one tool, and `"run_command|write_to_file"` or
`".*_file.*"` match by regex. For `PreInvocation`, `PostInvocation`, and `Stop`
the matcher is ignored (handlers are listed directly under the event).

---

## Where hooks are configured

Hooks live in a **`hooks.json`** file (separate from `settings.json`):

| Scope | Location |
|-------|----------|
| Global | `~/.gemini/config/hooks.json` |
| Workspace | `<project-root>/.agents/hooks.json` |

If a hook is declared in both scopes, **both run**. This mirrors the
customization roots in [configuration.md](./configuration.md) and
[customization.md](./customization.md): the global customization root is
`~/.gemini/config/` and the workspace root is `.agents/`.

> One community guide instead reports the global file at
> `~/.gemini/antigravity-cli/hooks.json` (alongside `settings.json`). The
> majority of sources and the customization-root convention point to
> `~/.gemini/config/hooks.json`; verify the exact global path for your version.

---

## Listing hooks

In an interactive session:

```
/hooks       # list all registered lifecycle hooks
```

Hooks can also be bundled inside [plugins](./plugins.md), so installing a plugin
may register hooks.

---

## Handler contract

A hook handler is a script. It receives a JSON object on **stdin** describing
the event (fields reported include the session id, a transcript path, the cwd,
a timestamp, the `hook_event_name`, and — for tool events — the tool name and
arguments), and it returns a JSON decision on **stdout**. A handler blocks by
returning a deny decision with a reason that is surfaced to the agent as a
steering hint; if **any** hook denies, the whole operation is blocked.

> **Schema caveat.** The precise output shape differs across community sources —
> some document `{"decision": "deny", "reason": "..."}` (with `"allow"` /
> `"deny"` / `"ask"`), others `{"allow_tool": false, "deny_reason": "..."}`.
> This wiki does not assert one canonical schema; confirm the field names and
> exit-code semantics at `https://antigravity.google/docs/hooks` for your
> installed version.

---

## See also

- [permissions.md](./permissions.md) — the other enforcement layer (allow/deny, modes)
- [customization.md](./customization.md) — rules & skills (the *suggestion* layers)
- [plugins.md](./plugins.md) — bundling hooks for distribution

---

## Sources

- Antigravity official docs — Hooks: `https://antigravity.google/docs/hooks` (Accessed 2026-07-02)
- Bundled offline docs: `~/.gemini/antigravity-cli/builtin/skills/antigravity_guide/references/cli.md` — `/hooks` command (Accessed 2026-07-02)
- Kanshi Tanaike, "A Developer's Guide to Agent Hooks in Antigravity CLI," Google Cloud Community / Medium: `https://medium.com/google-cloud/a-developers-guide-to-agent-hooks-in-antigravity-cli-4c1440febd11` (Accessed 2026-07-02)
- danicat.dev, "Mastering Hooks in Coding Agents": `https://danicat.dev/posts/20260610-mastering-hooks/` (Accessed 2026-07-02)
- Installed binary, verified 2026-07-02: `agy` v1.0.13 contains exactly these five hook kinds in its `hooks_pb` protos (`PreToolHookArgs/Result`, `PostToolHookArgs/Result`, `PreInvocationHookArgs/Result`, `PostInvocationHookArgs/Result`, `StopHookArgs/Result`), a `PreToolHookDeniedError`, and `hooks.json` discovery strings — corroborating the event list and config file name above.
