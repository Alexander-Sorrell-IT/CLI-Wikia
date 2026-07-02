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

## Sources

- GitHub Copilot CLI official docs: <https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli> and <https://github.com/github/copilot-cli> (Accessed 2026-07-02)
- Core pages of this wiki (hooks, configuration, cli-reference, custom-instructions, mcp, permissions) were re-verified against the official docs and the installed `copilot` CLI 1.0.68 on 2026-07-02; this page has not been individually re-verified since — confirm details against the official docs above.
