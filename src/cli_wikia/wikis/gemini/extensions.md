# Extensions

Gemini CLI extensions package prompts, MCP servers, custom commands, context files, themes, hooks, sub-agents, agent skills, and policies into a single shareable bundle. They make capabilities easy to install, version, and distribute. Browse the [extension gallery](https://geminicli.com/extensions/browse/) to see what's available.

Manage extensions from your shell with the `gemini extensions` command group. Inside an interactive session, use `/extensions list` to view installed extensions; most management operations are **not** available in interactive mode and take effect only after restarting the session.

---

## What an extension can bundle

| Feature | What it is | Invoked by |
|---|---|---|
| **MCP servers** | Expose new tools and data sources to the model (`mcpServers` in the manifest). | Model |
| **Context file (`GEMINI.md`)** | Markdown instructions loaded into the model's context every session. | CLI → model |
| **Custom commands** | Slash-command shortcuts (`.toml` files under `commands/`). | User |
| **Agent skills** | Specialized workflows activated only when relevant (`skills/<name>/SKILL.md`). | Model |
| **Hooks** | Intercept lifecycle events, e.g. before/after a tool call (`hooks/hooks.json`). | CLI |
| **Sub-agents** (preview) | Delegatable agents defined as `.md` files under `agents/`. | Model/User |
| **Policies** | Policy Engine rules and safety checkers (`.toml` files under `policies/`). | CLI |
| **Themes** | Custom UI color schemes (`themes` array in the manifest). | User (`/theme`) |

---

## Installing extensions

Install from a GitHub repository URL or a local path. Gemini CLI copies the extension at install time; pull later changes with `gemini extensions update`. Installing from GitHub requires `git`.

```bash
gemini extensions install <source> [--ref <ref>] [--auto-update] \
  [--pre-release] [--consent] [--skip-settings]
```

| Flag | Description |
|---|---|
| `--ref <ref>` | Install a specific git ref (branch, tag, or commit). |
| `--auto-update` | Enable automatic updates for this extension. |
| `--pre-release` | Allow installing pre-release versions. |
| `--consent` | Acknowledge security risks and skip the confirmation prompt. |
| `--skip-settings` | Skip the configure-on-install step. |

```bash
# From GitHub (default branch)
gemini extensions install https://github.com/gemini-cli-extensions/workspace

# Pin to a branch / tag / commit
gemini extensions install github.com/user/repo --ref dev

# From a local path
gemini extensions install ./my-extension
```

Extensions are loaded from `<home>/.gemini/extensions`. When the CLI starts it loads all extensions and merges their configs; on conflict, workspace configuration takes precedence.

---

## Managing extensions

| Command | Description |
|---|---|
| `gemini extensions list` | List installed extensions and their status (also `/extensions list` in-session). |
| `gemini extensions install <source> [flags]` | Install an extension. |
| `gemini extensions uninstall <name...>` | Uninstall one or more extensions. |
| `gemini extensions update <name>` | Update one extension to its manifest version. |
| `gemini extensions update --all` | Update all installed extensions. |
| `gemini extensions disable <name> [--scope <scope>]` | Disable an extension (globally or per-workspace). |
| `gemini extensions enable <name> [--scope <scope>]` | Re-enable a disabled extension. |
| `gemini extensions new <path> [template]` | Scaffold a new extension from a template. |
| `gemini extensions link <path>` | Symlink a dev directory for local testing. |
| `gemini extensions config <name> [setting] [--scope <scope>]` | View/update an extension's settings. |

For `enable`/`disable`/`config`, `--scope` is `user` or `workspace`. Extensions are enabled globally by default.

> The `mcp-server`, `context`, and `custom-commands` templates are available to `gemini extensions new`, e.g. `gemini extensions new my-ext mcp-server`.

---

## Local development with `link`

`gemini extensions link <path>` symlinks your development directory into the extensions directory, so code changes are picked up after a rebuild + restart — no reinstall needed.

```bash
cd my-extension
npm install
gemini extensions link .
```

Verify tools appear in the debug console (**F12**) and that custom commands resolve. Restart the session after manifest changes.

---

## The manifest: `gemini-extension.json`

Every extension has a `gemini-extension.json` in its root.

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "description": "My awesome extension",
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${extensionPath}/my-server.js"],
      "cwd": "${extensionPath}"
    }
  },
  "contextFileName": "GEMINI.md",
  "excludeTools": ["run_shell_command"],
  "migratedTo": "https://github.com/new-owner/new-extension-repo",
  "plan": {
    "directory": ".gemini/plans"
  }
}
```

| Field | Description |
|---|---|
| `name` | Unique identifier; used for command conflict resolution. Lowercase/numbers with dashes (no underscores or spaces). Should match the extension directory name. |
| `version` | Extension version. |
| `description` | Short description shown on geminicli.com/extensions. |
| `mcpServers` | Map of MCP servers (same shape as `settings.json`). Loaded on startup. |
| `contextFileName` | Name of the context file to load (defaults to `GEMINI.md` if present). |
| `excludeTools` | Tool names to hide from the model; supports command-specific restrictions for `run_shell_command`. |
| `migratedTo` | New repo URL; the CLI checks it for updates and migrates the install. |
| `plan.directory` | Fallback directory for planning artifacts. |
| `settings` | Array of user-provided settings (see below). |
| `themes` | Array of custom theme definitions. |

### Notes on `mcpServers` in extensions

- All MCP server config options are supported **except `trust`** (an extension can't auto-trust itself).
- Use `${extensionPath}` for files inside the extension so the config stays portable.
- Keep the executable in `command` and its arguments in `args` (don't combine them).
- If both an extension and `settings.json` define a server with the same name, the `settings.json` definition wins.

### `excludeTools` vs MCP server `excludeTools`

The manifest's top-level `excludeTools` blocks built-in tools (and supports argument-level blocks like `"run_shell_command(rm -rf)"`). This is distinct from the `excludeTools` inside an MCP server config, which filters that server's tools.

---

## Variables

Gemini CLI substitutes these in `gemini-extension.json` and `hooks/hooks.json`:

| Variable | Description |
|---|---|
| `${extensionPath}` | Absolute path to the extension's directory. |
| `${workspacePath}` | Absolute path to the current workspace. |
| `${/}` | Platform-specific path separator. |

```json
"args": ["${extensionPath}${/}example.js"]
```

---

## Extension settings

Settings let an extension collect values (API keys, URLs) from the user at install time. They're stored in a `.env` file in the extension directory, or in the system keychain when marked sensitive.

```json
{
  "name": "my-api-extension",
  "version": "1.0.0",
  "settings": [
    {
      "name": "API Key",
      "description": "Your API key for the service.",
      "envVar": "MY_API_KEY",
      "sensitive": true
    }
  ]
}
```

| Field | Description |
|---|---|
| `name` | Display name of the setting. |
| `description` | Explanation shown to the user. |
| `envVar` | Environment variable the value is exposed as. |
| `sensitive` | If `true`, stored in the system keychain and obfuscated in the UI. |

Update settings later with:

```bash
gemini extensions config <name> [setting] [--scope <scope>]
```

### Environment variable sanitization

For security, extensions do **not** inherit the full shell environment. They get only:

1. Standard safe variables (e.g. `HOME`, `PATH`, `TMPDIR`).
2. Variables declared in the `settings` array via `envVar`.

If your extension's MCP server needs an env var (API key, host, config path), you **must** declare it in `settings` so the CLI allowlists it.

---

## Custom commands

Place `.toml` files in a `commands/` subdirectory; the directory layout sets the command name. For an extension named `gcp`:

- `commands/deploy.toml` → `/deploy`
- `commands/gcs/sync.toml` → `/gcs:sync` (colon-namespaced)

```toml
# commands/fs/grep-code.toml  →  /fs:grep-code
prompt = """
Please summarize the findings for the pattern `{{args}}`.

Search Results:
!{grep -r {{args}} .}
"""
```

`{{args}}` injects arguments; `!{...}` runs a shell command and pipes its output into the prompt.

### Command conflict resolution

Extension commands have the lowest precedence. If an extension command name collides with a user or project command, the extension version is prefixed with the extension name using a dot, e.g. `/gcp.deploy`. Run `/help` to see all commands and their sources.

---

## Context, skills, hooks, sub-agents, policies, themes

- **Context** — a `GEMINI.md` in the extension root is loaded into every session where the extension is active. Set `contextFileName` to use a different filename. Keep it concise and goal-focused.
- **Agent skills** — `skills/<name>/SKILL.md` (with YAML frontmatter `name`/`description`) is auto-discovered and activated by the model when relevant.
- **Hooks** — defined in `hooks/hooks.json` (not in the manifest), intercept lifecycle events.
- **Sub-agents** (preview) — `.md` definition files under `agents/`.
- **Policies** — `.toml` files under `policies/` contribute Policy Engine rules and safety checkers. They run in tier 2 (above defaults, below user/admin policies). For security, any `allow` decisions or `yolo` configs in extension policies are **ignored** — an extension cannot auto-approve tool calls.
- **Themes** — defined in the manifest `themes` array; selected via `/theme` or `ui.theme`. An extension theme is shown with the extension name in parentheses, e.g. `shades-of-green (my-green-extension)`.

```toml
# policies/policies.toml
[[rule]]
mcpName = "my_server"
toolName = "dangerous_tool"
decision = "ask_user"
priority = 100
```

---

## Recommended structure

```text
my-extension/
├── package.json
├── tsconfig.json
├── gemini-extension.json
├── GEMINI.md
├── commands/
├── skills/
├── src/
│   ├── index.ts
│   └── tools/
└── dist/
```

- **Use TypeScript** for type safety; keep source in `src/`, build output in `dist/`.
- **Bundle dependencies** (e.g. with `esbuild`) to speed installs and avoid conflicts.

---

## Security best practices

- **Least privilege** — request only the tools the server needs; avoid broad access like full shell.
- **Restrict dangerous tools** in the manifest, e.g. `"excludeTools": ["run_shell_command(rm -rf *)"]`.
- **Validate tool inputs** — the server runs on the user's machine; guard against path traversal and arbitrary execution.
- **Mark secrets `sensitive: true`** so they live in the keychain.

---

## Releasing

- **Semantic versioning** — major (breaking, e.g. renamed tools/args), minor (new tools/commands), patch (fixes).
- **Release channels via git branches** — users pick stability with `--ref`:

  ```bash
  gemini extensions install github.com/user/repo          # stable (default branch)
  gemini extensions install github.com/user/repo --ref dev # development
  ```

- **Clean artifacts** — for GitHub Releases, ship only `dist/`, `gemini-extension.json`, and `package.json`; exclude `node_modules/` and `src/`.
- **Test** — verify with `gemini extensions link` in a live session; for MCP servers, unit-test tool logic (Vitest/Jest) by mocking the transport.

---

## Troubleshooting

| Symptom | Things to check |
|---|---|
| Extension not in `/extensions list` | `gemini-extension.json` is valid JSON in the root; `name` matches the directory name; restart the CLI. |
| MCP server/tools not working | Check CLI logs for startup failure; run the server's `command`+`args` directly; open the debug console (**F12**) to inspect calls. |
| Custom command not responding | User/project commands take precedence — try the prefixed `/extension.command`; run `/help` to list sources. |

---

## See also

- [mcp.md](./mcp.md) — MCP server configuration and the `gemini mcp` commands
- [configuration.md](./configuration.md) — `settings.json` and scopes
- [cli-reference.md](./cli-reference.md) — full command and flag reference
