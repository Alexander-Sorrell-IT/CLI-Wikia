# Configuration (OpenAI / ChatGPT CLI)

The `openai` CLI is configured mainly through environment variables, with
command-line flags overriding them per call.

## Authentication

```bash
export OPENAI_API_KEY=sk-...
```

Or pass it inline (overrides the env var):

```bash
openai -k sk-... api models.list
```

> The API key is a secret. Prefer the environment variable over `-k` on the
> command line (which can leak into shell history and process listings).

## Common environment variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Your API key |
| `OPENAI_BASE_URL` | Override the API base URL (also `-b/--api-base`) |
| `OPENAI_ORG_ID` / `--organization` | Run under a specific organization |

> Exact env var names can vary by SDK version — confirm against the installed
> OpenAI Python SDK docs (`openai 2.24.0` here).

## Pointing at a different backend

The CLI can target OpenAI or Azure OpenAI:

```bash
# Custom/self-hosted compatible endpoint
openai -b https://my-endpoint/v1 api chat.completions.create -m my-model -g user "hi"

# Azure OpenAI
openai -t azure \
  --azure-endpoint https://endpoint.openai.azure.com \
  --api-version 2024-xx-xx \
  api chat.completions.create -m <deployment> -g user "hi"
```

| Flag | Description |
|------|-------------|
| `-t/--api-type {openai,azure}` | Choose backend |
| `--azure-endpoint <url>` | Azure resource endpoint |
| `--api-version <ver>` | Azure API version |
| `--azure-ad-token <token>` | Azure AD token instead of API key |
| `-p/--proxy <proxy...>` | Route through a proxy |

See [cli-reference.md](./cli-reference.md) for all global flags.
