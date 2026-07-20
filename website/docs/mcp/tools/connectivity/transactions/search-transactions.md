---
title: search-transactions
sidebar_position: 1
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: search-transactions tool reference - Greg Kolinski
*/}

# search-transactions

Search EDI transactions the way the Customer Portal Transactions page does — one call covers direction, type (interchange envelopes or file parcels), a date window, ECGrid ID or qualifier+EDI-ID filters, and live box views for blocked, pending, no-route, pending-download, and delivery-error traffic.

> ℹ️ **Interactive UI Component:** This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.

## Tool Name

`connectivity_transaction_search-transactions`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.type` | string | Yes | Transaction kind: `Interchange` (X12/EDIFACT envelopes) or `File` (parcels). One kind per query. |
| `request.direction` | string | Yes | Flow direction from the mailbox's perspective: `Inbound`, `Outbound`, or `Both` (merges the two legs). |
| `request.networkId` | integer \| null | No | ECGrid network ID scoping the query (&gt;= 1). Defaults to the caller's own network resolved from the API-key session. Example: 7. |
| `request.mailboxId` | integer \| null | No | ECGrid mailbox ID scoping the query. Defaults to `-1` = ALL mailboxes in the network. `0` = the network root mailbox. Example: 142. |
| `request.beginDate` | string \| null | No | Inclusive start of the search window, ISO 8601. Defaults to one day before `endDate`. Interpreted using `timeZoneId` or `utcOffsetMinutes` if supplied, else UTC. Example: `2026-07-01T00:00:00Z`. |
| `request.endDate` | string \| null | No | Inclusive end of the search window, ISO 8601. Defaults to the current UTC time (omitting both fields searches the most recent 24 hours). Example: `2026-07-02T23:59:59Z`. |
| `request.myEcgridId` | integer \| null | No | Caller-side ECGrid ID filter (numeric primary key). Omit or pass `-1` for any. Example: 5040122. |
| `request.partnerEcgridId` | integer \| null | No | Partner-side ECGrid ID filter (numeric primary key). Omit or pass `-1` for any. Example: 6928311. |
| `request.myQualifier` | string \| null | No | Caller-side EDI qualifier (ISA05/ISA07, e.g. `ZZ`). Supply with `myEdiId` as an alternative to `myEcgridId`. Max 4 chars. |
| `request.myEdiId` | string \| null | No | Caller-side wire EDI identifier (ISA06/ISA08). Supply with `myQualifier`; mutually exclusive with `myEcgridId`. Max 35 chars. |
| `request.partnerQualifier` | string \| null | No | Partner-side EDI qualifier. Supply with `partnerEdiId` as an alternative to `partnerEcgridId`. Max 4 chars. |
| `request.partnerEdiId` | string \| null | No | Partner-side wire EDI identifier. Supply with `partnerQualifier`; mutually exclusive with `partnerEcgridId`. Max 35 chars. |
| `request.view` | string | No | Which transactions view to search. `Archive` (default) = historical portal-parity search. Interchange views: `Blocked` (held), `Pending` (in-flight/delayed), `NoRoute` (outbound without a route). Parcel views: `PendingDownload` (`File` + `Inbound`), `DeliveryError` (`File` + `Outbound`). Invalid view/type/direction combinations return VALIDATION_ERROR. |
| `request.statusGroup` | string | No | Client-side status filter applied within the returned page: `All` (default), `ActiveErrors`, or `Complete`. Leg totals stay UNFILTERED. |
| `request.interchangeControlId` | string \| null | No | Interchange control ID (ISA13) filter. Only valid with `type` = `Interchange`. Max 128 chars. |
| `request.mailbagControlId` | string \| null | No | Mailbag control ID filter. Only valid with `type` = `File`. Max 128 chars. |
| `request.timeZoneId` | string \| null | No | IANA/Windows time zone ID for the dates (e.g. `Asia/Bangkok`). Mutually exclusive with `utcOffsetMinutes`. Max 64 chars. |
| `request.utcOffsetMinutes` | integer \| null | No | UTC offset in minutes (e.g. `420` for UTC+7). Range -840..840. Mutually exclusive with `timeZoneId`. |
| `request.pageNo` | integer \| null | No | 1-based page number applied to each directional leg. Defaults to 1. |
| `request.recordsPerPage` | integer \| null | No | Records per page per leg, 1..1000. Defaults to 100. Direction `Both` can return up to twice this. |

> 📝 **View-specific pagination behaviour**
>
> The `Blocked`, `Pending`, and `NoRoute` interchange views scan the entire date window — `pageNo` and `recordsPerPage` are ignored. An over-large window returns `partial: true`; narrow the date range and retry. The `PendingDownload` and `DeliveryError` parcel views query live state; dates and paging are also ignored for those views.

## Response

Returns the applied `filters` (re-send with an adjusted `pageNo` to paginate), a `rows` array of matching transactions, per-leg totals, and a `totalRecords` count. An empty `rows` array means no matches — this is a successful outcome, not an error.

```json
{
  "data": {
    "filters": {
      "type": "Interchange",
      "direction": "Inbound",
      "networkId": 7,
      "mailboxId": -1,
      "beginDate": "2026-07-05T00:00:00Z",
      "endDate": "2026-07-06T00:00:00Z",
      "view": "Archive",
      "statusGroup": "All",
      "pageNo": 1,
      "recordsPerPage": 100
    },
    "rows": [
      {
        "transactionId": 123456789,
        "type": "interchange",
        "direction": "inbound",
        "transactionDateTime": "2026-07-05T14:22:10Z",
        "processDate": "2026-07-05T14:22:11Z",
        "statusDate": "2026-07-05T14:22:12Z",
        "statusCode": "4000",
        "statusLabel": "Complete: CLOSED",
        "controlNumber": "000000042",
        "standard": "X12",
        "documentType": "X12",
        "fileName": "",
        "bytes": 2048,
        "parcelIds": [987654321],
        "parcelCount": 1,
        "from": {
          "networkId": 8,
          "networkName": "Partner VAN",
          "mailboxId": 500,
          "mailboxName": "",
          "ecgridId": 6928311,
          "qualifier": "ZZ",
          "ediId": "PARTNERACME",
          "description": "Acme Hardware"
        },
        "to": {
          "networkId": 7,
          "networkName": "ECGrid Production",
          "mailboxId": 142,
          "mailboxName": "acme-prod@example.com",
          "ecgridId": 5040122,
          "qualifier": "ZZ",
          "ediId": "MYCOMPANY",
          "description": "My Company"
        }
      }
    ],
    "count": 1,
    "totalInbound": 1,
    "totalOutbound": 0,
    "totalRecords": 1
  },
  "partial": false,
  "warnings": null
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `data.filters` | object | The sanitised filters actually applied. Re-send with an adjusted `pageNo` to fetch the next page of the same search. |
| `data.rows` | array | Matching transaction rows. Direction `Both` merges both legs sorted by `transactionDateTime` descending. Empty array means no matches — not an error. |
| `data.rows[].transactionId` | integer | ECGrid primary key: interchange ID when `type` is `interchange`, parcel ID when `type` is `file`. Chain `get-interchange-by-id` or `get-parcel-by-id` for full detail. |
| `data.rows[].type` | string | Row kind: `interchange` or `file`. Matches the request `type`. |
| `data.rows[].direction` | string | Flow direction of this row: `inbound` or `outbound`. |
| `data.rows[].transactionDateTime` | string | UTC date/time of the transaction (interchange envelope date or parcel entry date). |
| `data.rows[].processDate` | string \| null | UTC timestamp when ECGrid processed the interchange. Null on `file` rows. |
| `data.rows[].statusDate` | string | UTC timestamp of the row's current status. |
| `data.rows[].statusCode` | string | Raw status code: numeric interchange status (e.g. `4000`) or `M`-prefixed parcel status (e.g. `M2400`). Empty if not set. |
| `data.rows[].statusLabel` | string | Human-readable status message. Empty if not set. |
| `data.rows[].controlNumber` | string | Interchange control ID (ISA13) on `interchange` rows, or mailbag control ID on `file` rows. Empty if not set. |
| `data.rows[].standard` | string | EDI standard (`X12`, `EDIFACT`, …). Empty on `file` rows. |
| `data.rows[].documentType` | string | Document type of the interchange (e.g. `X12`). Empty on `file` rows. |
| `data.rows[].fileName` | string | Original file name of the parcel payload. Empty on `interchange` rows. |
| `data.rows[].bytes` | integer | Payload size in bytes. |
| `data.rows[].parcelIds` | array | IDs of parcels carrying this interchange. Empty array on `file` rows. |
| `data.rows[].parcelCount` | integer | Number of entries in `parcelIds`. |
| `data.rows[].from` | object | Sender-side routing and EDI identity. |
| `data.rows[].from.networkId` | integer | ECGrid network ID of the sender. |
| `data.rows[].from.networkName` | string | Human-readable network name. Empty if not set. |
| `data.rows[].from.mailboxId` | integer | ECGrid mailbox ID of the sender. |
| `data.rows[].from.mailboxName` | string | Mailbox name. Populated on `file` rows only; empty on `interchange` rows. |
| `data.rows[].from.ecgridId` | integer | ECGrid ID of the sender's trading partner. `0` if not resolved. |
| `data.rows[].from.qualifier` | string | EDI partner-ID qualifier (ISA05/ISA07). Empty if not resolved. |
| `data.rows[].from.ediId` | string | Wire-level EDI identifier (ISA06/ISA08). Empty if not resolved. |
| `data.rows[].from.description` | string | Free-form label for this trading partner. Empty if not resolved. |
| `data.rows[].to` | object | Recipient-side routing and EDI identity — same shape as `from`. |
| `data.count` | integer | Number of rows in the `rows` array on this page. |
| `data.totalInbound` | integer | Total matching inbound records across all pages. `0` when the inbound leg was not queried. |
| `data.totalOutbound` | integer | Total matching outbound records across all pages. `0` when the outbound leg was not queried. |
| `data.totalRecords` | integer | Total matching records across all queried legs (sum of leg totals). |
| `partial` | boolean | `true` when the result is truncated (e.g. an over-large scan window). Narrow the date range and retry. |
| `warnings` | array \| null | Plain-language warnings about the search result. Null when none. |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_transaction_search-transactions",
    "arguments": {
      "request": {
        "type": "Interchange",
        "direction": "Inbound",
        "mailboxId": 142,
        "beginDate": "2026-07-05T00:00:00Z",
        "endDate": "2026-07-06T00:00:00Z"
      }
    }
  }
}
```

## Example Prompts

- `Show me all inbound interchanges from the last 24 hours`
- `Are there any transactions currently blocked?`
- `Show pending inbound files for mailbox 142`
- `Find all delivery errors from yesterday`

## See Also

- [Tools Overview](../../overview.md) — full list of available MCP tools
- [Authentication](../../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [get-interchange-by-id](../interchanges/get-interchange-by-id.md) — look up a single interchange by its numeric ID
- [get-parcel-by-id](../parcels/get-parcel-by-id.md) — look up a single parcel by its numeric ID
- [get-document-counts-by-status](../interchanges/get-document-counts-by-status.md) — aggregate status-histogram counts without row listing
