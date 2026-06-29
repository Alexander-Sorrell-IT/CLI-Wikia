# Skills

Skills are reusable, specialized instructions packaged as `SKILL.md` files. They extend Copilot with on-demand capabilities the agent pulls in when relevant — narrower than a [custom agent](custom-agents.md), broader than a single instruction.

Reference: `copilot skill --help`.

---

## Where skills come from

| Source | Location |
|---|---|
| Project | `.github/skills/`, `.agents/skills/`, or `.claude/skills/` |
| Personal | `~/.copilot/skills/` or `~/.agents/skills/` |
| Plugin | Skills bundled by installed [plugins](plugins.md) |
| Custom | Directories you add with `copilot skill add <directory>` |

Each skill is a subdirectory containing a `SKILL.md` file (plus any supporting files it references). The `.github/skills/`, `.claude/skills/`, and `.agents/skills/` paths mean Copilot can reuse skills authored for other agent ecosystems.

---

## Managing skills

```bash
copilot skill list                    # all available skills
copilot skill add <file|url|dir>      # add a skill from a file, URL, or directory
copilot skill remove <name|dir>       # remove a skill or a custom skill directory
```

Inside a session, `/skills` opens the management UI.

---

## How skills are used

Skills are discovered at startup and surfaced to the model. When your request matches a skill's described purpose, Copilot loads that skill's instructions to guide its work. Use `/env` to confirm which skills loaded for the current session.

---

## Authoring a skill

At minimum a skill is a directory with a `SKILL.md`:

```
my-skill/
└── SKILL.md
```

`SKILL.md` describes what the skill does and the steps Copilot should follow. Place the directory under one of the source locations above (e.g. `.github/skills/my-skill/`) or register it with `copilot skill add ./my-skill`.

> The exact `SKILL.md` frontmatter schema isn't fully enumerated in the CLI's built-in help — verify field-level details in the official docs before relying on advanced fields.

---

## See also

- [custom-agents.md](custom-agents.md) — a full persona vs a single capability
- [plugins.md](plugins.md) — distribute skills as part of a plugin
- [custom-instructions.md](custom-instructions.md) — always-on repo guidance
