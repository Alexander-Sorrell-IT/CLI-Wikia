# muse auth

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `--help` + launcher script + observed `~/.config/muse/`.

`muse auth|login|logout` manage provider credentials in
`~/.config/muse/auth.json` (`MUSE_AUTH_PATH` overrides). Launcher env:
`MUSE_LOGIN`, `MUSE_CHANNEL`, `MUSE_NO_AUTO_UPDATE`,
`MUSE_UPDATE_INTERVAL_SECONDS`, `MUSE_SYNC_UPDATE`, `MUSE_RELEASE_INFO`,
`MUSE_LAUNCHER_INSTALL`. Downloads come from the vendor lookaside host
with auth headers; `--base-url` overrides the provider URL per run.
`trust.json` records per-project trust decisions consumed by plugins,
delegation, and project sources.
