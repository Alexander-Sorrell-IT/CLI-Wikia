# Extensions (Gemini CLI)

Gemini CLI supports extensions that add capabilities to the agent. Manage them
with the `gemini extensions` command (alias: `gemini extension`).

## The extensions command

```
gemini extensions <command>
```

> The `--help` output lists `gemini extensions <command>` as the entry point
> for managing extensions but does not enumerate its individual subcommands.
> Run `gemini extensions --help` for the available subcommands.

## Listing extensions

List all available extensions and exit:

```bash
gemini -l
# or
gemini --list-extensions
```

## Using specific extensions

By default, all extensions are used. Restrict a session to specific
extensions with `-e` / `--extensions`:

```bash
gemini -e ext-a,ext-b "run the workflow"
```

| Flag | Description |
|------|-------------|
| `-e, --extensions` | List of extensions to use. If not provided, all extensions are used (array) |
| `-l, --list-extensions` | List all available extensions and exit |

## Related

- See [cli-reference.md](cli-reference.md) for the full flag list.

> Verify exact values in the official docs / run `gemini extensions --help`.
