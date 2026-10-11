# muse headless and MSP

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse exec --help` + `muse schema` export (320KB, exact).

`muse exec [PROMPT]` runs one prompt non-interactively; `--json` streams
JSONL events; `--prompt-file`, `--output-schema` (meta only),
`--max-model-steps`, `--max-tool-output-bytes`, `--session-id` pin runs.
`muse serve` hosts an MSP session over stdio; `muse schema
generate-json-schema|generate-typescript-definitions` exports the exact
wire surface (manifest + `msp.schema.json` + method/notif/error indexes).
Schema is versioned per binary — regenerate, never hand-copy.
`--provider echo` gives deterministic offline runs for probing.
