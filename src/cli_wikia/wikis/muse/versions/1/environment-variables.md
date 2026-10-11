# muse environment variables

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: launcher script strings + `--help` + probes.

| Variable | Effect |
|----------|--------|
| `MUSE_AUTH_PATH` | Override `auth.json` location |
| `MUSE_LOGIN` | Launcher login behavior |
| `MUSE_CHANNEL` / `MUSE_RELEASE_INFO` | Update channel/pin |
| `MUSE_NO_AUTO_UPDATE` / `MUSE_UPDATE_INTERVAL_SECONDS` / `MUSE_SYNC_UPDATE` | Update control |
| `MUSE_LAUNCHER_INSTALL` | Install target |
| `MUSE_PROJECTS_HOME` | Projects home (else `~/.muse/projects`) |
| `XDG_CONFIG_HOME` | Relocates `~/.config/muse` (proven in probes) |
| `QWEN_TLS_INSECURE` | N/A (qwen-only; muse uses `--tls-insecure`) |

No `MUSE_CONFIG_DIR` analog was found; config relocation goes through XDG.
