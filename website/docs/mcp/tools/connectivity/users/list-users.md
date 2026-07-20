---
title: list-users
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-users tool reference - Greg Kolinski
*/}

# list-users

List ECGrid users matching the supplied filters, scoped to what the caller's APIKey can see. Use for discovery: browsing a network's user roster, finding all locked-out accounts on a network, searching by partial login / email substring, or auditing how many users share a mailbox. At least one of `networkId`, `mailboxId`, or `name` MUST be supplied (scope filter); `lockedOut` is a post-filter and is NOT a valid scope on its own — omit-all-three is rejected as VALIDATION_ERROR. Combine filters to narrow results (e.g. `networkId=7` + `lockedOut=true` → locked-out users on network 7). Returns an array of user records (`users`) plus a `count`. This tool deliberately bypasses the response cache so the result always reflects current state — useful for support workflows that mutate users (unlock, suspend, terminate) and immediately re-list to confirm. When the caller already knows a specific user, prefer `connectivity_user_get-user-by-id` or `connectivity_user_get-user-by-login` (cached, faster, single record).

## Tool Name

`connectivity_user_list-users`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer \| null | Conditionally required | Scope filter. Restrict results to one ECGrid network. Positive integer >= 1. At least one of `networkId`, `mailboxId`, or `name` MUST be supplied — `lockedOut` alone is not a valid scope. |
| `request.mailboxId` | integer \| null | Conditionally required | Scope filter. Restrict results to one mailbox within the network. `0` = the network's root mailbox; `-1` = all mailboxes (no mailbox filter). Only meaningful when `networkId` is also supplied. Counts toward the at-least-one-of requirement. |
| `request.name` | string \| null | Conditionally required | Scope filter. Case-insensitive substring filter applied to the user's login/email (example: `acme` matches `alice@acme.com` and `bob@acme.example.org`). Up to 40 characters. For an exact lookup by full login, prefer `connectivity_user_get-user-by-login` instead. Counts toward the at-least-one-of requirement. |
| `request.lockedOut` | boolean \| null | No | Post-filter. When `true`, return only users whose account is currently locked out. When `false` or omitted, return all users matching the other filters. Does NOT count as a scope filter — `lockedOut` alone without `networkId` / `mailboxId` / `name` is rejected as VALIDATION_ERROR. |

## Response

Returns a `count` and a `users` array, each entry matching the profile shape from `get-user-by-id`. Always reflects current state — cache is bypassed.

```json
{
  "count": 2,
  "users": [
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
    },
    {
      "userId": 57,
      "loginName": "bob.jones@example.com",
      "firstName": "Bob",
      "lastName": "Jones",
      "company": "Acme Corp",
      "email": "bob.jones@example.com",
      "phone": "555-123-4567",
      "timeZoneOffset": -5,
      "authLevel": "MailboxUser",
      "lockoutStatus": true,
      "networkId": 7,
      "mailboxId": 142,
      "lastLogin": "2026-06-20T08:15:00Z",
      "openSessions": 0,
      "timeOut": 3600,
      "created": "2025-01-10T10:00:00Z",
      "modified": "2026-07-01T11:45:00Z"
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Total number of users returned |
| `users` | array | Array of user profile objects |
| `users[].userId` | integer | Unique numeric user ID |
| `users[].loginName` | string | Login name / email address |
| `users[].firstName` | string | First name |
| `users[].lastName` | string | Last name |
| `users[].company` | string | Company or organization name |
| `users[].email` | string | Contact email address |
| `users[].authLevel` | string | Authorization level (see [AuthLevel enum](../../../../appendix/enums.md)) |
| `users[].lockoutStatus` | boolean | `true` if the account is currently locked out |
| `users[].networkId` | integer | ECGrid network ID this user belongs to |
| `users[].mailboxId` | integer | Mailbox ID within the network |
| `users[].lastLogin` | string | ISO 8601 timestamp of most recent login |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_user_list-users",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": null,
        "name": null,
        "lockedOut": null
      }
    }
  }
}
```

### Locked-out users on a network

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "connectivity_user_list-users",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": null,
        "name": null,
        "lockedOut": true
      }
    }
  }
}
```

## Example Prompts

- "List all users on network 7"
- "Show locked-out users on network 7"
- "Find users with \"acme\" in their login"

## See Also

- [get-user-me](./get-user-me.md)
- [get-user-by-id](./get-user-by-id.md)
