# Enforcement (cli-enforcement on Bob)

The cli-enforcement engine can be deployed onto Bob exactly like any other
Claude-based CLI. Bob's config root is `.agents/` — the deployer detects this
automatically from the wikia.

---

## Deploy

```bash
cli-enforcement deploy bob --write
```

This:
1. Asks cli-wikia for Bob's hook events, config root (`.agents/`), and topics
2. Wires all 16 enforcement stages to Claude's matching hook events
3. Copies 32+ engine scripts into `.agents/mcp/`
4. Writes `points_config.yaml` (constant scoring engine)
5. Writes `project_config.yaml` (KB gates from Bob wikia topics)
6. Merges hook entries into `.agents/settings.json`

---

## The point system

Bob starts every session at **500 points**. Points gate editing rights.

### Earning

| Action | Points |
|---|---|
| Clean edit (passes flake8 + pattern checks) | +15 |
| Section completed | +25 |
| Workflow completed | +60 |
| Read docs before editing | +8 |
| Quoted proof | +5 |

### Losing

| Violation | Points |
|---|---|
| Skipped reading docs before first edit | −75 |
| Hallucination (edited file without reading it first) | −100 |
| Ignored spec | −100 |
| Hardcoded path | −40 |
| Bare except clause | −25 |
| Cascade needed Opus | −15 |
| Section rolled back | −50 |
| Hard stop triggered | −500 |

### Thresholds

| Points | Effect |
|---|---|
| ≥ 400 | Can edit |
| < 400, no PRE snapshot | **Blocked from all edits** |
| < 0 | Catastrophic — full block |

---

## 10 pre-edit blocking checks

Before every Edit/Write, `enforce_check.py` runs these in order:

0. **Self-protection** — cannot edit `.agents/mcp/`, `settings.json`, state files
1. **Hard stop** — blocked if a hard stop is active
2. **Points threshold** — blocked if points < 400 (without a PRE snapshot)
3. **Workflow PRE snapshot** — blocked if no workflow started
4. **Instructions read** — blocked if `AGENTS.md` not read before first edit
5. **Section required** — blocked if editing a component file without an active section
6. **KB gate** — blocked if the component's understanding doc not read
7. **Multiple files** — blocked if editing a new file without approval of previous
8. **Anti-hallucination** — blocked if file not read, or read is stale/hash mismatch
9. **Agent report pending** — blocked if a subagent output not yet read
10. **Cascade** — blocked if a cascade investigation is waiting for deployment

---

## Sync after Bob wikia updates

When new topics are added to the Bob wiki, re-sync to update KB gates:

```bash
cli-enforcement sync bob --write
```

This updates `project_config.yaml` (new/removed KB gates) and re-wires hooks
if any new events appeared. The points engine (`points_config.yaml`) is never
touched by sync.

---

## Remove

```bash
cli-enforcement remove bob --write
```

Removes `.agents/mcp/` — leaves `settings.json` intact.

---

## Sources

cli-enforcement documentation and the deployed enforcement engine. Accessed 2026-08.
