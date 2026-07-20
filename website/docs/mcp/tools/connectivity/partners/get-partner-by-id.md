---
title: get-partner-by-id
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-partner-by-id tool reference - Greg Kolinski
*/}

# get-partner-by-id

Look up a single ECGrid interconnect (trading-partner relationship) by its numeric interconnect ID. Use when the caller already has the integer ID — for example from a previous `connectivity_partner_list-partners` result, a ticket, or an admin reference. Returns the interconnect's full profile: lifecycle timestamps, status, contact info, partner-side references and AS2 IDs, both trading-partner ECGrid ID summaries (TP1/TP2), and compact user references. Returns NOT_FOUND when no interconnect matches the ID. Results are limited to what the caller's APIKey can see.

> ℹ️ **Interactive UI Component:** This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.

## Tool Name

`connectivity_partner_get-partner-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.partnerId` | integer | Yes | The numeric interconnect (trading-partner) ID. Positive integer >= 1. Example: 12345. Same value as `InterconnectIDInfo.interconnectId` returned by list calls. |

## Response

Returns the interconnect's full profile including lifecycle timestamps, status, contact info, TP1/TP2 ECGrid ID summaries, and compact user references.

```json
{
  "interconnectId": 12345,
  "uniqueId": "abc123def456",
  "created": "2024-01-15T10:30:00Z",
  "modified": "2024-06-01T08:00:00Z",
  "activated": "2024-01-20T09:00:00Z",
  "completed": "2024-01-20T09:15:00Z",
  "canceled": null,
  "delayed": null,
  "lastTraffic": "2026-07-05T14:22:00Z",
  "status": "Completed",
  "contactName": "Jane Smith",
  "contactEmail": "jane.smith@acme.example.com",
  "reference1": "PO-2024-001",
  "reference2": null,
  "as2Id1": "ACME-AS2",
  "as2Id2": "BETA-AS2",
  "tp1": {
    "ecgridId": 6928311,
    "qualifier": "ZZ",
    "id": "ACMECORP",
    "networkId": 7,
    "networkName": "Loren Data Corp",
    "mailboxId": 142,
    "mailboxName": "acme-prod@example.com",
    "description": "ACME Corporation Production",
    "useType": "Production"
  },
  "tp2": {
    "ecgridId": 7100042,
    "qualifier": "ZZ",
    "id": "BETACORP",
    "networkId": 7,
    "networkName": "Loren Data Corp",
    "mailboxId": 200,
    "mailboxName": "beta-prod@example.com",
    "description": "Beta Corporation Production",
    "useType": "Production"
  },
  "requestor": { "userId": 1001, "loginName": "jane.smith@acme.example.com" },
  "contact": { "userId": 1002, "loginName": "support@lorendata.com" },
  "netOps": { "userId": 1003, "loginName": "netops@lorendata.com" }
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `interconnectId` | integer | The numeric interconnect ID (primary key) |
| `uniqueId` | string | Opaque unique identifier for the relationship |
| `created` | string | ISO 8601 timestamp — when the interconnect was created |
| `modified` | string | ISO 8601 timestamp — when the interconnect was last modified |
| `activated` | string \| null | ISO 8601 timestamp — when the interconnect became active |
| `completed` | string \| null | ISO 8601 timestamp — when both sides accepted the interconnect |
| `canceled` | string \| null | ISO 8601 timestamp — when the interconnect was canceled (null if not) |
| `delayed` | string \| null | ISO 8601 timestamp — when the interconnect was delayed (null if not) |
| `lastTraffic` | string \| null | ISO 8601 timestamp — most recent EDI traffic across this relationship |
| `status` | string | Lifecycle status — Pending, Completed, Canceled, Delayed, Problem, or AuthorizationRequired |
| `contactName` | string \| null | Human-readable name of the partner-side contact |
| `contactEmail` | string \| null | Email address of the partner-side contact |
| `reference1` | string \| null | Free-form reference field #1 (e.g. PO number, contract ID) |
| `reference2` | string \| null | Free-form reference field #2 |
| `as2Id1` | string \| null | AS2 identifier for the TP1 side |
| `as2Id2` | string \| null | AS2 identifier for the TP2 side |
| `tp1` | object | TP1 ECGrid ID summary — network, mailbox, qualifier/id, description, useType |
| `tp2` | object | TP2 ECGrid ID summary — same shape as `tp1` |
| `requestor` | object | Compact user reference (userId + loginName) for the user who requested this interconnect |
| `contact` | object | Compact user reference for the assigned contact |
| `netOps` | object | Compact user reference for the NetOps owner |

## UI Component

When this tool is called from Claude Desktop or Claude.ai, the response includes a visual widget rendered from `ui://partner/detail.html` displaying the interconnect profile alongside the AI's text response.

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_partner_get-partner-by-id",
    "arguments": {
      "request": { "partnerId": 12345 }
    }
  }
}
```

## Example Prompts

- `Show me trading partner 12345`
- `What's the status of interconnect 99999?`
- `Who are the contacts for interconnect 12345?`

## See Also

- [list-partners](./list-partners.md) — discover interconnects by status, mailbox, network, or ECGrid ID pair
- [check-partner-config](./check-partner-config.md) — health-check a partner's configuration for setup completeness
- [get-partner-document-counts](./get-partner-document-counts.md) — view EDI document volume for a trading partner
