# Themes, keyboard shortcuts & notifications

Gemini CLI lets you customize its color scheme with built-in or custom themes,
rebind keyboard shortcuts, and receive system notifications when a session needs
attention.

## Themes

Change the theme with the `/theme` command or the `ui.theme` setting. Selected
themes are saved in your configuration and remembered across sessions.

### Built-in themes

| Dark themes        | Light themes     |
| ------------------ | ---------------- |
| `ANSI`             | `ANSI Light`     |
| `Atom One`         | `Ayu Light`      |
| `Ayu`              | `Default Light`  |
| `Default`          | `GitHub Light`   |
| `Dracula`          | `Google Code`    |
| `GitHub`           | `Solarized Light`|
| `Holiday`          | `Xcode`          |
| `Shades Of Purple` |                  |
| `Solarized Dark`   |                  |
| `Tokyo Night`      |                  |

### Changing themes

1. Enter `/theme` in Gemini CLI.
2. A selection dialog lists the available themes (some interfaces show a live
   preview as you move).
3. Use the arrow keys to select, then confirm.

> If a theme is set in `settings.json` (by name or file path), you must remove
> the `theme` setting before `/theme` can change it interactively.

### Custom themes

Define your own themes under `ui.customThemes` in user, project, or system
`settings.json`. Each theme is an object keyed by a unique name. Two properties
are required: `name` (must match the key) and `type` (must be `"custom"`).

```json
{
  "ui": {
    "customThemes": {
      "MyCustomTheme": {
        "name": "MyCustomTheme",
        "type": "custom",
        "background": { "primary": "#181818" },
        "text": { "primary": "#f0f0f0", "secondary": "#a0a0a0" }
      }
    }
  }
}
```

Color values may be hex codes (`#FF0000`) or CSS color names (`coral`, `teal`).

#### Color / semantic tokens

| Group        | Tokens                                                                 |
| ------------ | --------------------------------------------------------------------- |
| `text`       | `primary`, `secondary`, `link`, `accent`, `response` (overrides `primary` for model responses) |
| `background` | `primary`, `diff.added`, `diff.removed`                                |
| `border`     | `default`, `focused`                                                   |
| `status`     | `success`, `warning`, `error`                                          |
| `ui`         | `comment`, `symbol`, `gradient` (array of colors)                      |

All sub-properties are optional, but providing at least `background.primary`,
`text.primary`, `text.secondary`, `text.link`, `text.accent`, and the `status`
colors is recommended for a cohesive UI.

#### Loading a theme from a file

Point `ui.theme` at a JSON file using the same structure as a custom theme:

```json
{ "ui": { "theme": "/path/to/your/theme.json" } }
```

> For safety, Gemini CLI loads theme files **only** from within your home
> directory. A theme outside it is rejected with a warning.

To use a custom theme, select it in `/theme` (it appears in the dialog) or set
`ui.theme` to its name. Themes provided by [extensions](./extensions.md) also
appear in the list, labeled with the extension name in parentheses, for example
`shades-of-green (green-extension)`.

## Keyboard shortcuts

Gemini CLI ships default keybindings for editing input, navigating history, and
controlling the UI. The most commonly used bindings:

### Basic controls

| Action                                             | Keys              |
| -------------------------------------------------- | ----------------- |
| Confirm selection / submit prompt                  | `Enter`           |
| Cancel / dismiss dialog                            | `Esc`, `Ctrl+[`   |
| Cancel current request, or quit when input empty   | `Ctrl+C`          |
| Exit when input buffer is empty                    | `Ctrl+D`          |
| Clear the terminal screen                           | `Ctrl+L`          |
| Suspend the CLI to the background                  | `Ctrl+Z`          |

### Editing & cursor

| Action                                | Keys                                   |
| ------------------------------------- | -------------------------------------- |
| Start / end of line                   | `Ctrl+A`/`Home`, `Ctrl+E`/`End`        |
| Move by word (left/right)             | `Ctrl+Left`/`Alt+B`, `Ctrl+Right`/`Alt+F` |
| Delete to end / start of line         | `Ctrl+K`, `Ctrl+U`                     |
| Delete previous / next word           | `Ctrl+W`/`Alt+Backspace`, `Alt+D`      |
| Undo / redo                           | `Ctrl+Z`, `Ctrl+Shift+Z`               |
| Insert newline without submitting     | `Ctrl+Enter`, `Shift+Enter`, `Ctrl+J`  |
| Open prompt in external editor        | `Ctrl+G`                               |
| Paste from clipboard                  | `Ctrl+V`                               |

