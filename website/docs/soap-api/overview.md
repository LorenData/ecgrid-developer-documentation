---
title: SOAP API Overview
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API overview page - Greg Kolinski */}

# SOAP API Overview

The ECGridOS SOAP API (v4.1) is a established API in maintenance mode — it receives critical security fixes only and will not gain new features.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations, use the [REST API](../rest-api/overview.md) instead.
:::

## Service Endpoint

| Resource | URL |
|---|---|
| Service | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| WSDL | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL` |
| Namespace | `http://www.ecgridos.net/` |

## Client Options

Choose a client strategy based on your project context.

| Library | Use Case |
|---|---|
| `dotnet-svcutil` | Recommended for new .NET 10 projects. Generates a typed proxy from the WSDL. |
| CoreWCF | Migrating existing WCF `.NET Framework` code to .NET 10. |
| Manual `HttpClient` | Minimal dependencies, full control over the raw SOAP envelope. |

### Generate a Typed Proxy with dotnet-svcutil

```bash
dotnet tool install --global dotnet-svcutil
dotnet-svcutil https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL
```

This generates `Reference.cs` containing the `ECGridOSClient` class and all data contract types. Add the generated file to your project and reference the `ServiceReference1` namespace (or rename as needed).

## Authentication

The SOAP API uses session-based authentication.

1. Call `Login()` with your credentials — it returns a `SessionID` string.
2. Pass that `SessionID` as the **first parameter** of every subsequent method call.
3. Call `Logout()` when the session is no longer needed.

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSClient(binding, endpoint);

string sessionID = await client.LoginAsync(
    userName, password,
    "MyApp", "1.0", "My Company", "Dev Name", "dev@example.com");

// Use sessionID for all subsequent calls...

await client.LogoutAsync(sessionID);
```

Sessions expire automatically after a period of inactivity. Always call `Logout()` in a `finally` block to release server-side resources.

## API Section Coverage

| Section | Methods | Notes |
|---|---|---|
| [Auth & Sessions](./auth/login.md) | 6 | Login, Logout, WhoAmI, SessionInfo, SessionLog, Version |
| [Networks](./networks/network-info.md) | 8 | NetworkInfo, NetworkList, NetworkAdd, NetworkUpdate, NetworkSetStatus, NetworkGateway, NetworkVPN, NetworkStatusSummary |
| [Mailboxes](./mailboxes/mailbox-info.md) | 9 | MailboxInfo, MailboxList, MailboxAdd, MailboxConfig, MailboxDescription, MailboxDeleteOnDownload, MailboxInboxTimeout, MailboxX12Delimiters, MailboxManaged |
| [IDs](./ids/ecgrid-id-info.md) | 9 | ECGridIDInfo, TPInfo, TPList, TPAdd, TPSearch, TPMove, TPAddVAN, TPUpdateDescription, TPUpdateDataEmail |
| [Partners](./partners/interconnect-info.md) | 7 | InterconnectInfo, InterconnectAdd, InterconnectListByStatus, InterconnectListByECGridID, InterconnectUpdate, InterconnectCancel, InterconnectCount, InterconnectNote |
| [Parcels](./parcels/parcel-inbox.md) | 8 | ParcelInbox, ParcelOutbox, ParcelUpload, ParcelDownload, ParcelDownloadConfirm, ParcelInfo, ParcelNote, ParcelResend |
| [Interchanges](./interchanges/interchange-inbox.md) | 7 | InterchangeInbox, InterchangeOutbox, InterchangeInfo, InterchangeManifest, InterchangeHeaderInfo, InterchangeResend, InterchangeCancel |
| [Callbacks](./callbacks/callback-add.md) | 7 | CallBackAdd, CallBackEventInfo, CallBackEventList, CallBackPendingList, CallBackFailedList, CallBackQueueInfo, CallBackTest |
| [Carbon Copies](./carbon-copies/carbon-copy-add.md) | 6 | CarbonCopyAdd, CarbonCopyInfo, CarbonCopyList, CarbonCopyActivate, CarbonCopySuspend, CarbonCopyTerminate |
| [Certificates](./certificates/certificate-add-public.md) | 5 | CertificateAddPublic, CertificateAddPrivate, CertificateCreatePrivate, CertificateRenewPrivate, CertificateTerminate |
| [Comms](./comms/comm-info.md) | 8 | CommInfo, CommList, CommFind, CommAdd, CommUpdate, CommPair, CommSetPair, CommDefaultMailbox |
| [Users](./users/user-info.md) | 10 | UserInfo, UserList, UserAdd, UserUpdate, UserSetAuthLevel, UserGetAPIKey, UserPassword, UserReset, UserSuspend, UserTerminate |
| [Keys](./keys/key-get.md) | 5 | KeyGet, KeySet, KeyList, KeyRemove, GenerateAPIKey |
| [Reports](./reports/report-instant-stats.md) | 5 | ReportInstantStats, ReportInterchangeStats, ReportMailboxStats, ReportTrafficStats, ReportMonthly |

## For New Integrations

Use the [REST API](../rest-api/overview.md), which offers:

- API Key and JWT Bearer authentication — no session management required
- JSON request/response bodies
- Standard HTTP status codes
- 121 endpoints across 16 resource groups (v2.6)

See the [REST vs SOAP guide](../guides/rest-vs-soap.md) for a full comparison.
