---
title: SOAP API Revision History
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API revision history page - Greg Kolinski */}

# SOAP API Revision History

Version history for the ECGridOS SOAP API. The current maintenance release is **v4.1**.

:::caution Established API
The SOAP API is in maintenance mode. No new features are planned. Only security patches and critical bug fixes will be applied. For new integrations, use the [ECGrid REST API](../rest-api/overview) instead. See the [migration guide](../guides/migrating-soap-to-rest) for assistance moving existing integrations.
:::

---

## v4.1 — Current Maintenance Release

**Status:** Maintenance mode (security patches only)  
**Endpoint:** `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx`  
**WSDL:** `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL`

### Summary

v4.1 is the current and final feature release of the ECGridOS SOAP API. It supports the full ECGrid feature set that was available at the time of the v4.1 release, covering authentication, networks, mailboxes, IDs, partners, parcels, interchanges, callbacks, carbon copies, certificates, communications channels, users, keys, and reports.

### What's Included

| Category | Key Methods |
|---|---|
| Auth | `Login`, `Logout`, `WhoAmI`, `SessionInfo`, `SessionLog`, `Version` |
| Networks | `NetworkInfo`, `NetworkList`, `NetworkAdd`, `NetworkUpdate`, `NetworkSetStatus`, `NetworkGateway`, `NetworkVPN`, `NetworkStatusSummary` |
| Mailboxes | `MailboxInfo`, `MailboxList`, `MailboxAdd`, `MailboxConfig`, `MailboxDescription`, `MailboxDeleteOnDownload`, `MailboxInboxTimeout`, `MailboxX12Delimiters`, `MailboxManaged` |
| IDs | `ECGridIDInfo`, `TPInfo`, `TPList`, `TPAdd`, `TPSearch`, `TPMove`, `TPAddVAN`, `TPUpdateDescription`, `TPUpdateDataEmail` |
| Partners | `InterconnectInfo`, `InterconnectAdd`, `InterconnectListByStatus`, `InterconnectListByECGridID`, `InterconnectUpdate`, `InterconnectCancel`, `InterconnectCount`, `InterconnectNote` |
| Parcels | `ParcelInbox`, `ParcelOutbox`, `ParcelUpload`, `ParcelDownload`, `ParcelDownloadConfirm`, `ParcelInfo`, `ParcelNote`, `ParcelResend` |
| Interchanges | `InterchangeInbox`, `InterchangeOutbox`, `InterchangeInfo`, `InterchangeManifest`, `InterchangeHeaderInfo`, `InterchangeResend`, `InterchangeCancel` |
| Callbacks | `CallBackAdd`, `CallBackEventInfo`, `CallBackEventList`, `CallBackPendingList`, `CallBackFailedList`, `CallBackQueueInfo`, `CallBackTest` |
| Carbon Copies | `CarbonCopyAdd`, `CarbonCopyInfo`, `CarbonCopyList`, `CarbonCopyActivate`, `CarbonCopySuspend`, `CarbonCopyTerminate` |
| Certificates | `CertificateAddPublic`, `CertificateAddPrivate`, `CertificateCreatePrivate`, `CertificateRenewPrivate`, `CertificateTerminate` |
| Comms | `CommInfo`, `CommList`, `CommFind`, `CommAdd`, `CommUpdate`, `CommPair`, `CommSetPair`, `CommDefaultMailbox` |
| Users | `UserInfo`, `UserList`, `UserAdd`, `UserUpdate`, `UserSetAuthLevel`, `UserGetAPIKey`, `UserPassword`, `UserReset`, `UserSuspend`, `UserTerminate` |
| Keys | `KeyGet`, `KeySet`, `KeyList`, `KeyRemove`, `GenerateAPIKey` |
| Reports | `ReportInstantStats`, `ReportInterchangeStats`, `ReportMailboxStats`, `ReportTrafficStats`, `ReportMonthly` |

---

## v4.0 → v4.1

**Change type:** Minor — no breaking changes.

Key changes from v4.0 to v4.1:

- Minor parameter additions to several methods (additional optional parameters appended to method signatures).
- Extended `Ex` and `ExA` method variants added for select operations to provide additional filtering and pagination options without replacing the base methods.
- Bug fixes and stability improvements.
- No methods were removed in this release.

---

## Maintenance Mode Policy

As of v4.1, the SOAP API is subject to the following maintenance policy:

| Change Type | Will Be Applied? |
|---|---|
| Security patches | Yes |
| Critical bug fixes | Yes, case-by-case |
| New methods or parameters | No |
| New resource types (e.g., Portals) | No — REST only |
| Breaking changes | No |

---

## REST API Equivalent

The ECGrid REST API (v2.6) covers all functionality available in ECGridOS SOAP v4.1, plus additional capabilities not available in SOAP (notably the Portals resource and enhanced reporting).

| SOAP API | REST API |
|---|---|
| ECGridOS v4.1 (maintenance) | REST v2.6 (active) |
| Session-based auth via `Login()` | API key or JWT Bearer token |
| XML SOAP envelope | JSON over HTTPS |
| WSDL-defined schema | OpenAPI 3.0 Swagger |

See the [Migrating SOAP to REST](../guides/migrating-soap-to-rest) guide for a full method-to-endpoint mapping and C# migration examples.

---

## See Also

- [SOAP API Overview](../soap-api/overview)
- [REST API Changelog](./rest-changelog)
- [Migrating SOAP to REST](../guides/migrating-soap-to-rest)
- [REST vs SOAP Guide](../guides/rest-vs-soap)
