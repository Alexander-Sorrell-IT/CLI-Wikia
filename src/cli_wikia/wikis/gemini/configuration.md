# Configuration

Gemini CLI is configured through three mechanisms that stack in a defined order:
**settings files** (`settings.json`), **environment variables** (including
`.env` files), and **command-line arguments**. This page covers the file
locations and precedence. For the full field catalog see [settings.md](./settings.md);
for env vars see [environment-variables.md](./environment-variables.md).

---

## Configuration layers (precedence)

Lower numbers are overridden by higher numbers:

1. **Default values** — hardcoded application defaults.
2. **System defaults file** — system-wide base layer (lowest-precedence file).
3. **User settings file** — `~/.gemini/settings.json`.
4. **Project settings file** — `.gemini/settings.json` in the project root.
5. **System settings file** — system-wide *overrides* (highest-precedence file).
6. **Environment variables** — including values from `.env` files.
7. **Command-line arguments** — win for that session.

Note the deliberate split: the **system *defaults*** file sits at the bottom so
admins can suggest defaults, while the **system *settings*** file sits above
user and project files so admins can enforce non-overridable policy. See
[enterprise.md](./enterprise.md).

---

## Settings file locations

| File | Location | Scope |
|---|---|---|
| System defaults | `/etc/gemini-cli/system-defaults.json` (Linux), `C:\ProgramData\gemini-cli\system-defaults.json` (Windows), `/Library/Application Support/GeminiCli/system-defaults.json` (macOS) | Base defaults for all users. Override path with `GEMINI_CLI_SYSTEM_DEFAULTS_PATH`. |
| User | `~/.gemini/settings.json` | All sessions for the current user. |
| Project | `.gemini/settings.json` in the project root | Only when running from that project. |
| System | `/etc/gemini-cli/settings.json` (Linux), `C:\ProgramData\gemini-cli\settings.json` (Windows), `/Library/Application Support/GeminiCli/settings.json` (macOS) | All users, all sessions — enforced overrides. Override path with `GEMINI_CLI_SYSTEM_SETTINGS_PATH`. |

JSON-aware editors get autocomplete and validation by referencing the schema:

```
https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json
```

Settings are organized into top-level **category objects** (`general`, `ui`,
`model`, `context`, `tools`, `mcp`, `security`, `advanced`, …). Each setting
must be placed inside its category. The complete reference is in
[settings.md](./settings.md).

```json
{
  "general": { "vimMode": true },
  "ui": { "theme": "GitHub Dark" },
  "model": { "name": "gemini-2.5-pro" },
  "context": { "fileName": "GEMINI.md" }
}
```

---

## The `.gemini` directory

A project's `.gemini/` directory holds project-scoped Gemini CLI files:

| Path | Purpose |
|---|---|
| `.gemini/settings.json` | Project settings |
| `.gemini/.env` | Project env vars (never excluded — see below) |
| `.gemini/commands/*.toml` | [Custom slash commands](./custom-commands.md) |
| `.gemini/agents/` | Local [subagents](./subagents.md) |
| `.gemini/sandbox-macos-<name>.sb`, `.gemini/sandbox.Dockerfile` | Custom [sandbox](./sandboxing.md) profiles |
| `GEMINI.md` | Project [context file](./context-files.md) |

---

## Environment variables in settings

String values in `settings.json` (and `gemini-extension.json`) can reference
environment variables, resolved when settings load:

| Syntax | Meaning |
|---|---|
| `$VAR_NAME` | Value of the variable |
| `${VAR_NAME}` | Value of the variable |
| `${VAR_NAME:-default}` | Value if set, otherwise `default` |

```json
{ "mcpServers": { "api": { "httpUrl": "https://api.example.com", "headers": { "Authorization": "Bearer ${API_TOKEN}" } } } }
```

### `.env` file loading order

1. `.env` in the current working directory.
2. Searching upward through parent directories until an `.env` is found, or the
   project root (`.git`) or home directory is reached.
3. Otherwise `~/.env`.

`DEBUG` and `DEBUG_MODE` are automatically **excluded** from project `.env`
files (so they don't interfere with the CLI), but variables in a
`.gemini/.env` file are **never** excluded. Customize the exclusion list with
the `advanced.excludedEnvVars` setting.

See [environment-variables.md](./environment-variables.md) for the full list.

---

## Command-line arguments

CLI flags override everything else for that session — e.g. `--model`,
`--approval-mode`, `--sandbox`, `--include-directories`. See
[cli-reference.md](./cli-reference.md).

---

## Shell history

Shell commands run inside the CLI are recorded per project at
`~/.gemini/tmp/<project_hash>/shell_history`, where `<project_hash>` is derived
from the project's root path.

---

## See also

- [settings.md](./settings.md) — every `settings.json` field, by category
- [environment-variables.md](./environment-variables.md) — all env vars and `.env` rules
- [cli-reference.md](./cli-reference.md) — command-line flags
- [context-files.md](./context-files.md) — `GEMINI.md` hierarchical context
- [enterprise.md](./enterprise.md) — locking config via system settings
