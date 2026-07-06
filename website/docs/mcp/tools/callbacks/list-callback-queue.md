{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-callback-queue tool reference - Greg Kolinski
*/}
---
title: list-callback-queue
sidebar_position: 4
---

# list-callback-queue

List the callback (webhook) delivery/retry queue under a specific (networkId, mailboxId) pair. A queue entry is one delivery attempt of a callback — useful for diagnosing callbacks that are pending or stuck failing. Use `view` to select the slice: `pending` (default) returns attempts awaiting or processing delivery; `failed` returns errored attempts within the last `maxDays` (which is required when `view = failed`). An empty result (count = 0) means no entries match — this is a successful outcome, not an error.

## Tool Name

`connectivity_callback_list-callback-queue`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | Internal numeric network ID that scopes the listing. Positive integer &gt;= 1. Example: 7. Combine with `mailboxId` to bound the query to one mailbox — both are required. Values of 0 or below are rejected as VALIDATION_ERROR. |
| `request.mailboxId` | integer | Yes | Internal numeric mailbox ID within `networkId`. Non-negative integer &gt;= 0. Example: 142. `0` is a valid value referring to the network's root mailbox. Values below 0 are rejected as VALIDATION_ERROR. |
| `request.view` | string | No | Which slice of the delivery queue to return: `pending` (default — attempts awaiting or processing delivery) or `failed` (attempts that have errored within the last `maxDays`). Any other value is rejected as VALIDATION_ERROR. |
| `request.maxDays` | integer | Conditional | Look-back window in days for the `failed` view. Range 1–365. Example: 30. **Required when `view = failed`; must be omitted when `view = pending`.** Supplying it with `view = pending`, or omitting it with `view = failed`, is VALIDATION_ERROR. |

## Response

Returns `count` plus a `queue` array of delivery attempt records; each entry carries status, callsRemaining, nextCall, the delivery log, and a lite reference to the parent callback event. HTTP auth credentials are never returned.

```json
{
  "count": 2,
  "queue": [
    {
      "callBackQueueId": 99010,
      "status": "Pending",
      "callsRemaining": 10,
      "nextCall": "2026-07-06T09:00:00Z",
      "log": [],
      "event": {
        "callBackEventId": 4821,
        "networkId": 7,
        "mailboxId": 142,
        "status": "Active",
        "url": "https://example.com/ecgrid-webhook",
        "httpAuthType": "Basic"
      }
    },
    {
      "callBackQueueId": 99011,
      "status": "Pending",
      "callsRemaining": 9,
      "nextCall": "2026-07-06T09:05:00Z",
      "log": [
        {
          "callDateTime": "2026-07-06T08:55:00Z",
          "httpStatus": 500,
          "message": "Internal Server Error"
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
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Number of queue entries returned. `0` means no entries match — not an error. |
| `queue` | array | Array of delivery attempt records |
| `queue[].callBackQueueId` | integer | Unique numeric ID of this delivery attempt (int64). Pass to `get-callback-queue-by-id` for full detail. |
| `queue[].status` | string | Attempt status: `Active`, `Pending`, `Completed`, `Error`, or `Canceled` |
| `queue[].callsRemaining` | integer | Number of retries remaining before this attempt is abandoned |
| `queue[].nextCall` | string \| null | ISO 8601 timestamp of the next scheduled retry, or null if completed or canceled |
| `queue[].log` | array | Per-attempt delivery log entries (callDateTime, httpStatus, message) for this attempt so far |
| `queue[].event` | object | Lite reference to the parent callback event registration |
| `queue[].event.callBackEventId` | integer | Numeric ID of the parent callback event registration |
| `queue[].event.networkId` | integer | ECGrid network ID that owns the registration |
| `queue[].event.mailboxId` | integer | ECGrid mailbox ID that owns the registration |
| `queue[].event.status` | string | Registration status: `Active`, `Development`, `Preproduction`, `Suspended`, or `Terminated` |
| `queue[].event.url` | string | Webhook target URL |
| `queue[].event.httpAuthType` | string | HTTP authentication type: `None`, `Basic`, or `Digest`. Credentials are never returned. |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_callback_list-callback-queue",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142,
        "view": "pending"
      }
    }
  }
}
```

## Example Prompts

- `Are there any pending callback deliveries for mailbox 142?`
- `Show me all failed callback attempts for mailbox 142 in the last 7 days`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [list-callback-events](./list-callback-events.md) — enumerate all callback registrations under a mailbox
- [get-callback-event-by-id](./get-callback-event-by-id.md) — look up a single registration with its embedded delivery queue
- [get-callback-queue-by-id](./get-callback-queue-by-id.md) — look up a single delivery attempt by its queue ID
