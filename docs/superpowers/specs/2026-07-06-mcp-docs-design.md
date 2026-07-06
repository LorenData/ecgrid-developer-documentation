# MCP Documentation Section — Design Spec

**Date:** 2026-07-06  
**Author:** Greg Kolinski  
**Status:** Approved — ready for implementation

---

## Summary

Add a new top-level MCP section to the ECGrid Developer Documentation Portal covering the ECGrid MCP Server (`mcp.ecgrid.io`). The section covers the ECGrid connectivity product only — Simplify and Catalog MCP tools are out of scope for this sprint and reserved for future sub-sections.

---

## Decisions Made

| Decision | Choice | Rationale |
|---|---|---|
| Nav position | 4 (between SOAP API and Common Operations) | MCP is a peer API paradigm, not a guide or sample |
| Tool documentation granularity | One page per tool | Consistent with REST API section; stable URLs per tool |
| Audience model | Single section, audience-aware pages | Developers and end users follow the same setup path; no split needed |
| Structural approach | Approach A — flat top-level pages + tools subsection | Mirrors REST/SOAP pattern; extensible for future products |
| Tool name source | Live `tools/list` from `mcp.ecgrid.io` | Authoritative; richer descriptions than release notes |

---

## Source Data

| Asset | Location | Notes |
|---|---|---|
| Live tool list | `E:\LD_Code\ECGrid Developer Documentation Portal\tools07062026.md` | Fetched 2026-07-06; 36 tools |
| MCP README | `C:\local docs\ECGrid-MCP\README.md` | Setup, auth, protocol, troubleshooting |
| MCP Agent Guide | `C:\local docs\ECGrid-MCP\ECGrid-MCP-Agent-Guide.md` | Developer patterns, chat loops, multi-LLM |
| MCP Release Notes | `C:\local docs\ECGrid-MCP\ECGrid-MCP-Release-Notes.md` | Release history, response shapes |

---

## Tool Inventory (Live — 2026-07-06)

**36 tools** confirmed in `tools/list`. All prefixed `connectivity_`.  
3 parcel list tools referenced in release notes but not yet deployed: `parcel_list-inbox-parcels`, `parcel_list-outbox-parcels`, `parcel_list-pending-inbox-parcels` — stub pages to be added when they ship.

### Tools with Interactive UI Components (10)

Identified via `_meta.ui.resourceUri` in live `tools/list`:

| Tool | UI Resource |
|---|---|
| `connectivity_mailbox_get-mailbox-by-id` | `ui://mailbox/detail.html` |
| `connectivity_mailbox_list-mailboxes` | `ui://mailbox/list.html` |
| `connectivity_ecgrid-id_find-edi-ids` | `ui://ecgrid-id/find.html` |
| `connectivity_ecgrid-id_get-ecgrid-id-by-id` | `ui://ecgrid-id/detail.html` |
| `connectivity_ecgrid-id_list-ecgrid-ids-by-mailbox` | `ui://ecgrid-id/by-mailbox.html` |
| `connectivity_partner_list-partners` | `ui://partner/list.html` |
| `connectivity_partner_get-partner-by-id` | `ui://partner/detail.html` |
| `connectivity_parcel_get-parcel-by-id` | `ui://parcel/detail.html` |
| `connectivity_interchange_get-interchange-by-id` | `ui://interchange/detail.html` |
| `connectivity_transaction_search-transactions` | `ui://transaction/search.html` |

### All Tools by Category

