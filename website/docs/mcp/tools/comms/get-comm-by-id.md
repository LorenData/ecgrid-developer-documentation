---
title: get-comm-by-id
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-comm-by-id tool reference - Greg Kolinski
*/}

# get-comm-by-id

Look up a single comm (communication channel) by its numeric comm ID, and inspect the SSL/TLS certificate(s) on that endpoint — reporting each certificate's validity status and expiration details. A comm is the transport-channel configuration (AS2, SFTP, FTP, HTTP, OFTP, and others) bound to a mailbox — it defines how that mailbox physically exchanges EDI, distinct from the logical EDI ID carried in X12 envelopes.

Use when the caller already has the integer comm ID — for example from a previous `connectivity_comm_list-comms` result, a ticket, or an admin reference — or to answer "is this trading partner's endpoint certificate valid / when does it expire?". Returns NOT_FOUND when no comm matches the integer ID. Results are scoped to the caller's APIKey — another tenant's comm surfaces as NOT_FOUND. Cached for 180 seconds per caller.

## Tool Name

`connectivity_comm_get-comm-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.commId` | integer | Yes | The numeric comm (communication channel) ID — the internal int32 primary key. Positive integer >= 1. Example: 4521. Same value as the `commId` field returned by `connectivity_comm_list-comms`. Values &lt;= 0 are rejected as VALIDATION_ERROR. |

## Response

Returns the channel profile including type, identifier, URL, security flags, receipt policy, lifecycle status, usage window, owner reference, and per-certificate metadata with computed validity.

```json
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
  "certificates": [
    {
      "subject": "CN=acme.example.com, O=ACME Corp, C=US",
      "issuer": "CN=DigiCert TLS RSA SHA256 2020 CA1",
      "thumbprint": "A1B2C3D4E5F6...",
      "serialNumber": "0F:A1:B2:C3:D4:E5:F6:07",
      "notBefore": "2025-01-01T00:00:00Z",
      "notAfter": "2026-01-01T00:00:00Z",
      "status": "Active",
      "validityStatus": "Valid",
      "isCurrentlyValid": true,
      "daysUntilExpiry": 179
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `commId` | integer | The numeric comm ID (primary key) |
| `type` | string | Transport protocol — as2, ftp, sftp, ftpsslimplicit, http, oftp, x400, gisb, rnif, cxml, peppol, as4, or undefined |
| `identifier` | string | The wire identifier for the channel — AS2-ID for AS2, hostname/login for FTP/SFTP |
| `url` | string \| null | Endpoint URL (AS2 endpoint, FTP host URL, etc.) |
| `sign` | boolean | Whether outbound EDI messages are signed |
| `encrypt` | boolean | Whether outbound EDI messages are encrypted |
| `compress` | boolean | Whether outbound EDI messages are compressed |
| `receiptType` | string | AS2 MDN receipt policy — None, SynchronousUnsigned, SynchronousSigned, AsynchronousUnsigned, or AsynchronousSigned |
| `httpAuthType` | string | HTTP authentication type — None, Basic, or Digest |
| `sslClientAuthentication` | boolean | Whether SSL client certificate authentication is required |
| `useType` | string | Use classification — Undefined, Test, Production, or TestAndProduction |
| `status` | string | Lifecycle status — Development, Active, Preproduction, Suspended, or Terminated |
| `usageWindowStart` | integer | Start hour (0–23) of the allowed usage window |
| `usageWindowEnd` | integer | End hour (0–23) of the allowed usage window |
| `created` | string | ISO 8601 timestamp — when the comm was created |
| `modified` | string | ISO 8601 timestamp — when the comm was last modified |
| `owner` | object | Compact owner reference: userId, loginName, authLevel |
| `certificates` | array | Per-certificate metadata entries (see below) |

### Certificate Fields

| Field | Type | Description |
|---|---|---|
| `subject` | string | Certificate subject distinguished name |
| `issuer` | string | Certificate issuer distinguished name |
| `thumbprint` | string | SHA-1 thumbprint (hex) |
| `serialNumber` | string | Certificate serial number |
| `notBefore` | string | ISO 8601 — certificate validity start |
| `notAfter` | string | ISO 8601 — certificate validity end |
| `status` | string | Lifecycle status of the certificate record |
| `validityStatus` | string | Computed: Valid, Expired, or NotYetValid |
| `isCurrentlyValid` | boolean | true when current date falls within notBefore–notAfter |
| `daysUntilExpiry` | integer | Days remaining until notAfter; negative when already expired |

:::note
HTTP auth username/password and raw certificate bytes are deliberately not returned. To enumerate all channels under a mailbox use `connectivity_comm_list-comms`.
:::

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_get-comm-by-id",
    "arguments": {
      "request": { "commId": 4521 }
    }
  }
}
```

## Example Prompts

- `Show me comm 789`
- `What AS2 communications are set up for mailbox 142?`
- `Is the certificate on comm 4521 still valid?`

## See Also

- [list-comms](./list-comms.md) — enumerate all channels under a known (networkId, mailboxId) pair
- [find-comms](./find-comms.md) — locate a comm by its wire identifier without knowing the mailbox
