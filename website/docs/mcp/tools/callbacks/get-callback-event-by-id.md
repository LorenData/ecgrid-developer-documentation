{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-callback-event-by-id tool reference - Greg Kolinski
*/}
---
title: get-callback-event-by-id
sidebar_position: 1
---

# get-callback-event-by-id

Look up a single callback (webhook) event registration by its numeric callback-event ID, together with its recent delivery and retry queue. A callback is a rule that makes ECGrid POST a notification to a configured URL when a parcel or interchange event occurs on a mailbox. Use when the caller already has the integer `callBackEventId` — for example from a previous `connectivity_callback_list-callback-events` result — and wants the registration config plus how its recent deliveries are going. Returns NOT_FOUND when no callback event matches the integer ID. Results are scoped to the caller's APIKey — another tenant's callback surfaces as NOT_FOUND.

## Tool Name

`connectivity_callback_get-callback-event-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.callBackEventId` | integer | Yes | The numeric callback-event ID — the internal int32 primary key of the webhook registration. Positive integer &gt;= 1. Example: 4821. Same value as the `callBackEventId` field returned by `list-callback-events`. Values of 0 or below are rejected as VALIDATION_ERROR. |
| `request.queueCount` | integer | No | Maximum number of recent delivery/retry queue entries to embed in the response `queue` array. Defaults to 25 when omitted. Range 1–32767. Example: 50. Use a larger value to see more retry history for a failing callback. |

## Response

Returns the callback registration config (systemObject, direction, frequency, maxCalls, status, url, httpAuthType) and a `queue` array of recent delivery attempts (each entry: status, callsRemaining, nextCall, and a delivery log). HTTP auth credentials are never returned.

```json
{
  "callBackEventId": 4821,
  "networkId": 7,
  "mailboxId": 142,
  "systemObject": "Parcel",
  "direction": "InBox",
  "frequency": 5,
  "maxCalls": 10,
  "status": "Active",
  "url": "https://example.com/ecgrid-webhook",
  "httpAuthType": "Basic",
  "queue": [
    {
      "callBackQueueId": 99001,
      "status": "Completed",
      "callsRemaining": 0,
      "nextCall": null,
      "log": [
        {
          "callDateTime": "2026-07-06T08:15:00Z",
          "httpStatus": 200,
          "message": "OK"
        }
      ]
    },
    {
      "callBackQueueId": 99002,
      "status": "Pending",
      "callsRemaining": 8,
      "nextCall": "2026-07-06T09:00:00Z",
      "log": []
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `callBackEventId` | integer | Unique numeric ID of this callback registration |
| `networkId` | integer | ECGrid network ID that owns this callback |
| `mailboxId` | integer | ECGrid mailbox ID that owns this callback |
| `systemObject` | string | ECGrid object type that triggers the callback (e.g. `Parcel`, `Interchange`) |
| `direction` | string | Traffic direction that triggers the callback: `InBox`, `OutBox`, or `NoDir` |
| `frequency` | integer | Retry frequency in minutes between delivery attempts |
| `maxCalls` | integer | Maximum number of delivery attempts before the queue entry is marked failed |
| `status` | string | Registration status: `Active`, `Development`, `Preproduction`, `Suspended`, or `Terminated` |
| `url` | string | Webhook target URL that ECGrid POSTs to |
| `httpAuthType` | string | HTTP authentication type configured for the target URL: `None`, `Basic`, or `Digest`. Credentials are never returned. |
| `queue` | array | Recent delivery/retry queue entries embedded in this response (up to `queueCount`). Call `get-callback-queue-by-id` for a single entry's full detail. |
| `queue[].callBackQueueId` | integer | Unique numeric ID of this delivery attempt (int64) |
| `queue[].status` | string | Attempt status: `Active`, `Pending`, `Completed`, `Error`, or `Canceled` |
| `queue[].callsRemaining` | integer | Number of delivery retries remaining before this attempt is abandoned |
| `queue[].nextCall` | string \| null | ISO 8601 timestamp of the next scheduled retry, or null if completed/canceled |
| `queue[].log` | array | Per-attempt delivery log entries (callDateTime, httpStatus, message) |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_callback_get-callback-event-by-id",
    "arguments": {
      "request": { "callBackEventId": 4821 }
    }
  }
}
```

## Example Prompts

- `Show me callback 4821 and its recent delivery attempts`
- `Is callback event 4821 working? Show me the last 50 queue entries`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [list-callback-events](./list-callback-events.md) — enumerate all callback registrations under a mailbox
- [get-callback-queue-by-id](./get-callback-queue-by-id.md) — look up a single delivery attempt by its queue ID
- [list-callback-queue](./list-callback-queue.md) — list pending or failed delivery attempts across a mailbox
