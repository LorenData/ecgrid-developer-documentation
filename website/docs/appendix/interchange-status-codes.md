---
title: Interchange Status Codes
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created interchange status codes reference page - Greg Kolinski */}

# Interchange Status Codes

An **interchange** is an individual EDI transaction set (or group of transaction sets) extracted from a parcel. This reference describes every status an interchange can hold during its lifecycle on ECGrid.

For parcel-level status codes, see [Parcel Status Codes](./parcel-status-codes).

---

## InBox States

Inbound interchanges are those received by your mailbox from a trading partner.

| Status | Description |
|---|---|
| `InBoxReady` | The interchange has been received and is ready for download. The recipient has not yet retrieved it. |
| `InBoxTransferred` | The interchange has been downloaded (transferred out) to the recipient's system. |
| `InBoxArchived` | The interchange has been moved to long-term archive storage after successful download. |

---

## OutBox States

Outbound interchanges are those sent from your mailbox to a trading partner.

| Status | Description |
|---|---|
| `outboxPending` | The interchange is queued and waiting for ECGrid to begin outbound delivery. |
| `outboxSent` | ECGrid has transmitted the interchange to the next-hop carrier or trading partner; awaiting acknowledgment. |
| `outboxAcknowledged` | The trading partner or receiving VAN has confirmed successful receipt. |
| `outboxRetry` | A delivery attempt failed; ECGrid is scheduled to retry automatically. |
| `outboxFailed` | All retry attempts have been exhausted. No further automatic delivery will be attempted. Manual intervention is required. |
| `outboxDeliveryError` | A delivery error was encountered during transit. The interchange may recover to `outboxRetry` or escalate to `outboxFailed`. |
| `outboxTransferred` | The interchange has been handed off to a downstream VAN or carrier for final delivery. |

---

## Special States

| Status | Description |
|---|---|
| `Cancelled` | The interchange was cancelled before delivery was completed. No further processing will occur. |
| `VaultReady` | The interchange is stored in the ECGrid Vault for long-term retention and compliance archiving. |

---

## AS2-Specific States

These statuses apply to interchanges routed over AS2 channels.

| Status | Description |
|---|---|
| `as2Receive` | The interchange was received via an AS2 channel. |
| `as2Sent` | The interchange was delivered via an AS2 channel. |

---

## FTP/SFTP-Specific States

These statuses apply to interchanges routed over FTP or SFTP channels.

| Status | Description |
|---|---|
| `ftpReceived` | The interchange was received via an FTP or SFTP channel. |
| `ftpSent` | The interchange was delivered via an FTP or SFTP channel. |

---

## Lifecycle Overview

A typical inbound interchange follows this path:

```
as2Receive / ftpReceived
    → InBoxReady
    → InBoxTransferred
    → InBoxArchived
```

A typical outbound interchange follows this path:

```
outboxPending
    → outboxSent
    → outboxAcknowledged  (success)

outboxPending
    → outboxSent
    → outboxRetry         (transient failure)
    → outboxFailed        (permanent failure)
```

---

## See Also

- [Parcel Status Codes](./parcel-status-codes) — file-container status codes
- [ENUMs Reference](./enums) — full `ParcelStatus` enum definition
- [REST: Get Interchange](../rest-api/interchanges/get-interchange) — retrieve a single interchange with its current status
- [REST: Interchange Inbox List](../rest-api/interchanges/inbox-list) — query inbound interchanges by status
- [REST: Interchange Outbox List](../rest-api/interchanges/outbox-list) — query outbound interchanges by status
