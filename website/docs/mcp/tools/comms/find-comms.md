---
title: find-comms
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: find-comms tool reference - Greg Kolinski
*/}

# find-comms

Find the comm (communication channel) records whose wire identifier matches a given `identifier` string for one transport protocol. Use when you have a channel identifier — for example an AS2-ID like `ACME-AS2` or an FTP hostname — and want the matching channel(s) without knowing the owning `networkId`/`mailboxId` first.

This is the right tool to answer "which mailbox owns this AS2 ID?" An empty result (count = 0) means no channel matches the identifier — a successful outcome, not NOT_FOUND. Results are scoped to the caller's APIKey. Cached 180 seconds per caller.

## Tool Name

`connectivity_comm_find-comms`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.identifier` | string | Yes | The wire identifier to locate — the comm's identifier for the chosen protocol (e.g. AS2-ID for an AS2 channel, login or hostname for FTP/SFTP). Length 1–128 characters. Example: `ACME-AS2`. Empty or whitespace is rejected as VALIDATION_ERROR. |
| `request.commType` | string | Yes | Required transport-protocol filter (case-insensitive). Allowed values: `none`, `ftp`, `sftp`, `as2`, `http`, `oftp`, `x400`, `gisb`, `rnif`, `cxml`, `ftpsslimplicit`, `peppol`, `as4`, `undefined`. Unknown values are rejected as VALIDATION_ERROR. |
| `request.showInactive` | boolean \| null | No | When `true`, include inactive (Suspended, Terminated) channels. Default `false`. |
| `request.useType` | string \| null | No | Optional use-type filter. Allowed values: `Undefined`, `Test`, `Production`, `TestAndProduction`. Default `TestAndProduction`. |
| `request.privateKeyRequired` | boolean \| null | No | When `true`, only channels with a private key available are returned. Default `false` — unlike `list-comms` (which defaults true), a find by identifier should locate the channel regardless of private-key presence. |

:::note Certificate inspection
This endpoint has no `withCerts` flag, so certificate details are not controllable here. To review certificate validity, expiry, or issuer call `connectivity_comm_get-comm-by-id` (always returns certificates) or `connectivity_comm_list-comms` with `withCerts: true`.
:::

## Response

Returns a count and array of matching comm records. Each record carries the same shape as `connectivity_comm_get-comm-by-id` minus certificate details.

```json
{
  "count": 1,
  "comms": [
    {
      "commId": 4521,
      "type": "as2",
      "identifier": "ACME-AS2",
      "url": "https://as2.acme.example.com:4080",
      "sign": true,
      "encrypt": true,
      "compress": false,
      "receiptType": "SynchronousSigned",
      "httpAuthType": "None",
      "sslClientAuthentication": false,
      "useType": "Production",
      "status": "Active",
      "usageWindowStart": 0,
      "usageWindowEnd": 23,
      "created": "2023-05-10T14:00:00Z",
      "modified": "2026-01-15T09:30:00Z",
      "owner": {
        "userId": 1001,
        "loginName": "admin@acme.example.com",
        "authLevel": "MailboxAdmin"
      },
      "certificates": []
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Number of matching channels |
| `comms` | array | Comm records — same shape as `connectivity_comm_get-comm-by-id` |
| `comms[].commId` | integer | The numeric comm ID (primary key) — use with `get-comm-by-id` to fetch certificate details |
| `comms[].type` | string | Transport protocol |
| `comms[].identifier` | string | Wire identifier that was matched |
| `comms[].url` | string \| null | Endpoint URL |
| `comms[].sign` | boolean | Whether outbound messages are signed |
| `comms[].encrypt` | boolean | Whether outbound messages are encrypted |
| `comms[].compress` | boolean | Whether outbound messages are compressed |
| `comms[].receiptType` | string | AS2 MDN receipt policy |
| `comms[].httpAuthType` | string | HTTP authentication type |
| `comms[].sslClientAuthentication` | boolean | Whether SSL client certificate auth is required |
| `comms[].useType` | string | Use classification |
| `comms[].status` | string | Lifecycle status |
| `comms[].owner` | object | Compact owner reference: userId, loginName, authLevel |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_find-comms",
    "arguments": {
      "request": {
        "identifier": "ACME-AS2",
        "commType": "as2"
      }
    }
  }
}
```

## Example Prompts

- `Which mailbox uses AS2 ID "ACME-CORP"?`
- `Find who owns FTP identifier "ftp.example.com"`

## See Also

- [get-comm-by-id](./get-comm-by-id.md) — look up a single channel by its integer comm ID (always returns certificates)
- [list-comms](./list-comms.md) — enumerate all channels under a known (networkId, mailboxId) pair
