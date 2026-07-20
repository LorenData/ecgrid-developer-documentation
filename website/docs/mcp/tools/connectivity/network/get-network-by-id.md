---
title: get-network-by-id
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-network-by-id tool reference - Greg Kolinski
*/}

# get-network-by-id

Look up a single ECGrid network by its numeric network ID. Use when the caller already has the integer ID (e.g. from a previous tool result, a ticket, or an admin reference). Returns the network's profile: name, lifecycle status, run status, outage status, primary contacts, associated user-account IDs (owner, routing, errors, interconnects, billing, …), public website URLs, owner-side routing metadata, and audit timestamps. Sensitive infrastructure (server hostnames, VPN secrets, FTP credentials, mailbox config) is deliberately excluded. Returns NOT_FOUND when no network matches the ID. Results are limited to what the caller's APIKey can see; another tenant's network ID will surface as NOT_FOUND.

## Tool Name

`connectivity_network_get-network-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.networkId` | integer | Yes | The numeric ECGrid network ID to look up (>= 1) |

## Response

Returns the network profile including name, lifecycle and run status, primary contacts, public URLs, and audit timestamps.

```json
{
  "networkId": 47,
  "name": "Acme Logistics EDI Network",
  "status": "Active",
  "runStatus": "Normal",
  "outageStatus": "None",
  "ownerUserId": 101,
  "ownerLoginName": "admin@acme-logistics.com",
  "ownerAuthLevel": "NetworkAdmin",
  "errorsUserId": 102,
  "errorsLoginName": "edi-errors@acme-logistics.com",
  "errorsAuthLevel": "NetworkUser",
  "interconnectsUserId": 103,
  "interconnectsLoginName": "interconnects@acme-logistics.com",
  "interconnectsAuthLevel": "NetworkUser",
  "billingUserId": 104,
  "billingLoginName": "billing@acme-logistics.com",
  "billingAuthLevel": "NetworkUser",
  "publicWebsite": "https://www.acme-logistics.com",
  "ediWebsite": "https://edi.acme-logistics.com",
  "routingNetworkId": 7,
  "created": "2020-04-01T00:00:00Z",
  "modified": "2026-06-15T10:22:44Z"
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `networkId` | integer | Unique numeric ECGrid network ID |
| `name` | string | Display name of the network |
| `status` | string | Lifecycle status (see [Status enum](../../../../appendix/enums.md)) |
| `runStatus` | string | Operational run state of the network |
| `outageStatus` | string | Current outage state (`None`, `Scheduled`, `Active`) |
| `ownerUserId` | integer | User ID of the network owner contact |
| `ownerLoginName` | string | Login name of the network owner contact |
| `ownerAuthLevel` | string | Auth level of the owner (see [AuthLevel enum](../../../../appendix/enums.md)) |
| `errorsUserId` | integer | User ID of the errors contact |
| `errorsLoginName` | string | Login name of the errors contact |
| `errorsAuthLevel` | string | Auth level of the errors contact |
| `interconnectsUserId` | integer | User ID of the interconnects contact |
| `interconnectsLoginName` | string | Login name of the interconnects contact |
| `interconnectsAuthLevel` | string | Auth level of the interconnects contact |
| `billingUserId` | integer | User ID of the billing contact |
| `billingLoginName` | string | Login name of the billing contact |
| `billingAuthLevel` | string | Auth level of the billing contact |
| `publicWebsite` | string | Public-facing website URL for the network owner |
| `ediWebsite` | string | EDI-specific website URL (partner portal, etc.) |
| `routingNetworkId` | integer | Network ID used for owner-side routing metadata |
| `created` | string | ISO 8601 timestamp when the network was created |
| `modified` | string | ISO 8601 timestamp of the most recent network update |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_network_get-network-by-id",
    "arguments": {
      "request": { "networkId": 47 }
    }
  }
}
```

## Example Prompts

- `Show me network 47`
- `What's the status of my ECGrid network?`
- `Who is the owner contact for network 7?`

## See Also

- [list-mailboxes](../mailboxes/list-mailboxes) — list all mailboxes on a network
- [get-user-me](../users/get-user-me) — check your own networkId
