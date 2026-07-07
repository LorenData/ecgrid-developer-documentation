---
title: get-interchange-by-id
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-interchange-by-id tool reference - Greg Kolinski
*/}

# get-interchange-by-id

Look up a single EDI interchange by its numeric interchange ID and return its full detail. An interchange is one X12 ISA…IEA or EDIFACT UNB…UNZ envelope — the unit of EDI routing on ECGrid. A parcel is the physical container that carries one or more interchanges. Use when the caller has a numeric interchange ID and wants its routing, status, EDI identity, and envelope header. Returns NOT_FOUND when no interchange matches the ID. Results are scoped to the caller's APIKey — another tenant's interchange surfaces as NOT_FOUND.

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::

## Tool Name

`connectivity_interchange_get-interchange-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.interchangeId` | integer | Yes | The numeric interchange ID to look up. Positive integer &gt;= 1. Example: 123456789. Same value as the `interchangeId` field returned by list-inbox-interchanges / list-outbox-interchanges. Values of 0 or below are rejected as VALIDATION_ERROR. |

## Response

Returns the interchange's identification, routing, current status, EDI identity, envelope header, and the parcel IDs that carry it.

```json
{
  "interchangeId": 123456789,
  "interchangeControlId": "000012345",
  "standard": "X12",
  "documentType": "850",
  "bytes": 2048,
  "interchangeDateTime": "2026-07-01T10:30:00Z",
  "processDate": "2026-07-01T10:30:15Z",
  "status": {
    "code": 4000,
    "description": "Complete: CLOSED",
    "statusDate": "2026-07-01T10:30:20Z"
  },
  "from": {
    "networkId": 7,
    "networkName": "ECGrid Production",
    "mailboxId": 142
  },
  "to": {
    "networkId": 7,
    "networkName": "ECGrid Production",
    "mailboxId": 200
  },
  "header": "ISA*00*          *00*          *ZZ*ACMECORP       *ZZ*BUYERCORP      *260701*1030*^*00501*000012345*0*P*>~",
  "tpFrom": {
    "ecgridId": 6928311,
    "qualifier": "ZZ",
    "id": "ACMECORP",
    "description": "Acme Shipping"
  },
  "tpTo": {
    "ecgridId": 5040122,
    "qualifier": "ZZ",
    "id": "BUYERCORP",
    "description": "Beta Retail"
  },
  "parcelIds": [987654321],
  "parcelCount": 1
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `interchangeId` | integer | Unique numeric interchange ID |
| `interchangeControlId` | string | EDI interchange control number from the envelope header |
| `standard` | string | EDI standard — `X12`, `EDIFACT`, `TRADACOMS`, `VDA`, `XML`, `TXT`, `PDF`, or `Binary` |
| `documentType` | string | EDI transaction set or document type (e.g. `850`, `810`, `ORDERS`) |
| `bytes` | integer | Size of the interchange in bytes |
| `interchangeDateTime` | string | ISO 8601 timestamp from the EDI interchange header |
| `processDate` | string | ISO 8601 timestamp when ECGrid processed the interchange |
| `status.code` | integer | Numeric `InterchangeStatus` code (e.g. `4000` = Complete: CLOSED, `4101` = CANCELED) |
| `status.description` | string | Human-readable status description |
| `status.statusDate` | string | ISO 8601 timestamp of the most recent status change |
| `from.networkId` | integer | Network ID of the sending party |
| `from.networkName` | string | Network name of the sending party |
| `from.mailboxId` | integer | Mailbox ID of the sending party |
| `to.networkId` | integer | Network ID of the receiving party |
| `to.networkName` | string | Network name of the receiving party |
| `to.mailboxId` | integer | Mailbox ID of the receiving party |
| `header` | string | Raw EDI envelope header segment (ISA for X12, UNB for EDIFACT) |
| `tpFrom` | object \| null | Sender trading-partner EDI identity. Null if not resolved. |
| `tpFrom.ecgridId` | integer | ECGrid ID of the sending trading partner |
| `tpFrom.qualifier` | string | EDI qualifier of the sending trading partner (e.g. `ZZ`) |
| `tpFrom.id` | string | EDI identifier of the sending trading partner |
| `tpFrom.description` | string | Human-readable label for the sending trading partner |
| `tpTo` | object \| null | Recipient trading-partner EDI identity. Null if not resolved. |
| `tpTo.ecgridId` | integer | ECGrid ID of the receiving trading partner |
| `tpTo.qualifier` | string | EDI qualifier of the receiving trading partner |
| `tpTo.id` | string | EDI identifier of the receiving trading partner |
| `tpTo.description` | string | Human-readable label for the receiving trading partner |
| `parcelIds` | array&lt;integer&gt; | List of parcel IDs that contain this interchange |
| `parcelCount` | integer | Number of parcels that contain this interchange |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_interchange_get-interchange-by-id",
    "arguments": {
      "request": { "interchangeId": 123456789 }
    }
  }
}
```

## Example Prompts

- `Show me interchange 123456789`
- `Who sent interchange 99999 and what's its status?`
- `What EDI document type is interchange 555555?`

## See Also

- [list-inbox-interchanges](./list-inbox-interchanges.md) — list inbound interchanges for a mailbox
- [list-outbox-interchanges](./list-outbox-interchanges.md) — list outbound interchanges for a mailbox
- [get-document-counts-by-status](./get-document-counts-by-status.md) — count interchanges by status over a date range
- [get-parcel-by-id](../parcels/get-parcel-by-id.md) — look up the parcel that carried this interchange
