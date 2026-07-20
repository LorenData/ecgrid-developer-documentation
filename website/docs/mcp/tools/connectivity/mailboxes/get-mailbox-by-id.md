---
title: get-mailbox-by-id
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-mailbox-by-id tool reference - Greg Kolinski
*/}

# get-mailbox-by-id

Look up a single ECGrid mailbox by its numeric mailbox ID. Use when the caller already has the integer ID (e.g. from a previous tool result, a ticket, or an admin reference). Returns the mailbox's profile: name, lifecycle status, use-type, managed flag, the seven role-based contacts (owner, errors, interconnects, notices, reports, customer service, accounting), delivery and X12 envelope configuration, default AS2 ID, owner-side billing metadata, and audit timestamps. Returns NOT_FOUND when no mailbox matches the ID. Results are limited to what the caller's APIKey can see; another tenant's mailbox ID will surface as NOT_FOUND.

> ℹ️ **Interactive UI Component:** This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.

## Tool Name

`connectivity_mailbox_get-mailbox-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.mailboxId` | integer | Yes | The numeric ECGrid mailbox ID to look up. Positive integer >= 1. Example: 142. |

## Response

Returns the mailbox profile including name, lifecycle status, use-type, managed flag, role-based contacts, delivery config, X12 config, billing metadata, and audit timestamps.

```json
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
  "errorsUserId": 102,
  "errorsLoginName": "edi-errors@example.com",
  "errorsAuthLevel": "MailboxUser",
  "interconnectsUserId": 103,
  "interconnectsLoginName": "interconnects@example.com",
  "interconnectsAuthLevel": "MailboxUser",
  "noticesUserId": 104,
  "noticesLoginName": "notices@example.com",
  "noticesAuthLevel": "MailboxUser",
  "reportsUserId": 105,
  "reportsLoginName": "reports@example.com",
  "reportsAuthLevel": "MailboxUser",
  "customerServiceUserId": 106,
  "customerServiceLoginName": "support@example.com",
  "customerServiceAuthLevel": "MailboxUser",
  "accountingUserId": 107,
  "accountingLoginName": "billing@example.com",
  "accountingAuthLevel": "MailboxUser",
  "priceListId": 10,
  "contractId": 55,
  "created": "2021-06-01T00:00:00Z",
  "modified": "2026-05-20T14:10:33Z"
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `mailboxId` | integer | Unique numeric ECGrid mailbox ID |
| `networkId` | integer | ECGrid network this mailbox belongs to |
| `name` | string | Mailbox name (typically an email address) |
| `description` | string | Human-readable display name for the mailbox |
| `status` | string | Lifecycle status (see [Status enum](../../../../appendix/enums.md)) |
| `useType` | string | Use type — Test, Production, or TestAndProduction (see [UseType enum](../../../../appendix/enums.md)) |
| `managed` | boolean | `true` if this is a managed mailbox |
| `ecgridAccount` | string | Short account identifier used internally |
| `defaultAs2Id` | integer | ECGrid ID of the default AS2 trading partner; `0` if none |
| `ownerUserId` | integer | User ID of the mailbox owner contact |
| `ownerLoginName` | string | Login name of the mailbox owner contact |
| `ownerAuthLevel` | string | Auth level of the owner (see [AuthLevel enum](../../../../appendix/enums.md)) |
| `errorsUserId` | integer | User ID of the errors contact |
| `errorsLoginName` | string | Login name of the errors contact |
| `errorsAuthLevel` | string | Auth level of the errors contact |
| `interconnectsUserId` | integer | User ID of the interconnects contact |
| `interconnectsLoginName` | string | Login name of the interconnects contact |
| `interconnectsAuthLevel` | string | Auth level of the interconnects contact |
| `noticesUserId` | integer | User ID of the notices contact |
| `noticesLoginName` | string | Login name of the notices contact |
| `noticesAuthLevel` | string | Auth level of the notices contact |
| `reportsUserId` | integer | User ID of the reports contact |
| `reportsLoginName` | string | Login name of the reports contact |
| `reportsAuthLevel` | string | Auth level of the reports contact |
| `customerServiceUserId` | integer | User ID of the customer service contact |
| `customerServiceLoginName` | string | Login name of the customer service contact |
| `customerServiceAuthLevel` | string | Auth level of the customer service contact |
| `accountingUserId` | integer | User ID of the accounting contact |
| `accountingLoginName` | string | Login name of the accounting contact |
| `accountingAuthLevel` | string | Auth level of the accounting contact |
| `priceListId` | integer | Owner-side price list ID for billing |
| `contractId` | integer | Owner-side contract ID for billing |
| `created` | string | ISO 8601 timestamp when the mailbox was created |
| `modified` | string | ISO 8601 timestamp of the most recent mailbox update |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_mailbox_get-mailbox-by-id",
    "arguments": {
      "request": { "mailboxId": 142 }
    }
  }
}
```

## Example Prompts

- `Show me mailbox 142`
- `What's the configuration of mailbox 500?`
- `Who is the owner contact for mailbox 142?`

## See Also

- [list-mailboxes](./list-mailboxes.md) — list all mailboxes on a network
- [get-mailbox-by-name](./get-mailbox-by-name.md) — search mailboxes by name substring
- [get-network-by-id](../network/get-network-by-id.md) — look up the parent network
