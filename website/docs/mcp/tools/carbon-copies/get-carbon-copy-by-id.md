{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-carbon-copy-by-id tool reference - Greg Kolinski
*/}
---
title: get-carbon-copy-by-id
sidebar_position: 1
---

# get-carbon-copy-by-id

Look up a single carbon copy rule by its numeric ID. A carbon copy rule duplicates EDI interchanges flowing from one trading-partner pair (originalFrom &rarr; originalTo) to a second "CC" destination pair (ccFrom &rarr; ccTo), optionally narrowed by GS-envelope filters and a transaction-set filter. Use when the caller already has the integer rule ID — for example from a previous `list-carbon-copies` result, a ticket, or an admin reference. Returns NOT_FOUND when no rule matches the ID. Results are scoped to the caller's APIKey. Cached for 180 seconds per caller.

## Tool Name

`connectivity_carbon-copy_get-carbon-copy-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.carbonCopyId` | integer | Yes | The numeric ID of the carbon copy rule — the internal int32 primary key. Positive integer &gt;= 1, max 2147483647. Example: 7701. Obtain from a `list-carbon-copies` result's `carbonCopyId` field. Values &lt;= 0 are rejected as VALIDATION_ERROR. |

## Response

Returns the carbon copy rule's IDs, the four endpoint summaries (originalFrom, originalTo, ccFrom, ccTo), GS and transaction-set filters, lifecycle status, and created/modified timestamps.

```json
{
  "carbonCopyId": 7701,
  "networkId": 7,
  "mailboxId": 142,
  "originalFrom": {
    "ecgridId": 1234567,
    "qualifier": "01",
    "id": "SENDER001",
    "description": "Acme Shipping"
  },
  "originalTo": {
    "ecgridId": 2345678,
    "qualifier": "01",
    "id": "RECEIVER001",
    "description": "Beta Retail"
  },
  "ccFrom": {
    "ecgridId": 1234567,
    "qualifier": "01",
    "id": "SENDER001",
    "description": "Acme Shipping"
  },
  "ccTo": {
    "ecgridId": 9876543,
    "qualifier": "01",
    "id": "AUDIT001",
    "description": "Audit Copy Mailbox"
  },
  "gsFrom": "",
  "gsTo": "",
  "transactionSet": "850",
  "status": "Active",
  "created": "2025-03-15T10:00:00Z",
  "modified": "2025-03-15T10:00:00Z"
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `carbonCopyId` | integer | Unique numeric ID of this carbon copy rule (int32) |
| `networkId` | integer | ECGrid network ID that owns the rule |
| `mailboxId` | integer | ECGrid mailbox ID that owns the rule |
| `originalFrom` | object | Summary of the original sender endpoint |
| `originalFrom.ecgridId` | integer | ECGrid ID of the original sender |
| `originalFrom.qualifier` | string | EDI qualifier for the original sender |
| `originalFrom.id` | string | EDI ID string for the original sender |
| `originalFrom.description` | string | Human-readable name for the original sender |
| `originalTo` | object | Summary of the original receiver endpoint |
| `originalTo.ecgridId` | integer | ECGrid ID of the original receiver |
| `originalTo.qualifier` | string | EDI qualifier for the original receiver |
| `originalTo.id` | string | EDI ID string for the original receiver |
| `originalTo.description` | string | Human-readable name for the original receiver |
| `ccFrom` | object | Summary of the CC copy sender endpoint |
| `ccFrom.ecgridId` | integer | ECGrid ID of the CC sender |
| `ccFrom.qualifier` | string | EDI qualifier for the CC sender |
| `ccFrom.id` | string | EDI ID string for the CC sender |
| `ccFrom.description` | string | Human-readable name for the CC sender |
| `ccTo` | object | Summary of the CC copy receiver endpoint |
| `ccTo.ecgridId` | integer | ECGrid ID of the CC receiver |
| `ccTo.qualifier` | string | EDI qualifier for the CC receiver |
| `ccTo.id` | string | EDI ID string for the CC receiver |
| `ccTo.description` | string | Human-readable name for the CC receiver |
| `gsFrom` | string | GS-envelope sender filter — empty string means match any |
| `gsTo` | string | GS-envelope receiver filter — empty string means match any |
| `transactionSet` | string | Transaction-set (document type) filter, e.g. `850`. Empty string means match any |
| `status` | string | Lifecycle status: `Development`, `Active`, `Preproduction`, `Suspended`, or `Terminated` |
| `created` | string | ISO 8601 timestamp when the rule was created |
| `modified` | string | ISO 8601 timestamp when the rule was last modified |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_carbon-copy_get-carbon-copy-by-id",
    "arguments": {
      "request": { "carbonCopyId": 7701 }
    }
  }
}
```

## Example Prompts

- `Show me the details for carbon copy rule 7701`
- `What is the CC destination for carbon copy rule 7701?`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [list-carbon-copies](./list-carbon-copies.md) — enumerate all carbon copy rules under a mailbox or APIKey
- [get-ecgrid-id-by-id](../ecgrid-ids/get-ecgrid-id-by-id.md) — fetch the full ECGrid ID record for an endpoint (owner, config, X12 delimiters)
