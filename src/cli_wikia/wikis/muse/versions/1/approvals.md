# muse approvals

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: MSP schema (`Approval*` defs) + `--help` + observed runs.

## Modes (closed enum — select, never construct)

Wire `ApprovalMode`: `allowAll`, `promptUnmatched`, `onRequest`,
`denyUnmatched`. CLI `--approval-mode untrusted|on-request|never`
(default `on-request`). `--parallel-tool-calls` / `--no-parallel-tool-calls`
and per-run `-c KEY=VALUE` tune matching.

## Decisions

`ApprovalDecision`: `approved`, `approvedForSession`,
`approvedPolicyAmendment`, `denied`, `deniedPolicyAmendment`, `timedOut`,
`abort`. Multi-stage flows use `ApprovalStage` (argv, position,
totalStages, resolution). Timeouts and aborts are first-class outcomes,
not errors.

## Judges and escalation

`--approval-judge always|never|auto` (untrusted workspaces behave as
`never`) with `--approval-judge-model` / `--approval-judge-effort`.
`ApprovalErrorCode` covers judge failures (`judgeFailedPolicyLoad`,
`judgeDenied`, `judgePolicyLoadDenied`, `judgePolicyLoadFailed`,
`judgePolicyLoadForbidden`, `judgePolicyLoadUnmatched`).

## Loop detection

`--reflection-loop-threshold N` (default 3) trips the suggestion-needed
flow when repeated tool-call patterns or repeated text are detected.
