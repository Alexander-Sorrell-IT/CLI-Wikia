# MCP — Model Context Protocol

Bob ships with two MCP servers bundled and available in all modes: **filelens**
and **sitemap**. Additional servers can be added via the Bob settings.

---

## Bundled servers

### filelens

Intelligent file reading for AI. Provides structural awareness of files before
reading content.

| Tool | What it does |
|---|---|
| `mcp__filelens__file_outline` | Scan a file's structure: classes, functions, headings with line numbers. Call this first before reading content. |
| `mcp__filelens__file_search` | Search a file for a keyword or regex pattern. Returns matching lines with surrounding context and exact line numbers. |
| `mcp__filelens__file_chunk` | Read a precise line range from a file, with line numbers. Use after `file_outline` or `file_search`. |
| `mcp__filelens__file_summarize` | Get a full picture of a file: structure outline + first 40 lines + last 20 lines. |
| `mcp__filelens__file_fetch` | Outline + targeted chunk in one call. Give it a file path and a target (function name, class, keyword). |

**When to use filelens vs native read_file:**
- Use `file_outline` first on any large file before reading content — saves tokens
- Use `file_chunk` for precise line ranges instead of reading the whole file
- Use `file_search` when you know what you're looking for but not where
- Use native `read_file` for small files or when you need the full content

---

### sitemap

Website awareness and content extraction for AI. Fetches and parses web pages
without HTML noise.

| Tool | What it does |
|---|---|
| `mcp__sitemap__site_fetch_page` | Fetch a URL and return clean readable text — no HTML tags, no scripts. |
| `mcp__sitemap__site_outline` | Discover what pages and routes exist on a site. Extracts all same-origin links, forms, and API hints. |
| `mcp__sitemap__site_search_page` | Fetch a URL and search it for a term in one call. Returns only matching sections. |
| `mcp__sitemap__site_awareness` | Build a full structured map of a site: every page with title+summary, every form, every API hint. |

---

## Adding MCP servers

Use the `configure-mcp` skill for step-by-step guidance:

```
use_skill("configure-mcp")
```

Or add directly to `.agents/settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server/index.js"],
      "env": { "API_KEY": "${MY_API_KEY}" }
    }
  }
}
```

Server types:
- `stdio` — local process (most common)
- `sse` — remote HTTP/SSE endpoint
- `http` — remote HTTP endpoint

---

## Building a custom MCP server

Use the `build-mcp-server` skill:

```
use_skill("build-mcp-server")
```

Covers project scaffolding, the `registerTool`/`registerResource`/`registerPrompt`
API, authentication patterns, building, and registering the server with Bob.

---

## Sources

Bob application documentation, filelens and sitemap MCP server documentation. Accessed 2026-08.
