---
title: Tools Overview
sidebar_position: 1
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP tools overview - Greg Kolinski
*/}

# Tools Reference

The ECGrid MCP Server exposes 41 Connectivity tools across 13 categories. All Connectivity tools are prefixed `connectivity_` and return structured JSON data.

Call `tools/list` at startup to get the current complete tool list with full input schemas — new tools are added regularly and the response is always authoritative. For programmatic discovery, `GET https://mcp.ecgrid.io/tools.json` returns the same registry without authentication.

## Tool Categories

| Category | Tools | Interactive UI |
|---|---|---|
| [System](./system/hello-world) | `hello-world`, `get-version`, `get-status-list` | — |
| [Users](./users/get-user-me) | `get-user-me`, `get-user-by-id`, `get-user-by-login`, `list-users` | — |
| [Network](./network/get-network-by-id) | `get-network-by-id` | — |
| [Mailboxes](./mailboxes/get-mailbox-by-id) | `get-mailbox-by-id`, `list-mailboxes`, `get-mailbox-by-name` | `get-mailbox-by-id`, `list-mailboxes` |
| [ECGrid IDs](./ecgrid-ids/get-ecgrid-id-by-id) | `get-ecgrid-id-by-id`, `find-edi-ids`, `list-ecgrid-ids-by-mailbox` | All three |
| [Partners](./partners/get-partner-by-id) | `get-partner-by-id`, `list-partners`, `check-partner-config`, `test-partner-delivery`, `get-partner-document-counts` | `get-partner-by-id`, `list-partners` |
| [Comms](./comms/get-comm-by-id) | `get-comm-by-id`, `list-comms`, `find-comms`, `test-comm`, `check-ftp-access` | — |
| [Parcels](./parcels/get-parcel-by-id) | `get-parcel-by-id`, `list-inbox-parcels`, `list-outbox-parcels`, `list-pending-inbox-parcels` | `get-parcel-by-id` |
| [Interchanges](./interchanges/get-interchange-by-id) | `get-interchange-by-id`, `list-inbox-interchanges`, `list-outbox-interchanges`, `get-document-counts-by-status` | `get-interchange-by-id` |
| [Transactions](./transactions/search-transactions) | `search-transactions` | `search-transactions` |
| [Callbacks](./callbacks/get-callback-event-by-id) | `get-callback-event-by-id`, `get-callback-queue-by-id`, `list-callback-events`, `list-callback-queue` | — |
| [Carbon Copies](./carbon-copies/get-carbon-copy-by-id) | `get-carbon-copy-by-id`, `list-carbon-copies` | — |
| [Keys](./keys/get-key) | `get-key`, `list-keys` | — |

## Response Modes

**Structured JSON** — all 41 tools return a structured JSON data object. The AI interprets this and presents it to the user in plain language. Developers use it directly in their applications.

**Interactive UI components** — 10 tools additionally render a visual, browsable widget in Claude Desktop and Claude.ai alongside the AI's text response. The tool call, parameters, and JSON response are identical regardless of whether a UI component renders. Identified in the table above.

## Other Product Groups

The server also hosts **Translation** and **DataSync** product groups. These are separate licensed products with their own tool prefixes (`translation_` and `datasync_`).

## Future Tools

Additional Connectivity, Translation, and Catalog tools will be documented here when released.
