# Configuration (DeepSeek Code)

## Config command

View or edit the configuration from the CLI:

```bash
deepseek-code config
```

## Config file

DeepSeek Code stores its configuration at:

```
~/.deepseek-code/config.json
```

### Fields

| Field | Example | Description |
|-------|---------|-------------|
| `model` | `"deepseek-v4-flash"` | Default model |
| `effortLevel` | `"high"` | Default reasoning effort (`low`/`medium`/`high`/`max`) |
| `thinking` | `"on"` | Reasoning mode (`on`/`off`/`max`) |
| `permissionMode` | `"acceptEdits"` | Default permission mode |
| `autoMemoryEnabled` | `true` | Enable automatic memory |
| `sessionPersistence` | `true` | Persist sessions to disk |

Example `~/.deepseek-code/config.json`:

```json
{
  "model": "deepseek-v4-flash",
  "effortLevel": "high",
  "thinking": "on",
  "permissionMode": "acceptEdits",
  "autoMemoryEnabled": true,
  "sessionPersistence": true
}
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `DEEPSEEK_CODE_MODEL` | Default model |

Save your API key interactively with:

```bash
deepseek-code auth login
deepseek-code auth status
```

## Related

- Model defaults — see [models.md](models.md).
- Permission defaults — see [permissions.md](permissions.md).

> Verify exact values in the official docs / run `deepseek-code config`.
