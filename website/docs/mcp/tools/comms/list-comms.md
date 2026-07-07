---
title: list-comms
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-comms tool reference - Greg Kolinski
*/}

# list-comms

List the comms (communication channels) registered under a specific (networkId, mailboxId) pair for one transport protocol. A comm is the transport-channel configuration (AS2, SFTP, FTP, and others) that defines how a mailbox physically exchanges EDI.

Use to enumerate the channels under a known mailbox — for example to review which AS2 or SFTP endpoints a mailbox uses. Both `networkId` and `mailboxId` must be known first; discover them via `list-mailboxes` or `connectivity_network_get-network-by-id`. `commType` is a required filter — a listing is always scoped to a single protocol. An empty result (count = 0) is a successful outcome, not NOT_FOUND. Results are scoped to the caller's APIKey. Cached 180 seconds per caller.

## Tool Name

`connectivity_comm_list-comms`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | Internal numeric network ID. Positive integer >= 1. Example: 7. Combine with `mailboxId` to identify exactly one mailbox — both are required. Values &lt;= 0 are rejected as VALIDATION_ERROR. |
| `request.mailboxId` | integer | Yes | Internal numeric mailbox ID within `networkId`. Non-negative integer >= 0. Example: 142. `0` refers to the network's root mailbox (not a sentinel for "all"). Values &lt; 0 are rejected as VALIDATION_ERROR. |
| `request.commType` | string | Yes | Required transport-protocol filter (case-insensitive). Allowed values: `none`, `ftp`, `sftp`, `as2`, `http`, `oftp`, `x400`, `gisb`, `rnif`, `cxml`, `ftpsslimplicit`, `peppol`, `as4`, `undefined`. Unknown values are rejected as VALIDATION_ERROR. |
| `request.withCerts` | boolean \| null | No | Controls whether certificate data is populated. Default `false` — the `certificates` array on every returned channel is empty when false. Set `true` whenever the caller wants to inspect certificate validity, expiry, issuer, or thumbprint across a mailbox's channels. |
| `request.showInactive` | boolean \| null | No | When `true`, include inactive (Suspended, Terminated) channels. Default `false` — only Active, Development, and Preproduction channels are returned. |
| `request.useType` | string \| null | No | Optional use-type filter. Allowed values: `Undefined`, `Test`, `Production`, `TestAndProduction`. Default `TestAndProduction`. Unknown values are rejected as VALIDATION_ERROR. |
| `request.privateKeyRequired` | boolean \| null | No | When `true`, only channels that have a private key available are returned. Default `true`. |

:::tip Certificate inspection
Set `withCerts: true` to inspect certificate validity, expiry, and issuer across all channels in a mailbox. Without this flag the `certificates` array is empty and cert-validity questions cannot be answered. For a single channel's certificate details, `connectivity_comm_get-comm-by-id` always returns certificates without any flag.
:::

## Response

Returns a count and array of comm records. Each record carries the same shape as `connectivity_comm_get-comm-by-id`; the `certificates` array is populated only when `withCerts: true`.

```json
{
  "count": 2,
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

**With `withCerts: true`**, each comm's `certificates` array is populated (same shape as in `connectivity_comm_get-comm-by-id`).

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Total number of matching channels |
| `comms` | array | Comm records — same shape as `connectivity_comm_get-comm-by-id` |
| `comms[].commId` | integer | The numeric comm ID (primary key) |
| `comms[].type` | string | Transport protocol |
| `comms[].identifier` | string | Wire identifier (AS2-ID, FTP hostname, etc.) |
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
| `comms[].certificates` | array | Certificate metadata — populated only when `withCerts: true` |

## Example Call — List AS2 Comms

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_list-comms",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142,
        "commType": "as2"
      }
    }
  }
}
```

## Example Call — List AS2 Comms With Certificates

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_list-comms",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142,
        "commType": "as2",
        "withCerts": true
      }
    }
  }
}
```

## Example Prompts

- `List all AS2 comms for mailbox 142 on network 7`
- `Show FTP connections for mailbox 500`
- `List AS2 comms with certificates for mailbox 142`

## See Also

- [get-comm-by-id](./get-comm-by-id.md) — look up a single channel by its integer comm ID (always returns certificates)
- [find-comms](./find-comms.md) — locate a channel by its wire identifier without knowing the mailbox
