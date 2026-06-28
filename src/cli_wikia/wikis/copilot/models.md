# Models (GitHub Copilot CLI)

## Selecting a model

Use `--model` to choose which AI model to use. Pass `auto` to let Copilot
pick the model for you:

```bash
copilot --model auto -p "write a function to parse CSV"
copilot --model <model> -p "refactor the logging module"
```

| Flag | Description |
|------|-------------|
| `--model <model>` | AI model to use (use `auto` to let Copilot pick) |

The `--help` output documents `--model` as a free-form value and the special
value `auto`, but does not enumerate the available model names.

> Verify exact model names and availability in the official Copilot docs.
> Custom Model Providers / BYOK are covered by `copilot help providers`.

## Context window tier

Choose how large a context window to use:

```bash
copilot --context long_context -p "review this large file"
```

| Flag | Values | Description |
|------|--------|-------------|
| `--context <tier>` | `default`, `long_context` | Context window tier |

## Reasoning effort

Control how much reasoning effort the model spends:

```bash
copilot --effort high -p "design a migration plan"
```

| Flag | Values |
|------|--------|
| `--effort, --reasoning-effort <level>` | `none`, `low`, `medium`, `high`, `xhigh`, `max` |

## Custom model providers (BYOK)

Copilot supports Custom Model Providers / Bring Your Own Key. See:

```bash
copilot help providers
```

> Verify exact values in the official docs / run `copilot --help`.
