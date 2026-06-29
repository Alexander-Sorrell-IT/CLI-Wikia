# Codex `exec` — Non-Interactive Automation

`codex exec` (alias `codex e`) runs Codex headless to completion — for scripts, pipelines, and CI. The agent works without a TUI and exits when done.

> **Not locally verified** — sourced from OpenAI's [CLI](https://developers.openai.com/codex/cli) docs; Codex isn't installed here. Confirm flags with `codex exec --help` after installing.

---

## Basic usage

```bash
codex exec "update the CHANGELOG for the latest release"
codex e "run the test suite and fix any failures"     # short alias
```

Authentication uses the same cached credentials as the interactive CLI ([codex-auth.md](./codex-auth.md)). `codex exec` exits **non-zero** if task submission fails — so it composes with shell error handling and CI gates.

---

## Piping context in

stdin is read as additional context, which makes `exec` composable with other tools:

```bash
git diff | codex exec "write a conventional-commit message for this diff"
git log --oneline -20 | codex e "summarize these commits for release notes"
cat error.log | codex exec "explain the root cause of this stack trace"
```

---

## Structured / machine-readable output

| Flag | Short | Purpose |
|---|---|---|
| `--json` | | Emit newline-delimited JSON events on stdout (parse with `jq`) |
| `--output-last-message` | `-o` | Write only the final assistant message to a file |
| `--output-schema` | | Validate structured output against a JSON schema file |
| `--ephemeral` | | Don't persist session files |
| `--skip-git-repo-check` | | Allow running outside a git repository |
| `--ignore-rules` | | Skip `execpolicy` rule files |

```bash
# Stream JSON events and extract assistant text
codex exec --json "list TODOs in src/" \
  | jq -rj 'select(.type=="item.completed") | .text? // empty'

# Final answer only, to a file
codex exec -o summary.txt "summarize the architecture of this repo"

# Constrain output to a schema
codex exec --output-schema schema.json "extract the public API as JSON"
```

---

## Approvals & sandbox in exec mode

Non-interactive runs can't show approval prompts, so pair `exec` with an approval policy that won't block. The common CI pattern is **read-only with no prompts**, or **workspace-write with `never`** for trusted automation:

```bash
# Read-only analysis in CI — never asks
codex exec --sandbox read-only --ask-for-approval never \
  --skip-git-repo-check "audit dependencies for known issues"

# Trusted hands-off edits inside the workspace
codex exec --full-auto "apply the lint autofixes and run the formatter"
```

See [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) for what each setting permits. Avoid `--yolo` in automation unless the environment is fully disposable.

---

## Resuming exec sessions

Continue a prior thread non-interactively (verify exact form with `codex exec --help`):

```bash
codex exec resume --last "now also update the docs"
```

`--ephemeral` opts out of persistence when you don't want the run saved.

---

## CI example

```bash
#!/usr/bin/env bash
set -euo pipefail
export OPENAI_API_KEY="$OPENAI_API_KEY"   # or a piped access token

codex exec --sandbox read-only --ask-for-approval never --json \
  "review the diff on this branch and flag correctness bugs" \
  | tee codex-review.jsonl
```

---

## See also

- [codex-cli-reference.md](./codex-cli-reference.md) — full flag list
- [codex-approvals-sandbox.md](./codex-approvals-sandbox.md) — safe automation presets
- [codex-auth.md](./codex-auth.md) — access tokens for CI
