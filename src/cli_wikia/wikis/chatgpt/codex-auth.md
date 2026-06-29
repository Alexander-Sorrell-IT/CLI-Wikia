# Codex Authentication

How Codex CLI signs in. From OpenAI's [Authentication](https://developers.openai.com/codex/auth) docs and the [openai/codex](https://github.com/openai/codex/blob/main/docs/authentication.md) repo.

> **Not locally verified** — sourced from official docs; Codex isn't installed here. Confirm flag spellings with `codex login --help` after installing.

---

## Two sign-in methods

| Method | Billing | Notes |
|---|---|---|
| **Sign in with ChatGPT** (default) | Subscription entitlements | Requires ChatGPT **Plus, Pro, Business, Edu, or Enterprise**; full feature set |
| **API key** | Usage-based (OpenAI API) | Some features may be limited or unavailable |

When no valid session exists, *Sign in with ChatGPT* is the default path.

---

## Sign in with ChatGPT (OAuth)

```bash
codex login          # opens a browser; after sign-in the token returns to the CLI
```

The browser completes an OAuth flow and returns an access token to the CLI/IDE extension.

### Headless / remote / SSH

OAuth needs a browser and a localhost callback (port **1455**). Options when there's no local browser:

```bash
# Device-code flow (beta) — sign in on another device
codex login --device-auth
```

- **Copy credentials:** sign in on a machine with a browser, then copy `~/.codex/auth.json` to the remote host.
- **SSH port-forward:** tunnel `localhost:1455` so the OAuth callback reaches your laptop's browser.

---

## API key

```bash
codex login          # then choose API key entry, or
# provide OPENAI_API_KEY in the environment
export OPENAI_API_KEY=sk-...
```

Get a key from the OpenAI dashboard. API-key auth supports local workflows; some ChatGPT-managed features are unavailable.

---

## Access tokens (enterprise / CI)

For non-interactive ChatGPT-workspace automation, an access token can be piped over stdin — no browser needed:

```bash
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
```

In **ChatGPT Enterprise** workspaces, admins can allow permitted members to create Codex access tokens for trusted automation. Use one when automation needs ChatGPT workspace access / managed entitlements / enterprise controls without an interactive sign-in. See OpenAI's [CI/CD auth guide](https://developers.openai.com/codex/auth/ci-cd-auth).

---

## Credential storage

Cached credentials live at `~/.codex/auth.json` (under `CODEX_HOME` if set). Where they're stored is configurable:

```toml
cli_auth_credentials_store = "auto"   # "file" | "keyring" | "auto"
```

Restrict which method is allowed:

```toml
forced_login_method = "chatgpt"       # "chatgpt" | "api"
```

> Codex **Cloud** features require multi-factor authentication (MFA).

---

## Status & logout

```bash
codex login status    # show current auth state (verify exact form)
codex logout          # remove cached credentials
```

`codex doctor` also reports auth health.

---

## Env vars

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | API key for API-key auth / custom providers |
| `CODEX_HOME` | Override the `~/.codex` directory (auth, config, history) |
| `CODEX_NON_INTERACTIVE` | Set during unattended installs |

(`CODEX_ACCESS_TOKEN` in the example above is just an env var you choose to hold a token — confirm any official names with the docs.)

---

## See also

- [codex-overview.md](./codex-overview.md) — first-run flow
- [codex-config.md](./codex-config.md) — `cli_auth_credentials_store`, `forced_login_method`
- [codex-exec.md](./codex-exec.md) — auth in CI / non-interactive runs
