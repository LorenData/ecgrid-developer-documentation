---
title: list-inbox-interchanges
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-07: list-inbox-interchanges tool reference - Greg Kolinski
*/}

# list-inbox-interchanges

List INBOUND EDI interchanges received by a mailbox. An interchange is one X12 ISA…IEA or EDIFACT UNB…UNZ envelope — the unit of EDI routing on ECGrid. The default view is the historical **Archive** paginated within a date window. Set a view flag to switch views: `blocked` returns interchanges held from delivery; `pending` returns interchanges awaiting processing. An empty result (`count = 0`) means no matches — not an error. Results are scoped to the caller's APIKey.

> ℹ️ **Use when...**
>
> You want to audit received EDI traffic or investigate stuck or blocked inbound interchanges. For outbound use `list-outbox-interchanges`. For a single interchange's full detail use `get-interchange-by-id`.

## Tool Name

`connectivity_interchange_list-inbox-interchanges`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | ECGrid network ID scoping the query. Positive integer &gt;= 1. Example: 7. |
| `request.mailboxId` | integer | Yes | ECGrid mailbox ID scoping the query. Non-negative integer &gt;= 0. `0` = network root mailbox. Example: 142. |
| `request.ecgridIdFrom` | integer | Yes | Sender ECGrid ID filter. Pass `-1` to match any sender. Example: 6928311. |
| `request.ecgridIdTo` | integer | Yes | Recipient ECGrid ID filter. Pass `-1` to match any recipient. Example: 5040122. |
| `request.beginDate` | string | Yes | Inclusive start of the date window, ISO 8601 UTC. Example: `2026-04-01T00:00:00Z`. |
| `request.endDate` | string | Yes | Inclusive end of the date window, ISO 8601 UTC. Example: `2026-04-30T23:59:59Z`. |
| `request.interchangeControlId` | string | No | Optional ISA13 interchange control ID filter. Empty or omitted = all control IDs. Max 128 characters. |
| `request.timeZoneId` | string | No | IANA or Windows time zone ID for the date window (e.g. `America/New_York`). Mutually exclusive with `utcOffsetMinutes` — supplying both is VALIDATION_ERROR. |
| `request.utcOffsetMinutes` | integer | No | UTC offset in minutes for the date window (e.g. `-300` for EST). Range -840..840. Mutually exclusive with `timeZoneId`. |
| `request.pageNo` | integer | No | 1-based page number for the Archive view. Defaults to 1. Ignored for flag views. |
| `request.recordsPerPage` | integer | No | Records per page for the Archive view, 1..1000. Defaults to 500. Ignored for flag views. |
| `request.blocked` | boolean | No | Switch to the BLOCKED view — interchanges held from delivery. Default false. Mutually exclusive with `pending`. |
| `request.pending` | boolean | No | Switch to the PENDING view — interchanges awaiting processing. Default false. Mutually exclusive with `blocked`. |

> ⚠️ **Date time zone:** Supply `timeZoneId` OR `utcOffsetMinutes` to interpret `beginDate`/`endDate` in a local time zone. Omitting both means the dates are treated as UTC. Supplying both is a VALIDATION_ERROR.

## Response

Returns `interchanges` (same per-row shape as `get-interchange-by-id`) plus pagination fields. Pagination fields are `0` for the non-paged flag views (`blocked`, `pending`).

