---
title: check-ftp-access
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: check-ftp-access tool reference - Greg Kolinski
*/}

# check-ftp-access

Diagnose why an FTP or SFTP connection to ECGrid is being refused by reading the FTP setup keys on a mailbox or network and, when an FTP login name is configured, the status of the ECGrid user behind it. Use when the caller asks "why is this FTP/SFTP login blocked", "is the FTP account active", "is this IP allowed to connect", or "is the FTP user locked out / over its session limit".

`networkId` is required. `mailboxId` is optional — when supplied, keys are read from the mailbox; otherwise from the network. `ip` is optional — when supplied, an additional section reports whether that address matches the FTP access allowlist. `ftpConfigured: false` means the object exists but has no FTP setup; a missing object surfaces as NOT_FOUND.

## Tool Name

`connectivity_comm_check-ftp-access`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | The numeric ECGrid network ID that owns the FTP setup. Positive integer >= 1. Example: 7. When `mailboxId` is omitted, FTP keys are read at the network level. |
| `request.mailboxId` | integer \| null | No | Optional mailbox ID whose FTP setup to inspect. Positive integer >= 1 when supplied. The network root mailbox (id 0) is not addressable via this tool. When supplied, keys are read from the mailbox; when omitted, from the network. Example: 142. |
| `request.ip` | string \| null | No | Optional IPv4 or IPv6 address to check against the FTP access allowlist (`ftp:ipaddress` key). When supplied, an `ip` section is added to the response reporting whether the address is allowed. Example: `203.0.113.5`. |

## Response

Returns a `data` envelope with an always-present `account` section, an optional `ip` section (only when `ip` is supplied), and an optional `user` section (only when an FTP login name is configured). If the user-status lookup degrades, `partial` is `true` and `warnings` explains what is missing while the FTP-key data is still returned.

```json
{
  "data": {
    "account": {
      "ftpConfigured": true,
      "status": "ACTIVE",
      "loginName": "ftpuser@acme.example.com",
      "hasCertificate": false
    },
    "ip": {
      "allowed": true
    },
    "user": {
      "lockedOut": false,
      "status": "Active",
      "openSessions": 1
    }
  },
  "partial": false,
  "warnings": []
}
```

**When `ip` is not supplied** the `ip` section is absent:

```json
{
  "data": {
    "account": {
      "ftpConfigured": true,
      "status": "ACTIVE",
      "loginName": "ftpuser@acme.example.com",
      "hasCertificate": false
    },
    "user": {
      "lockedOut": false,
      "status": "Active",
      "openSessions": 0
    }
  },
  "partial": false,
  "warnings": []
}
```

**When FTP is not configured** (`ftpConfigured: false`):

```json
{
  "data": {
    "account": {
      "ftpConfigured": false,
      "status": null,
      "loginName": null,
      "hasCertificate": false
    }
  },
  "partial": false,
  "warnings": []
}
```

## Response Fields

### Top Level

| Field | Type | Description |
|---|---|---|
| `data` | object | Response envelope containing account, ip, and user sections |
| `partial` | boolean | `true` when the user-status lookup degraded — FTP-key data is still present |
| `warnings` | array | Plain-language descriptions of any degraded lookups |

### `data.account`

| Field | Type | Description |
|---|---|---|
| `ftpConfigured` | boolean | `true` when FTP keys are present and configured on the object |
| `status` | string \| null | Raw FTP status value from `ftp:status` key (e.g. `ACTIVE`, `PENDING`) |
| `loginName` | string \| null | FTP login name configured on the object |
| `hasCertificate` | boolean | Whether a certificate is associated — raw certificate material is never returned |

### `data.ip` (only when `ip` parameter is supplied)

| Field | Type | Description |
|---|---|---|
| `allowed` | boolean | `true` when the supplied IP matches an entry in the `ftp:ipaddress` allowlist |

### `data.user` (only when an FTP login name is configured)

| Field | Type | Description |
|---|---|---|
| `lockedOut` | boolean | Whether the ECGrid user account is currently locked out |
| `status` | string | Lifecycle status of the ECGrid user (e.g. Active, Suspended, Terminated) |
| `openSessions` | integer | Number of currently open sessions for this user |

## Example Call — Check Account and IP

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_check-ftp-access",
    "arguments": {
      "request": {
        "networkId": 7,
        "mailboxId": 142,
        "ip": "203.0.113.5"
      }
    }
  }
}
```

## Example Call — Check Account Only (No IP Test)

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "connectivity_comm_check-ftp-access",
    "arguments": {
      "request": {
        "networkId": 47,
        "mailboxId": 500
      }
    }
  }
}
```

## Example Prompts

- `Why is the FTP login for mailbox 142 being refused?`
- `Is IP 203.0.113.5 allowed for FTP on network 7?`
- `Check FTP access status for mailbox 500 on network 47`

## See Also

- [test-comm](./test-comm.md) — actively test FTP or AS2 delivery by sending a live test parcel
- [list-comms](./list-comms.md) — enumerate all comm channels configured for a mailbox
