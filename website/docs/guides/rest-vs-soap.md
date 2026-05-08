---
title: REST vs SOAP — Choosing the Right API
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created REST vs SOAP comparison guide - Greg Kolinski */}

# REST vs SOAP — Choosing the Right API

ECGrid exposes two APIs covering the same EDI platform. This guide helps you decide which one to use for your integration.

## At a Glance

| Feature | REST API (v2.6) | SOAP API (v4.1) |
|---|---|---|
| Status | **Active** | Established |
| Protocol | HTTPS + JSON | HTTPS + XML |
| Authentication | API Key (`X-API-Key` header) or Bearer JWT | `SessionID` string from `Login()` or API Key |
| Client generation | Any HTTP client or OpenAPI code generator | `dotnet-svcutil` or manual `HttpClient` |
| Endpoint count | 121 endpoints across 16 resource groups | ~242 methods across comparable groups |
| Error format | JSON `ApiErrorResponse` | SOAP Fault + `ECGridOSSOAPErrorCode` |
| New features | Yes — actively developed | No — Critical only |
| OpenAPI / Swagger | Yes — `https://rest.ecgrid.io/swagger/v2/swagger.json` | No |
| Response format | JSON | XML |

## Use the REST API When…

- Starting a new integration from scratch
- Building a web application, mobile app, or microservice
- You want standard HTTP tooling (Postman, curl, OpenAPI generators)
- You need access to newer capabilities (Portals, enhanced reporting, etc.)
- You want predictable JSON error responses and HTTP status codes

## Use the SOAP API When…

- You have an **existing SOAP integration** and the cost of migration outweighs the benefit
- Your workflow depends on a specific established SOAP method that has no direct REST equivalent
- You are in a regulated environment that has already certified against the SOAP interface and cannot change

## Feature Parity Overview

The two APIs cover the same core resources. The table below maps top-level resource groups.

| Resource | REST | SOAP | Notes |
|---|---|---|---|
| Auth / Sessions | `POST /v2/auth/login` | `Login()` | Different auth model — see below |
| Networks | `/v2/networks` | `NetworkInfo()`, etc. | Full parity |
| Mailboxes | `/v2/mailboxes` | `MailboxInfo()`, etc. | Full parity |
| IDs (Trading Partners) | `/v2/ids` | `TPInfo()`, etc. | Full parity |
| Partners (Interconnects) | `/v2/partners` | `InterconnectXxx()` | Full parity |
| Parcels | `/v2/parcels` | `ParcelXxx()` | Full parity |
| Interchanges | `/v2/interchanges` | `InterchangeXxx()` | Full parity |
| Callbacks | `/v2/callbacks` | `CallBackXxx()` | Full parity |
| Carbon Copies | `/v2/carbon-copies` | `CarbonCopyXxx()` | Full parity |
| Certificates | `/v2/certificates` | `CertificateXxx()` | Full parity |
| Comms | `/v2/comms` | `CommXxx()` | Full parity |
| Users | `/v2/users` | `UserXxx()` | Full parity |
| Keys | `/v2/keys` | `KeyXxx()` | Full parity |
| Portals | `/v2/portals` | — | **REST only** |
| Reports | `/v2/reports` | `ReportXxx()` | Full parity |
| Status Lists | `/v2/status-lists` | `StatusList()` | Full parity |

## Authentication Differences

REST and SOAP use fundamentally different authentication models.

**REST** uses a stateless, header-based approach:

```http
X-API-Key: your-api-key-here
```

Or a short-lived JWT obtained from `POST /v2/auth/login`:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**SOAP** uses a stateful session token:

```csharp
// Every SOAP method takes a SessionID as its first parameter
var parcelList = await client.ParcelInBoxAsync(sessionID, mailboxID, ...);
```

Sessions must be explicitly created (`Login()`) and destroyed (`Logout()`). They expire after inactivity.

See [Authentication & Session Management](./authentication-session-management.md) for a full deep-dive.

## Migrating from SOAP to REST

If you have an existing SOAP integration and want to move to REST, see the [Migration Guide](./migrating-soap-to-rest.md). It includes a method mapping table and before/after C# examples.

## Related

- [Authentication & Session Management](./authentication-session-management.md)
- [Connecting via SOAP](./connecting-via-soap.md)
- [Migrating from SOAP to REST](./migrating-soap-to-rest.md)
- [REST API Overview](../rest-api/overview.md)
- [SOAP API Overview](../soap-api/overview.md)
