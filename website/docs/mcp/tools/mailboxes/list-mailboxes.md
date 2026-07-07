---
title: list-mailboxes
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-mailboxes tool reference - Greg Kolinski
*/}

# list-mailboxes

List every mailbox in one ECGrid network. Use to browse or enumerate a network's mailboxes when you do not have a name to search by (e.g. "show the mailboxes on network 7", or just "list my mailboxes"). `networkId` is optional: supply it to list a specific network; omit it to list the caller's own home network, resolved from the current session. There is no "all networks" mode — the result is always scoped to a single network. Returns an array of mailbox records (`mailboxes`) plus a `count`; the array may be empty when the network has no mailboxes.

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::

## Tool Name

`connectivity_mailbox_list-mailboxes`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer \| null | No | ECGrid network ID to list mailboxes for. Positive integer >= 1. When omitted or null, defaults to the caller's own home network resolved from the current session. |

## Response

Returns a `count` and a `mailboxes` array. Each mailbox record has the same shape as the response from `get-mailbox-by-id`. Always reflects current state — cache is bypassed.

```json
{
  "count": 2,
  "mailboxes": [
    {
      "mailboxId": 142,
      "networkId": 7,
      "name": "acme-prod@example.com",
      "description": "ACME Production Mailbox",
      "status": "Active",
      "useType": "Production",
      "managed": false,
      "ecgridAccount": "acme-prod",
      "defaultAs2Id": 0,
      "ownerUserId": 101,
      "ownerLoginName": "admin@example.com",
      "ownerAuthLevel": "MailboxAdmin",
      "created": "2021-06-01T00:00:00Z",
      "modified": "2026-05-20T14:10:33Z"
    },
    {
      "mailboxId": 143,
      "networkId": 7,
      "name": "acme-test@example.com",
      "description": "ACME Test Mailbox",
      "status": "Active",
      "useType": "Test",
      "managed": false,
      "ecgridAccount": "acme-test",
      "defaultAs2Id": 0,
      "ownerUserId": 101,
      "ownerLoginName": "admin@example.com",
      "ownerAuthLevel": "MailboxAdmin",
      "created": "2021-06-01T00:00:00Z",
      "modified": "2026-05-20T14:10:33Z"
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Total number of mailboxes returned |
| `mailboxes` | array | Array of mailbox profile objects |
| `mailboxes[].mailboxId` | integer | Unique numeric ECGrid mailbox ID |
| `mailboxes[].networkId` | integer | ECGrid network this mailbox belongs to |
| `mailboxes[].name` | string | Mailbox name (typically an email address) |
| `mailboxes[].description` | string | Human-readable display name for the mailbox |
| `mailboxes[].status` | string | Lifecycle status (see [Status enum](../../../appendix/enums.md)) |
| `mailboxes[].useType` | string | Use type — Test, Production, or TestAndProduction (see [UseType enum](../../../appendix/enums.md)) |
| `mailboxes[].managed` | boolean | `true` if this is a managed mailbox |
| `mailboxes[].ecgridAccount` | string | Short account identifier used internally |
| `mailboxes[].defaultAs2Id` | integer | ECGrid ID of the default AS2 trading partner; `0` if none |
| `mailboxes[].ownerUserId` | integer | User ID of the mailbox owner contact |
| `mailboxes[].ownerLoginName` | string | Login name of the mailbox owner contact |
| `mailboxes[].ownerAuthLevel` | string | Auth level of the owner (see [AuthLevel enum](../../../appendix/enums.md)) |
| `mailboxes[].created` | string | ISO 8601 timestamp when the mailbox was created |
| `mailboxes[].modified` | string | ISO 8601 timestamp of the most recent mailbox update |

## Example Call

### List mailboxes on a specific network

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_mailbox_list-mailboxes",
    "arguments": {
      "request": { "networkId": 47 }
    }
  }
}
```

### List mailboxes on the caller's home network

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "connectivity_mailbox_list-mailboxes",
    "arguments": {
      "request": { "networkId": null }
    }
  }
}
```

## Example Prompts

- `List all mailboxes on my network`
- `How many mailboxes does network 47 have?`
- `Show all mailboxes for network 7`

## See Also

- [get-mailbox-by-id](./get-mailbox-by-id.md) — look up a single mailbox by numeric ID
- [get-mailbox-by-name](./get-mailbox-by-name.md) — search mailboxes by name substring
- [get-network-by-id](../network/get-network-by-id.md) — look up the parent network
