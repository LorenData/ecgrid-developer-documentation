---
title: Resources & Prompts
sidebar_position: 7
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP resources and prompts reference - Greg Kolinski
*/}

# Resources & Prompts

The ECGrid MCP Server exposes MCP Resources and MCP Prompts in addition to tools. These do **not** appear in `tools/list` — they are available to MCP clients that request them via `resources/list` and `prompts/list`.

## MCP Resources

Resources are server-side reference data that AI agents can read during a session.

| Resource | Description |
|---|---|
| `Glossary` | ECGrid terminology reference — qualifier codes, status code meanings, object type definitions |
| `InterchangeStatus` | Complete interchange status code catalog with descriptions and severity levels |
| `ParcelStatus` | Complete parcel status code catalog with descriptions and severity levels |

> MCP-compatible AI tools (Claude Desktop, Cursor, Windsurf) load resources automatically when the AI needs them. Developers can request them via `resources/read`.

## MCP Prompts

Prompts are guided multi-step sequences exposed by the server.

| Prompt | Description |
|---|---|
| `InvestigatePartner` | Guided sequence for diagnosing a trading partner relationship — checks config, traffic history, and delivery status in order |
| `TriageStuckInterchange` | Guided sequence for triaging a stuck or pending interchange — walks through parcel status, route config, and retry state |

> Use prompts by asking your AI: *"Investigate this trading partner"* or *"Triage this stuck interchange"* — the AI will invoke the guided sequence automatically if your MCP client supports prompts.

## Status Code Reference

The `connectivity_system_get-status-list` tool returns the complete ECGrid status-code catalog at runtime — use it to resolve any status code seen on parcels or interchanges.

See also: the `connectivity_system_get-status-list` tool — documented in the Tools section once the tools pages are published.
