# muse skills

> wiki-version: 1 | cli-version: 1.4.4 | verified: 2026-10-10
> source: `muse skills --help` + live `skills list --source built-in`.

Skills are Markdown capability packs (name + description + body) with
enable/disable/validate/install/import/update/uninstall lifecycle and
user|project scope (`--scope user|project`, `--all`).

## Commands

`list` (`--source all|built-in|user|project|plugin`, `--details`),
`inspect <id>` (shows body; bundled bodies live under
`~/.local/share/muse/skills/`), `enable|disable <id>`, `validate
<path>` (front-matter + body), `install <source>` (file/dir/URL),
`import --from claude|codex` (foreign skills + rules), `update`
(refresh manifests), `uninstall <id>`.

## Built-in roster (observed, 25+)

doctor, create-plugin, create-skill, plan, grill, import/resume/migrate
family, read-session, manage-settings, git, python-env, durable-test-
collateral, browser-app-delivery, greenfield-project-scaffolding,
table-fit, taste, workflow-authoring, requirements-clarification, +
plugin skills (e.g. threejs). Reminder skills (`tbh-reminders`) inject
system-reminders at safe points. Foreign imports land staged for review,
never auto-trusted.
