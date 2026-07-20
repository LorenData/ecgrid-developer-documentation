---
title: Quick Start
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Initial MCP quick start - Greg Kolinski
2026-07-20: Update Step 1 for multi-credential model; add multiple-products section - Greg Kolinski
*/}

# Quick Start

Connect the ECGrid MCP Server to your AI tool in four steps.

## Step 1 — Get Your Credential

The ECGrid MCP Server supports three products. You need the credential for each product you want to use:

| Product | Header | Credential |
|---|---|---|
| ECGrid Connectivity | `X-Connectivity-API-Key` | ECGrid API key — your ECGrid Portal → account settings |
| GPA (DataSync) | `X-DataSync-API-Key` | GPA Personal Access Token (PAT) — from your GPA administration portal |
| Translation | `X-Translation-API-Key` | Translation API key — provided with your Translation subscription |

If you use multiple products, see [Adding Multiple Products](#adding-multiple-products) after completing setup.

> 🔒 Your credential goes in the config only — not in your conversation with the AI. Treat it like a password.

## Step 2 — Check Node.js (Claude Desktop only)

> **Developers calling the MCP server directly over HTTP:** skip this step. Node.js is not required for HTTP integrations.

Open a terminal and run:

```bash
node --version
```

You need **v18 or later**. If Node.js is missing or too old, install the LTS version from [nodejs.org](https://nodejs.org).

> Node.js is required by Claude Desktop as a local bridge to remote MCP servers — not by ECGrid. This is a one-time install.

## Step 3 — Add the Config Block

Add the following to your `claude_desktop_config.json` (replace `YOUR_API_KEY_HERE` with your ECGrid API key):

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
        "X-Connectivity-API-Key:YOUR_API_KEY_HERE",
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

## Adding Multiple Products

To use DataSync (GPA) or Translation alongside Connectivity, add their headers to the same config block — one `"ecgrid-mcp"` entry handles everything:

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
        "X-Connectivity-API-Key:YOUR_CONNECTIVITY_KEY",
        "--header",
        "X-DataSync-API-Key:YOUR_GPA_PAT",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

The MCP Server routes each credential to its product automatically.

## Need More Detail?

- [Full Claude Desktop setup](./connecting/claude-desktop) — merge instructions, hidden folder tips, troubleshooting
- [Cursor, Windsurf, and other tools](./connecting/cursor-windsurf)
- [Direct HTTP connection (developers)](./connecting/developer-http)