| Category | Tools (connectivity_ prefix implied) |
|---|---|
| System (3) | `system_hello-world`, `system_get-version`, `system_get-status-list` |
| Users (4) | `user_get-user-me`, `user_get-user-by-id`, `user_get-user-by-login`, `user_list-users` |
| Network (1) | `network_get-network-by-id` |
| Mailboxes (3) | `mailbox_get-mailbox-by-id`, `mailbox_list-mailboxes`, `mailbox_get-mailbox-by-name` |
| ECGrid IDs (3) | `ecgrid-id_get-ecgrid-id-by-id`, `ecgrid-id_find-edi-ids`, `ecgrid-id_list-ecgrid-ids-by-mailbox` |
| Partners (5) | `partner_get-partner-by-id`, `partner_list-partners`, `partner_check-partner-config`, `partner_test-partner-delivery`, `partner_get-partner-document-counts` |
| Comms (5) | `comm_get-comm-by-id`, `comm_list-comms`, `comm_find-comms`, `comm_test-comm`, `comm_check-ftp-access` |
| Parcels (1+3 stubs) | `parcel_get-parcel-by-id` + stubs for inbox/outbox/pending list |
| Interchanges (2) | `interchange_get-interchange-by-id`, `interchange_get-document-counts-by-status` |
| Transactions (1) | `transaction_search-transactions` |
| Callbacks (4) | `callback_get-callback-event-by-id`, `callback_get-callback-queue-by-id`, `callback_list-callback-events`, `callback_list-callback-queue` |
| Carbon Copies (2) | `carbon-copy_get-carbon-copy-by-id`, `carbon-copy_list-carbon-copies` |
| Keys (2) | `key_get-key`, `key_list-keys` |

---

## Navigation Changes

### Existing positions that shift

| Section | Old position | New position |
|---|---|---|
| SOAP API | 4 | 5 |
| Common Operations | 5 | 6 |
| Appendix | 6 | 7 |
| Code Samples | 7 | 8 |
| Changelog | 8 | 9 |

### Top navbar additions

Add `mcpSidebar` entry between `soapApiSidebar` and `commonOpsSidebar` in `docusaurus.config.ts`.

### Home page (`website/src/pages/index.tsx`)

1. **Hero buttons** — add `ECGrid MCP` button linking to `/docs/mcp/overview`
2. **Hero badge strip** — add `ECGrid MCP — New` pill (new `mcpPill` CSS class)
3. **"Choose Your API" cards** — add 5th MCP card (`badgeVariant: 'mcp'`):
   - Badge: `New`
   - Title: `ECGrid MCP`
   - Description: Connect any MCP-compatible AI to your ECGrid account. Natural language access to your network, mailboxes, trading partners, and transactions — no custom integration code.
   - Bullets: 36 tools across 13 categories · Claude Desktop, Cursor, Windsurf, and any HTTP agent · X-APIKey authentication · `mcp.ecgrid.io`
   - Link: `MCP Reference →` → `/docs/mcp/overview`
4. **Quick Links** — add `Quick Start — MCP` → `/docs/mcp/quick-start`

### Footer additions

- Documentation column: add `MCP` → `/docs/mcp/overview`
- Live References column: add `ECGrid MCP Server` → `https://mcp.ecgrid.io`

---

## Full File Tree

```
website/docs/mcp/
├── _category_.json                     position: 4, label: "MCP"
├── overview.md
├── quick-start.md
├── connecting/
│   ├── _category_.json                 label: "Connect Your AI Tool"
│   ├── claude-desktop.md
│   ├── cursor-windsurf.md
│   └── developer-http.md
├── authentication.md
├── protocol-reference.md
├── building-agents.md
├── tools/
│   ├── _category_.json                 label: "Tools Reference"
│   ├── overview.md
│   ├── system/
│   │   ├── _category_.json
│   │   ├── hello-world.md
│   │   ├── get-version.md
│   │   └── get-status-list.md
│   ├── users/
│   │   ├── _category_.json
│   │   ├── get-user-me.md
│   │   ├── get-user-by-id.md
│   │   ├── get-user-by-login.md
│   │   └── list-users.md
│   ├── network/
│   │   ├── _category_.json
│   │   └── get-network-by-id.md
│   ├── mailboxes/
│   │   ├── _category_.json
│   │   ├── get-mailbox-by-id.md
│   │   ├── list-mailboxes.md
│   │   └── get-mailbox-by-name.md
│   ├── ecgrid-ids/
│   │   ├── _category_.json
│   │   ├── get-ecgrid-id-by-id.md
│   │   ├── find-edi-ids.md
│   │   └── list-ecgrid-ids-by-mailbox.md
│   ├── partners/
│   │   ├── _category_.json
│   │   ├── get-partner-by-id.md
│   │   ├── list-partners.md
│   │   ├── check-partner-config.md
│   │   ├── test-partner-delivery.md
│   │   └── get-partner-document-counts.md
│   ├── comms/
│   │   ├── _category_.json
│   │   ├── get-comm-by-id.md
│   │   ├── list-comms.md
│   │   ├── find-comms.md
│   │   ├── test-comm.md
│   │   └── check-ftp-access.md
│   ├── parcels/
│   │   ├── _category_.json
│   │   ├── get-parcel-by-id.md
│   │   ├── list-inbox-parcels.md          ← stub (not yet deployed)
│   │   ├── list-outbox-parcels.md         ← stub (not yet deployed)
│   │   └── list-pending-inbox-parcels.md  ← stub (not yet deployed)
│   ├── interchanges/
│   │   ├── _category_.json
│   │   ├── get-interchange-by-id.md
│   │   └── get-document-counts-by-status.md
│   ├── transactions/
│   │   ├── _category_.json
│   │   └── search-transactions.md
│   ├── callbacks/
│   │   ├── _category_.json
│   │   ├── get-callback-event-by-id.md
│   │   ├── get-callback-queue-by-id.md
│   │   ├── list-callback-events.md
│   │   └── list-callback-queue.md
│   ├── carbon-copies/
│   │   ├── _category_.json
│   │   ├── get-carbon-copy-by-id.md
│   │   └── list-carbon-copies.md
│   └── keys/
│       ├── _category_.json
│       ├── get-key.md
│       └── list-keys.md
├── resources-and-prompts.md
├── other-ai-platforms.md
└── troubleshooting.md

website/docs/changelog/
└── mcp-release-notes.md
```

