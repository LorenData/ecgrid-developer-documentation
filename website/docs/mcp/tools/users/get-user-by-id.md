{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-user-by-id tool reference - Greg Kolinski
*/}
---
title: get-user-by-id
---

# get-user-by-id

Look up a single ECGrid user by their numeric user ID. Use when the caller already has the integer ID (e.g. from a previous tool result, a ticket, or an admin reference). Returns the user's profile: login, name, company, contact info, network/mailbox affiliation, auth level, lockout status, timestamps. Returns NOT_FOUND when no user matches the ID. Results are limited to what the caller's APIKey can see; another tenant's user ID will surface as NOT_FOUND. For text identifiers (login name, email) use `connectivity_user_get-user-by-login`; for the caller's own profile use `connectivity_user_get-user-me`; for discovery (substring search, locked-out roster) use `connectivity_user_list-users`.

## Tool Name

`connectivity_user_get-user-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.userId` | integer | Yes | The numeric ECGrid user ID. Positive integer >= 1. Example: 42. |

## Response

Returns the specified user's full profile.

```json
{
  "userId": 42,
  "loginName": "jane.smith@example.com",
  "firstName": "Jane",
  "lastName": "Smith",
  "company": "Acme Corp",
  "email": "jane.smith@example.com",
  "phone": "555-867-5309",
  "timeZoneOffset": -5,
  "authLevel": "MailboxAdmin",
  "lockoutStatus": false,
  "networkId": 7,
  "mailboxId": 142,
  "lastLogin": "2026-07-05T14:22:10Z",
  "openSessions": 1,
  "timeOut": 3600,
  "created": "2024-03-15T08:00:00Z",
  "modified": "2026-06-01T09:30:00Z"
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `userId` | integer | Unique numeric user ID |
| `loginName` | string | Login name / email address used to sign in |
| `firstName` | string | First name |
| `lastName` | string | Last name |
| `company` | string | Company or organization name |
| `email` | string | Contact email address |
| `phone` | string | Phone number |
| `timeZoneOffset` | integer | UTC offset in hours |
| `authLevel` | string | Authorization level (see [AuthLevel enum](../../../appendix/enums.md)) |
| `lockoutStatus` | boolean | `true` if the account is currently locked out |
| `networkId` | integer | ECGrid network ID this user belongs to |
| `mailboxId` | integer | Mailbox ID within the network |
| `lastLogin` | string | ISO 8601 timestamp of the most recent login |
| `openSessions` | integer | Number of currently active sessions |
| `timeOut` | integer | Session timeout in seconds |
| `created` | string | ISO 8601 timestamp when this user account was created |
| `modified` | string | ISO 8601 timestamp of the most recent profile update |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_user_get-user-by-id",
    "arguments": { "request": { "userId": 42 } }
  }
}
```

## Example Prompts

- "Look up user 12345"
- "Show me the profile for user ID 9876"

## See Also

- [get-user-me](./get-user-me.md)
- [list-users](./list-users.md)