```json
{
  "interchanges": [
    {
      "interchangeId": 123456789,
      "interchangeControlId": "000012345",
      "standard": "X12",
      "documentType": "850",
      "bytes": 2048,
      "interchangeDateTime": "2026-04-15T14:30:00Z",
      "processDate": "2026-04-15T14:30:15Z",
      "status": {
        "code": 4000,
        "description": "Complete: CLOSED",
        "statusDate": "2026-04-15T14:30:20Z"
      },
      "from": {
        "networkId": 7,
        "networkName": "ECGrid Production",
        "mailboxId": 200
      },
      "to": {
        "networkId": 7,
        "networkName": "ECGrid Production",
        "mailboxId": 142
      },
      "header": "ISA*00*          *00*          *ZZ*BUYERCORP      *ZZ*ACMECORP       *260415*1430*^*00501*000012345*0*P*>~",
      "tpFrom": {
        "ecgridId": 5040122,
        "qualifier": "ZZ",
        "id": "BUYERCORP",
        "description": "Beta Retail"
      },
      "tpTo": {
        "ecgridId": 6928311,
        "qualifier": "ZZ",
        "id": "ACMECORP",
        "description": "Acme Shipping"
      },
      "parcelIds": [987654321],
      "parcelCount": 1
    }
  ],
  "pageNumber": 1,
  "pageSize": 500,
  "count": 1,
  "totalRecords": 1,
  "totalPages": 1
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `interchanges` | array | Interchange records matching the query. Same per-row shape as `get-interchange-by-id`. |
| `interchanges[].interchangeId` | integer | Unique numeric interchange ID (int64). Pass to `get-interchange-by-id` for full detail. |
| `interchanges[].interchangeControlId` | string | EDI interchange control number (X12 ISA13). Empty if not set. |
| `interchanges[].standard` | string | EDI standard: `X12`, `EDIFACT`, `TRADACOMS`, `VDA`, `XML`, `TXT`, `PDF`, or `Binary`. |
| `interchanges[].documentType` | string | EDI transaction set or document type (e.g. `850`, `810`). Empty if not set. |
| `interchanges[].bytes` | integer | Interchange payload size in bytes. |
| `interchanges[].interchangeDateTime` | string | ISO 8601 UTC — interchange date/time from the EDI envelope header. |
| `interchanges[].processDate` | string | ISO 8601 UTC — when ECGrid processed the interchange. |
| `interchanges[].status.code` | integer | Numeric interchange status code (e.g. `4000` = Complete: CLOSED). See `get-status-list`. |
| `interchanges[].status.description` | string | Human-readable status description. |
| `interchanges[].status.statusDate` | string | ISO 8601 UTC — most recent status change timestamp. |
| `interchanges[].from.networkId` | integer | Network ID of the sending party. |
| `interchanges[].from.networkName` | string | Network name of the sending party. |
| `interchanges[].from.mailboxId` | integer | Mailbox ID of the sending party. |
| `interchanges[].to.networkId` | integer | Network ID of the receiving party. |
| `interchanges[].to.networkName` | string | Network name of the receiving party. |
| `interchanges[].to.mailboxId` | integer | Mailbox ID of the receiving party. |
| `interchanges[].header` | string | Raw EDI envelope header segment (ISA for X12, UNB for EDIFACT). Empty if not set. |
| `interchanges[].tpFrom` | object \| null | Sender trading-partner EDI identity. Null if not resolved. |
| `interchanges[].tpFrom.ecgridId` | integer | ECGrid ID of the sending trading partner. |
| `interchanges[].tpFrom.qualifier` | string | EDI qualifier of the sending trading partner (e.g. `ZZ`). |
| `interchanges[].tpFrom.id` | string | EDI identifier of the sending trading partner. |
| `interchanges[].tpFrom.description` | string | Human-readable label for the sending trading partner. |
| `interchanges[].tpTo` | object \| null | Recipient trading-partner EDI identity. Null if not resolved. |
| `interchanges[].tpTo.ecgridId` | integer | ECGrid ID of the receiving trading partner. |
| `interchanges[].tpTo.qualifier` | string | EDI qualifier of the receiving trading partner. |
| `interchanges[].tpTo.id` | string | EDI identifier of the receiving trading partner. |
| `interchanges[].tpTo.description` | string | Human-readable label for the receiving trading partner. |
| `interchanges[].parcelIds` | array | IDs of the parcels carrying this interchange. Empty if none. |
| `interchanges[].parcelCount` | integer | Number of entries in `parcelIds`. |
| `pageNumber` | integer | Current page number (Archive view). `0` for flag views. |
| `pageSize` | integer | Records per page (Archive view). `0` for flag views. |
| `count` | integer | Number of interchanges in this result. |
| `totalRecords` | integer | Total matching interchanges across all pages (Archive view). `0` for flag views. |
| `totalPages` | integer | Total page count (Archive view). `0` for flag views. |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_interchange_list-inbox-interchanges",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142,
        "ecgridIdFrom": -1,
        "ecgridIdTo": -1,
        "beginDate": "2026-04-01T00:00:00Z",
        "endDate": "2026-04-30T23:59:59Z"
      }
    }
  }
}
```

## Example Prompts

- `List all inbound interchanges for mailbox 142 in April 2026`
- `Are there any blocked inbound interchanges for mailbox 142?`
- `Show me all 850 purchase orders received by mailbox 142 this month`

## See Also

- [Tools Overview](../../overview.md) — full list of available MCP tools
- [Authentication](../../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [list-outbox-interchanges](./list-outbox-interchanges.md) — list outbound interchanges sent from a mailbox
- [get-interchange-by-id](./get-interchange-by-id.md) — look up a single interchange's full detail
- [get-document-counts-by-status](./get-document-counts-by-status.md) — count interchanges by status over a date range
- [get-parcel-by-id](../parcels/get-parcel-by-id.md) — look up the parcel that carried an interchange
