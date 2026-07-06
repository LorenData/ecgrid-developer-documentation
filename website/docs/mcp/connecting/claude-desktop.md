{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Claude Desktop connection guide - Greg Kolinski
*/}
---
title: Claude Desktop
sidebar_position: 1
---

# Connect Claude Desktop

Full setup guide for connecting the ECGrid MCP Server to Claude Desktop on macOS and Windows.

## Let Claude Install It For You

The fastest way — paste one of these prompts into Claude and let it handle the setup.

### Option A — Claude Desktop (Fully Automated)

> Use this if you are already inside Claude Desktop. Claude Desktop has computer use capabilities — it can open a terminal, check for Node.js, locate and edit your config file, and verify the connection.

Copy and paste into Claude Desktop:

```
I want to connect the ECGrid MCP server to Claude Desktop. Please set it up for me by doing the following — ask my permission before taking any action that changes my system:

1. Ask me for my ECGrid API key (I can get it from https://api.ecgridos.io/ → account settings if I don't have it handy)
2. Open a terminal and run `node --version` to check if Node.js is installed
   - If Node.js v18 or higher is installed: confirm it and continue
   - If Node.js is missing or below v18: tell me what you found, ask my permission, then download and run the LTS installer from https://nodejs.org
3. Locate my claude_desktop_config.json file and open it
4. Add the ECGrid MCP block in the correct location, safely merging with any existing content
5. Fill in my API key in the X-APIKey line — no spaces around the colon
6. Show me the final file contents before saving and ask my permission to save
7. After I confirm, save the file and ask me to fully restart Claude Desktop
8. After I restart, test the connection by running: Test the ECGrid MCP connection

The ECGrid MCP server URL is https://mcp.ecgrid.io/mcp. Authentication uses the X-APIKey header. The mcpServers block to add is:
{
  "ecgrid-mcp": {
    "command": "npx",
    "args": ["-y","mcp-remote","https://mcp.ecgrid.io/mcp","--header","X-APIKey:PLACEHOLDER","--transport","http-only"]
  }
}
```

### Option B — Claude.ai Web or Mobile (Step-by-Step Guidance)

Copy and paste into any Claude conversation for guided manual setup.

```
I want to connect the ECGrid MCP server to Claude Desktop. Please guide me through setup step by step. Ask me for my ECGrid API key, my OS, then walk me through Node.js check/install, finding the config file, and adding the ECGrid MCP block with my key filled in. Server URL: https://mcp.ecgrid.io/mcp, auth header: X-APIKey.
```

---

## Manual Setup

### Step 1 — Check and Install Node.js

Open a terminal and run:

```
node --version
```

You need **v18 or later**. Install from [nodejs.org](https://nodejs.org) if missing or too old.

:::tip macOS — opening Terminal
Press `Cmd + Space`, type `Terminal`, press Enter.
:::

:::tip Windows — opening Command Prompt
Press the Windows key, type `cmd`, press Enter.
:::

### Step 2 — Find Your Config File

The fastest way: Claude Desktop → hamburger menu (☰) → **Settings** → **Developer** → **Edit Config**.

Manual paths:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

:::caution macOS — Library folder is hidden
Use **Go** → **Go to Folder** (Cmd+Shift+G) and paste `~/Library/Application Support/Claude/`.
:::

:::caution Windows — AppData folder is hidden
Paste `%APPDATA%\Claude\` directly into the File Explorer address bar.
:::

### Step 3 — Add the Config Block

**New file or empty file** — paste this exactly:

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

**File already has content** — add the `"ecgrid-mcp"` block inside the existing `"mcpServers"` section. Never duplicate the outer `{}` or add a second `"mcpServers"` key. Validate with [jsonlint.com](https://jsonlint.com) if unsure.

### Step 4 — Restart and Test

Fully close and reopen Claude Desktop, then type:

```
Test the ECGrid MCP connection
```

A successful response returns your ECGrid login name, auth level, and network ID.

## Troubleshooting

See the [Troubleshooting](../troubleshooting.md) page for a full table of error causes and fixes.
