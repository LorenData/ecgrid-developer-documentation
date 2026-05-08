---
title: Platform Overview
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create platform overview page - Greg Kolinski */}

# Platform Overview

ECGrid is Loren Data Corp's B2B EDI value-added network (VAN). It routes EDI interchanges between trading partners, providing reliable store-and-forward messaging, partner connectivity, and operational visibility through a pair of APIs.

## What ECGrid Does

At its core, ECGrid acts as a hub between any two trading partners that need to exchange EDI data (X12, EDIFACT, or other formats). Senders submit files to their ECGrid Mailbox; ECGrid routes each interchange to the correct destination Mailbox based on EDI IDs; receivers poll or are notified when files are ready for pickup.

```
Sender Application
       │
       ▼
  Your Mailbox  ──────►  ECGrid VAN  ──────►  Partner Mailbox
       │                                              │
       │                                              ▼
  (upload parcel)                           Partner Application
                                             (download parcel)
```

ECGrid handles the routing, acknowledgment tracking, retransmission, and audit trail — your application only needs to upload and download files.

## Key Concepts

### Network

A **Network** is the top-level organizational unit in ECGrid. It corresponds to a VAN operator or a large enterprise operating their own ECGrid instance. All Mailboxes belong to a Network.

### Mailbox

A **Mailbox** is the functional unit for sending and receiving EDI. Each Mailbox has its own inbox and outbox. Your application authenticates against a Mailbox (or Network) and reads/writes files there.

### ECGrid ID (Trading Partner ID)

An **ECGrid ID** is the internal identifier that maps to a trading partner's EDI qualifier and ID pair (for example, `01:123456789`). ECGrid uses IDs to route interchanges to the correct Mailbox. A single Mailbox can own multiple ECGrid IDs.

### Parcel

A **Parcel** is the file-level container — a single uploaded or downloaded EDI file. When you call the upload endpoint, you create a Parcel. When you call the download endpoint, you retrieve a Parcel's contents.

### Interchange

An **Interchange** is a single EDI transaction set within a Parcel — the ISA/IEA envelope in X12, or the UNA/UNZ envelope in EDIFACT. One Parcel can contain multiple Interchanges. ECGrid tracks each Interchange individually for status, acknowledgment, and reporting.

### Partner (Interconnect)

A **Partner** (called an *Interconnect* in the SOAP API) is the relationship record between two ECGrid IDs that authorizes them to exchange EDI. Before two trading partners can transact, an Interconnect must be established.

### Callback

A **Callback** is a webhook registration. When a configured event occurs (parcel received, interchange acknowledged, etc.), ECGrid POSTs a notification to your registered endpoint, eliminating the need to poll.

## Two APIs

| | REST API v2.6 | ECGridOS SOAP API v4.1 |
|---|---|---|
| **Status** | Active | Established |
| **Base URL** | `https://rest.ecgrid.io` | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| **Format** | JSON over HTTPS | XML (SOAP 1.1) over HTTPS |
| **Auth** | `X-API-Key` header or `Bearer` JWT | `SessionID` from `Login()` |
| **Swagger / WSDL** | [swagger.json](https://rest.ecgrid.io/swagger/v2/swagger.json) | [WSDL](https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL) |

Both APIs cover the same core resources: Networks, Mailboxes, IDs, Partners, Parcels, Interchanges, Callbacks, Carbon Copies, Certificates, Comms, Users, Keys, and Reports. The REST API additionally supports Portals, which has no SOAP equivalent.


## Supported EDI Standards

ECGrid routes any of the following standards without transformation:

- **X12** (all versions, all transaction sets)
- **EDIFACT**
- **TRADACOMS**
- **VDA**
- **XML, TXT, PDF, Binary** (pass-through)
- **And more**

## Next Steps

- [Authentication & API Keys](./authentication-api-keys.md) — how to get credentials and authenticate
- [Quick Start — REST API](./quick-start-rest.md) — make your first REST call in minutes
- [Quick Start — SOAP API](./quick-start-soap.md) — connect with the established SOAP API
