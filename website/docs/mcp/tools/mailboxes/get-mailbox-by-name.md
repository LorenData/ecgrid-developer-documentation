{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-mailbox-by-name tool reference - Greg Kolinski
*/}
---
title: get-mailbox-by-name
---

# get-mailbox-by-name

Look up ECGrid mailboxes inside one network by a name substring. Use when the caller knows the target network and a fragment of the mailbox name or email (e.g. `acme` matches `acme-prod@example.com` and `acme-test@example.com`). Both `networkId` and `name` are required — there is no "all networks / all names" mode. Returns an array of mailbox records (`mailboxes`) plus a `count`; the array may be empty when no mailbox in the network matches the substring. This tool deliberately bypasses the response cache so the result always reflects current state. When the caller already knows a specific mailbox's numeric ID, prefer `get-mailbox-by-id` (cached, faster, single record).

## Tool Name

`connectivity_mailbox_get-mailbox-by-name`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | Restrict results to mailboxes inside one ECGrid network. Positive integer >= 1. If the network ID is unknown, resolve it first via `connectivity_network_get-network-by-id`. |
| `request.name` | string | Yes | Case-insensitive substring filter applied to the mailbox name. May be a full email address (e.g. `john.doe@example.com`) or a partial name (e.g. `acme`). 1 to 128 characters. |

## Response

Returns a `count` and a `mailboxes` array. Each mailbox record has the same shape as the response from `get-mailbox-by-id`. Always reflects current state — cache is bypassed. An empty array (`count: 0`) is a valid successful outcome — it means no mailbox in the network matched the substring.

```json
{
  "count": 2,
  "mailboxes": [
    {
      "mailboxId": 142,
      "networkId": 47,
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
      "networkId": 47,
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

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_mailbox_get-mailbox-by-name",
    "arguments": {
      "request": {
        "networkId": 47,
        "name": "acme"
      }
    }
  }
}
```

## Example Prompts

- `Find mailboxes with "acme" in their name on network 47`
- `Search for mailboxes containing "test" on network 7`

## See Also

- [get-mailbox-by-id](./get-mailbox-by-id.md) — look up a single mailbox by numeric ID (cached, faster)
- [list-mailboxes](./list-mailboxes.md) — list all mailboxes on a network without a name filter
- [get-network-by-id](../network/get-network-by-id.md) — resolve a network ID if unknown
