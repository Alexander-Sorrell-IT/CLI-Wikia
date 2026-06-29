# Custom Agents

A custom agent is a reusable persona with its own instructions, tool access, model, and MCP servers. You define one in a Markdown file with a `.agent.md` extension and YAML frontmatter, then invoke it by name.

Reference: [Creating custom agents for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli) and the [custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration).

---

## Where agent files live

| Scope | Location |
|---|---|
| Project | `.github/agents/<name>.agent.md` |
| Personal | `~/.copilot/agents/<name>.agent.md` |

If a project and a personal agent share a name, **the one in your home directory wins**. The filename (without `.agent.md`) is the agent's identifier used with `--agent`.

---

## File format

A `.agent.md` file is YAML frontmatter followed by the agent's system instructions (the prompt body, max **30,000 characters**).

```yaml
---
name: implementation-planner
description: Creates detailed implementation plans and technical
  specifications in markdown format
tools: ["read", "search", "edit"]
---

You are a technical planning specialist focused on creating
comprehensive implementation plans. Your responsibilities:

- Analyze requirements and break them down into actionable tasks
- Create detailed technical specifications and architecture documentation
- Generate implementation plans with clear steps, dependencies, and timelines
```

### Frontmatter properties

| Property | Type | Meaning |
|---|---|---|
| `description` | string (**required**) | The agent's purpose and capabilities — also used for inference-based selection |
| `name` | string | Display name (optional; defaults from the filename) |
| `tools` | list or comma-separated string | Tools the agent may use. Default: **all tools**. Supports wildcards like `mcp-server/*` or specific `github/tool-name` |
| `model` | string | Model for this agent; inherits the session default if unset |
| `mcp-servers` | object | Extra MCP servers/tools available only to this agent |
| `target` | string | Target context: `vscode` or `github-copilot` |
| `disable-model-invocation` | boolean | Prevent the cloud agent from auto-selecting this agent |
| `user-invocable` | boolean | Whether a user can pick this agent |
| `metadata` | object | Arbitrary name/value annotations |

> Restricting `tools` writes a tools specification into the file. Leaving it out grants all tools.

---

## Creating an agent

Inside a session, `/agent` lets you create one two ways:

- **Let Copilot generate it** — describe the expertise and use cases; Copilot drafts a profile you can review, retry, or accept.
- **Manual guided setup** — provide a name (lowercase + hyphens recommended), description, instructions, and tool access.

You can also just write the `.agent.md` file by hand.

---

## Invoking an agent

| Method | How |
|---|---|
| CLI flag | `copilot --agent security-auditor --prompt "Check /src/app/validator.go"` |
| Slash command | `/agent [name]` and pick from the list |
| Explicit | Tell Copilot to use a named agent in your prompt |
| Inference | Use a prompt that matches the agent's `description`/trigger words |

```bash
copilot --agent security-auditor -p "Check /src/app/validator.go" --allow-all-tools
```

---

## Local vs remote agents

Org/enterprise can publish remote custom agents. Set `customAgents.defaultLocalOnly: true` in `settings.json` to use only local agents and ignore remote ones.

---

## See also

- [custom-instructions.md](custom-instructions.md) — repo-wide guidance (AGENTS.md) vs per-agent personas
- [skills.md](skills.md) — narrower, callable capabilities
- [plugins.md](plugins.md) — bundle agents for distribution
- [permissions.md](permissions.md) — how `tools` restrictions are enforced