### History, navigation & input

| Action                                        | Keys              |
| --------------------------------------------- | ----------------- |
| Previous / next history entry                 | `Ctrl+P`, `Ctrl+N`|
| Reverse-search history                        | `Ctrl+R`          |
| Accept inline suggestion                      | `Tab`             |
| Queue current prompt after the running task   | `Tab`             |
| Scroll up / down                              | `Shift+Up`, `Shift+Down` |
| Scroll page up / down                         | `Page Up`, `Page Down` |

### App controls

| Action                                                        | Keys        |
| ------------------------------------------------------------- | ----------- |
| Toggle debug console (error details)                          | `F12`       |
| Toggle full TODO list                                         | `Ctrl+T`    |
| Toggle Markdown rendering                                     | `Alt+M`     |
| Toggle mouse mode                                             | `Ctrl+S`    |
| Toggle YOLO (auto-approval) mode                              | `Ctrl+Y`    |
| Cycle approval modes (default → auto-edit → plan)             | `Shift+Tab` |
| Expand/collapse content blocks or paste placeholders          | `Ctrl+O`    |
| Toggle background shell visibility / list                     | `Ctrl+B`, `Ctrl+L` |

### Prompt-line shortcuts

- `!` on an empty prompt: enter or exit shell mode.
- `?` on an empty prompt: toggle the shortcuts panel.
- `Tab` `Tab` while typing: toggle between minimal and full UI details.
- `Esc` `Esc` (twice): clear a non-empty prompt, otherwise rewind previous
  interactions.

Vim mode (NORMAL/INSERT) is available with `/vim` or the `general.vimMode: true`
setting.

### Customizing keybindings

Create `~/.gemini/keybindings.json` — a JSON array of `{ "command", "key" }`
objects (VS Code-like). Prefix a command with `-` to unbind.

```json
[
  { "command": "edit.clear", "key": "cmd+l" },
  { "command": "-app.toggleYolo", "key": "ctrl+y" },
  { "command": "input.submit", "key": "ctrl+y" }
]
```

- Matching is **explicit**: a binding for `ctrl+f` won't fire on `ctrl+shift+f`.
- Binding a key does **not** auto-unbind it from other commands.
- Modifiers: `ctrl`, `shift`, `alt` (`opt`/`option`), `cmd` (`meta`). Base keys
  may be any single code point or named keys (`enter`, `escape`, `tab`, `f1`–`f35`,
  `numpad0`–`numpad9`, etc.).

> Terminal limits: on Windows Terminal, `shift+enter` needs v1.25+ and `shift+tab`
> is unsupported on Node 20 / older Node 22; macOS Terminal does not support
> `shift+enter`.

## Notifications (experimental)

Gemini CLI can send system notifications when a session completes or needs your
attention (such as waiting for tool approval) — handy for long-running tasks and
Plan Mode while you work in other windows.

Enable via `/settings` (**General → Enable Notifications**) or in `settings.json`:

```json
{ "general": { "enableNotifications": true } }
```

| Notification type | Triggered when                                            |
| ----------------- | --------------------------------------------------------- |
| Action required   | The model is waiting for user input or tool approval.     |
| Session complete  | A session finishes successfully.                          |

The CLI uses the **OSC 9** terminal escape sequence, supported by terminals like
iTerm2, WezTerm, Ghostty, and Kitty. If your terminal lacks OSC 9 support, the
CLI falls back to a terminal bell (BEL), which most terminals turn into a taskbar
flash or alert sound.

## See also

- [settings.md](./settings.md) — `ui.theme`, `ui.customThemes`, `general.enableNotifications`
- [configuration.md](./configuration.md) — settings scopes and precedence
- [commands.md](./commands.md) — `/theme`, `/settings`, `/vim`
- [extensions.md](./extensions.md) — themes provided by extensions
