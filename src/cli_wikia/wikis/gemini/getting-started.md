# Getting Started

Gemini CLI brings Google's Gemini models to your terminal as an AI coding agent. This page covers installation, authentication, free and paid quotas, basic usage, upgrading, troubleshooting, and uninstalling.

## Install

The standard install uses `npm` and requires **Node.js 20 or higher**:

```bash
npm install -g @google/gemini-cli
```

Then launch it:

```bash
gemini
```

To run without a global install, use `npx`:

```bash
npx @google/gemini-cli
```

Other package managers (pnpm, yarn, bun) and Homebrew can also install it; verify exact commands in the official installation docs.

## First run

1. Run `gemini` after installation.
2. At the prompt **"How would you like to authenticate for this project?"** choose **1. Sign in with Google**.
3. Select your Google account and click **Sign in**.

Some account types require a Google Cloud project (see authentication below). After authenticating, you can start issuing prompts.

## Authentication

| Method | Who it's for | How to set up | Key env vars |
|---|---|---|---|
| **Sign in with Google** | Individual developers (Gemini Code Assist) | Run `gemini`, choose "Sign in with Google", complete OAuth | — (some accounts need `GOOGLE_CLOUD_PROJECT`) |
| **Gemini API key** | Developers wanting direct API access / pay-as-you-go | Get a key at [Google AI Studio](https://aistudio.google.com/app/apikey); store it securely | `GEMINI_API_KEY` |
| **Vertex AI** | Enterprise / Google Cloud users | Configure project and location; use Express Mode (free) or regular mode | `GOOGLE_CLOUD_PROJECT`, location settings |
| **Google Workspace** | Organization users on Code Assist licenses | Admin assigns a Code Assist Standard/Enterprise entitlement | `GOOGLE_CLOUD_PROJECT` |

> Store keys securely: keep them in a `.gemini/.env` file (auto-loaded by the CLI) or your OS keyring rather than in scripts or source control.

> **Individual users:** if you see an error about needing a *named user on your organization's subscription*, unset `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_PROJECT_ID` from your shell config and `.env` files — setting them forces an organization subscription check.

Enforce the exact authentication identifiers (e.g. `oauth-personal`) per the official authentication docs. Third-party agents may not piggyback on Gemini CLI's OAuth — the supported way to use other agents with Gemini is a Vertex AI or Google AI Studio API key.

## Quotas and pricing

Gemini CLI has a generous free tier; paid tiers and pay-as-you-go raise or remove daily limits.

| Auth method | Tier / subscription | Max requests / user / day |
|---|---|---|
| Google account | Gemini Code Assist (Individual) | 1,000 |
| | Google AI Pro | 1,500 |
| | Google AI Ultra | 2,000 |
| Gemini API key | Free tier (unpaid, Flash only) | 250 |
| | Pay-as-you-go | Varies (per token/call) |
| Vertex AI | Express Mode (free, 90 days before billing) | Varies |
| | Pay-as-you-go | Varies |
| Google Workspace | Code Assist Standard | 1,500 |
| | Code Assist Enterprise | 2,000 |
| | Workspace AI Ultra | 2,000 |

Three broad categories:

- **Free usage** — experimentation and light use.
- **Paid tier (fixed price)** — predictable cost with higher daily quotas (Google AI Pro/Ultra, Code Assist licenses).
- **Pay-as-you-go** — per-token billing via a Gemini API key or Vertex AI; the only way to avoid quota interruptions, but more expensive for many small calls.

Google AI Pro/Ultra higher limits cover Gemini 2.5 (Pro and Flash) and are **shared** across Gemini CLI and agent mode in the Code Assist IDE extensions. Google does **not** use your data to improve its models on paid plans.

### Check usage

Use `/stats model` inside a session for a snapshot of token usage and quota limits. A model-usage summary is also printed when you exit. Cached-token savings appear in `/stats` only when token caching is active (Gemini API key or Vertex AI; not OAuth).

## Basic usage

After authenticating, issue prompts directly in the terminal. Gemini asks permission before running tools or modifying files (choose **Allow once** / **Allow for this session**).

```
Rename the photos in my "photos" directory based on their contents.
```

```
Clone the 'chalk' repository from https://github.com/chalk/chalk, read its key source files, and explain how it works.
```

```
Combine the two .csv files into a single .csv file, with each year a different column.
```

```
Write unit tests for Login.js.
```

## Upgrading

Check your version:

```bash
gemini --version        # or gemini -v, or /about inside a session
```

Update a global npm install to the latest release:

```bash
npm install -g @google/gemini-cli@latest
```

If you built from source, pull the latest changes and run `npm run build`.

## Common troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `API error: 429 - Resource exhausted` | Exceeded your request/rate limit. Check usage, batch prompts, or request a quota increase. |
| `command not found: gemini` | The npm global bin directory isn't on your `PATH`, or the install failed. Reinstall with `npm install -g @google/gemini-cli@latest`. |
| `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` / `unable to get local issuer certificate` | Corporate TLS inspection. Set `NODE_USE_SYSTEM_CA=1`; if needed, point `NODE_EXTRA_CA_CERTS` at your corporate root CA. |
| `Failed to sign in ... not currently available in your location` | Your location isn't supported for Code Assist for individuals; check the available-locations list. |
| `Failed to sign in ... Request contains an invalid argument` | Workspace/Cloud-linked Gmail accounts may not activate the free tier. Set `GOOGLE_CLOUD_PROJECT`, or use a Gemini API key from AI Studio. |
| CLI won't enter interactive mode | An env var starting with `CI_` (e.g. `CI_TOKEN`) is detected as a CI environment. Run with `env -u CI_TOKEN gemini`. |
| `DEBUG=true` in project `.env` has no effect | `DEBUG`/`DEBUG_MODE` are excluded from project `.env` files. Use a `.gemini/.env` file instead. |
| `chmod` etc. crash on Windows | Unix-only commands; use Git Bash or WSL. |
| `npm WARN deprecated` during install | Harmless informational warnings; the install still works. |

Use the `--debug` flag for verbose output (press **F12** in interactive mode for the debug console). Selected exit codes for scripting: `41` auth error, `42` input error, `44` sandbox error, `52` invalid config, `53` turn limit reached.

## Uninstall

```bash
npm uninstall -g @google/gemini-cli
```

Configuration and history remain in `~/.gemini` (and any project `.gemini` directories); remove them manually if you want a clean slate.

## See also

- [configuration.md](./configuration.md) — settings files and options
- [cli-reference.md](./cli-reference.md) — command-line flags
- [commands.md](./commands.md) — slash commands including `/stats`
- [environment-variables.md](./environment-variables.md) — `GEMINI_API_KEY`, `GOOGLE_CLOUD_PROJECT`, and more
- [enterprise.md](./enterprise.md) — org deployment, telemetry, and token caching
