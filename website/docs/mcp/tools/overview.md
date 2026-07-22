---
title: Tools Overview
sidebar_position: 1
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP tools overview - Greg Kolinski
2026-07-20: Group tools by product (Connectivity / DataSync / Translation) - Greg Kolinski
2026-07-20: Move connectivity tools into connectivity/ subfolder; add datasync tools - Greg Kolinski
*/}

# Tools Reference

The ECGrid MCP Server hosts tools across three product groups: **Connectivity**, **DataSync (GPA)**, and **Translation**. Each product group requires its own credential header — a single connection can carry multiple headers.

Call `tools/list` at startup to get the current complete tool list with full input schemas — the response is always authoritative. For programmatic discovery, `GET https://mcp.ecgrid.io/tools.json` returns the same registry without authentication.

---

## Connectivity Tools

**Credential:** `X-Connectivity-API-Key` — your ECGrid API key

37 tools across 13 categories. All Connectivity tools are prefixed `connectivity_` and return structured JSON data.

| Category | Tools | Interactive UI |
|---|---|---|
| [System](./connectivity/system/get-version) | `get-version`, `get-status-list` | — |
| [Users](./connectivity/users/get-user-by-id) | `get-user-by-id`, `get-user-by-login`, `list-users` | — |
| [Network](./connectivity/network/get-network-by-id) | `get-network-by-id` | — |
| [Mailboxes](./connectivity/mailboxes/get-mailbox-by-id) | `get-mailbox-by-id`, `list-mailboxes`, `get-mailbox-by-name` | `get-mailbox-by-id`, `list-mailboxes` |
| [ECGrid IDs](./connectivity/ecgrid-ids/get-ecgrid-id-by-id) | `get-ecgrid-id-by-id`, `find-edi-ids`, `list-ecgrid-ids-by-mailbox` | All three |
| [Partners](./connectivity/partners/get-partner-by-id) | `get-partner-by-id`, `list-partners`, `check-partner-config`, `test-partner-delivery`, `get-partner-document-counts` | `get-partner-by-id`, `list-partners` |
| [Comms](./connectivity/comms/get-comm-by-id) | `get-comm-by-id`, `list-comms`, `find-comms`, `test-comm`, `check-ftp-access` | — |
| [Parcels](./connectivity/parcels/get-parcel-by-id) | `get-parcel-by-id`, `list-inbox-parcels`, `list-outbox-parcels`, `list-pending-inbox-parcels` | `get-parcel-by-id` |
| [Interchanges](./connectivity/interchanges/get-interchange-by-id) | `get-interchange-by-id`, `list-inbox-interchanges`, `list-outbox-interchanges`, `get-document-counts-by-status` | `get-interchange-by-id` |
| [Transactions](./connectivity/transactions/search-transactions) | `search-transactions` | `search-transactions` |
| [Callbacks](./connectivity/callbacks/get-callback-event-by-id) | `get-callback-event-by-id`, `get-callback-queue-by-id`, `list-callback-events`, `list-callback-queue` | — |
| [Carbon Copies](./connectivity/carbon-copies/get-carbon-copy-by-id) | `get-carbon-copy-by-id`, `list-carbon-copies` | — |
| [Keys](./connectivity/keys/get-key) | `get-key`, `list-keys` | — |

### Response Modes

**Structured JSON** — all Connectivity tools return a structured JSON data object. The AI interprets this and presents it to the user in plain language. Developers use it directly in their applications.

**Interactive UI components** — 10 tools additionally render a visual, browsable widget in Claude Desktop and Claude.ai alongside the AI's text response. The tool call, parameters, and JSON response are identical regardless of whether a UI component renders. Identified in the table above.

---

## DataSync Tools

**Credential:** `X-DataSync-API-Key` — your GPA Personal Access Token (PAT)

5 tools across 3 categories. All DataSync tools are prefixed `datasync_`.

| Category | Tools |
|---|---|
| [Company](./datasync/company/list-companies) | `list-companies` |
| [Catalog](./datasync/catalog/list-catalogs) | `list-catalogs`, `list-catalog-products` |
| [Product](./datasync/product/list-products) | `list-products`, `get-product-details` |

---

## Translation Tools

**Credential:** `X-Translation-API-Key` — your Translation API key

Translation tools are prefixed `translation_`. Tool documentation will be published here as tools are released.
