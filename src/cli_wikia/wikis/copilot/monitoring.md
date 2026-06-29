# Monitoring (OpenTelemetry)

Copilot CLI can export **OpenTelemetry** traces and metrics covering agent interactions, LLM calls, tool executions, and token usage. Names and attributes follow the OTel **GenAI Semantic Conventions**, so the data works with any OTel backend (Jaeger, Grafana, Datadog, Honeycomb, Langfuse, Azure Monitor, …).

Reference: `copilot help monitoring`.

---

## Enabling

OTel is off by default. It activates when **any** of these is true:

- `COPILOT_OTEL_ENABLED=true`
- `OTEL_EXPORTER_OTLP_ENDPOINT` is set
- `COPILOT_OTEL_FILE_EXPORTER_PATH` is set

```bash
# OTLP/HTTP to a local collector (e.g. Jaeger)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 copilot

# File output for offline / CI
COPILOT_OTEL_FILE_EXPORTER_PATH=/tmp/copilot-otel.jsonl copilot
```

---

## Key variables

| Variable | Purpose |
|---|---|
| `COPILOT_OTEL_ENABLED` | Explicitly enable OTel |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint URL (auto-enables OTel) |
| `COPILOT_OTEL_EXPORTER_TYPE` | `otlp-http` (default) or `file` |
| `COPILOT_OTEL_FILE_EXPORTER_PATH` | JSON-lines output file (auto-enables OTel) |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/json` (default) or `http/protobuf` (`grpc` unsupported) |
| `COPILOT_OTEL_SOURCE_NAME` | Instrumentation scope name (default `github.copilot`) |
| `OTEL_SERVICE_NAME` | Service name (default `github-copilot`) |
| `OTEL_RESOURCE_ATTRIBUTES` | Extra `key=value` resource attributes |
| `OTEL_EXPORTER_OTLP_HEADERS` | Auth headers (e.g. `Authorization=Bearer …`) |
| `OTEL_LOG_LEVEL` | OTel diagnostic level (separate from `--log-level`): `NONE`…`ALL` |

### TLS / mTLS for the collector

| Variable | Purpose |
|---|---|
| `OTEL_EXPORTER_OTLP_CERTIFICATE` | Extra CA PEM to trust (merged with the OS store) |
| `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` / `_CLIENT_KEY` | mTLS client cert + unencrypted key (both required together) |

Client-cert/CA settings require an **`https://`** endpoint — configuring them against `http://` fails startup rather than exporting in cleartext. Per-signal `_TRACES_` / `_METRICS_` overrides exist for protocol, certificate, and client-cert variables. Note: `NODE_EXTRA_CA_CERTS` does **not** affect the OTLP exporter (it uses a native Rust transport).

---

## What gets exported

**Traces** — a span tree per agent interaction:

```
invoke_agent                 Agent orchestration (all LLM calls + tool executions)
  plan                       Plan-mode task decomposition
    chat <model>             LLM calls used to generate the plan
    execute_tool <tool>      Tool calls used while planning
  chat <model>               Individual LLM API call
  execute_tool <tool>        Individual tool invocation
```

Spans carry model name, token counts, durations, costs, and error info. Subagent invocations are linked into the same trace via context propagation.

**Metrics:**

| Metric | Meaning |
|---|---|
| `gen_ai.client.operation.duration` | LLM/agent call duration |
| `gen_ai.client.token.usage` | Token counts by type |
| `gen_ai.invoke_agent.duration` | Agent invocation duration |
| `gen_ai.execute_tool.duration` | Tool execution duration |
| `github.copilot.tool.call.count` | Tool invocations |
| `github.copilot.tool.call.duration` | Tool execution latency |
| `github.copilot.agent.turn.count` | LLM round-trips per invocation |

---

## Content capture

By default only metadata is exported — no prompts, responses, or tool arguments. Set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` to also capture full messages, system instructions, tool definitions, and tool call args/results.

> **Warning:** content capture may include source code, file contents, and user prompts. Only enable it in trusted environments.

---

## See also

- [logging.md](logging.md) — local CLI logs (different from OTel)
- [billing.md](billing.md) — usage and AI credits
- [environment-variables.md](environment-variables.md) — all OTel vars
