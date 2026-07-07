---
title: get-callback-queue-by-id
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-callback-queue-by-id tool reference - Greg Kolinski
*/}

# get-callback-queue-by-id

Look up a single callback (webhook) delivery/retry queue entry by its numeric queue ID. A queue entry is one delivery attempt of a callback registration — it carries the attempt status, calls remaining, next-call time, the per-attempt delivery log, and a lite reference to the parent callback event. Use when the caller has a specific `callBackQueueId` — for example from `list-callback-queue` or the `queue` array of `get-callback-event-by-id` — and wants that one attempt's full detail. Returns NOT_FOUND when no queue entry matches the ID. Results are scoped to the caller's APIKey.

:::caution ID type matters
The argument to this tool is a **`callBackQueueId`** (a delivery-attempt ID), NOT a `callBackEventId` (a registration ID). Passing a `callBackEventId` here will return NOT_FOUND. To read a callback registration use `get-callback-event-by-id`; to list the queue across a mailbox use `list-callback-queue`.
:::

## Tool Name

`connectivity_callback_get-callback-queue-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.callBackQueueId` | integer | Yes | The numeric callback-QUEUE entry ID — the internal int64 primary key of a single delivery attempt. Non-negative integer &gt;= 0. Example: 99001. This is the `callBackQueueId` returned by `list-callback-queue` or the `queue` array of `get-callback-event-by-id`, NOT a `callBackEventId`. Values below 0 are rejected as VALIDATION_ERROR. |

## Response

Returns the queue entry's status, callsRemaining, nextCall, delivery log array, and a lite reference to the parent callback event registration.

```json
{
  "callBackQueueId": 99001,
  "status": "Error",
  "callsRemaining": 3,
  "nextCall": "2026-07-06T10:30:00Z",
  "test": false,
  "log": [
    {
      "callDateTime": "2026-07-06T08:15:00Z",
      "httpStatus": 503,
      "message": "Service Unavailable"
    },
    {
      "callDateTime": "2026-07-06T09:15:00Z",
      "httpStatus": 503,
      "message": "Service Unavailable"
    }
  ],
  "event": {
    "callBackEventId": 4821,
    "networkId": 7,
    "mailboxId": 142,
    "status": "Active",
    "url": "https://example.com/ecgrid-webhook",
    "httpAuthType": "Basic"
  }
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `callBackQueueId` | integer | Unique numeric ID of this delivery attempt (int64) |
| `status` | string | Attempt status: `Active`, `Pending`, `Completed`, `Error`, or `Canceled` |
| `callsRemaining` | integer | Number of retries remaining before this attempt is abandoned |
| `nextCall` | string \| null | ISO 8601 timestamp of the next scheduled retry, or null if completed or canceled |
| `test` | boolean | `true` if this was a test delivery rather than a live event trigger |
| `log` | array | Per-attempt delivery log entries for this queue entry |
| `log[].callDateTime` | string | ISO 8601 timestamp of this delivery attempt |
| `log[].httpStatus` | integer | HTTP status code returned by the webhook target |
| `log[].message` | string | Response message or error detail from the delivery attempt |
| `event` | object | Lite reference to the parent callback registration |
| `event.callBackEventId` | integer | Numeric ID of the parent callback event registration |
| `event.networkId` | integer | ECGrid network ID that owns the registration |
| `event.mailboxId` | integer | ECGrid mailbox ID that owns the registration |
| `event.status` | string | Registration status: `Active`, `Development`, `Preproduction`, `Suspended`, or `Terminated` |
| `event.url` | string | Webhook target URL |
| `event.httpAuthType` | string | HTTP authentication type: `None`, `Basic`, or `Digest`. Credentials are never returned. |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_callback_get-callback-queue-by-id",
    "arguments": {
      "request": { "callBackQueueId": 99001 }
    }
  }
}
```

## Example Prompts

- `Show me the detail for callback queue entry 99001`
- `What happened with delivery attempt 99001? Show me the log`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [get-callback-event-by-id](./get-callback-event-by-id.md) — look up a callback registration plus its embedded queue
- [list-callback-queue](./list-callback-queue.md) — list pending or failed delivery attempts across a mailbox
- [list-callback-events](./list-callback-events.md) — enumerate all callback registrations under a mailbox
