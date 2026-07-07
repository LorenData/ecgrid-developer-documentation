{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Initial MCP quick start - Greg Kolinski
*/}
---
title: Quick Start
sidebar_position: 2
---

# Quick Start

Connect the ECGrid MCP Server to your AI tool in four steps.

## Step 1 — Get Your ECGrid API Key

Go to the [ECGrid Developer Portal](https://api.ecgridos.io/), log in, and copy your API key from account settings. This is the same key used for the REST and SOAP APIs — no new account needed.

## Step 2 — Check Node.js (Claude Desktop only)

> **Developers calling the MCP server directly over HTTP:** skip this step. Node.js is not required for HTTP integrations.

Open a terminal and run:

```bash
node --version
```

You need **v18 or later**. If Node.js is missing or too old, install the LTS version from [nodejs.org](https://nodejs.org).

> Node.js is required by Claude Desktop as a local bridge to remote MCP servers — not by ECGrid. This is a one-time install.

## Step 3 — Add the Config Block

Add the following to your `claude_desktop_config.json` (replace `YOUR_API_KEY_HERE`):

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

Config file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Or open it directly: Claude Desktop → hamburger menu (☰) → Settings → Developer → Edit Config.

Fully restart Claude Desktop after saving.

## Step 4 — Test the Connection

Type this prompt in your AI tool:

```
Test the ECGrid MCP connection
```

A successful response returns your ECGrid login name, auth level, network ID, and current server time.

## Need More Detail?

- [Full Claude Desktop setup](./connecting/claude-desktop) — merge instructions, hidden folder tips, troubleshooting
- [Cursor, Windsurf, and other tools](./connecting/cursor-windsurf)
- [Direct HTTP connection (developers)](./connecting/developer-http)
