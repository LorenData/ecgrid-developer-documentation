{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-key tool reference - Greg Kolinski
*/}
---
title: get-key
sidebar_position: 1
---

# get-key

Fetch a single ECGrid key/value record by its exact key name, scoped to one system object and one visibility. A key is a named value attached to an ECGrid object (mailbox, network, user, and others) — for example the `ftp:status` or `ftp:loginname` setup keys on a mailbox. Use when the caller already knows the key name and its visibility — for example from a previous `list-keys` result — and wants just that value. To enumerate all keys on an object and discover their names and visibility, use `list-keys` first. Returns NOT_FOUND when no key matches the name within that scope and visibility. Results are scoped to the caller's APIKey. Not cached — key values can expire and Session-scoped keys are short-lived.

## Tool Name

`connectivity_key_get-key`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.systemObject` | string | Yes | The ECGrid system-object class the key is attached to. See enum table below. For (S)FTP setup keys this is usually `Mailbox` or `Network`. Pair with `objectId` to identify the specific object. |
| `request.objectId` | integer | Yes | The numeric ID of the object named by `systemObject`, e.g. the mailbox ID when systemObject=Mailbox. Positive integer &gt;= 1. Example: 142. The root ID 0 is rejected as VALIDATION_ERROR. |
| `request.key` | string | Yes | The exact key name to fetch — typically a dotted/namespaced string, e.g. `ftp:status`. 1–512 characters. Use `list-keys` to discover which keys exist on an object before guessing this value. |
| `request.visibility` | string | Yes | The visibility scope to read the key from. One of: `Private`, `Shared`, `Public`, `Session`. The backend looks the key up within a single visibility scope — it must match the key's actual visibility. Use `list-keys` first to see each key's visibility. |

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

### visibility Enum

| Value | Description |
|---|---|
| `Private` | Visible only to the owning network/mailbox |
| `Shared` | Visible to the owning network/mailbox and its trading partners |
| `Public` | Visible to any authenticated caller |
| `Session` | Short-lived session-scoped value |

## Response

Returns the key record: name, verbatim value (not redacted), meta, visibility, created timestamp, and expiry.

```json
{
  "key": "ftp:loginname",
  "value": "acme_shipping_ftp",
  "meta": "",
  "visibility": "Private",
  "created": "2025-01-10T08:00:00Z",
  "expires": null
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `key` | string | The key name (matches the requested key) |
| `value` | string | The verbatim stored value — not redacted, not masked |
| `meta` | string | Optional metadata string associated with the key |
| `visibility` | string | Visibility scope: `Private`, `Shared`, `Public`, or `Session` |
| `created` | string | ISO 8601 timestamp when the key was created |
| `expires` | string \| null | ISO 8601 timestamp when the key expires, or null if it does not expire |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_key_get-key",
    "arguments": {
      "request": {
        "systemObject": "Mailbox",
        "objectId": 142,
        "key": "ftp:loginname",
        "visibility": "Private"
      }
    }
  }
}
```

## Example Prompts

- `What is the FTP username stored for mailbox 142?`
- `Fetch the ftp:loginname Private key on mailbox 142`

## See Also

- [Tools Overview](../overview.md) — full list of available MCP tools
- [Authentication](../../authentication.md) — how to authenticate with the ECGrid MCP Server
- [list-keys](./list-keys.md) — enumerate all keys on an object to discover their names and visibility
