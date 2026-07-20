---
title: list-keys
sidebar_position: 2
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-keys tool reference - Greg Kolinski
*/}

# list-keys

List all key/value records attached to an ECGrid system object across every visibility. A key is a named value attached to an object (mailbox, network, user, and others) — for example the `ftp:status`, `ftp:loginname`, or `ftp:ipaddress` setup keys on a mailbox. Use when the caller wants to enumerate or discover the keys on an object — for example "what keys are set on this mailbox" or "what is the FTP config for this network". To fetch one known key by name and visibility, use `get-key`. An empty result (count = 0) means the object has no keys — a successful outcome, not NOT_FOUND. Results are scoped to the caller's APIKey. Not cached — key values can expire and Session-scoped keys are short-lived.

## Tool Name

`connectivity_key_list-keys`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.systemObject` | string | Yes | The ECGrid system-object class whose keys to list. See enum table below. For (S)FTP setup keys this is usually `Mailbox` or `Network`. Pair with `objectId` to identify the specific object. |
| `request.objectId` | integer | Yes | The numeric ID of the object named by `systemObject`, e.g. the mailbox ID when systemObject=Mailbox. Range 1–9223372036854775807 (int64). Example: 142. The root ID 0 is rejected as VALIDATION_ERROR. |

### systemObject Enum

| Value | Description |
|---|---|
| `System` | Global system-level keys |
| `User` | Keys attached to a user record |
| `Network` | Keys attached to a network |
| `Mailbox` | Keys attached to a mailbox (most common for (S)FTP setup keys) |
| `EcgridId` | Keys attached to an ECGrid ID / trading partner |
| `Interconnect` | Keys attached to a partner interconnect rule |
| `Migration` | Keys attached to a migration record |
| `Parcel` | Keys attached to a parcel/file record |
| `Interchange` | Keys attached to an interchange record |
| `CarbonCopy` | Keys attached to a carbon copy rule |
| `CallBackEvent` | Keys attached to a callback event registration |
| `As2` | Keys attached to an AS2 comm record |
| `Comm` | Keys attached to a comm (communications) record |
| `Gisb` | Keys attached to a GISB comm record |
| `InterconnectNote` | Keys attached to an interconnect note |
| `PriceList` | Keys attached to a price list |
| `Contract` | Keys attached to a contract record |
| `Invoice` | Keys attached to an invoice record |

## Response

Returns a `count` and a `keys` array; each element carries the key name, verbatim value, meta, visibility, created timestamp, and expiry.

```json
{
  "count": 3,
  "keys": [
    {
      "key": "ftp:status",
      "value": "Active",
      "meta": "",
      "visibility": "Private",
      "created": "2025-01-10T08:00:00Z",
      "expires": null
    },
    {
      "key": "ftp:loginname",
      "value": "acme_shipping_ftp",
      "meta": "",
      "visibility": "Private",
      "created": "2025-01-10T08:00:00Z",
      "expires": null
    },
    {
      "key": "ftp:ipaddress",
      "value": "203.0.113.45",
      "meta": "",
      "visibility": "Private",
      "created": "2025-01-10T08:00:00Z",
      "expires": null
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Total number of keys returned |
| `keys` | array | Array of key/value records |
| `keys[].key` | string | The key name — typically a dotted/namespaced string, e.g. `ftp:loginname` |
| `keys[].value` | string | The verbatim stored value — not redacted, not masked |
| `keys[].meta` | string | Optional metadata string associated with the key |
| `keys[].visibility` | string | Visibility scope: `Private`, `Shared`, `Public`, or `Session` |
| `keys[].created` | string | ISO 8601 timestamp when the key was created |
| `keys[].expires` | string \| null | ISO 8601 timestamp when the key expires, or null if it does not expire |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_key_list-keys",
    "arguments": {
      "request": {
        "systemObject": "Mailbox",
        "objectId": 142
      }
    }
  }
}
```

## Example Prompts

- `What FTP setup keys are on mailbox 142?`
- `List all keys configured for network 7`

## See Also

- [Tools Overview](../../overview.md) — full list of available MCP tools
- [Authentication](../../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [get-key](./get-key.md) — fetch a single key by its exact name and visibility
