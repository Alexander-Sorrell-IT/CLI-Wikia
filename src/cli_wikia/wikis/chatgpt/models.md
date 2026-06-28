# Models (OpenAI / ChatGPT)

## Selecting a model

Every API call takes `-m / --model`:

```bash
openai api chat.completions.create -m gpt-4o -g user "hello"
```

## Listing available models

The authoritative, always-current list comes from the API itself:

```bash
openai api models.list          # all models your key can access
openai api models.retrieve -i gpt-4o   # details for one model
```

## Common model families

OpenAI's lineup changes often. As a rough guide (verify with `models.list`):

| Family | Typical use |
|--------|-------------|
| `gpt-4o` / `gpt-4o-mini` | General chat, multimodal, fast/cheap (mini) |
| `gpt-4.1` family | Stronger reasoning / longer context |
| `o`-series (reasoning) | Step-by-step reasoning tasks |
| `gpt-3.5-turbo` | Legacy, low cost |

> Exact model IDs, context windows, and pricing change frequently. **Do not
> rely on this table for specifics** — run `openai api models.list` and check
> the official OpenAI models documentation for current details.

## Tuning generation

- `-t/--temperature` — randomness (0 deterministic … ~0.9 creative)
- `-P/--top_p` — nucleus sampling (mutually exclusive with temperature)
- `-M/--max-tokens` — cap output length
- `-n/--n` — number of completions
- `--stream` — stream tokens as generated

See [cli-reference.md](./cli-reference.md) for the full option list.
