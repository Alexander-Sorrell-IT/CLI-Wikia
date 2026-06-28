# Models (Gemini CLI)

## Selecting a model

Use the `-m` / `--model` flag to choose which model the CLI uses:

```bash
gemini -m <model> "write a function to parse CSV"
```

| Flag | Type | Description |
|------|------|-------------|
| `-m, --model` | string | Model to use |

The flag takes a model name as a string. When omitted, the CLI uses its
default model.

## Model names

The `--help` output documents `-m, --model` as a free-form string but does not
enumerate the available model names.

> Verify exact model names and availability in the official Gemini docs, or
> run `gemini --help`. Model identifiers change over time and depend on your
> account access.

## Related flags

| Flag | Description |
|------|-------------|
| `--context` | (Not present in Gemini CLI ground truth — see official docs) |

> Only `-m`/`--model` is documented for model selection in the version 0.22.4
> help output.
