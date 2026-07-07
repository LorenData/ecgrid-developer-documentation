---
title: hello-world
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: hello-world tool reference - Greg Kolinski
*/}

# hello-world

Greets the caller and returns their identity from the ECGrid backend.

## Tool Name

`connectivity_system_hello-world`

## Auth Level Required

Any

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.name` | string \| null | No | Optional display name; falls back to the caller's loginName. Max 256 characters. |

## Response

Structured JSON — greeting message, loginName, authLevel, networkId, mailboxId, serverTimeUtc.

```json
{
  "message": "Hello, Your Name, from ECGrid MCP server.",
  "loginName": "your-login",
  "authLevel": "NetworkUser",
  "networkId": "47",
  "mailboxId": "0",
  "serverTimeUtc": "2026-07-06T14:00:00Z"
}
```

## Response Fields

| Field | Description |
|---|---|
| `message` | Greeting confirming the name passed in (or your loginName) |
| `loginName` | Your ECGrid account login name |
| `authLevel` | Your account's permission tier — see [Authentication](../../authentication.md) |
| `networkId` | The ECGrid network your account belongs to |
| `mailboxId` | Your mailbox ID (0 = network-level account) |
| `serverTimeUtc` | Current ECGrid server time in UTC |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_system_hello-world",
    "arguments": {
      "request": { "name": "Your Name" }
    }
  }
}
```

## Example Prompts

- `Test the ECGrid MCP connection`
- `What is my ECGrid auth level?`
- `What network ID does ECGrid return for me?`

## See Also

- [get-version](./get-version.md) — confirm API and backend versions
- [Authentication](../../authentication.md) — auth levels explained
