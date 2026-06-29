# Plugins (Antigravity)

Antigravity has a plugin system and can **import plugins from the Gemini CLI or
Claude**, easing migration from those tools.

```bash
agy plugin <command> [arguments]
# `agy plugins` is an alias for `agy plugin`
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List imported plugins |
| `import [source]` | Import plugins from `gemini` or `claude` |
| `install <target>` | Install a plugin (supports `plugin@marketplace`) |
| `uninstall <name>` | Uninstall a plugin |
| `enable <name>` | Enable a plugin |
| `disable <name>` | Disable a plugin |
| `validate [path]` | Validate a plugin |
| `link <mp> <target>` | Generate a link to a marketplace |
| `help` | Show plugin help |

## Migrating from Gemini CLI / Claude

```bash
agy plugin import gemini     # bring over Gemini CLI plugins
agy plugin import claude     # bring over Claude plugins
agy plugin list              # confirm what was imported
```

## Installing from a marketplace

```bash
agy plugin install some-plugin@some-marketplace
agy plugin enable some-plugin
```

> Verified from `agy plugin --help` (v1.0.12). Run `agy plugin help` for the
> latest commands.
