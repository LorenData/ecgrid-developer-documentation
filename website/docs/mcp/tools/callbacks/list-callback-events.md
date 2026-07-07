---
title: list-callback-events
sidebar_position: 3
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-callback-events tool reference - Greg Kolinski
*/}

# list-callback-events

List the callback (webhook) registrations under a specific (networkId, mailboxId) pair. A callback is a rule that makes ECGrid POST a notification to a configured URL when a parcel or interchange event occurs on the mailbox. Use to enumerate which callbacks a mailbox has and review their config and status. Both `networkId` and `mailboxId` must be known — discover them via `list-mailboxes` or `connectivity_network_get-network-by-id`. An empty result (count = 0) means no callbacks match — this is a successful outcome, not an error.

## Tool Name

`connectivity_callback_list-callback-events`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | Internal numeric network ID that scopes the listing. Positive integer &gt;= 1. Example: 7. Combine with `mailboxId` to identify exactly one mailbox — both are required. Values of 0 or below are rejected as VALIDATION_ERROR. |
| `request.mailboxId` | integer | Yes | Internal numeric mailbox ID within `networkId`. Non-negative integer &gt;= 0. Example: 142. `0` is a valid value referring to the network's root mailbox. Values below 0 are rejected as VALIDATION_ERROR. |
| `request.showInactive` | boolean | No | When `true`, include inactive (Suspended, Terminated) callback registrations. Defaults to `false` — only Active, Development, and Preproduction registrations are returned. |

## Response

Returns `count` plus an `events` array of registration config records. The per-event `queue` array is empty by design — call `get-callback-event-by-id` to retrieve a registration with its embedded delivery queue. HTTP auth credentials are never returned.

```json
{
  "count": 2,
  "events": [
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
      "queue": []
    },
    {
      "callBackEventId": 4822,
      "networkId": 7,
      "mailboxId": 142,
      "systemObject": "Interchange",
      "direction": "OutBox",
      "frequency": 10,
      "maxCalls": 5,
      "status": "Active",
      "url": "https://example.com/ecgrid-webhook-out",
      "httpAuthType": "None",
      "queue": []
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Number of callback registrations returned. `0` means no callbacks match — not an error. |
| `events` | array | Array of callback registration records |
| `events[].callBackEventId` | integer | Unique numeric ID of this callback registration. Pass to `get-callback-event-by-id` to retrieve its delivery queue. |
| `events[].networkId` | integer | ECGrid network ID that owns this callback |
| `events[].mailboxId` | integer | ECGrid mailbox ID that owns this callback |
| `events[].systemObject` | string | ECGrid object type that triggers the callback (e.g. `Parcel`, `Interchange`) |
| `events[].direction` | string | Traffic direction that triggers the callback: `InBox`, `OutBox`, or `NoDir` |
| `events[].frequency` | integer | Retry frequency in minutes between delivery attempts |
| `events[].maxCalls` | integer | Maximum number of delivery attempts before a queue entry is marked failed |
| `events[].status` | string | Registration status: `Active`, `Development`, `Preproduction`, `Suspended`, or `Terminated` |
| `events[].url` | string | Webhook target URL that ECGrid POSTs to |
| `events[].httpAuthType` | string | HTTP authentication type: `None`, `Basic`, or `Digest`. Credentials are never returned. |
| `events[].queue` | array | Always empty in this listing response — call `get-callback-event-by-id` to retrieve a registration's queue |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_callback_list-callback-events",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142
      }
    }
  }
}
```

## Example Prompts

- `List all callbacks configured for mailbox 142`
- `Show me every webhook registration on mailbox 142, including inactive ones`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [get-callback-event-by-id](./get-callback-event-by-id.md) — look up a single registration with its embedded delivery queue
- [list-callback-queue](./list-callback-queue.md) — list pending or failed delivery attempts across a mailbox
- [get-callback-queue-by-id](./get-callback-queue-by-id.md) — look up a single delivery attempt by its queue ID
