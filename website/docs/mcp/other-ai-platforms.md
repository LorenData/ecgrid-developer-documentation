---
title: Other AI Platforms
sidebar_position: 8
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Other AI platforms page - Greg Kolinski
*/}

# Other AI Platforms

The ECGrid MCP Server uses the open MCP standard. Any AI tool or platform that supports MCP natively can connect using the server URL and API key — no additional setup required.

## ChatGPT

ChatGPT has a dedicated setup guide covering Custom GPT Actions (works today via the ECGrid REST API OpenAPI spec) and native MCP via ChatGPT Apps (pending ECGrid Bearer/OAuth support).

See [Connect ChatGPT to ECGrid](./connecting/chatgpt.md).

## Platforms Without Native MCP Support

For platforms that do not support MCP natively — such as Grok and others — ECGrid provides a full REST API that any platform can call directly:

- **ECGrid REST API**: [rest.ecgrid.io](https://rest.ecgrid.io/index.html) — full interactive documentation
- **OpenAPI / Swagger spec**: [rest.ecgrid.io/swagger/v2/swagger.json](https://rest.ecgrid.io/swagger/v2/swagger.json) — import into LangChain, or any OpenAPI-compatible toolchain

The REST API uses the same ECGrid API key (`X-APIKey` header) and covers the full breadth of ECGrid operations.

## Using ECGrid Tools with OpenAI and Other LLMs

The ECGrid MCP client HTTP code is identical regardless of which LLM you use. Only the LLM client and tool schema format change. See the [Building Agents](./building-agents.md) page for the OpenAI chat loop examples and the Anthropic/OpenAI/Gemini tool schema translation table.
