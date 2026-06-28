# Remote Control

Connect [claude.ai/code](https://claude.ai/code) or the Claude mobile app to a Claude Code session running on **your** machine. Start at your desk, pick it up from your phone or another browser. Your filesystem, MCP servers, tools, and project config stay available — nothing moves to the cloud.

> Research preview. Available on all plans. On Team/Enterprise it's off by default until an admin enables the toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code). Requires Claude Code v2.1.51+.

---

## Remote Control vs. Claude Code on the web

Both use the claude.ai/code interface. The key difference:

- **Remote Control**: session runs **on your machine**. Local MCP servers, tools, project config all stay available.
- **[Claude Code on the web](./claude-code-web.md)**: session runs in **Anthropic-managed cloud infrastructure**.

Use Remote Control when you're in the middle of local work and want to keep going from another device. Use the web when you want zero local setup or want to work on a repo you don't have cloned.

---

## Requirements

- **Subscription**: Pro, Max, Team, or Enterprise. API keys not supported. On Team/Enterprise an admin must enable Remote Control in [admin settings](https://claude.ai/admin-settings/claude-code).
- **Auth**: `claude` then `/login` via claude.ai if not already.
- **Workspace trust**: run `claude` in your project dir at least once to accept the trust dialog.

---

## Three ways to start

### 1. Server mode (no local interactive session)

```bash
claude remote-control
```

The process stays running, waiting for remote connections. Displays a session URL and (press space) a QR code.

| Flag | Description |
|---|---|
| `--name "My Project"` | Custom session title visible at claude.ai/code |
| `--remote-control-session-name-prefix <p>` | Prefix for auto-generated names (default: hostname → `myhost-graceful-unicorn`). Or set `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` |
| `--spawn <mode>` | How the server creates sessions: `same-dir` (default — all share cwd; can conflict on same files), `worktree` (each on-demand session gets its own [git worktree](./agents.md)), `session` (single-session; rejects extra connections, set at startup only). Press `w` at runtime to toggle between same-dir and worktree |
| `--capacity <N>` | Max concurrent sessions (default 32). Cannot use with `--spawn=session` |
| `--verbose` | Detailed logs |
| `--sandbox` / `--no-sandbox` | Toggle [sandboxing](./sandboxing.md) for filesystem/network isolation. Off by default |

### 2. Interactive session

```bash
claude --remote-control "My Project"        # alias --rc
```

Full interactive session you can also drive from the web. Unlike server mode, you can type messages locally while it's also available remotely.

### 3. From an existing session

```
/remote-control            # alias /rc
/remote-control My Project
```

Carries over your current conversation. Displays session URL + QR.

> The `--verbose`, `--sandbox`, `--no-sandbox` flags are not available with `/remote-control`.

### 4. From VS Code

In the [Claude Code VS Code extension](./ide-integrations.md), type `/remote-control` or `/rc` in the prompt box. Requires Claude Code v2.1.79+. A banner appears showing connection status; click **Open in browser** to go directly to the session. Click the close icon on the banner to disconnect.

> The VS Code command does not accept a name argument or display a QR code. Title is derived from your conversation history or first prompt.

---

## Connect from another device

- **Open the session URL** in any browser.
- **Scan the QR code** — opens directly in the Claude app. With `claude remote-control`, press space to toggle the QR display.
- **Open [claude.ai/code](https://claude.ai/code)** or the Claude app and find the session by name. Remote Control sessions show a computer icon with a green status dot when online.

The session title is chosen in this order:

1. The name you passed to `--name`, `--remote-control`, or `/remote-control`
2. The title set by `/rename`
3. The last meaningful message in conversation history
4. Auto-generated like `myhost-graceful-unicorn`

If the environment already has an active session, you'll be asked to continue or start fresh.

If you don't have the Claude app yet, use `/mobile` to display a download QR code.

---

## Enable Remote Control for all sessions

Run `/config` and set **Enable Remote Control for all sessions** to `true`. With this on, every interactive Claude Code process registers one remote session. To run multiple concurrent sessions from a single process, use server mode.

---

## Connection and security

Your local Claude Code session makes **outbound HTTPS only** and never opens inbound ports. Claude Code registers with the Anthropic API and polls for work. When you connect from another device, the server routes messages between the web/mobile client and your local session over a streaming connection.

All traffic travels through the Anthropic API over TLS. The connection uses **multiple short-lived credentials**, each scoped to a single purpose and expiring independently.

---

## Mobile push notifications

When Remote Control is active, Claude can send push notifications to your phone.

Claude decides when to push — typically when a long-running task finishes or it needs a decision. You can also request a push: `notify me when the tests finish`. No per-event configuration beyond on/off.

> Requires Claude Code v2.1.110+.

Setup:

1. Install the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).
2. Sign in with the same Claude Code account.
3. Allow notifications.
4. In your terminal: `/config` → enable **Push when Claude decides**.

If notifications don't arrive:
- `/config` shows "No mobile registered" → open the Claude app on your phone to refresh its push token.
- iOS Focus modes / notification summaries can suppress. Check Settings → Notifications → Claude.
- Android battery optimization can delay. Exempt the Claude app.

---

## Limitations

- **One remote session per interactive process.** Outside server mode, each Claude Code instance supports one remote session at a time.
- **Local process must keep running.** Closing the terminal or `claude` process ends the session.
- **Network outage > ~10 minutes** times out the session and exits the process. Restart `claude remote-control`.
- **Ultraplan disconnects Remote Control** — both occupy the claude.ai/code interface.
- **Some commands are local-only.** Interactive picker commands (`/mcp`, `/plugin`, `/resume`) work only from local CLI. Text-output commands (`/compact`, `/clear`, `/context`, `/usage`, `/exit`, `/extra-usage`, `/recap`, `/reload-plugins`) work from mobile/web.

---

## Troubleshooting

| Error | What it means |
|---|---|
| "Remote Control requires a claude.ai subscription" | Not authenticated with claude.ai. Run `claude auth login`. Unset `ANTHROPIC_API_KEY` if set |
| "Remote Control requires a full-scope login token" | You used `claude setup-token` or `CLAUDE_CODE_OAUTH_TOKEN`. Those are inference-only. Run `claude auth login` for a session token |
| "Unable to determine your organization for Remote Control eligibility" | Cached account info stale. Run `claude auth login` |
| "Remote Control is not yet enabled for your account" | Eligibility check failing. Unset `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` / `DISABLE_TELEMETRY`. Doesn't work with Bedrock/Vertex/Foundry. If none apply, `/logout` then `/login` |
| "Remote Control is disabled by your organization's policy" | Multiple causes: API-key auth (need claude.ai), admin hasn't enabled it, or admin toggle is grayed out (data-retention/compliance restriction — contact Anthropic support) |
| "Remote credentials fetch failed" | Couldn't get short-lived credential. Run with `--verbose` to see full error |

---

## How to choose between remote work options

| | Trigger | Where Claude runs | Setup | Best for |
|---|---|---|---|---|
| **Dispatch** | Message a task from mobile app | Your machine (Desktop) | Pair mobile app with Desktop | Delegating while away |
| **Remote Control** | Drive a running session from claude.ai or mobile | Your machine (CLI or VS Code) | `claude remote-control` | Steering in-progress work from another device |
| **Channels** | Push events from chat app or your server | Your machine (CLI) | Install channel plugin | Reacting to external events (CI failures, chat messages) |
| **Slack** | Mention `@Claude` in a channel | Anthropic cloud | Install Slack app + Claude Code on the web | PRs and reviews from team chat |
| **Scheduled tasks** | Set a schedule | CLI / Desktop / cloud | Pick a frequency | Recurring automation |

---

## See also

- [claude-code-web.md](./claude-code-web.md) — when to use the cloud instead
- [channels.md](./channels.md) — push events instead of driving the session
- [cli-reference.md](./cli-reference.md) — `claude remote-control`, `--rc`, `--remote-control-session-name-prefix`
- [permissions.md](./permissions.md) — pre-approving common ops
