# IDE Integration

Gemini CLI integrates with your editor through a companion extension, giving the CLI live workspace context and a native in-editor diff experience. There are two integration paths:

1. **VS Code companion extension** — for VS Code and compatible editors (Antigravity, Cursor, Windsurf, and other forks).
2. **Agent Client Protocol (ACP)** — an open protocol used by editors like JetBrains IDEs and Zed, which discover and install Gemini CLI via the ACP Agent Registry.

## What the integration provides

The **Gemini CLI Companion** extension gives the CLI real-time context and a native UI:

- **Workspace context** — the CLI automatically becomes aware of:
  - the **10 most recently accessed files** in your workspace (local files on disk only),
  - your active **cursor position**,
  - any **selected text** (up to 16 KB; longer selections are truncated).
- **Native diffing** — when Gemini suggests an edit, it opens in your IDE's native diff viewer. You can review, edit, accept, or reject the change in place.
- **VS Code commands** — available from the Command Palette (`Cmd/Ctrl+Shift+P`):

| Command | Action |
|---|---|
| `Gemini CLI: Run` | Start a new session in the integrated terminal |
| `Gemini CLI: Accept Diff` | Accept the changes in the active diff editor |
| `Gemini CLI: Close Diff Editor` | Reject the changes and close the diff editor |
| `Gemini CLI: View Third-Party Notices` | Show third-party notices |

## Installation

There are three ways to set up the VS Code integration.

### 1. Automatic nudge (recommended)

Run Gemini CLI inside a supported editor's integrated terminal. It detects the environment and prompts you to connect; answering **Yes** installs the companion extension and enables the connection automatically.

### 2. Manual install from the CLI

If you dismissed the prompt, run inside the CLI:

```
/ide install
```

This finds and installs the correct extension for your IDE.

### 3. Manual install from a marketplace

- **VS Code:** [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=google.gemini-cli-vscode-ide-companion)
- **VS Code forks:** [Open VSX Registry](https://open-vsx.org/extension/google/gemini-cli-vscode-ide-companion)

After a manual marketplace install, run `/ide enable` in the CLI to activate the integration. (The "Gemini CLI Companion" listing may appear low in search results — try sorting by "Newly Published".)

## The `/ide` command

| Command | Purpose |
|---|---|
| `/ide install` | Install the companion extension for the detected IDE |
| `/ide enable` | Enable and connect to the IDE companion |
| `/ide disable` | Disable the IDE connection |
| `/ide status` | Show connection status and the context received from the IDE |

When enabled, Gemini CLI automatically attempts to connect to the companion extension. `/ide status`, when connected, shows which IDE it is connected to and the list of recently opened files it is aware of (limited to 10 local files).

## Working with diffs

When you ask Gemini to modify a file, it can open a diff directly in the editor.

**Accept a diff** — click the checkmark in the diff title bar, save the file (`Cmd/Ctrl+S`), run **Gemini CLI: Accept Diff**, or reply `yes` in the CLI.

**Reject a diff** — click the `x` icon, close the diff tab, run **Gemini CLI: Close Diff Editor**, or reply `no` in the CLI.

You can edit the suggested changes in the diff view before accepting. Choosing **Allow for this session** in the CLI auto-accepts future changes, so they no longer surface as diffs in the IDE.

## Agent Client Protocol (ACP)

ACP standardizes how AI coding agents talk to editors, so an agent implemented once works with any ACP-compliant editor. Gemini CLI is officially listed in the **ACP Agent Registry**, letting supporting IDEs install and update it directly — no manual downloads or IDE-specific extensions.

| IDE | Integration |
|---|---|
| **JetBrains** (IntelliJ IDEA, PyCharm, GoLand, etc.) | Built-in registry support; install ACP agents directly |
| **Zed** | Integrates with the ACP Agent Registry to browse, install, and manage agents |
| **Other ACP-compatible IDEs** | Install Gemini CLI through their built-in registry features |

### Experimental Zed integration

For Zed specifically, the CLI also supports a dedicated mode flag:

```bash
gemini --experimental-zed-integration
```

This runs Gemini CLI as an ACP agent for Zed. As an experimental flag, behavior may change — verify in official docs.

## Manual PID override

If automatic IDE detection fails, or you want to associate a standalone terminal session with a specific IDE instance, set `GEMINI_CLI_IDE_PID` to that IDE's process ID. When set, the CLI skips auto-detection and connects using the provided PID.

```bash
export GEMINI_CLI_IDE_PID=12345
```

```powershell
$env:GEMINI_CLI_IDE_PID=12345
```

The CLI also relies on `GEMINI_CLI_IDE_WORKSPACE_PATH` and `GEMINI_CLI_IDE_SERVER_PORT`, which the companion extension sets automatically when its integrated terminal launches.

## Using with sandboxing

- **macOS Seatbelt:** the integration needs network access to reach the companion extension — use a Seatbelt profile that allows network access.
- **Docker/Podman:** the CLI auto-discovers the IDE server on `host.docker.internal`, so it can connect to the VS Code extension on the host. Usually no special configuration is required, but your Docker networking must allow container-to-host connections.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Failed to connect to IDE companion extension` | Missing `GEMINI_CLI_IDE_WORKSPACE_PATH` / `GEMINI_CLI_IDE_SERVER_PORT`; extension not running | Ensure the companion extension is installed and enabled, then open a **new** terminal in the IDE |
| `IDE connection error. The connection was lost unexpectedly` | Connection dropped | Run `/ide enable`; if it persists, open a new terminal or restart the IDE |
| `Directory mismatch` | CLI's working directory is outside the open workspace | `cd` into the IDE's workspace directory and restart the CLI |
| `please open a workspace folder` | No workspace open in the IDE | Open a workspace and restart the CLI |
| `IDE integration is not supported in your current environment` | Not running inside a supported IDE | Launch the CLI from a supported IDE's integrated terminal |
| `No installer is available for IDE` | No automated installer for your IDE | Install "Gemini CLI Companion" manually from the marketplace |

For ACP-specific issues, see the ACP Mode documentation.

## See also

- [configuration.md](./configuration.md) — settings reference
- [environment-variables.md](./environment-variables.md) — `GEMINI_CLI_IDE_PID` and related variables
- [cli-reference.md](./cli-reference.md) — `--experimental-zed-integration` and other flags
- [commands.md](./commands.md) — slash command reference
