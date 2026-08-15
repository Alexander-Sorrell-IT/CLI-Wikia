# Skills

Skills extend what Bob can do. Each skill is a directory containing a `SKILL.md`
file. Bob activates a skill when the user's request matches the skill's
description, or when the user calls `use_skill` with the skill name.

---

## How skills work

1. Bob reads the skill's description (from `SKILL.md` frontmatter).
2. When a user request matches, Bob calls `use_skill` to load the full instructions.
3. The skill instructions are injected into context and Bob follows them for that task.
4. Each skill is activated **at most once per context window**. If context is
   compacted, re-activate with `use_skill` again.

---

## Skill file format

```
.agents/skills/
└── skill-name/
    └── SKILL.md    ← required; contains frontmatter + body
```

`SKILL.md` frontmatter (YAML between `---` fences):

```yaml
---
name: skill-name
description: "One-sentence description. Used for auto-matching."
---
```

Body: the instructions Bob follows when the skill is active. Can be any length.

---

## Available skills (installed on this machine)

| Skill | Description |
|---|---|
| `bug-bounty` | Complete bug bounty workflow — recon, vulnerability hunting, LLM/AI security, bypass tables, reporting |
| `bb-methodology` | Master orchestrator for bug bounty hunting sessions; routes to other skills by phase |
| `web2-vuln-classes` | Reference for 20 web2 bug classes with root causes, detection patterns, bypass tables |
| `web2-recon` | Web2 recon pipeline — subdomain enum, live host discovery, URL crawling, JS analysis |
| `security-arsenal` | Security payloads, bypass tables, wordlists, always-rejected bug list |
| `triage-validation` | Finding validation before writing any report — 7-Question Gate, pre-submission gates |
| `report-writing` | Bug bounty report writing for H1/Bugcrowd/Intigriti/Immunefi |
| `ai-bug-bounty` | Web-app vulnerability scanning via the AI-Bug-Bounty Python toolkit |
| `bounty-hunter-atlas` | Atlas skill for bounty hunting |
| `meme-coin-audit` | Meme coin and token security audit — rug pull detection, Solana SPL analysis |
| `source-command-memory-gc` | Inspect or rotate hunt-memory JSONL files |
| `create-skill` | Guide for creating a new Bob skill (SKILL.md) |
| `create-mode` | Guide for creating a new custom Bob mode |
| `configure-mcp` | Add a new MCP server or diagnose an existing one |
| `build-mcp-server` | Guide for building a custom MCP server from scratch |
| `xlsx-insights` | Analysis, extraction, or insights from Excel (.xlsx) workbooks |

---

## Activating a skill

```
use_skill("skill-name")
```

Bob activates skills automatically when the description matches the task, or you
can say: *"use the bug-bounty skill"* / *"activate report-writing"*.

---

## Creating a new skill

Activate the `create-skill` skill for the exact format and gotchas:

```
use_skill("create-skill")
```

Quick summary:
1. Create `.agents/skills/my-skill/SKILL.md`
2. Add YAML frontmatter with `name` and `description`
3. Write the instructions in the body
4. Bob will pick it up automatically on next session start

---

## Skill location

Skills are discovered from:

| Location | Scope |
|---|---|
| `.agents/skills/` in the project root | Project-scoped |
| `~/.config/bob/skills/` | User-scoped (all projects) |

Project skills take precedence over user skills when names conflict.

---

## Sources

Bob application documentation and the installed skill files at `.agents/skills/`. Accessed 2026-08.
