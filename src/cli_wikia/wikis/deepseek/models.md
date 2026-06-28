# Models (DeepSeek Code)

## Selecting a model

Use `--model` to choose which model to run:

```bash
deepseek-code --model pro "refactor the logging module"
deepseek-code --model flash "quick fix for the typo"
```

| Flag | Values | Description |
|------|--------|-------------|
| `--model <name>` | `pro`, `flash`, or a full model ID | Model to use |

Per the ground truth, the named shortcuts map to the DeepSeek V4 backend:

- **Pro** — DeepSeek V4 Pro 1.6T
- **Flash** — DeepSeek V4 Flash 284B

You may also pass a full model ID (for example `deepseek-v4-flash`, as seen in
the config file).

## Reasoning effort

Control how much effort the model spends:

```bash
deepseek-code --effort max "design a migration plan"
```

| Flag | Values | Default |
|------|--------|---------|
| `--effort <level>` | `low`, `medium`, `high`, `max` | `high` |

## Thinking / reasoning mode

```bash
deepseek-code --thinking max "trace this race condition"
```

| Flag | Values | Description |
|------|--------|-------------|
| `--thinking on\|off\|max` | `on`, `off`, `max` | Control reasoning mode |

## Fallback model

Automatically fall back to another model when the default is overloaded:

```bash
deepseek-code --model pro --fallback-model flash "do the task"
```

| Flag | Description |
|------|-------------|
| `--fallback-model <name>` | Auto-fallback when default overloaded |

## Defaults via environment / config

- `DEEPSEEK_CODE_MODEL` — sets the default model.
- The config file `model` / `effortLevel` / `thinking` fields set defaults.
  See [configuration.md](configuration.md).

> Verify exact model IDs and pricing in the official DeepSeek docs / run
> `deepseek-code --help`.
