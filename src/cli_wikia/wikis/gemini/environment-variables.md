# Environment Variables

Gemini CLI reads a number of environment variables for authentication, model
selection, telemetry, sandboxing, and behavior overrides. Env vars sit above
settings files but below command-line flags in [precedence](./configuration.md).
They can be exported in your shell profile or placed in an `.env` file (see
loading order below).

---

## Authentication & API access

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | API key for the Gemini API (one of several auth methods). |
| `GOOGLE_API_KEY` | Google Cloud API key — required for Vertex AI **express mode**. |
| `GOOGLE_CLOUD_PROJECT` | Google Cloud project ID — required for Code Assist or Vertex AI. In Cloud Shell, defaults to a special project unless set in `.env`. |
| `GOOGLE_CLOUD_LOCATION` | Vertex AI region (e.g. `us-central1`) — required for non-express Vertex AI. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a service-account credentials JSON file. |
| `GOOGLE_GENAI_API_VERSION` | Override the Gemini API version used by the SDK (e.g. `v1`). |
| `GOOGLE_GEMINI_BASE_URL` | Override the Gemini API base URL (HTTPS, or localhost). |
| `GOOGLE_VERTEX_BASE_URL` | Override the Vertex AI base URL (HTTPS, or localhost). |
| `CODE_ASSIST_ENDPOINT` | Code Assist server endpoint (dev/testing). |

See [getting-started.md](./getting-started.md) for choosing an auth method.

## Model

| Variable | Purpose |
|---|---|
| `GEMINI_MODEL` | Default model, overriding the built-in default (e.g. `gemini-3-flash-preview`). |

## Paths & storage

| Variable | Purpose |
|---|---|
| `GEMINI_CLI_HOME` | Root directory for user-level config/storage (the `.gemini` folder is created inside). Useful for shared/CI environments. |
| `GEMINI_CONFIG_DIR` | Custom directory for user-level configuration. *(verify in official docs)* |
| `GEMINI_CLI_SYSTEM_SETTINGS_PATH` | Override the system settings file path. |
| `GEMINI_CLI_SYSTEM_DEFAULTS_PATH` | Override the system defaults file path. |
| `GEMINI_CLI_TRUSTED_FOLDERS_PATH` | Override the `trustedFolders.json` location. |

## Trust & IDE

| Variable | Purpose |
|---|---|
| `GEMINI_CLI_TRUST_WORKSPACE` | `"true"` trusts the current workspace for the session (good for CI). See [permissions.md](./permissions.md). |
| `GEMINI_CLI_IDE_PID` | Manually bind to a specific IDE process PID. See [ide-integration.md](./ide-integration.md). |

## Sandboxing & system prompt

| Variable | Purpose |
|---|---|
| `GEMINI_SANDBOX` | `true`, `false`, `docker`, `podman`, or a custom command — equivalent to the `sandbox` setting. See [sandboxing.md](./sandboxing.md). |
| `SEATBELT_PROFILE` | macOS Seatbelt profile: `permissive-open` (default), `restrictive-open`, `strict-open`, `strict-proxied`, or a custom profile name. |
| `GEMINI_SYSTEM_MD` | Replace the built-in system prompt with a Markdown file (`true`/`1` → `./.gemini/system.md`, or a path). See [headless.md](./headless.md). |
| `GEMINI_WRITE_SYSTEM_MD` | Write the current built-in system prompt to a file for review. |

## Telemetry

All override the corresponding `telemetry.*` settings — see [enterprise.md](./enterprise.md).

| Variable | Purpose |
|---|---|
| `GEMINI_TELEMETRY_ENABLED` | `true`/`1` to enable telemetry. |
| `GEMINI_TELEMETRY_TARGET` | `local` or `gcp`. |
| `GEMINI_TELEMETRY_OTLP_ENDPOINT` | OTLP endpoint. |
| `GEMINI_TELEMETRY_OTLP_PROTOCOL` | `grpc` or `http`. |
| `GEMINI_TELEMETRY_TRACES_ENABLED` | Detailed tracing with large attributes. |
| `GEMINI_TELEMETRY_LOG_PROMPTS` | Log user prompts. |
| `GEMINI_TELEMETRY_OUTFILE` | Output file when target is `local`. |
| `GEMINI_TELEMETRY_USE_COLLECTOR` | Use an external OTLP collector. |
| `OTLP_GOOGLE_CLOUD_PROJECT` | GCP project for telemetry export. |

## Behavior, UI, networking

| Variable | Purpose |
|---|---|
| `GEMINI_CLI` | Set to `1` automatically inside `!` shell commands so scripts can detect they're running under Gemini CLI. |
| `GEMINI_CLI_SURFACE` | Custom label added to the `User-Agent` header. |
| `DEBUG` / `DEBUG_MODE` | Verbose debug logging. **Excluded from project `.env` files** by default; use `.gemini/.env`. |
| `NO_COLOR` | Disable all color output. |
| `CLI_TITLE` | Customize the CLI window title. |
| `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` | Standard proxy configuration for outbound requests. |

---

## `.env` file loading

The CLI loads the first `.env` it finds:

1. `.env` in the current working directory.
2. Searching upward through parent directories until it reaches the project root
   (`.git`) or the home directory.
3. Otherwise `~/.env`.

Extensions may each ship their own `.env`. Variables in a `.gemini/.env` file are
**never excluded** (unlike `DEBUG`/`DEBUG_MODE` in a plain project `.env`).

## Secret redaction

When running tools (e.g. shell commands), Gemini CLI makes a best-effort attempt
to **redact secrets** from inherited environment variables:

- **By name** — variables containing `TOKEN`, `SECRET`, `PASSWORD`, `KEY`,
  `AUTH`, `CREDENTIAL`, `PRIVATE`, `CERT`.
- **By value** — private keys, certificates, credential-bearing URLs, and known
  API-key/token patterns (GitHub, Google, AWS, Stripe, Slack, …).
- **Always redacted** — `CLIENT_ID`, `DB_URI`, `DATABASE_URL`, `CONNECTION_STRING`.
- **Never redacted** — common system vars (`PATH`, `HOME`, `USER`, `SHELL`,
  `TERM`, `LANG`), anything starting with `GEMINI_CLI_`, and GitHub Actions vars.

Tune this with `security.allowedEnvironmentVariables` /
`security.blockedEnvironmentVariables` (a.k.a.
`security.environmentVariableRedaction.allowed` / `blocked`) in
[settings.json](./settings.md):

```json
{
  "security": {
    "allowedEnvironmentVariables": ["MY_PUBLIC_KEY", "NOT_A_SECRET_TOKEN"],
    "blockedEnvironmentVariables": ["INTERNAL_IP_ADDRESS"]
  }
}
```

---

## Referencing env vars inside settings

`settings.json` values support `$VAR`, `${VAR}`, and `${VAR:-default}`
expansion. See [configuration.md](./configuration.md).

---

## See also

- [configuration.md](./configuration.md) — layers, precedence, `.env` rules
- [settings.md](./settings.md) — settings equivalents of these variables
- [getting-started.md](./getting-started.md) — authentication setup
- [sandboxing.md](./sandboxing.md) — `GEMINI_SANDBOX`, `SEATBELT_PROFILE`
- [enterprise.md](./enterprise.md) — telemetry configuration
