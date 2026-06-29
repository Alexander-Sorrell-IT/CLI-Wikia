# Models

Gemini CLI runs on Google's Gemini family. You pick a model with the `/model`
command, the `-m`/`--model` flag, the `GEMINI_MODEL` environment variable, or the
`model.name` setting. The recommended default is **Auto**, which lets the CLI
choose the best model per task.

## Model aliases

The CLI groups models behind aliases. **Pro** models maximize reasoning, **Flash**
models maximize speed, and **Auto** routes between them automatically.

| Alias        | Use it for                                | Routes to                                      |
| ------------ | ----------------------------------------- | ---------------------------------------------- |
| `auto`       | Default; balanced speed/quality per task  | The best Gemini model for the request          |
| `pro`        | Complex reasoning, multi-stage debugging  | A Pro model (e.g. `gemini-3-pro-preview`)      |
| `flash`      | Fast responses to simpler prompts         | A Flash model                                  |
| `flash-lite` | Quickest, lightweight conversions         | `gemini-2.5-flash-lite`                         |

`auto` is the default model when nothing else is configured.

## Concrete model names

| Model                    | Family     | Notes                                            |
| ------------------------ | ---------- | ------------------------------------------------ |
| `gemini-3-pro-preview`   | Gemini 3   | Most capable; used by **Auto (Gemini 3)** / Pro  |
| `gemini-3-flash-preview` | Gemini 3   | Fast Gemini 3 model; used by **Auto (Gemini 3)** |
| `gemini-2.5-pro`         | Gemini 2.5 | High reasoning; routing fallback for Gemini 3 Pro |
| `gemini-2.5-flash`       | Gemini 2.5 | Fast; routing fallback for 2.5 Pro               |
| `gemini-2.5-flash-lite`  | Gemini 2.5 | Lightweight; used for internal utility calls     |

> A `gemini-3.1-pro-preview` model is rolling out. To check access, run `/model`,
> select **Manual**, and look for it in the list. When available it joins
> **Auto (Gemini 3)** routing and can be launched directly with
> `gemini -m gemini-3.1-pro-preview`. Verify availability in official docs.

## Selecting a model

### The `/model` command

Run `/model` in an interactive session to open a picker:

| Option            | Description                                       | Models                                           |
| ----------------- | ------------------------------------------------- | ------------------------------------------------ |
| Auto (Gemini 3)   | Let the system choose the best Gemini 3 model.    | `gemini-3-pro-preview`, `gemini-3-flash-preview` |
| Auto (Gemini 2.5) | Let the system choose the best Gemini 2.5 model.  | `gemini-2.5-pro`, `gemini-2.5-flash`             |
| Manual            | Select a specific model.                          | Any available model.                             |

Changes apply to all subsequent interactions in the session.

> The `/model` command and `--model` flag do **not** override the model used by
> sub-agents, so model-usage reports may still show other models.

### The `-m` / `--model` flag

```bash
gemini -m gemini-2.5-pro
gemini --model gemini-3-pro-preview
gemini -p "convert this to YAML" -m flash-lite
```

### As a default

```bash
export GEMINI_MODEL=gemini-2.5-flash
```

```json
// settings.json
{ "model": { "name": "gemini-2.5-pro" } }
```

### Model selection precedence

The model is resolved in this order (first match wins):

1. **`--model` flag** — always used when present.
2. **`GEMINI_MODEL` environment variable**.
3. **`model.name` in `settings.json`**.
4. **Local Gemma router** (experimental, if enabled) — picks a Gemini model.
5. **Default** — `auto`.

## Best practices

- **Default to Auto.** It balances speed and quality, picking the right model as
  task complexity varies within a single project.
- **Switch to Pro** when you need more reasoning ("smarter"): complex or
  multi-stage debugging, architecture work.
- **Switch to Flash or Flash-Lite** when you need a quick, simple answer (for
  example, converting a JSON object to YAML).

## Model routing

Gemini CLI automatically falls back to a healthy model when the primary one
fails. Routing is enabled by default and managed by the
`ModelAvailabilityService`.

1. **Model failure** — on quota or server errors, the CLI begins fallback.
2. **User consent** — by default the CLI prompts you before switching. Some
   internal utility calls (prompt completion, classification) use a **silent**
   fallback chain: `gemini-2.5-flash-lite` → `gemini-2.5-flash` →
   `gemini-2.5-pro`, without prompting or changing your configured model.
3. **Model switch** — once approved (or under a silent policy), the fallback
   model is used for the current turn or the rest of the session.

### Auto vs. Pro routing (Gemini 3)

| Routing | Behavior                                                                                                       |
| ------- | -------------------------------------------------------------------------------------------------------------- |
| Auto    | Classifies each prompt. Simple → `gemini-2.5-flash`. Complex → Gemini 3 Pro if enabled, else `gemini-2.5-pro`. |
| Pro     | Select **Pro** in `/model` to prioritize the most capable model available, including Gemini 3 Pro.             |

### Usage limits and fallback

When you hit your Gemini 3 Pro daily limit, the CLI offers to switch to
`gemini-2.5-pro`, upgrade for higher limits, or stop. Hitting the 2.5 Pro limit
prompts a fallback to `gemini-2.5-flash`. If Gemini 3 Pro is overloaded
(capacity error), you can keep trying (with exponential backoff) or fall back to
`gemini-2.5-pro`.

> To enable Gemini 3, upgrade to the latest CLI
> (`npm install -g @google/gemini-cli@latest`), run `/model`, and select
> **Auto (Gemini 3)** (requires version 0.21.1 or later). On Gemini Code Assist,
> an admin must select the **Preview** release channel and you must set
> **Preview Features** to `true` via `/settings`.

