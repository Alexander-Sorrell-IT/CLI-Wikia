# muse models

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `--help` + model-catalog dir + observed settings.

Providers: `echo` (deterministic offline), `meta` (default), `local`.
`--model <id>`; observed: `muse-spark-1.3-contributor`.
Reasoning: `--reasoning-effort none|minimal|low|medium|high|xhigh|max|ultra`
(default high); per-model overrides in `model_reasoning_efforts`.
`muse model-profile` shows resolution per knob and effort tier.
Catalog cache: `~/.local/share/muse/model-catalog/`.
`--fallback-model` (repeatable, max 3), `--advisor`,
`--approval-judge-model` / `--approval-judge-effort` for the judge.
