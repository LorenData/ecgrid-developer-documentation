---
title: Claude Desktop
sidebar_position: 1
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Claude Desktop connection guide - Greg Kolinski
*/}

# Connect Claude Desktop

Full setup guide for connecting the ECGrid MCP Server to Claude Desktop on macOS and Windows.

## Let Claude Install It For You

The fastest way — paste one of these prompts into Claude and let it handle the setup.

:::caution Keep your API key out of the chat
Treat your ECGrid API key like a password. The prompts below leave `YOUR_API_KEY_HERE` as a placeholder — **fill in your actual key directly in the config file**, not in the chat. Get your key from [api.ecgridos.io](https://api.ecgridos.io) → account settings.
:::

### Option A — Claude Desktop (Fully Automated)

> Use this if you are already inside Claude Desktop. Claude Desktop has computer use capabilities — it can open a terminal, check for Node.js, locate and edit your config file, and verify the connection.

Copy and paste into Claude Desktop:

```
I want to connect the ECGrid MCP server to Claude Desktop. Please set it up for me by doing the following — ask my permission before taking any action that changes my system:

1. Open a terminal and run `node --version` to check if Node.js is installed
   - If Node.js v18 or higher is installed: confirm it and continue
   - If Node.js is missing or below v18: tell me what you found, ask my permission, then download and run the LTS installer from https://nodejs.org
2. Locate my claude_desktop_config.json file and open it
3. Add the ECGrid MCP block in the correct location, safely merging with any existing content — use YOUR_API_KEY_HERE as the placeholder for the API key
4. Show me the final file contents before saving and ask my permission to save
5. After I confirm, save the file and remind me to replace YOUR_API_KEY_HERE with my actual ECGrid API key before restarting
6. After I update the key, ask me to fully restart Claude Desktop
7. After I restart, test the connection by running: Test the ECGrid MCP connection

The ECGrid MCP server URL is https://mcp.ecgrid.io/mcp. Authentication uses the X-APIKey header. The mcpServers block to add is:
{
  "ecgrid-mcp": {
    "command": "npx",
    "args": ["-y","mcp-remote","https://mcp.ecgrid.io/mcp","--header","X-APIKey:YOUR_API_KEY_HERE","--transport","http-only"]
  }
}
```

After Claude finishes setup, open the config file and replace `YOUR_API_KEY_HERE` with your actual ECGrid API key before restarting Claude Desktop.

### Option B — Claude.ai Web or Mobile (Step-by-Step Guidance)

Copy and paste into any Claude conversation for guided manual setup.

```
I want to connect the ECGrid MCP server to Claude Desktop. Please guide me through setup step by step: check my OS, walk me through Node.js check/install, finding the config file, and adding the ECGrid MCP block. Use YOUR_API_KEY_HERE as the placeholder — I will fill in my actual key directly in the config file. Server URL: https://mcp.ecgrid.io/mcp, auth header: X-APIKey.
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

See the [Troubleshooting](../troubleshooting) page for a full table of error causes and fixes.
