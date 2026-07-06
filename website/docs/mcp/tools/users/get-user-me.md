{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-user-me tool reference - Greg Kolinski
*/}
---
title: get-user-me
---

# get-user-me

Return the session and profile record for the caller themselves — the user identified by the inbound APIKey. Use for any "who am I?", "what's my account?", "what network/mailbox am I on?", "what's my auth level?" question, or to confirm the caller's identity / scope before invoking another tool. Returns the calling user's identity (userId, login, name, email, phone, company) plus session metadata (sessionId, ECGridOS version, last login, time-zone offset, auth level, network/mailbox affiliation, open sessions, session timeout). Takes no input arguments — identity comes entirely from the inbound APIKey header. To look up another user's profile by ID or login, use `connectivity_user_get-user-by-id` / `connectivity_user_get-user-by-login` instead.

## Tool Name

`connectivity_user_get-user-me`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

This tool takes no parameters. Pass an empty `request` object.

## Response

Returns the calling user's full profile and current session metadata.

```json
{
  "ecgridOsVersion": "4.1.2.0",
  "sessionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "sessionEventId": 88001234,
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
| `ecgridOsVersion` | string | ECGridOS backend version currently running |
| `sessionId` | string | Active session token associated with this API call |
| `sessionEventId` | integer | Internal event ID for this session |
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
    "name": "connectivity_user_get-user-me",
    "arguments": { "request": {} }
  }
}
```

## Example Prompts

- "Who am I?"
- "What's my ECGrid account?"
- "What auth level does my API key have?"

## See Also

- [get-user-by-id](./get-user-by-id.md)
- [Authentication & API Keys](../../authentication.md)
