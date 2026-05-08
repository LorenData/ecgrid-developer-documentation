---
title: REST API Changelog
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created REST API changelog page - Greg Kolinski */}

# REST API Changelog

Version history for the ECGrid REST API. The current active version is **v2.6**.

:::info Authoritative Source
This changelog reflects known version information at the time of documentation. For the definitive and up-to-date version history, refer to the live Swagger UI at [rest.ecgrid.io/swagger](https://rest.ecgrid.io/swagger/index.html).
:::

---

## v2.6 — Current Release

**Status:** Active  
**Base URL:** `https://rest.ecgrid.io/v2`

### Summary

v2.6 is the current production release of the ECGrid REST API. It provides 121 endpoints across 16 resource tags.

### What's Included

| Tag | Endpoint Count | Notes |
|---|---|---|
| Auth | 6 | Login, logout, refresh token, session info, password change, version |
| Networks | 6 | Get, list, update network; get contact, update config, X12 delimiters |
| Mailboxes | 7 | Get, create, list, update mailbox; update config, X12 delimiters, delete |
| IDs | 13 | Full ECGrid ID management including TP move, VAN add, data email |
| Partners | 7 | Interconnect management with notes support |
| Parcels | 15 | Full parcel lifecycle: upload, download, confirm, inbox/outbox, cancel, resend, manifest |
| Interchanges | 8 | Interchange query, cancel, resend, manifest, header info |
| Callbacks | 8 | Webhook management, event queuing, test endpoint |
| CarbonCopies | 5 | CC routing rules: create, read, update, delete |
| Certificates | 5 | X.509, PGP, and SSH certificate management |
| Comms | 8 | Communication channel configuration and pairing |
| Users | 16 | Full user lifecycle: create, update, terminate, roles, SMS, API key management |
| Keys | 4 | API key management |
| Portals | 2 | Portal provisioning per mailbox |
| Reports | 8 | Interchange stats, mailbox stats, traffic reports, monthly reports |
| StatusLists | 1 | Live status list retrieval (`GET /v2/status-lists`) |

### Notable Additions in v2.6

- **Portals tag** — New capability for provisioning and managing mailbox portals. No SOAP equivalent.
- **StatusLists endpoint** — Live `GET /v2/status-lists` for retrieving current system status lists.
- **Extended Users tag** — 16 endpoints including SMS send, set network/mailbox, generate password, and per-user session reset.

---

## v2.x Series

**Status:** Active development branch  
**Versioning policy:** Breaking changes are introduced only with a major version bump (e.g., v2.x → v3.0). Non-breaking additions (new endpoints, optional fields) may be introduced in minor versions without a version bump in the URL path.

### Backward Compatibility Commitment

- Existing endpoints will not have request or response fields removed within the v2 series.
- New optional fields may be added to request or response bodies at any time.
- Deprecated endpoints will be marked with a notice in the Swagger UI before removal.

---

## Migration from SOAP

If you are moving from the ECGridOS SOAP API (v4.1) to the REST API, see the [Migrating SOAP to REST](../getting-started/migrating-soap-to-rest) guide for a method-by-method mapping.

---

## See Also

- [REST API Overview](../rest-api/overview)
- [SOAP API Revision History](./soap-revision-history)
- [Live Swagger UI](https://rest.ecgrid.io/swagger/index.html)
