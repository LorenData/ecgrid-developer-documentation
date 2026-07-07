---
title: get-parcel-by-id
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-parcel-by-id tool reference - Greg Kolinski
*/}

# get-parcel-by-id

Look up a single parcel by its numeric parcel ID and return its full detail. A parcel is the physical file container that carries one or more EDI interchanges through a mailbox. Use when the caller has a numeric parcel ID and wants the parcel's routing, identification, current status, and the interchanges inside it. Returns NOT_FOUND when no parcel matches the ID. Results are scoped to the caller's APIKey — another tenant's parcel surfaces as NOT_FOUND.

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::

## Tool Name

`connectivity_parcel_get-parcel-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.parcelId` | integer (int64) | Yes | The numeric parcel ID — the internal 64-bit primary key of the parcel to look up. Positive integer >= 1. Example: 987654321. Same value returned by `connectivity_parcel_list-inbox-parcels`, `connectivity_parcel_list-outbox-parcels`, and `connectivity_parcel_list-pending-inbox-parcels`. Values of 0 or below are rejected as VALIDATION_ERROR. |

## Response

Returns the parcel's identification, routing, current status, and the interchanges it contains.

```json
{
  "parcelId": 987654321,
  "parcelDate": "2026-07-01T10:30:00Z",
  "parcelBytes": 4096,
  "fileName": "ACME_850_20260701.edi",
  "mailbagControlId": "MB-20260701-001",
  "status": {
    "code": 200,
    "description": "InBoxReady",
    "statusDate": "2026-07-01T10:30:15Z"
  },
  "from": {
    "networkId": 7,
    "networkName": "ECGrid Production",
    "mailboxId": 142,
    "mailboxName": "acme-prod@example.com"
  },
  "to": {
    "networkId": 7,
    "networkName": "ECGrid Production",
    "mailboxId": 200,
    "mailboxName": "buyer-prod@retailer.com"
  },
  "interchanges": [
    {
      "interchangeId": 112233,
      "statusCode": 200,
      "statusDescription": "InBoxReady",
      "statusDate": "2026-07-01T10:30:15Z",
      "documentType": "850"
    }
  ],
  "interchangeCount": 1
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `parcelId` | integer (int64) | Unique numeric parcel ID |
| `parcelDate` | string | ISO 8601 timestamp when the parcel was received/created |
| `parcelBytes` | integer | Size of the parcel file in bytes |
| `fileName` | string | Original file name of the parcel |
| `mailbagControlId` | string | Mailbag control ID assigned at submission |
| `status.code` | integer | Numeric status code |
| `status.description` | string | Human-readable status description |
| `status.statusDate` | string | ISO 8601 timestamp of the most recent status change |
| `from.networkId` | integer | Network ID of the sending party |
| `from.networkName` | string | Network name of the sending party |
| `from.mailboxId` | integer | Mailbox ID of the sending party |
| `from.mailboxName` | string | Mailbox name of the sending party |
| `to.networkId` | integer | Network ID of the receiving party |
| `to.networkName` | string | Network name of the receiving party |
| `to.mailboxId` | integer | Mailbox ID of the receiving party |
| `to.mailboxName` | string | Mailbox name of the receiving party |
| `interchanges` | array | List of interchanges contained in this parcel |
| `interchanges[].interchangeId` | integer | Unique interchange ID |
| `interchanges[].statusCode` | integer | Numeric status code for this interchange |
| `interchanges[].statusDescription` | string | Human-readable interchange status |
| `interchanges[].statusDate` | string | ISO 8601 timestamp of the interchange's most recent status change |
| `interchanges[].documentType` | string | EDI transaction set / document type (e.g. `850`, `810`) |
| `interchangeCount` | integer | Total number of interchanges in the parcel |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_parcel_get-parcel-by-id",
    "arguments": {
      "request": { "parcelId": 987654321 }
    }
  }
}
```

## Example Prompts

- `Show me parcel 987654321`
- `What's the status of this parcel?`
- `Which interchanges does parcel 12345 contain?`

## See Also

- [list-inbox-parcels](./list-inbox-parcels.md) — list inbound parcels by date range (coming soon)
- [list-outbox-parcels](./list-outbox-parcels.md) — list outbound parcels by date range (coming soon)
- [list-pending-inbox-parcels](./list-pending-inbox-parcels.md) — list parcels awaiting download (coming soon)