## Model steering (experimental)

Model steering lets you guide the agent in real time while it works, without
stopping it. It is disabled by default; enable it via `/settings` (search for
**Model Steering**) or in `settings.json`:

```json
{ "experimental": { "modelSteering": true } }
```

While the agent is working (spinner visible), type a hint and press **Enter**.
The CLI acknowledges it with a small fast model and injects it into the model's
context for the next turn, which re-evaluates its plan and adjusts. It is useful
for correcting paths, skipping steps, adding context, or redirecting effort, and
is especially handy during Plan Mode and long-running sub-agent runs.

## Generation settings (`modelConfigs`)

The Model Configuration system (`ModelConfigService`) gives power users direct
control over generation hyperparameters. It lives under the `modelConfigs` key
in your settings.

> Power-user feature. Values pass to the model provider with minimal validation;
> incompatible combinations may cause runtime API errors.

### `ModelConfig` object

| Property                | Type   | Description                                  |
| ----------------------- | ------ | -------------------------------------------- |
| `model`                 | string | The model to call (e.g. `gemini-2.5-pro`).   |
| `generateContentConfig` | object | Passed directly to the `@google/genai` SDK.  |

### Common `generateContentConfig` parameters

| Parameter         | Type   | Description                                                  |
| ----------------- | ------ | ----------------------------------------------------------- |
| `temperature`     | number | Output randomness. `0.0` is deterministic; `>0.7` creative. |
| `topP`            | number | Nucleus sampling probability.                               |
| `maxOutputTokens` | number | Limit on generated response length.                         |
| `thinkingConfig`  | object | Reasoning config, e.g. `thinkingBudget`, `includeThoughts`. |

### Aliases and overrides

The system has two primitives:

- **`customAliases`** — named, reusable presets. An alias can `extends` another
  (including system defaults like `chat-base`); child settings win over parent.
  An alias need not name a concrete `model` if it is only a base for others.
- **`overrides`** — conditional rules matched at request time on `model` and/or
  `overrideScope` (typically the agent name). More specific matches (more matched
  keys) win; ties resolve to last defined.

Resolution: the requested model string is resolved through the alias `extends`
chain to a base config, then matching overrides are merged onto it by
specificity.

```json
"modelConfigs": {
  "customAliases": {
    "base":      { "modelConfig": { "generateContentConfig": { "temperature": 0.0 } } },
    "chat-base": { "extends": "base", "modelConfig": { "generateContentConfig": { "temperature": 0.7 } } }
  },
  "overrides": [
    {
      "match": { "overrideScope": "codebaseInvestigator" },
      "modelConfig": { "generateContentConfig": { "thinkingConfig": { "thinkingBudget": 4096 } } }
    }
  ]
}
```

You can also route a stable alias to a preview model for A/B testing without
touching client code:

```json
"modelConfigs": {
  "overrides": [
    { "match": { "model": "gemini-2.5-pro" }, "modelConfig": { "model": "gemini-2.5-pro-experimental-001" } }
  ]
}
```

## Local model routing & Gemma setup (experimental)

Instead of asking a hosted model to make routing decisions, Gemini CLI can run a
local **Gemma 3 1B** model to classify each request as simple or complex
(simple → Flash, complex → Pro). This trades a few milliseconds of local latency
for lower hosted-model token usage. If the local server is down, the CLI
silently falls back to the cloud classifier.

### Automated setup

```bash
gemini gemma setup        # downloads runtime + model (~1 GB), configures, starts server
```

| Command               | What it does                                                |
| --------------------- | ----------------------------------------------------------- |
| `gemini gemma setup`  | Full install (binary + model + settings + server start).    |
| `gemini gemma status` | Health check of what's installed and running.               |
| `gemini gemma start`  | Start the LiteRT server (auto-starts on launch by default). |
| `gemini gemma stop`   | Stop the LiteRT server.                                     |
| `gemini gemma logs`   | Tail server logs to watch routing requests live.            |
| `/gemma`              | In-session status panel.                                    |

Setup flags: `--port <n>`, `--no-start`, `--force`, `--skip-model`.

### Configuration

```json
{
  "experimental": {
    "gemmaModelRouter": {
      "enabled": true,
      "classifier": {
        "host": "http://localhost:9379",
        "model": "gemma3-1b-gpu-custom"
      }
    }
  }
}
```

| Field              | Type    | Required | Description                                          |
| ------------------ | ------- | -------- | ---------------------------------------------------- |
| `enabled`          | boolean | Yes      | Must be `true` to enable the feature.                |
| `classifier`       | object  | Yes      | Local model endpoint configuration.                  |
| `classifier.host`  | string  | Yes      | URL to the local server, `http://localhost:<port>`.  |
| `classifier.model` | string  | Yes      | Must be `"gemma3-1b-gpu-custom"`.                     |

Restart the CLI after changing this config. To disable, set `enabled: false` or
run `gemini gemma stop`. For air-gapped or firewalled environments the runtime
(LiteRT-LM) and model can be installed manually — see the official Manual Local
Model Routing Setup guide.

## See also

- [cli-reference.md](./cli-reference.md) — `-m`/`--model`, `gemini gemma`
- [settings.md](./settings.md) — `model.name`, `modelConfigs`, `experimental`
- [configuration.md](./configuration.md) — `GEMINI_MODEL`, precedence
- [commands.md](./commands.md) — `/model`, `/settings`, `/gemma`
