# Status Line

A customizable shell-script bar at the bottom of Claude Code that displays real-time session metadata: model, context usage, costs, git status, anything you want.

---

## Configuration

```json
// settings.json
{
  "statusLine": {
    "command": "~/.claude/status-line.sh",
    "updateInterval": 1000
  }
}
```

`command` is run periodically (every `updateInterval` ms). It receives session JSON on stdin and prints what to display.

`disableAllHooks: true` also disables the status line.

---

## JSON input on stdin

```json
{
  "session_id": "abc123",
  "model": "claude-opus-4-7",
  "context": {
    "tokens_used": 5000,
    "max_tokens": 200000,
    "percentage": 2.5
  },
  "usage": {
    "input_tokens": 3000,
    "output_tokens": 2000,
    "cache_read_tokens": 500,
    "estimated_cost_usd": 0.042
  },
  "git": {
    "branch": "main",
    "status": "clean",
    "modified_files": 0
  },
  "cwd": "/path/to/project"
}
```

---

## Single-line example

```bash
#!/bin/bash
input=$(cat)
branch=$(echo "$input" | jq -r '.git.branch')
used=$(echo  "$input" | jq '.context.percentage | floor')
cost=$(echo  "$input" | jq '.usage.estimated_cost_usd')

echo "$branch  Context: ${used}%  Cost: \$${cost}"
```

---

## Multi-line example

```bash
#!/bin/bash
input=$(cat)
model=$(echo  "$input" | jq -r '.model')
cwd=$(echo    "$input" | jq -r '.cwd')
branch=$(echo "$input" | jq -r '.git.branch')
used=$(echo   "$input" | jq '.context.percentage | floor')
cost=$(echo   "$input" | jq '.usage.estimated_cost_usd')

# Line 1: model · cwd · branch
echo "$model  $cwd  $branch"

# Line 2: context bar + cost
printf "Context: ["
printf "#%.0s" $(seq 1 $used)
printf "-%.0s" $(seq $((100-used)) 100)
printf "] ${used}%%  Cost: \$${cost}"
```

---

## Plugin status lines

Plugins can ship status-line scripts. The plugin's `${CLAUDE_PLUGIN_ROOT}/statusline/status.sh` (or wherever the plugin's settings.json points) is loaded when the plugin is enabled.

---

## Best practices

- Keep refresh interval ≥ 500ms for performance.
- Echo nothing if you have nothing to show — empty output is fine.
- Status-line failures are silent; debug by running the script with a sample stdin first.
- Use `jq -r` for raw strings, `jq` (no flag) for numbers.
- For git info, prefer `.git.branch` from the JSON over running `git` yourself — JSON is faster and already aware of detached HEAD, etc.

---

## See also

- [settings.md](./settings.md) — `statusLine` key
- [environment-variables.md](./environment-variables.md) — env vars passed to the script
