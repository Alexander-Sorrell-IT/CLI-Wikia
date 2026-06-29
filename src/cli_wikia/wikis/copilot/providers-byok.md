# Custom Model Providers (BYOK)

Copilot CLI can bypass GitHub's model routing and talk directly to **your own** model provider — "bring your own key." This works with any OpenAI-compatible endpoint (including local servers like Ollama, vLLM, and Foundry Local), Azure OpenAI, and Anthropic.

Reference: `copilot help providers`.

---

## How it activates

Set `COPILOT_PROVIDER_BASE_URL`. Once set, the CLI uses your provider instead of GitHub's routing, and **GitHub authentication is not required**.

A model is also required — set `COPILOT_MODEL`, `COPILOT_PROVIDER_MODEL_ID`, or `--model`.

---

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `COPILOT_PROVIDER_BASE_URL` | — | Endpoint URL (required to activate BYOK) |
| `COPILOT_PROVIDER_TYPE` | `openai` | `openai`, `azure`, or `anthropic` |
| `COPILOT_PROVIDER_API_KEY` | — | API key (optional for local providers like Ollama) |
| `COPILOT_PROVIDER_BEARER_TOKEN` | — | Bearer token (takes precedence over the API key) |
| `COPILOT_PROVIDER_WIRE_API` | `completions` | `completions`, or `responses` for GPT-5 series |
| `COPILOT_PROVIDER_TRANSPORT` | `http` | `http` or `websockets` (use with `responses` for OpenAI Responses over WebSocket) |
| `COPILOT_PROVIDER_AZURE_API_VERSION` | versionless v1 | Azure API version; set e.g. `2024-10-21` for the legacy versioned route |

### Model identification

| Variable | Default | Purpose |
|---|---|---|
| `COPILOT_MODEL` | — | Simplest option — sets **both** the model ID and the wire model |
| `COPILOT_PROVIDER_MODEL_ID` | `COPILOT_MODEL` | Well-known base model name (e.g. `gpt-5.4`, `claude-sonnet-4`) used for agent config & token limits |
| `COPILOT_PROVIDER_WIRE_MODEL` | `COPILOT_MODEL` | The exact model name your provider expects (e.g. a fine-tune or Azure deployment) |
| `COPILOT_PROVIDER_MAX_PROMPT_TOKENS` | catalog/default | Override max prompt tokens |
| `COPILOT_PROVIDER_MAX_OUTPUT_TOKENS` | catalog/default | Override max output tokens |

**Why both IDs?** Matching a recognized `COPILOT_PROVIDER_MODEL_ID` lets the agent apply model-specific behavior (tool support, token limits, prompting strategy). Without a recognized ID it falls back to safe defaults. The wire model is what's actually sent for inference. Token limits resolve in order: manual env vars → built-in catalog → defaults.

---

## Examples

```bash
# Ollama (local, no API key)
COPILOT_PROVIDER_BASE_URL=http://localhost:11434/v1 \
  COPILOT_MODEL=deepseek-coder-v2:16b \
  copilot

# Any OpenAI-compatible endpoint
COPILOT_PROVIDER_BASE_URL=https://my-api.example.com/v1 \
  COPILOT_PROVIDER_API_KEY=sk-... \
  COPILOT_MODEL=gpt-4 \
  copilot

# Azure OpenAI with a custom deployment name
COPILOT_PROVIDER_TYPE=azure \
  COPILOT_PROVIDER_BASE_URL=https://my-resource.openai.azure.com \
  COPILOT_PROVIDER_API_KEY=your-key \
  COPILOT_PROVIDER_MODEL_ID=gpt-4 \
  COPILOT_PROVIDER_WIRE_MODEL=my-gpt4-deployment \
  copilot

# Anthropic
COPILOT_PROVIDER_TYPE=anthropic \
  COPILOT_PROVIDER_BASE_URL=https://api.anthropic.com \
  COPILOT_PROVIDER_API_KEY=sk-ant-... \
  COPILOT_MODEL=claude-sonnet-4-20250514 \
  copilot
```

---

## Notes & gotchas

- **Azure:** use type `azure` (not `openai`) and pass only the host URL — the SDK builds the full path.
- **GPT-5 series:** use `COPILOT_PROVIDER_WIRE_API=responses`; add `COPILOT_PROVIDER_TRANSPORT=websockets` for the Responses API over WebSocket.
- **Local/OpenAI-compatible:** Ollama, vLLM, and Foundry Local all use type `openai`.
- **Offline:** combine with `COPILOT_OFFLINE=true` for a fully local, no-network setup (GitHub auth, telemetry, web tools, GitHub MCP, and auto-update are all disabled).
- BYOK models do **not** participate in GitHub AI-credit billing or the `continueOnAutoMode` auto-switch.

---

## See also

- [environment-variables.md](environment-variables.md) — all env vars
- [models.md](models.md) — the GitHub-routed model catalog
- [cli-vs-api.md](cli-vs-api.md) — CLI vs programmatic API access
