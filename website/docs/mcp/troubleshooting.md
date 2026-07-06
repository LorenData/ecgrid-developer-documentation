{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP troubleshooting page - Greg Kolinski
*/}
---
title: Troubleshooting
sidebar_position: 9
---

# Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or missing API key | Verify `X-APIKey` value — no spaces around the colon |
| `406 Not Acceptable` | Missing or incorrect `Accept` header | Set `Accept: application/json, text/event-stream` on every request |
| `429 Too Many Requests` | Per-IP rate limit hit | Wait 60 seconds and retry — check `Retry-After` header |
| `503 Service Unavailable` | Server concurrency cap reached | Wait 1 second and retry — this is transient |
| `Connection refused` | Incorrect server URL | Use `https://mcp.ecgrid.io/mcp` exactly |
| Tool not appearing in AI assistant | Config not loaded | Fully restart the AI application after saving the config file |
| Can't find the config file | Unsure of location | Claude Desktop → hamburger menu → Settings → Developer → Edit Config |
| Can't find the config file on macOS | Library folder is hidden | Use Go → Go to Folder, paste `~/Library/Application Support/Claude/` |
| Can't find the config file on Windows | AppData folder is hidden | Paste `%APPDATA%\Claude\` into the File Explorer address bar |
| `node: command not found` | Node.js not installed | See [Quick Start](./quick-start.md) Step 2 — Claude Desktop users only |
| Node.js version too old | Version below v18 | Install the LTS version from [nodejs.org](https://nodejs.org) |
| JSON parse error on config file | Malformed JSON | Paste your config into [jsonlint.com](https://jsonlint.com) to find the error |
| ECGrid block not working despite no error | `mcpServers` block placed outside main object | The block must be inside the single outer `{}` — see [Claude Desktop setup](./connecting/claude-desktop.md) |
| `loginName` shows unexpected value | Wrong API key | Confirm the key at the [ECGrid Developer Portal](https://api.ecgridos.io/) |
| `413 Payload Too Large` | Request body over 64 KB | Reduce request payload size |
| Empty `tools/list` response | Server unreachable or bad auth | Check API key and network connectivity; verify URL |

> **Still stuck?** Paste the [ECGrid MCP Overview](./overview.md) into Claude or any AI assistant and describe what you're seeing. The AI can help diagnose the issue step by step. Or contact [ECGrid Support](https://ecgrid.freshdesk.com/support/home).
