---
title: Introduction
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create portal landing page intro - Greg Kolinski */}

# ECGrid Developer Documentation Portal

Welcome to the ECGrid Developer Documentation Portal. This site is the authoritative reference for integrating with **ECGrid** — Loren Data Corp's B2B EDI value-added network (VAN) — using either the modern REST API or the established SOAP API.

## What is ECGrid?

ECGrid is Loren Data Corp's production EDI platform, routing hundreds of millions of EDI interchanges between trading partners across every major industry. Whether you are onboarding a new trading partner, automating file pickup and delivery, or building a full EDI workflow into your application, ECGrid provides the infrastructure and APIs to do it reliably.

## Choosing Your API

ECGrid exposes two integration surfaces:

| | REST API v2.6 | ECGridOS SOAP API v4.1 |
|---|---|---|
| **Status** | Active — recommended for all new work | Established — maintenance mode only |
| **Protocol** | HTTPS + JSON | HTTPS + XML (SOAP 1.1) |
| **Authentication** | `X-API-Key` header or `Bearer` JWT | `SessionID` parameter (from `Login()`) |
| **Base URL** | `https://rest.ecgrid.io` | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| **Best for** | New integrations, modern apps, automation | Existing SOAP clients, established integrations |

:::tip New integrations
If you are starting a new project, use the **REST API**. It is actively developed, returns clean JSON, and supports both API key and JWT authentication. See the [REST Quick Start](./getting-started/quick-start-rest.md) to make your first call in minutes.
:::

:::caution Existing SOAP integrations
The SOAP API (`ECGridOS v4.1`) remains fully operational but receives only critical bug fixes. Loren Data recommends migrating new feature work to REST. See the [SOAP Quick Start](./getting-started/quick-start-soap.md) if you must use SOAP.
:::

## Authentication at a Glance

**REST API — two options:**

```http
# Option 1: API Key (recommended for server-to-server)
X-API-Key: your-api-key-here

# Option 2: Bearer JWT (obtained via POST /v2/auth/login)
Authorization: Bearer eyJhbGci...
```

**SOAP API — session token:**

Every SOAP method takes a `SessionID` as its first parameter. Obtain one by calling `Login()` and pass it to all subsequent calls. Always call `Logout()` when finished.

## Where to Go Next

| Goal | Start here |
|---|---|
| Understand the platform and key concepts | [Platform Overview](./getting-started/platform-overview.md) |
| Get an API key and authenticate | [Authentication & API Keys](./getting-started/authentication-api-keys.md) |
| Make your first REST API call | [Quick Start — REST API](./getting-started/quick-start-rest.md) |
| Connect via SOAP | [Quick Start — SOAP API](./getting-started/quick-start-soap.md) |
| Browse all REST endpoints | [REST API Reference](./rest-api/overview.md) |
| Browse all SOAP methods | [SOAP API Reference](./soap-api/overview.md) |
| See end-to-end workflow examples | [Common Operations](./common-operations/overview.md) |
| Download .NET 10 sample projects | [Code Samples](./code-samples/overview.md) |

## API Coverage

The REST API v2.6 covers **121 endpoints** across 16 resource groups: Auth, Networks, Mailboxes, IDs, Partners, Parcels, Interchanges, Callbacks, Carbon Copies, Certificates, Comms, Users, Keys, Portals, Reports, and Status Lists.

The SOAP API v4.1 provides equivalent coverage across the same resource areas, with the exception of Portals (REST only).
