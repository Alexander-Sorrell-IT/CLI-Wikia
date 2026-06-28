# The Advisor Tool

The `advisor` tool is a built-in mechanism for getting a **second opinion mid-task** from a stronger reviewer model that sees your full conversation transcript. It's not a skill, agent, or plugin — it's a top-level tool surfaced into Claude's tool set when available.

---

## What it is

When Claude calls `advisor()`, the *entire conversation history* — task description, every tool call, every result, all reasoning — is automatically forwarded to a stronger reviewer model. The advisor sees exactly what Claude has done, then returns advice.

**No parameters.** No prompt to construct. The tool call itself is the request.

---

## When to use it

Call `advisor()`:

1. **BEFORE substantive work.** Before writing, before committing to an interpretation, before building on an assumption. Orientation work (finding files, fetching a source, seeing what's there) is fine to do first; *writing*, *editing*, and *declaring an answer* are substantive.

2. **When you believe the task is complete.** Make the deliverable durable first (write the file, save the result, commit the change), then call advisor. The advisor call takes time; if the session ends during it, a durable result persists and an unwritten one doesn't.

3. **When stuck.** Errors recurring, approach not converging, results not fitting.

4. **When considering a change of approach.**

---

## When NOT to call it (yet)

On short reactive tasks where the next action is dictated by tool output Claude just read, the advisor adds little. The advisor's value peaks **on the first call, before the approach crystallizes**. After that, marginal value drops fast.

On tasks longer than a few steps: at minimum, call advisor **once before committing to an approach** and **once before declaring done**.

---

## How to weight the advice

Give it serious weight. **But:**

- If you follow a step and it fails empirically, adapt. A failed empirical test trumps theoretical advice.
- If you have primary-source evidence that contradicts a specific claim (the file says X, the paper states Y), trust the primary source.

**Important caveat:** a passing self-test is not evidence the advice is wrong — it's evidence your test doesn't check what the advice is checking.

---

## When the advisor disagrees with prior data

If you've already retrieved data pointing one way and the advisor points another: **don't silently switch**. Surface the conflict in one more advisor call:

> "I found X, you suggest Y, which constraint breaks the tie?"

The advisor saw the evidence but may have underweighted it. A reconcile call is cheaper than committing to the wrong branch.

---

## Practical patterns

### Pattern 1: Plan → advise → execute

```
1. Read the relevant files (orientation).
2. Form an approach.
3. Call advisor() with the approach taking shape.
4. Adjust based on the advice.
5. Implement.
```

### Pattern 2: Done → advise → ship

```
1. Implement the change.
2. Write the deliverable durably (write file, commit, save).
3. Call advisor() to verify completion.
4. Address feedback (if any) before declaring done.
```

### Pattern 3: Stuck → advise → unstuck

```
1. Tried approach A. Errors.
2. Tried approach B. Different errors.
3. Call advisor() — describe what was tried and why nothing converges.
4. Apply suggested next step.
```

---

## Advisor vs alternatives

|  | Advisor | Subagent (e.g. code-reviewer) | rubber-duck-validator skill |
|---|---|---|---|
| Sees | Full transcript automatically | Only what you brief it on in the prompt | Only the artifact you pass it |
| Tooling | Stronger reviewer model | Whatever model the subagent specifies | Standard model with checklist |
| Best for | Quick mid-task validation | Independent review with explicit context | Forced line-by-line walk through one artifact |
| Cost | One additional model call | Full subagent session | Skill load + adversarial pass |
| When | Before/after substantive work, when stuck | When you need targeted independent analysis | Before declaring done on a non-trivial deliverable |

---

## Why the advisor matters

The reviewer model has **different blind spots than the working model**. By forwarding the full transcript, it sees:
- What was tried and what didn't work
- What evidence was gathered
- What assumptions were made
- What the user actually asked for

…and can catch errors that the working model has rationalized into the plan. Catching a bad approach **before** committing to it is far cheaper than backing out a half-implemented bad approach.

---

## Common Anti-pattern

> "I'll just figure it out myself first, then check with the advisor at the end."

**No.** That's exactly when the advisor's value collapses. The advisor's biggest leverage is *before* you commit to an approach. After you've built around an interpretation, advice that contradicts it is expensive to apply (you have to undo).

The discipline: **call advisor before substantive writing, not after.**

---

## See also

- [stacking.md](./stacking.md) — composing the advisor with subagents and skills
- [agents.md](./agents.md) — when to delegate to a subagent instead
