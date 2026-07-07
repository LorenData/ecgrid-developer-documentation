---
title: get-document-counts-by-status
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-document-counts-by-status tool reference - Greg Kolinski
*/}

# get-document-counts-by-status

Count EDI documents (interchanges) processed over a date range, grouped by customer ECGrid ID and split by direction (FROM/TO), with a per-status histogram inside each direction. Use for status-distribution count questions: "how many of last month's documents failed?", "how many inbound interchanges are still pending vs. complete?", "which status codes did this mailbox produce in the last 14 days?". This tool only **counts** — it cannot list or identify individual interchanges by ID. To find or list individual interchanges (e.g. locate pending, blocked, or stuck interchanges with their IDs, partners, and dates) use `search-transactions`.

## Tool Name

`connectivity_interchange_get-document-counts-by-status`

## Auth Level Required

Any (scoped to caller's APIKey)

## Input Modes

This tool supports two mutually exclusive input modes. `ecgridId` takes precedence when supplied.

| Mode | Required Fields | Behavior |
|---|---|---|
| **Mode A** — ECGrid ID scoped | `request.ecgridId` | Resolves `(networkId, mailboxId)` automatically via the ECGrid ID lookup. Filters report rows to that single ECGrid ID. `customers[]` always has exactly one entry. Any `networkId` / `mailboxId` also sent are ignored. |
| **Mode B** — Mailbox scoped | `request.networkId` + `request.mailboxId` | Calls the report directly without an ECGrid ID lookup. No row filtering — `customers[]` surfaces every distinct ECGrid ID active on the mailbox in the window. |

:::note Network-only scope not supported
The backend report requires a mailbox. Use Mode B with a specific `(networkId, mailboxId)` pair, or call this tool once per mailbox to cover a full network.
:::

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.ecgridId` | integer \| null | Conditional (Mode A) | Internal numeric ECGrid ID. Takes precedence over `networkId` / `mailboxId` when supplied. Example: 6928311. The tool resolves `(networkId, mailboxId)` from this ID and filters report rows to this ECGrid ID only. NOT_FOUND when the ID does not exist or is not visible to the caller's APIKey. Values &lt;= 0 are rejected as VALIDATION_ERROR. |
| `request.networkId` | integer \| null | Conditional (Mode B) | Network (VAN) ID. Required together with `mailboxId` when `ecgridId` is not supplied. Example: 1101. Ignored when `ecgridId` is supplied. |
| `request.mailboxId` | integer \| null | Conditional (Mode B) | Mailbox ID. Required together with `networkId` when `ecgridId` is not supplied. Example: 2202401. Minimum value 0 (mailbox ID 0 is a valid sentinel). A mailbox with multiple ECGrid IDs yields multiple entries in `customers[]`. Ignored when `ecgridId` is supplied. |
| `request.startDate` | string | Yes | Inclusive start of the reporting window, ISO 8601 UTC. Example: `2026-07-01T00:00:00Z`. The window must not exceed 30 days — longer ranges are rejected as VALIDATION_ERROR. Narrow the range or issue multiple calls for longer periods. |
| `request.endDate` | string | Yes | Inclusive end of the reporting window, ISO 8601 UTC. Example: `2026-07-06T23:59:59Z`. Must be on or after `startDate` and within 30 days of it. |

## Response

Returns the resolved scope, the queried date range, a top-level total, and a `customers[]` array. An empty `customers[]` means no interchanges were processed in the window — this is a successful outcome, not an error.

```json
{
  "scope": {
    "networkId": 7,
    "networkName": "ECGrid Production",
    "mailboxId": 142,
    "mailboxName": "acme-prod@example.com"
  },
  "startDate": "2026-07-01T00:00:00Z",
  "endDate": "2026-07-06T23:59:59Z",
  "total": 1234,
  "customers": [
    {
      "ecgridId": 6928311,
      "customer": "ACMECORP",
      "qid": "ZZ*ACMECORP",
      "total": 1234,
      "byDirection": {
        "from": {
          "total": 820,
          "byStatus": {
            "4000": 800,
            "4101": 20
          }
        },
        "to": {
          "total": 414,
          "byStatus": {
            "4000": 410,
            "1101": 4
          }
        }
      }
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `scope.networkId` | integer | Network ID used for the report |
| `scope.networkName` | string | Network name — populated in Mode A; may be empty in Mode B |
| `scope.mailboxId` | integer | Mailbox ID used for the report |
| `scope.mailboxName` | string | Mailbox name — populated in Mode A; may be empty in Mode B |
| `startDate` | string | Echoed start of the queried window (ISO 8601) |
| `endDate` | string | Echoed end of the queried window (ISO 8601) |
| `total` | integer | Total interchange count across all customers in the window |
| `customers` | array | One entry per distinct ECGrid ID active in the window |
| `customers[].ecgridId` | integer | Internal numeric ECGrid ID for this customer row |
| `customers[].customer` | string | Wire-level EDI identifier (the `id` portion of the qualifier/id pair) |
| `customers[].qid` | string | Fully qualified identifier in `qualifier*id` format |
| `customers[].total` | integer | Total interchanges for this customer in the window |
| `customers[].byDirection.from.total` | integer | Total outbound interchanges (FROM this customer) |
| `customers[].byDirection.from.byStatus` | object | Map of numeric status code → count for outbound interchanges |
| `customers[].byDirection.to.total` | integer | Total inbound interchanges (TO this customer) |
| `customers[].byDirection.to.byStatus` | object | Map of numeric status code → count for inbound interchanges |

:::note Status code keys
Status codes in `byStatus` are raw numeric `InterchangeStatus` codes as string keys — for example `"4000"` (Complete: CLOSED), `"4101"` (CANCELED), `"1101"` (Interchange Control-No mismatch). Zero-count status codes are omitted from the map.
:::

## Example Call — Mode A (ECGrid ID)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_interchange_get-document-counts-by-status",
    "arguments": {
      "request": {
        "ecgridId": 6928311,
        "startDate": "2026-07-01T00:00:00Z",
        "endDate": "2026-07-06T23:59:59Z"
      }
    }
  }
}
```

## Example Call — Mode B (Mailbox)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_interchange_get-document-counts-by-status",
    "arguments": {
      "request": {
        "networkId": 1101,
        "mailboxId": 2202401,
        "startDate": "2026-07-01T00:00:00Z",
        "endDate": "2026-07-06T23:59:59Z"
      }
    }
  }
}
```

## Example Prompts

- `How many interchanges were delivered vs. failed for mailbox 142 this week?`
- `Show me the status breakdown for ECGrid ID 12345 this month`

## See Also

- [get-interchange-by-id](./get-interchange-by-id.md) — look up a single interchange by its numeric ID
- [search-transactions](../transactions/search-transactions) — list individual interchanges by date range, direction, and view (pending, blocked, no-route)
