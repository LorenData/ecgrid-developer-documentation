---
title: Cursor, Windsurf & Others
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Cursor/Windsurf connection guide - Greg Kolinski
*/}

# Cursor, Windsurf & Other MCP Tools

Many MCP-compatible tools support remote MCP servers natively — no Node.js required.

## Cursor

Add to `~/.cursor/mcp.json` or via **Settings → MCP**:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "url": "https://mcp.ecgrid.io/mcp",
      "headers": {
        "X-APIKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## Windsurf

Add via **Settings → MCP Servers → Add Server**, or edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "serverUrl": "https://mcp.ecgrid.io/mcp",
      "headers": {
        "X-APIKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## Other MCP-Compatible Tools

Use the same server URL and header for any tool that supports remote MCP servers:

| Item | Value |
|---|---|
| Server URL | `https://mcp.ecgrid.io/mcp` |
| Auth header | `X-APIKey: YOUR_API_KEY_HERE` |
| Transport | HTTP (SSE response) |

Config formats vary by tool version — check your tool's documentation. You can also paste the [ECGrid MCP Overview URL](../overview.md) into your AI and ask: *"How do I add this MCP server to [tool name]?"*

## Verify the Connection

After configuring, test with:

```
Test the ECGrid MCP connection
```

Expected: your ECGrid login name, auth level, network ID, and server time.
