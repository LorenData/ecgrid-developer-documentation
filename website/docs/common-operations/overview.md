---
title: Common Operations Overview
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create common-operations overview page - Greg Kolinski */}

# Common Operations Overview

This section provides step-by-step guides for the most frequent ECGrid integration tasks. Every guide shows both the **REST API** and the **SOAP API** side by side, so you can choose the approach that matches your stack.

## What's Covered

| Guide | What It Does | REST Endpoint | SOAP Method |
|---|---|---|---|
| [Poll for Inbound Files](./poll-inbound-files) | Check your mailbox for EDI files ready to download | `POST /v2/parcels/inbox-list` | `ParcelInBox()` |
| [Download a File](./download-a-file) | Retrieve the raw bytes of an inbound parcel | `POST /v2/parcels/download` | `ParcelDownload()` |
| [Confirm a Download](./confirm-download) | Mark a parcel as delivered to prevent re-delivery | `POST /v2/parcels/confirm` | `ParcelDownloadConfirm()` |
| [Upload a File](./upload-a-file) | Send an EDI file into ECGrid for routing and delivery | `POST /v2/parcels/upload` | `ParcelUpload()` |
| [Send EDI to a Trading Partner](./send-edi-to-trading-partner) | Look up a partner's ECGrid ID and deliver an EDI document | `POST /v2/parcels/upload` | `TPSearch()` + `ParcelUpload()` |
| [Create a Mailbox](./create-a-mailbox) | Provision a new mailbox under your network | `POST /v2/mailboxes` | `MailboxAdd()` |
| [Onboard a Trading Partner](./onboard-trading-partner) | Register a new trading partner (ECGrid ID + interconnect) | `POST /v2/ids` | `TPAdd()` + `InterconnectAdd()` |
| [Set Up an Interconnect](./setup-interconnect) | Establish a partner relationship between two ECGrid IDs | `POST /v2/partners` | `InterconnectAdd()` |
| [Configure Callbacks](./configure-callbacks) | Register a webhook endpoint for real-time event notifications | `POST /v2/callbacks` | `CallBackAdd()` |
| [Manage Users and Permissions](./manage-users-permissions) | Create users and assign auth levels | `POST /v2/users` | `UserAdd()` |
| [Work with Carbon Copies](./work-with-carbon-copies) | Mirror inbound or outbound EDI traffic to a secondary mailbox | `POST /v2/carbon-copies` | `CarbonCopyAdd()` |

## Recommended Integration Pattern

For most integrations, the core loop is:

1. **Poll** — call the inbox list endpoint on a schedule (every 1–15 minutes is typical).
2. **Download** — fetch the bytes for each parcel that is `InBoxReady`.
3. **Confirm** — call the confirm endpoint for every parcel you successfully save. Without confirmation ECGrid will re-deliver the file.
4. **Process** — parse and route the EDI content in your application.
5. **Upload** — when your application has outbound EDI to send, upload it to ECGrid for delivery.

```
Poll inbox  →  Download parcel  →  Confirm download  →  Process EDI
                                                              ↓
                                                       Upload outbound
```

## REST vs. SOAP — Quick Comparison

| Concern | REST | SOAP |
|---|---|---|
| Auth | `X-API-Key` header or Bearer JWT | `SessionID` first parameter |
| Payload format | JSON (request/response) | XML envelope |
| File bytes | Base64-encoded JSON field | Base64-encoded XML element |
| Recommended for new work | Yes | No — maintenance mode only |

See [REST vs. SOAP Guide](../getting-started/rest-vs-soap) for a full comparison.

## Prerequisites

- An active ECGrid API key (REST) or valid session obtained from `Login()` (SOAP).
- Your **NetworkID** and **MailboxID** — found in the ECGrid portal or returned by the `GetMe` / `WhoAmI` endpoints.
- For outbound sends: the trading partner's **ECGridID** or ISA qualifier/ID pair.

:::tip Getting Your IDs
Call `GET /v2/users/me` (REST) or `WhoAmI(sessionID)` (SOAP) to retrieve your NetworkID, MailboxID, and ECGridID in one call.
:::