**Total new files: ~68**

---

## Page Templates

### Tool Page

```markdown
---
title: <display name>
---

# <display name>

<Description from live tools/list — verbatim or lightly trimmed for doc audience.>

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::   ← omit if no _meta.ui.resourceUri

## Tool Name

`connectivity_<category>_<slug>`

## Auth Level Required

Any (scoped to caller's APIKey)  ← or specific level if required

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.field` | type | Yes/No | From inputSchema description |

## Response

<One sentence.>

```json
{ example response shape from release notes }
```

## Response Fields

| Field | Type | Description |
|---|---|---|

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_<category>_<slug>",
    "arguments": { "request": { ... } }
  }
}
```

## Example Prompts   ← natural-language tools only

## See Also
```

### Other page types
- **overview.md** — what MCP is, ECGrid MCP server URL, two audiences, link to quick start. Under 400 words.
- **quick-start.md** — 4-step flow (key → Node.js → config → test). Self-contained for non-technical readers.
- **authentication.md** — API key vs Bearer JWT, auth levels table, key security.
- **protocol-reference.md** — HTTP endpoints, SSE format, two-step parse, JSON-RPC, initialize, rate limits, errors, health probes.
- **building-agents.md** — request lifecycle, system prompt, C#/JS/Python chat loops (Anthropic + OpenAI), schema translation table.
- **resources-and-prompts.md** — 3 resources + 2 prompts; explains these don't appear in tools/list.
- **other-ai-platforms.md** — non-MCP platforms → REST API path. Short.
- **troubleshooting.md** — full troubleshooting table from README.
- **tools/overview.md** — category table, UI component list, tools/list guidance, future product note.
- **changelog/mcp-release-notes.md** — reformatted release notes matching existing changelog style.

---

## Future: Simplify and Catalog MCP Tools

When Simplify and Catalog ship MCP tools, they get their own sub-sections inside `tools/`:

```
tools/
  simplify/     ← future sprint
  catalog/      ← future sprint
```

The `tools/overview.md` already notes this with a placeholder. No other structural changes needed.

---

## CSS / Styling

- Add `mcpPill` style to `custom.css` matching the pattern of `restPill`, `soapPill`, etc.
- Add `cardMcp` and `badgeMcp` variants to `index.module.css` for the home page API card.
- Brand color: use ECGrid orange `#F26522` (accent) to differentiate MCP from the blue REST card and gray SOAP card.

---

## sidebars.ts Addition

```typescript
mcpSidebar: [{ type: 'autogenerated', dirName: 'mcp' }],
```

Insert after `soapApiSidebar` in the `sidebars` export.
