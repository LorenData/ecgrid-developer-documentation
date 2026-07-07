---
title: test-comm
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: test-comm tool reference - Greg Kolinski
*/}

# test-comm

Actively self-test whether ECGrid can deliver to a customer's own configured communication channel (receive direction) by sending a throwaway test parcel from an ECGrid loopback test ID to the given ECGrid ID over that channel, then reading the parcel's delivery status. Use when the caller asks whether their own FTP or AS2 channel is "working", "receiving", or "reachable" — given the customer ECGrid ID and the channel type (`Ftp` or `As2`).

To test delivery to another trading partner (not your own channel) use `connectivity_partner_test-partner-delivery`.

## Tool Name

`connectivity_comm_test-comm`

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
| `request.ecgridId` | integer | Yes | The customer's ECGrid ID (the receive side) whose channel to self-test. Positive integer >= 1. Example: 7704344. The test parcel is delivered TO this ID over its configured comm. |
| `request.commType` | string | Yes | Which communication channel to test: `Ftp` or `As2`. Selects the ECGrid loopback test ID used as the parcel sender. OFTP is not yet supported. |
| `request.parcelId` | integer \| null | No | Omit on Step 1 (initiate). Supply the `parcelId` from Step 1 on Step 2 (poll) to check delivery status. Example: 987654321. |
| `request.documentType` | string \| null | No | Optional EDI document standard for the test payload. Default `EDIFACT`. Accepted values: `Binary`, `EDIFACT`, `PDF`, `TRADACOMS`, `TXT`, `VDA`, `X12`, `XML`. Reachability does not depend on payload type. |

## Response

Returns the delivery test result including a reachability flag, normalized verdict, raw status codes, the parcel ID for polling, and the loopback ECGrid ID used as sender.

**Pending (Step 1 or in-flight Step 2):**

```json
{
  "reachable": null,
  "verdict": "pending",
  "statusCode": "OutBoxQueued",
  "statusDescription": "Queued for delivery",
  "parcelId": 987654321,
  "loopbackEcgridId": 6001234
}
```

**Final result (Step 2 — delivered):**

```json
{
  "reachable": true,
  "verdict": "delivered",
  "statusCode": "InBoxReady",
  "statusDescription": "In mailbox, ready for download",
  "parcelId": 987654321,
  "loopbackEcgridId": 6001234
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `reachable` | boolean \| null | `true` when delivery succeeded; `false` when delivery failed; `null` when still pending |
| `verdict` | string | Normalized outcome: `delivered`, `failed`, `aborted`, or `pending` |
| `statusCode` | string | Raw ECGrid parcel status code (e.g. `InBoxReady`, `OutBoxQueued`, `outboxDeliveryError`) |
| `statusDescription` | string | Human-readable description of the current parcel status |
| `parcelId` | integer | The numeric ID of the test parcel — use this on Step 2 to poll delivery status |
| `loopbackEcgridId` | integer | The ECGrid loopback test ID used as the sender |

## Example Call — Step 1 (Initiate)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_test-comm",
    "arguments": {
      "request": {
        "ecgridId": 7704344,
        "commType": "As2"
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
    "name": "connectivity_comm_test-comm",
    "arguments": {
      "request": {
        "ecgridId": 7704344,
        "commType": "As2",
        "parcelId": 987654321
      }
    }
  }
}
```

## Example Prompts

- `Test AS2 connectivity for ECGrid ID 12345`
- `Check if FTP delivery is working for ECGrid ID 99999`

## See Also

- [check-ftp-access](./check-ftp-access.md) — diagnose FTP login, IP allowlist, and account status without sending traffic
- [find-comms](./find-comms.md) — discover the comm identifier or comm ID before testing
