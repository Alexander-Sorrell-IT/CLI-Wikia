# Logging

Copilot CLI writes local logs you can use to diagnose a session. This is separate from [OpenTelemetry monitoring](monitoring.md), which exports structured traces/metrics to a backend.

Reference: `copilot help logging`.

---

## Where logs go

By default logs are written to `~/.copilot/logs/`. Change the directory per run:

```bash
copilot --log-dir ./logs
```

---

## Log levels

Set with `--log-level <level>` or the `logLevel` setting:

| Level | Output |
|---|---|
| `none` | Nothing |
| `error` | Errors only |
| `warning` | Errors + warnings |
| `info` | Errors + warnings + info |
| `debug` | Everything, including debug |
| `all` | Same as `debug` |
| `default` | Same as `info` (errors + warnings + info) |

```bash
copilot --log-level debug
```

In `settings.json`, set `logLevel` to `all` for persistent debug logging.

---

## Diagnosing a session

Inside a session, `/diagnose` analyzes the current session log (optionally with a custom prompt) to help explain what happened or why something failed.

---

## Note on OTel diagnostics

`OTEL_LOG_LEVEL` is a **separate** diagnostic level for the OpenTelemetry exporter (`NONE`…`ALL`) and does not affect the CLI's `--log-level`. See [monitoring.md](monitoring.md).

---

## See also

- [monitoring.md](monitoring.md) — OpenTelemetry traces and metrics
- [configuration.md](configuration.md) — the `logLevel` setting
