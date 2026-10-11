# muse enterprise

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse config --help` + observed `config status` output.

Two planes: `defaults` and `policy` (`{"schema_version":1,"settings":
{...}}` documents, NOT the flat user settings.json).
`muse config validate --plane <defaults|policy> --file <path>` checks a
document; `muse config status` shows plane state. `muse config generate
--plane <name>` creates a document from the active runtime; `apply` writes
it; `--apply` on validate validates then writes. `--sync` triggers
launcher sync (`MUSE_SYNC_UPDATE`). Observed status: no planes, 0 backing
files, `lastSync=no-prior-sync`, `generatedNext=no`: pure local config.
