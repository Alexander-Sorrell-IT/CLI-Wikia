# OpenAI CLI Reference

Complete reference for the `openai` command, derived from `openai --help`
(version 2.24.0).

## Usage

```
openai [global options] {api,tools,migrate,grit} ...
```

## Global options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help |
| `-v, --verbose` | Set verbosity |
| `-V, --version` | Show program version |
| `-b, --api-base <url>` | API base URL to use |
| `-k, --api-key <key>` | API key to use (overrides env) |
| `-p, --proxy <proxy...>` | Proxy/proxies to use |
| `-o, --organization <org>` | Organization to run as (defaults to your default org) |
| `-t, --api-type {openai,azure}` | Backend API to call |
| `--api-version <ver>` | Azure API version |
| `--azure-endpoint <url>` | Azure endpoint, e.g. `https://endpoint.openai.azure.com` |
| `--azure-ad-token <token>` | Azure Active Directory token |

## Top-level subcommands

| Command | Purpose |
|---------|---------|
| `openai api` | Direct API calls (chat, images, audio, files, models, fine-tuning) |
| `openai tools` | Client-side convenience tools |
| `openai migrate` | Migration helper |
| `openai grit` | Grit-based code transforms |

## `openai api` subcommands

```
chat.completions.create
completions.create
images.generate
images.edit
images.create_variation
audio.transcriptions.create
audio.translations.create
files.create | files.retrieve | files.delete | files.list
models.list | models.retrieve | models.delete
fine_tuning.jobs.create | .retrieve | .list | .cancel | .list_events
```

## `openai api chat.completions.create`

The main chat endpoint.

```
openai api chat.completions.create -m <model> -g <role> <content> [options]
```

| Option | Description |
|--------|-------------|
| `-g, --message <role> <content>` | A message in `{role} {content}` form. Repeat for multiple messages. **(required)** |
| `-m, --model <model>` | Model to use. **(required)** |
| `-n, --n <N>` | How many completions to generate |
| `-M, --max-tokens <N>` | Max tokens to generate |
| `-t, --temperature <T>` | Sampling temperature (0 = deterministic, ~0.9 = creative). Mutually exclusive with `--top_p` |
| `-P, --top_p <P>` | Nucleus sampling. Mutually exclusive with `--temperature` |
| `--stop <seq>` | Stop sequence |
| `--stream` | Stream tokens as they're ready |

### Example

```bash
openai api chat.completions.create \
  -m gpt-4o \
  -g system "You are a terse assistant." \
  -g user "Summarize REST in one sentence." \
  -M 100 -t 0.2 --stream
```

## `openai tools`

```
openai tools fine_tunes.prepare_data
```

Client-side convenience tools (e.g. preparing data for fine-tuning).

> Verified from `openai --help`. Run `openai api <subcommand> --help` for the
> full option set of any subcommand.
