---
title: get-user-by-login
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-user-by-login tool reference - Greg Kolinski
*/}

# get-user-by-login

Look up a single ECGrid user by their login name or email address. Use when the caller has a textual identifier (most ECGrid logins ARE full email addresses, e.g. `jane.smith@example.com`). Returns the same profile shape as `connectivity_user_get-user-by-id`. Returns NOT_FOUND when no user matches; VALIDATION_ERROR when the input contains control characters, null bytes, or injection characters (`< > { } ' " ; \`) — those are rejected before the backend is called. Results are limited to the caller's APIKey scope. If you only have a numeric ID use `connectivity_user_get-user-by-id`; for substring / partial-match discovery use `connectivity_user_list-users` with `name`.

## Tool Name

`connectivity_user_get-user-by-login`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.loginName` | string | Yes | Login name or full email address used to sign in to ECGrid. Most logins are email addresses (example: `jane.smith@example.com`). Length 8–128 characters after trim. Control characters, null bytes, and injection characters `< > { } ' " ; \` are rejected before the backend is called. |

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
    "name": "connectivity_user_get-user-by-login",
    "arguments": { "request": { "loginName": "jane.smith@example.com" } }
  }
}
```

## Example Prompts

- "Look up user jane.smith@example.com"
- "Find the ECGrid user with login \"acme.admin\""

## See Also

- [get-user-me](./get-user-me.md)
- [list-users](./list-users.md)
