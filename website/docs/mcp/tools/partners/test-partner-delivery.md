---
title: test-partner-delivery
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: test-partner-delivery tool reference - Greg Kolinski
*/}

# test-partner-delivery

Actively test whether EDI delivery works across an ECGrid interconnect (trading-partner relationship) by sending a throwaway test parcel through the grid and reading its delivery status. Use when the caller asks whether a partner is reachable, connected, receiving, or wants to confirm a channel works end-to-end — given the integer interconnect ID. Returns NOT_FOUND when no interconnect matches the ID or it has no resolvable ECGrid IDs. An inactive (suspended/terminated) interconnect returns verdict `not_tested` without sending a parcel.

## Tool Name

`connectivity_partner_test-partner-delivery`

## Auth Level Required

Any (scoped to caller's APIKey)

---

## Two-Step Pattern

This tool is **non-blocking and two-step**. A single call does not wait for delivery to complete. Instead:

**Step 1 — Initiate (call WITHOUT `parcelId`)**

Omit `request.parcelId` entirely. The tool sends the test parcel and returns immediately with:
- `verdict`: `"pending"` — the parcel is in flight
- `parcelId`: the numeric ID of the test parcel

**Step 2 — Poll (call WITH `parcelId`)**

Pass the `parcelId` from Step 1 back as `request.parcelId`. The tool checks the parcel's current delivery status and returns the final verdict (`delivered`, `failed`, or `aborted`). The parcel may still be in flight on the first poll — repeat Step 2 until the verdict is no longer `pending`.

---

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.interconnectId` | integer | Yes | The numeric interconnect (trading-partner relationship) ID to test. Positive integer >= 1. Example: 12345. Same value as `InterconnectIDInfo.interconnectId` from `connectivity_partner_list-partners` or `connectivity_partner_get-partner-by-id`. |
| `request.direction` | string \| null | No | Direction of the test parcel. `Tp1ToTp2` (default) sends from TP1 to TP2 and tests TP2's inbound endpoint. `Tp2ToTp1` reverses the direction. Call twice to test both endpoints. |
| `request.parcelId` | integer \| null | No | Omit on Step 1 (initiate). Supply on Step 2 (poll) — pass the `parcelId` returned from the initiation call to check delivery status. |
| `request.documentType` | string \| null | No | Optional EDI document standard for the test payload. Default `EDIFACT`. Accepted values: `Binary`, `EDIFACT`, `PDF`, `TRADACOMS`, `TXT`, `VDA`, `X12`, `XML`. Reachability does not depend on the payload type; override only to exercise a specific document standard. |

## Response

Returns the delivery test result including reachability flag, normalized verdict, raw status codes, the parcel ID for polling, resolved ECGrid IDs, and plain-language notes.

```json
{
  "reachable": true,
  "verdict": "delivered",
  "statusCode": "InBoxReady",
  "statusDescription": "In mailbox, ready for download",
  "parcelId": 987654321,
  "fromEcgridId": 6928311,
  "toEcgridId": 7100042,
  "notes": "Test parcel delivered successfully to TP2 mailbox."
}
```

**Pending (Step 1 or in-flight Step 2):**

```json
{
  "reachable": null,
  "verdict": "pending",
  "statusCode": "OutBoxQueued",
  "statusDescription": "Queued for delivery",
  "parcelId": 987654321,
  "fromEcgridId": 6928311,
  "toEcgridId": 7100042,
  "notes": "Test parcel is in flight. Poll again with parcelId 987654321 to check the result."
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `reachable` | boolean \| null | `true` when delivery succeeded; `false` when delivery failed; `null` when still pending or not tested |
| `verdict` | string | Normalized outcome: `delivered`, `failed`, `aborted`, `pending`, or `not_tested` |
| `statusCode` | string | Raw ECGrid parcel status code (e.g. `InBoxReady`, `OutBoxQueued`, `outboxDeliveryError`) |
| `statusDescription` | string | Human-readable description of the current parcel status |
| `parcelId` | integer | The numeric ID of the test parcel — use this on Step 2 to poll delivery status |
| `fromEcgridId` | integer | Resolved sender ECGrid ID (the originating side based on `direction`) |
| `toEcgridId` | integer | Resolved recipient ECGrid ID (the destination side based on `direction`) |
| `notes` | string \| null | Plain-language explanation of the result or next steps (e.g. polling instruction) |

## Example Call — Step 1 (Initiate)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_partner_test-partner-delivery",
    "arguments": {
      "request": {
        "interconnectId": 12345,
        "direction": "Tp1ToTp2"
      }
    }
  }
}
```

## Example Call — Step 2 (Poll)

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "connectivity_partner_test-partner-delivery",
    "arguments": {
      "request": {
        "interconnectId": 12345,
        "parcelId": 987654321
      }
    }
  }
}
```

## Example Prompts

- `Test delivery to trading partner 12345`
- `Send a test to check if interconnect 99999 is working`
- `Is TP2 receiving for partner 12345?`

## See Also

- [check-partner-config](./check-partner-config.md) — static configuration health-check (no traffic sent)
- [get-partner-by-id](./get-partner-by-id.md) — view the raw interconnect profile before testing
- [list-partners](./list-partners.md) — discover interconnect IDs to test
