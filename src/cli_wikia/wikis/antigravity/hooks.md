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

---

## What hooks are for

Typical uses:

- Block a class of commands or file writes regardless of what the model decides.
- Run a validation/formatter/test step automatically at a lifecycle point.
- Gate an action behind an external check before it is allowed to proceed.

Because hooks are deterministic, they are the right tool when you need something
to happen (or *never* happen) **for sure**, rather than asking the agent nicely.

---

## Listing hooks

In an interactive session:

```
/hooks       # list all registered lifecycle hooks
```

Hooks can be bundled inside [plugins](./plugins.md), so installing a plugin may
register hooks.

---

## Status & caveats

Hooks are listed in the official docs sitemap
(`https://antigravity.google/docs/hooks`) and surfaced in the CLI via `/hooks`,
but the bundled offline docs do **not** enumerate the available hook events,
their input/output schema, or exit-code semantics.

> **Verify in official docs.** The full catalog of hook events, the handler
> contract (how a hook receives context and how it blocks — e.g. via exit codes),
> and where hooks are configured on disk should be confirmed at
> `https://antigravity.google/docs/hooks`. This wiki does not invent those
> details. Community guides describe Antigravity hooks as deterministic
> lifecycle guards, consistent with the model above, but specifics may vary by
> version.

---

## See also

- [permissions.md](./permissions.md) — the other enforcement layer (allow/deny, modes)
- [customization.md](./customization.md) — rules & skills (the *suggestion* layers)
- [plugins.md](./plugins.md) — bundling hooks for distribution
