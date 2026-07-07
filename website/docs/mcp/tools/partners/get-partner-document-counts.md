---
title: get-partner-document-counts
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-partner-document-counts tool reference - Greg Kolinski
*/}

# get-partner-document-counts

Report how many EDI documents (interchanges) one specific ECGrid ID exchanged with each of its trading partners over a date range, with byte volumes. Use for volume and traffic questions scoped to one ECGrid ID and window — for example "which trading partners drove the most volume for this customer?" or "how many bytes did this Customer/QID send and receive this month?". Results are ranked by total interchange count descending and capped at `topN`. Returns NOT_FOUND when the `ecgridId` does not exist or is not visible to the caller's APIKey.

## Tool Name

`connectivity_partner_get-partner-document-counts`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.ecgridId` | integer | Yes | The internal numeric ECGrid ID to report on. Positive integer >= 1. Example: 6928311. Drives scope resolution — the tool looks up this record to derive its network, mailbox, qualifier, and ID, then fetches the document count report. NOT_FOUND when the ID does not exist or is not visible to the caller's APIKey. |
| `request.startDate` | string | Yes | Inclusive start of the reporting window, ISO 8601 UTC. Example: `2026-07-01T00:00:00Z`. The window must not exceed 30 days; longer ranges are rejected as VALIDATION_ERROR. |
| `request.endDate` | string | Yes | Inclusive end of the reporting window, ISO 8601 UTC. Example: `2026-07-06T23:59:59Z`. Must be on or after `startDate` and within 30 days of it. |
| `request.topN` | integer \| null | No | Maximum number of trading-partner rows to return, ranked by interchange count descending. Optional, 1–500. Defaults to 50 when omitted. When this ECGrid ID has more partner rows than this limit, the response is truncated and flagged via `truncated`/`omittedRowCount`. Raise `topN` (max 500) or narrow the date range for full coverage. |

## Response

Returns scope metadata echoed from the ECGrid ID lookup, the queried date range, top-level rollup totals, truncation flags, and a `partners` array ranked by interchange volume descending. An empty `partners` array means no documents were exchanged in the window — this is a successful outcome, NOT an error.

```json
{
  "ecgridId": 6928311,
  "customer": "ACMECORP",
  "qid": "ZZ*ACMECORP",
  "networkId": 7,
  "networkName": "Loren Data Corp",
  "mailboxId": 142,
  "mailboxName": "acme-prod@example.com",
  "startDate": "2026-07-01T00:00:00Z",
  "endDate": "2026-07-06T23:59:59Z",
  "totalInterchanges": 1482,
  "totalBytes": 52428800,
  "appliedTopN": 50,
  "truncated": false,
  "omittedRowCount": 0,
  "partners": [
    {
      "tradingPartner": "BETACORP",
      "tradingPartnerQid": "ZZ*BETACORP",
      "totalInterchanges": 850,
      "totalBytes": 30000000
    },
    {
      "tradingPartner": "GAMMACORP",
      "tradingPartnerQid": "01*9876543210",
      "totalInterchanges": 632,
      "totalBytes": 22428800
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `ecgridId` | integer | The ECGrid ID the report is scoped to |
| `customer` | string | Wire-level EDI identifier (the `id` portion of the qualifier/id pair) |
| `qid` | string | Fully qualified identifier in `qualifier*id` format |
| `networkId` | integer | ECGrid network owning this ECGrid ID |
| `networkName` | string | Human-readable name of the owning network |
| `mailboxId` | integer | Mailbox owning this ECGrid ID |
| `mailboxName` | string | Human-readable name of the owning mailbox |
| `startDate` | string | Echoed start of the queried window (ISO 8601) |
| `endDate` | string | Echoed end of the queried window (ISO 8601) |
| `totalInterchanges` | integer | Total interchange count across all trading partners in the window |
| `totalBytes` | integer | Total byte volume across all trading partners in the window |
| `appliedTopN` | integer | The `topN` limit actually applied (echoed from request or default 50) |
| `truncated` | boolean | `true` when the result was capped at `topN` — more rows exist beyond the limit |
| `omittedRowCount` | integer | Number of partner rows omitted due to `topN` truncation |
| `partners` | array | Trading-partner rows ranked by `totalInterchanges` descending |
| `partners[].tradingPartner` | string | Wire-level EDI identifier of the trading partner (the `id` portion) |
| `partners[].tradingPartnerQid` | string | Fully qualified identifier of the trading partner in `qualifier*id` format |
| `partners[].totalInterchanges` | integer | Number of interchanges exchanged with this partner in the window |
| `partners[].totalBytes` | integer | Total byte volume exchanged with this partner in the window |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_partner_get-partner-document-counts",
    "arguments": {
      "request": {
        "ecgridId": 6928311,
        "startDate": "2026-07-01T00:00:00Z",
        "endDate": "2026-07-06T23:59:59Z",
        "topN": 50
      }
    }
  }
}
```

## Example Prompts

- `Show document counts for ECGrid ID 12345 over the last week`
- `Which trading partners sent the most documents to mailbox 142 this month?`
- `How many interchanges did ECGrid ID 6928311 exchange with each partner in July?`

## See Also

- [get-partner-by-id](./get-partner-by-id.md) — view a specific interconnect's profile by ID
- [list-partners](./list-partners.md) — discover all interconnects for a mailbox or network
- [list-ecgrid-ids-by-mailbox](../ecgrid-ids/list-ecgrid-ids-by-mailbox.md) — enumerate ECGrid IDs under a mailbox before iterating document counts
