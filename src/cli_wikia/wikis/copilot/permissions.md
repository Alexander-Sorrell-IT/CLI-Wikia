# Permissions (GitHub Copilot CLI)

GitHub Copilot CLI controls what the agent may do through fine-grained
allow/deny lists for tools, paths, and URLs, plus "allow all" switches.

## Allow everything

| Flag | Description |
|------|-------------|
| `--allow-all` | Enable all permissions (= `--allow-all-tools` + `--allow-all-paths` + `--allow-all-urls`) |
| `--allow-all-tools` | Allow all tools to run automatically (env: `COPILOT_ALLOW_ALL`); required for non-interactive mode |
| `--allow-all-paths` | Allow access to any path |
| `--allow-all-urls` | Allow access to all URLs without confirmation |

> `--allow-all-tools` (or the `COPILOT_ALLOW_ALL` env var) is required for
> non-interactive mode.

```bash
copilot --allow-all -p "run the full workflow"
```

## Tools

| Flag | Description |
|------|-------------|
| `--allow-tool[=tools...]` | Tools the CLI has permission to use |
| `--deny-tool[=tools...]` | Tools the CLI may not use |
| `--available-tools[=tools...]` | Only these tools will be available to the model |
| `--excluded-tools[=tools...]` | Tools not available to the model |
| `--no-ask-user` | Disable the `ask_user` tool (autonomous) |

```bash
copilot --allow-tool=shell --deny-tool=write -p "investigate the bug"
```

## Paths

| Flag | Description |
|------|-------------|
| `--add-dir <directory>` | Add a directory to the allowed list for file access |
| `--allow-all-paths` | Allow access to any path |

```bash
copilot --add-dir ../shared -p "use the shared helpers"
```

## URLs

| Flag | Description |
|------|-------------|
| `--allow-url[=urls...]` | Allow access to specific URLs or domains |
| `--deny-url[=urls...]` | Deny URLs/domains (takes precedence over `--allow-url`) |
| `--allow-all-urls` | Allow access to all URLs without confirmation |

```bash
copilot --allow-url=https://api.example.com --deny-url=https://evil.example
```

> `--deny-url` takes precedence over `--allow-url`.

## More detail

```bash
copilot help permissions
```

## Related

- Autonomous runs pair permissions with autopilot mode — see
  [modes.md](modes.md).

> Verify exact values in the official docs / run `copilot --help`.
