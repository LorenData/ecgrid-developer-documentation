---
title: list-partners
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-partners tool reference - Greg Kolinski
*/}

# list-partners

List ECGrid interconnects (trading-partner relationships), scoped to what the caller's APIKey can see. Use for discovery: browsing partners on a network, finding all pending or suspended interconnects, listing every partner of one mailbox, or pulling every interconnect between two specific ECGrid IDs. To list the trading partners of a mailbox, call this tool with `mailboxId` set to that mailbox ID — it returns every interconnect for the mailbox in a single call. Omitting all filters returns every visible interconnect. This tool deliberately bypasses the response cache so results always reflect current state.

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::

## Tool Name

`connectivity_partner_list-partners`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

All parameters are optional, but at least a `mailboxId` or `networkId` is recommended to scope results. Calling with no parameters returns every interconnect visible to the APIKey.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.mailboxId` | integer \| null | No | Restrict results to one mailbox. A concrete value (>= 1) works without `networkId` — the tool resolves the owning network automatically. Sentinels: `-1` = any mailbox, `0` = the network's root mailbox. A `mailboxId` matching no mailbox surfaces as NOT_FOUND. |
| `request.networkId` | integer \| null | No | Restrict results to one ECGrid network. Sentinel: `-1` = any network. Only meaningful when combined with `status`; pass `networkId` explicitly to skip the mailbox-based network lookup. |
| `request.status` | string \| null | No | Filter by interconnect status. Defaults to `NoStatusChange` when omitted — a bare call lists every visible interconnect regardless of status. Allowed values: `Pending`, `Completed`, `Canceled`, `Delayed`, `Problem`, `AuthorizationRequired`, `NoStatusChange`. Unknown values are rejected as VALIDATION_ERROR. |
| `request.ecgridId1` | integer \| null | No | Optional ECGrid ID #1 in an interconnect pair filter. Omit unless filtering by a specific pair — do not send `-1`. Supply a concrete (>= 1) value to activate pair filtering; use `-1` on the other side to mean "any". When neither side is concrete, pair filtering is dropped and the search falls back to status/mailbox scoping. |
| `request.ecgridId2` | integer \| null | No | Optional ECGrid ID #2 in an interconnect pair filter. Same rules as `ecgridId1`. |
| `request.maxDays` | integer \| null | No | Traffic-recency window in days. `-1` = no limit (default when omitted). A positive N looks back N days and returns only interconnects with traffic within that window. Pass a positive N to restrict by recency. Only meaningful when combined with `status`. |

## Response

Returns a count and array of interconnect records. Each record has the same shape as `connectivity_partner_get-partner-by-id`. An empty `partners` array with `count = 0` is a successful outcome, not an error.

```json
{
  "count": 2,
  "partners": [
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
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Number of interconnect records returned |
| `partners` | array | Array of interconnect records (may be empty) |
| `partners[].interconnectId` | integer | The numeric interconnect ID (primary key) |
| `partners[].status` | string | Lifecycle status — Pending, Completed, Canceled, Delayed, Problem, or AuthorizationRequired |
| `partners[].created` | string | ISO 8601 timestamp — when the interconnect was created |
| `partners[].lastTraffic` | string \| null | ISO 8601 timestamp — most recent EDI traffic across this relationship |
| `partners[].tp1` | object | TP1 ECGrid ID summary — network, mailbox, qualifier/id, description, useType |
| `partners[].tp2` | object | TP2 ECGrid ID summary — same shape as `tp1` |
| `partners[].contactName` | string \| null | Human-readable name of the partner-side contact |
| `partners[].contactEmail` | string \| null | Email address of the partner-side contact |
| `partners[].as2Id1` | string \| null | AS2 identifier for the TP1 side |
| `partners[].as2Id2` | string \| null | AS2 identifier for the TP2 side |

See [get-partner-by-id](./get-partner-by-id.md) for the complete field list on each record.

## UI Component

When this tool is called from Claude Desktop or Claude.ai, the response includes a visual widget rendered from `ui://partner/list.html` displaying the interconnect list alongside the AI's text response.

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_partner_list-partners",
    "arguments": {
      "request": {
        "mailboxId": 142,
        "status": "Completed"
      }
    }
  }
}
```

## Example Prompts

- `List all trading partners for mailbox 142`
- `Show partners with Problem status on network 7`
- `List active partners from the last 30 days`

## See Also

- [get-partner-by-id](./get-partner-by-id.md) — look up a single interconnect by ID (cached, faster)
- [check-partner-config](./check-partner-config.md) — health-check a specific partner's configuration
- [get-partner-document-counts](./get-partner-document-counts.md) — view EDI document volume for a trading partner
