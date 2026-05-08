---
title: Parcel Status Codes
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created parcel status codes reference page - Greg Kolinski */}

# Parcel Status Codes

A **parcel** is the file-level container transmitted between trading partners on ECGrid. Each parcel wraps one or more EDI interchanges. Parcel status tracks where the file is in the transmission lifecycle — from receipt or queueing through final delivery or archival.

For status codes at the interchange level (individual EDI transactions), see [Interchange Status Codes](./interchange-status-codes).

---

## InBox States

Inbound parcels are files that have arrived at your mailbox from a trading partner or carrier.

| Status | Description |
|---|---|
| `InBoxReady` | The parcel file has been received and is available for download. Your system has not yet retrieved it. Polling your inbox will return this parcel. |
| `InBoxTransferred` | The parcel file has been successfully downloaded by the recipient. A download confirmation (`confirm-download`) should follow to acknowledge receipt. |
| `InBoxArchived` | The parcel has been moved to long-term archive storage after a successful confirmed download. It is no longer returned in standard inbox queries. |

---

## OutBox States

Outbound parcels are files queued for delivery from your mailbox to a trading partner or carrier.

| Status | Description |
|---|---|
| `outboxPending` | The parcel has been accepted by ECGrid and is queued for outbound transmission. No delivery attempt has been made yet. |
| `outboxSent` | ECGrid has transmitted the parcel to the next hop (carrier, VAN, or trading partner endpoint). Awaiting delivery confirmation. |
| `outboxAcknowledged` | The receiving party has confirmed successful receipt of the parcel. This is a terminal success state. |
| `outboxRetry` | The initial delivery attempt failed. ECGrid will automatically retry according to its retry schedule. The parcel is not yet permanently failed. |
| `outboxFailed` | All delivery retry attempts have been exhausted. The parcel could not be delivered. Manual investigation and possible resend are required. |
| `outboxDeliveryError` | A delivery error occurred during transmission. This is a transient error state that may resolve to `outboxRetry` or `outboxFailed`. |
| `outboxTransferred` | The parcel has been handed off to a downstream carrier or VAN for final leg delivery. ECGrid's direct responsibility has ended. |

---

## Channel-Specific States

These states indicate both the direction and the communication channel used for the parcel.

| Status | Description |
|---|---|
| `as2Receive` | The parcel was received over an AS2 channel. Indicates inbound AS2 traffic. |
| `as2Sent` | The parcel was delivered over an AS2 channel. Indicates successful outbound AS2 delivery. |
| `ftpReceived` | The parcel was received over an FTP or SFTP channel. Indicates inbound FTP/SFTP traffic. |
| `ftpSent` | The parcel was delivered over an FTP or SFTP channel. Indicates successful outbound FTP/SFTP delivery. |

---

## Special States

| Status | Description |
|---|---|
| `Cancelled` | The parcel was explicitly cancelled before delivery completed. All interchanges within the parcel are also cancelled. No further processing will occur. |
| `VaultReady` | The parcel has been stored in the ECGrid Vault for long-term compliance archiving. It can be retrieved via vault queries but is no longer in the active inbox or outbox. |

---

## Parcel vs. Interchange Status

| Concept | Scope | Use Case |
|---|---|---|
| Parcel status | The entire file | Tracking file-level transmission (upload, download, delivery) |
| Interchange status | Individual EDI transaction within the file | Tracking EDI-level routing and acknowledgment |

A single parcel may contain multiple interchanges. The parcel may reach `outboxAcknowledged` while individual interchanges inside it are still being processed for functional acknowledgment (997/999).

---

## Lifecycle Overview

**Inbound parcel (your mailbox receives):**

```
as2Receive / ftpReceived
    → InBoxReady
    → InBoxTransferred  (after download)
    → InBoxArchived     (after confirm-download)
```

**Outbound parcel (your mailbox sends):**

```
outboxPending           (after upload)
    → outboxSent
    → outboxAcknowledged   (success path)

outboxPending
    → outboxSent
    → outboxRetry          (transient failure)
    → outboxFailed         (permanent failure — requires manual action)
```

---

## See Also

- [Interchange Status Codes](./interchange-status-codes) — EDI transaction-level status codes
- [ENUMs Reference](./enums) — full `ParcelStatus` enum definition
- [REST: Get Parcel](../rest-api/parcels/get-parcel) — retrieve a single parcel and its current status
- [REST: Inbox List](../rest-api/parcels/inbox-list) — query inbound parcels by status
- [REST: Outbox List](../rest-api/parcels/outbox-list) — query outbound parcels by status
- [REST: Confirm Download](../rest-api/parcels/confirm-download) — acknowledge download and advance parcel to `InBoxArchived`
- [Common Operations: Download a File](../common-operations/download-a-file) — end-to-end download workflow
