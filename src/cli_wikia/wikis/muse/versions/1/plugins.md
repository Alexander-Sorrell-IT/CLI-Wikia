# muse plugins

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: plugin contract + capability examples + live install/approve probes
> under an isolated HOME.

## Manifest

A native plugin is a workspace dir containing `.muse-plugin/plugin.json`
(`schemaVersion: 1`, id grammar `^[a-z0-9][a-z0-9._-]{0,79}$`, Windows
reserved basenames rejected). `compat: {source: native, manifestDir:
.muse-plugin}`. Supported families: skills, commands, hooks, mcpServers,
reminders. Unsupported: tools, agents, outputStyles, settings, apps.
Reserved ids include `muse-core`, `loop`, `tbh-reminders`, `threejs`.

## Lifecycle

`muse plugins install <path> --scope user|project` (validates, freezes
into `plugins/cache/`, reports `enabled/trust/provenance`) →
`muse plugins approve <id>` (hooks require review before activation) →
active. `list`, `uninstall`, `validate <path>` (`--profile`).
Capability paths resolve from the PLUGIN ROOT; hook source files cannot be
shared by two hook IDs. Commands are Markdown templates; reminders are
scheduled nudges.

## Trust and provenance

`PluginSource`: curated, marketplaceUserAdded, foreignImport,
nativeLocal. Untrusted workspaces block project-local sources. Cache is
content-hashed (`cache/<source>/<id>/<hash>/package`).
