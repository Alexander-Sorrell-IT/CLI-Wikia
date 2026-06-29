# Environment Variables

Full list from `copilot help environment`. Many mirror a CLI flag or `settings.json` key; the env var usually takes precedence for the current process.

---

## Authentication & host

| Variable | Purpose |
|---|---|
| `COPILOT_GITHUB_TOKEN` | Auth token (highest precedence). Use a fine-grained PAT with *Copilot Requests* |
| `GH_TOKEN` | Auth token (second precedence) |
| `GITHUB_TOKEN` | Auth token (third precedence) |
| `GH_HOST` | GitHub hostname for auth/API; defaults to `github.com`. Set to your GHE Cloud data-residency host (e.g. `mycompany.ghe.com`) |
| `COPILOT_GH_HOST` | Host used **only** by Copilot CLI, overriding `GH_HOST` |

## Core behavior

| Variable | Purpose |
|---|---|
| `COPILOT_HOME` | Override the config/state dir (default `$HOME/.copilot`) |
| `COPILOT_ALLOW_ALL` | `true` = allow all tools automatically (same as `--allow-all-tools`) |
| `COPILOT_MODEL` | Default model (overridden by `--model` / `/model`) |
| `COPILOT_AUTO_UPDATE` | `false` disables auto-update. Off by default in CI |
| `COPILOT_OFFLINE` | `true` = offline mode: skips GitHub auth, telemetry, web tools, GitHub MCP, and auto-update. Requires a local provider (`COPILOT_PROVIDER_BASE_URL`) |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Comma-separated extra dirs to search for instruction files (beyond git root and cwd) |
| `COPILOT_EDITOR` / `VISUAL` / `EDITOR` | Editor for interactive editing (e.g. the plan), in that precedence |

## Custom model providers (BYOK)

See [providers-byok.md](providers-byok.md) for the full story.

| Variable | Purpose |
|---|---|
| `COPILOT_PROVIDER_BASE_URL` | Provider endpoint URL — **activates BYOK** (GitHub auth not required) |
| `COPILOT_PROVIDER_TYPE` | `openai` (default), `azure`, or `anthropic` |
| `COPILOT_PROVIDER_API_KEY` | Provider API key (optional for local providers) |
| `COPILOT_PROVIDER_BEARER_TOKEN` | Bearer token (takes precedence over the API key) |
| `COPILOT_PROVIDER_WIRE_API` | `completions` (default) or `responses` (GPT-5 series) |
| `COPILOT_PROVIDER_TRANSPORT` | `http` (default) or `websockets` |
| `COPILOT_PROVIDER_AZURE_API_VERSION` | Azure API version (default: versionless v1) |
| `COPILOT_PROVIDER_MODEL_ID` | Well-known model ID for agent config & token limits |
| `COPILOT_PROVIDER_WIRE_MODEL` | Model name sent to the provider for inference |
| `COPILOT_PROVIDER_MAX_PROMPT_TOKENS` | Override max prompt tokens |
| `COPILOT_PROVIDER_MAX_OUTPUT_TOKENS` | Override max output tokens |

## Networking & proxy

| Variable | Purpose |
|---|---|
| `HTTP_PROXY` / `HTTPS_PROXY` | Proxy for HTTP/HTTPS (case-insensitive); overrides `proxyUrl` |
| `NO_PROXY` | Comma-separated hosts that bypass the proxy |
| `COPILOT_PROXY_KERBEROS_SPN` | Kerberos/Negotiate SPN for proxy auth |

## Terminal & rendering

| Variable | Purpose |
|---|---|
| `NO_COLOR` | Any value disables color (<https://no-color.org>) |
| `COLORFGBG` | `fg;bg` hint for dark/light background detection |
| `PLAIN_DIFF` | `true` disables rich diff rendering |
| `COPILOT_DISABLE_TERMINAL_TITLE` | Disable terminal-title updates |

## Search engine

| Variable | Purpose |
|---|---|
| `USE_BUILTIN_RIPGREP` | `false` = use `rg` from PATH instead of the bundled one |
| `USE_TGREP` | Force tgrep indexed search on/off regardless of repo size |
| `USE_TGREP_WARM_START` | `true` blocks startup until the tgrep index is ready |

## OpenTelemetry / monitoring

The CLI exports OTel traces/metrics. Detailed in [monitoring.md](monitoring.md).

| Variable | Purpose |
|---|---|
| `COPILOT_OTEL_ENABLED` | `true` enables OTel |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint (setting it auto-enables OTel) |
| `COPILOT_OTEL_EXPORTER_TYPE` | `otlp-http` (default) or `file` |
| `COPILOT_OTEL_FILE_EXPORTER_PATH` | JSON-lines file output (auto-enables OTel) |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/json` (default) or `http/protobuf` |
| `COPILOT_OTEL_SOURCE_NAME` | Instrumentation scope name (default `github.copilot`) |
| `OTEL_SERVICE_NAME` | Service name (default `github-copilot`) |
| `OTEL_RESOURCE_ATTRIBUTES` | Extra `key=value` resource attributes |
| `OTEL_EXPORTER_OTLP_HEADERS` | Auth headers for the exporter |
| `OTEL_EXPORTER_OTLP_CERTIFICATE` | CA PEM to trust (merged with OS store) |
| `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` / `_CLIENT_KEY` | mTLS client cert + key (both required) |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | `true` captures full prompts/responses/tool args (sensitive) |
| `OTEL_LOG_LEVEL` | OTel diagnostic level: `NONE`…`ALL` |

(Per-signal `_TRACES_`/`_METRICS_` variants exist for protocol, certificate, and client-cert variables.)

---

## See also

- [providers-byok.md](providers-byok.md) — BYOK in depth
- [configuration.md](configuration.md) — the `settings.json` equivalents
- [monitoring.md](monitoring.md) — what OTel exports
