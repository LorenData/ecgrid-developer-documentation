---
title: MCP Overview
sidebar_position: 1
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Initial MCP section overview - Greg Kolinski
*/}

# ECGrid MCP

**You create the experience. We power the connections.**

The ECGrid MCP Server brings ECGrid's full B2B connectivity layer directly into AI agents, AI assistants, and AI-powered applications via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

## What Is MCP?

The Model Context Protocol is an open standard that lets AI tools connect to external services as native capabilities. Once the ECGrid MCP Server is connected, your AI can call ECGrid operations directly — no custom integration code required per operation.

## The ECGrid MCP Server

| Item | Value |
|---|---|
| Server URL | `https://mcp.ecgrid.io/mcp` |
| Protocol | MCP over HTTP (JSON-RPC 2.0) |
| MCP Version | `2024-11-05` |
| Authentication | `X-APIKey` header (your ECGrid API key) |
| Tools | 41 tools across 13 categories |

## Who This Is For

**ECGrid customers** — connect Claude Desktop (or any MCP-compatible AI tool) to your ECGrid account in about 5 minutes. Ask your AI about trading partners, transaction history, mailboxes, and network status in plain language instead of logging into the portal.

**Developers** — add ECGrid B2B capabilities to any AI agent, chatbot, or automation workflow. All tools return structured JSON for programmatic consumption. A subset of tools additionally render an interactive UI component in Claude Desktop and Claude.ai.

## Next Steps

- **New to MCP?** → [Quick Start](./quick-start.md)
- **Setting up Claude Desktop?** → [Connect Your AI Tool](./connecting/claude-desktop)
- **Building an agent?** → [Building Agents](./building-agents)
- **Looking up a specific tool?** → [Tools Reference](./tools/overview)
