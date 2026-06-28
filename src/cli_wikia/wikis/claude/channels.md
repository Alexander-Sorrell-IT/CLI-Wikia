# Channels

Channels push events from non-Claude sources (Telegram, Discord, iMessage, CI webhooks, custom servers) **into your running Claude Code session**, so Claude can react to things that happen while you're not at the terminal. Channels can be **two-way** — Claude reads the event and replies back through the same channel.

> **Research preview.** Requires Claude Code v2.1.80+. claude.ai login (no console/API-key auth). Team/Enterprise orgs must explicitly enable.

A channel is technically an **MCP server** that declares the `claude/channel` capability. You install it as a [plugin](./plugins.md) and configure with your own credentials.

---

## Comparison: where channels fit

| Feature | What it does | Good for |
|---|---|---|
| [Claude Code on the web](./claude-code-web.md) | Runs tasks in a fresh cloud sandbox cloned from GitHub | Async work you check on later |
| [Claude in Slack](https://code.claude.com/docs/en/slack) | Spawns a web session from `@Claude` mention | Starting tasks from team chat |
| Standard [MCP server](./mcp.md) | Claude queries it during a task; nothing pushed | On-demand access |
| [Remote Control](./remote-control.md) | You drive your local session from claude.ai or mobile | Steering an in-progress session |
| **Channels** | Push events INTO your already-running local session | Reacting to external events while away |

---

## Supported channel plugins

All from `claude-plugins-official`. Each requires [Bun](https://bun.sh).

### Telegram

```bash
# 1. Create a bot in @BotFather and copy the token

# 2. Install the plugin
/plugin install telegram@claude-plugins-official
/reload-plugins

# 3. Configure
/telegram:configure <token>          # saves to ~/.claude/channels/telegram/.env
                                      # or set TELEGRAM_BOT_TOKEN in shell

# 4. Restart with channels enabled
claude --channels plugin:telegram@claude-plugins-official

# 5. Pair: send any message to your bot. Bot replies with a code.
/telegram:access pair <code>

# 6. Lock down (allowlist only your account)
/telegram:access policy allowlist
```

### Discord

```bash
# 1. Create bot in Discord Developer Portal, enable "Message Content Intent"
# 2. Invite to server with permissions: View Channels, Send Messages,
#    Send Messages in Threads, Read Message History, Attach Files, Add Reactions

/plugin install discord@claude-plugins-official
/reload-plugins
/discord:configure <token>
claude --channels plugin:discord@claude-plugins-official

# 3. DM your bot, get pairing code
/discord:access pair <code>
/discord:access policy allowlist
```

### iMessage (macOS)

Reads Messages.app database directly, sends replies via AppleScript. No bot/external service needed.

```bash
# Grant Full Disk Access for ~/Library/Messages/chat.db when prompted
# (or Settings → Privacy & Security → Full Disk Access → add your terminal)

/plugin install imessage@claude-plugins-official
claude --channels plugin:imessage@claude-plugins-official

# Texting yourself bypasses access control automatically.
# To allow another contact:
/imessage:access allow +15551234567
/imessage:access allow user@example.com
```

The first reply Claude sends triggers a macOS Automation prompt asking if your terminal can control Messages. Click OK.

### fakechat (demo)

Localhost chat UI for testing the channel flow with no external service.

```bash
/plugin install fakechat@claude-plugins-official
claude --channels plugin:fakechat@claude-plugins-official
# Open http://localhost:8787, type a message
```

---

## How messages arrive

When a message comes in, your session sees:

```xml
<channel source="fakechat">
hey, what's in my working directory?
</channel>
```

Claude reads it, does the work, and calls the channel's `reply` tool. The reply shows up on the other side. **In your terminal you see the tool call and a confirmation ("sent"); the actual reply text appears on the other platform**, not in your terminal.

---

## Permissions during away-mode

If Claude hits a permission prompt while you're away, the session pauses until you respond. Two options:

- **Permission relay**: channel plugins that declare the [permission relay capability](https://code.claude.com/docs/en/channels-reference#relay-permission-prompts) can forward prompts to you so you can approve/deny remotely.
- **`--dangerously-skip-permissions`**: bypasses prompts entirely. Only use in trusted environments.

---

## CLI flags

| Flag | What it does |
|---|---|
| `--channels plugin:<name>@<marketplace>` | Channels to listen on. Space-separate for multiple |
| `--dangerously-load-development-channels <entries>` | Load channels not on the approved allowlist (for dev). Accepts `plugin:<name>@<marketplace>` and `server:<name>` entries. Prompts for confirmation |

---

## Security

Every approved channel plugin maintains a **sender allowlist**. Only IDs you've added can push messages; everyone else is silently dropped.

- **Telegram / Discord** bootstrap via pairing.
- **iMessage** auto-allows messages from yourself; add other contacts with `/imessage:access allow`.

On top of that, you control which servers are enabled per session with `--channels`, and on Team/Enterprise plans, an org admin controls availability with `channelsEnabled`.

> Being in `.mcp.json` isn't enough to push messages — a server also has to be named in `--channels`.

The allowlist also gates **permission relay** if the channel declares it. Anyone who can reply through the channel can approve/deny tool use — only allowlist senders you trust with that authority.

---

## Enterprise controls

On Team/Enterprise plans, channels are **off by default**. Two managed settings users cannot override:

| Setting | Purpose | When unset |
|---|---|---|
| `channelsEnabled` | Master switch. `true` to enable. Set in [admin console](https://claude.ai/admin-settings/claude-code) toggle or directly in managed settings | Channels blocked |
| `allowedChannelPlugins` | Allowlist of plugins that can register. Replaces the Anthropic-maintained list when set. Requires `channelsEnabled: true` | Anthropic default list applies |

Pro/Max users without an org skip these checks.

```json
// managed settings
{
  "channelsEnabled": true,
  "allowedChannelPlugins": [
    { "marketplace": "claude-plugins-official", "plugin": "telegram" },
    { "marketplace": "claude-plugins-official", "plugin": "discord" },
    { "marketplace": "acme-corp-plugins",       "plugin": "internal-alerts" }
  ]
}
```

When `allowedChannelPlugins` is set, it **replaces** the Anthropic allowlist entirely. Empty array blocks all channel plugins from the allowlist (but `--dangerously-load-development-channels` can still bypass for local testing). To block channels entirely including the dev flag, leave `channelsEnabled` unset.

If a user passes a plugin to `--channels` not on the org's list, Claude Code starts normally but the channel doesn't register, and the startup notice explains why.

---

## Build your own channel

The full reference is at [Channels reference](https://code.claude.com/docs/en/channels-reference). Pattern:

1. Build an MCP server that declares the `claude/channel` capability.
2. Define how messages arrive (HTTP webhook, file watcher, polling, etc.).
3. Define a `reply` tool the model can call to send back.
4. Optionally declare permission-relay capability.
5. Test with `--dangerously-load-development-channels server:<name>`.

Examples include CI/Sentry webhooks injecting events into a session where Claude already has your files open and remembers your debugging context.

---

## See also

- [mcp.md](./mcp.md) — channels are technically MCP servers
- [plugins.md](./plugins.md) — channels ship as plugins
- [remote-control.md](./remote-control.md) — alternative for driving sessions remotely
- [hooks.md](./hooks.md) — `Notification` hook reacts to channel messages
