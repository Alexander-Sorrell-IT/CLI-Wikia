# muse compaction

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse exec --help` + hook events.

Strategies: `summary-preserved-suffix/v1`,
`prefix-extension-summary/v1`, `prefix-extension-inventory-summary/v1`
(`--context-compaction-strategy`). Soft/hard thresholds as fractions
(`--context-compaction-soft-threshold`, `--context-compaction-hard-
threshold`). `PreCompact` / `PostCompact` hooks bracket the run —
enforcement uses them for ledger checkpoints. Session `compact`/`compacted`
events appear in the log stream.
