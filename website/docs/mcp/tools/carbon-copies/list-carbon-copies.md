---
title: list-carbon-copies
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-carbon-copies tool reference - Greg Kolinski
*/}

# list-carbon-copies

List carbon copy rules. A carbon copy rule duplicates EDI interchanges flowing from one trading-partner pair (originalFrom &rarr; originalTo) to a second "CC" destination pair (ccFrom &rarr; ccTo). Supply both `networkId` and `mailboxId` to scope the listing to one mailbox; omit both to list every rule visible to the caller's APIKey. Optional filters narrow results by original sender, original receiver, or active status. An empty result (count = 0) is a successful outcome — not NOT_FOUND. Results are scoped to the caller's APIKey. Not cached.

> ⚠️ **Paired parameters:** `networkId` and `mailboxId` must be supplied **together** — passing only one is rejected as VALIDATION_ERROR. Either supply both to scope to a mailbox, or omit both to list across the entire APIKey.

## Tool Name

`connectivity_carbon-copy_list-carbon-copies`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Conditional | Network scope. Must be paired with `mailboxId` — both or neither. Positive integer &gt;= 1, max 2147483647. Example: 7. Omit both `networkId` and `mailboxId` to list across the entire APIKey. |
| `request.mailboxId` | integer | Conditional | Mailbox scope within `networkId`. Must be paired with `networkId` — both or neither. Use `0` for the network's root mailbox; `-1` for all mailboxes in the network. Min -1, max 2147483647. Example: 142. |
| `request.ecgridIdFrom` | integer | No | Filter: only return rules whose original sender (originalFrom) is this ECGrid ID. Omit to match any sender. Positive integer &gt;= 1. |
| `request.ecgridIdTo` | integer | No | Filter: only return rules whose original receiver (originalTo) is this ECGrid ID. Omit to match any receiver. Positive integer &gt;= 1. |
| `request.showInactive` | boolean | No | Include Suspended and Terminated rules in results. Default `false` — only Development, Active, and Preproduction rules are returned. |

## Response

Returns a `count` and a `carbonCopies` array; each element carries the rule's IDs, the four endpoint summaries, GS and transaction-set filters, status, and created/modified timestamps.

```json
{
  "count": 2,
  "carbonCopies": [
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
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Total number of rules returned |
| `carbonCopies` | array | Array of carbon copy rule records |
| `carbonCopies[].carbonCopyId` | integer | Unique numeric ID of the rule (int32) |
| `carbonCopies[].networkId` | integer | ECGrid network ID that owns the rule |
| `carbonCopies[].mailboxId` | integer | ECGrid mailbox ID that owns the rule |
| `carbonCopies[].originalFrom` | object | Summary of the original sender endpoint (ecgridId, qualifier, id, description) |
| `carbonCopies[].originalTo` | object | Summary of the original receiver endpoint (ecgridId, qualifier, id, description) |
| `carbonCopies[].ccFrom` | object | Summary of the CC copy sender endpoint (ecgridId, qualifier, id, description) |
| `carbonCopies[].ccTo` | object | Summary of the CC copy receiver endpoint (ecgridId, qualifier, id, description) |
| `carbonCopies[].gsFrom` | string | GS-envelope sender filter — empty string means match any |
| `carbonCopies[].gsTo` | string | GS-envelope receiver filter — empty string means match any |
| `carbonCopies[].transactionSet` | string | Transaction-set (document type) filter, e.g. `850`. Empty string means match any |
| `carbonCopies[].status` | string | Lifecycle status: `Development`, `Active`, `Preproduction`, `Suspended`, or `Terminated` |
| `carbonCopies[].created` | string | ISO 8601 timestamp when the rule was created |
| `carbonCopies[].modified` | string | ISO 8601 timestamp when the rule was last modified |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_carbon-copy_list-carbon-copies",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142
      }
    }
  }
}
```

## Example Prompts

- `List all carbon copy rules for mailbox 142 on network 7`
- `Show me all CC rules that copy traffic from ECGrid ID 1234567`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [get-carbon-copy-by-id](./get-carbon-copy-by-id.md) — fetch a single carbon copy rule by its numeric ID
- [get-ecgrid-id-by-id](../ecgrid-ids/get-ecgrid-id-by-id.md) — fetch the full ECGrid ID record for an endpoint (owner, config, X12 delimiters)
