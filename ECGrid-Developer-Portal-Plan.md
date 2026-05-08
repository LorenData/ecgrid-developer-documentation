# ECGrid Developer Portal — Site Plan & Structure

## Overview

A unified developer documentation site covering the ECGrid REST API (v2.6, active) and
ECGridOS SOAP API (v4.1, legacy). Built with Docusaurus, hosted on GitHub Pages under
the LorenData GitHub organization.

**Repository:** `LorenData/ecgrid-developer-portal`
**Target URL:** `(https://developerdocs.ecgrid.com)`
**Stack:** Docusaurus 3, GitHub Pages, GitHub Actions for deploy

---

## Source References

| Asset | URL |
|---|---|
| SOAP Service | https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx |
| WSDL | https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL |
| REST Base URL | https://rest.ecgrid.io |
| Swagger JSON | https://rest.ecgrid.io/swagger/v2/swagger.json |
| Swagger UI | https://rest.ecgrid.io/swagger/index.html |
| Existing GitHub Repo | https://github.com/LorenData/ECGrid-API |
| Existing Wiki | https://github.com/LorenData/ECGrid-API/wiki |

---

## Repository Layout

```
ecgrid-developer-portal/
├── website/                        ← Docusaurus site root
│   ├── docs/                       ← All markdown content (~244 files)
│   ├── static/                     ← Images, logos, favicon
│   ├── src/
│   │   └── css/custom.css
│   ├── docusaurus.config.js
│   └── sidebars.js
├── samples/                        ← .NET 10 source code examples
│   ├── README.md
│   ├── rest/
│   │   ├── ECGrid-REST-dotnet10-Console/
│   │   ├── ECGrid-REST-dotnet10-AspNetCore-MVC/
│   │   ├── ECGrid-REST-dotnet10-WorkerService/
│   │   └── ECGrid-REST-dotnet10-MinimalAPI/
│   └── soap/
│       ├── ECGrid-SOAP-dotnet10-Console-HttpClient/
│       └── ECGrid-SOAP-dotnet10-Console-SvcUtil/
└── README.md
```

---

## SOAP Client Library Options

| Library | Notes |
|---|---|
| `dotnet-svcutil` | MS built-in WSDL proxy generator. Generates typed C# client. Best practice for modern .NET. |
| CoreWCF | Open source WCF replacement for .NET 6+. Full WCF compatibility. |
| SoapCore | Lightweight SOAP middleware for ASP.NET Core. |
| Manual HttpClient | Raw SOAP envelope via `HttpClient`. Most control, shown in samples. |

---

## Authentication

**REST:** API Key (`X-API-Key` header) or JWT Bearer token (`Authorization: Bearer <token>`)
**SOAP:** SessionID returned from `Login()` or User APIKey passed to every subsequent method 

---

## REST API Endpoint Count: 121 endpoints across 16 tags (v2.6)

| Tag | Count |
|---|---|
| Auth | 6 |
| Callbacks | 8 |
| CarbonCopies | 5 |
| Certificates | 5 |
| Comms | 8 |
| IDs | 13 |
| Interchanges | 8 |
| Keys | 4 |
| Mailboxes | 7 |
| Networks | 6 |
| Parcels | 15 |
| Partners | 7 |
| Portals | 2 |
| Reports | 8 |
| StatusLists | 1 |
| Users | 16 |
| **Total** | **121** |

---

## Full Site Navigation / Sidebar Menu

```
Getting Started
  Platform Overview
  Authentication & API Keys
  Quick Start — REST
  Quick Start — SOAP

Guides
  REST vs SOAP — Which to Use
  Authentication & Session Management
  Connecting via SOAP
  Error Handling & Troubleshooting
  Migrating SOAP to REST

REST API  (v2.6 — Active)
  Overview
  Auth
  Networks
  Mailboxes
  IDs
  Partners
  Parcels
  Interchanges
  Callbacks & Webhooks
  Carbon Copies
  Certificates
  Comms
  Users
  Keys
  Portals
  Reports
  Status Lists

SOAP API  (v4.1 — Legacy)
  Overview
  Auth & Sessions
  Networks
  Mailboxes
  IDs
  Partners
  Parcels
  Interchanges
  Callbacks & Webhooks
  Carbon Copies
  Certificates
  Comms
  Users
  Keys
  Reports

Common Operations
  Overview
  Poll for Inbound Files
  Download a File
  Confirm a Download
  Upload a File
  Send EDI to a Trading Partner
  Create a Mailbox
  Onboard a Trading Partner
  Set Up an Interconnect
  Configure Callbacks & Webhooks
  Manage Users & Permissions
  Work with Carbon Copies

Appendix
  Interchange Status Codes
  Parcel Status Codes
  ENUMs
  Error Codes

Code Samples
  Overview
  REST — .NET 10 Console
  REST — .NET 10 ASP.NET Core MVC
  REST — .NET 10 Worker Service
  REST — .NET 10 Minimal API
  SOAP — .NET 10 HttpClient
  SOAP — .NET 10 dotnet-svcutil

Changelog
  REST API Changelog
  SOAP Revision History
```

---

## Complete docs/ File Tree

### Getting Started (5 files)
- docs/intro.md
- docs/getting-started/_category_.json
- docs/getting-started/platform-overview.md
- docs/getting-started/authentication-api-keys.md
- docs/getting-started/quick-start-rest.md
- docs/getting-started/quick-start-soap.md

### Guides (6 files)
- docs/guides/_category_.json
- docs/guides/rest-vs-soap.md
- docs/guides/authentication-session-management.md
- docs/guides/connecting-via-soap.md
- docs/guides/error-handling-troubleshooting.md
- docs/guides/migrating-soap-to-rest.md

### REST API (122 files — 1 overview + 121 endpoints)
- docs/rest-api/_category_.json + overview.md
- docs/rest-api/auth/ — 6 files
- docs/rest-api/networks/ — 6 files
- docs/rest-api/mailboxes/ — 7 files
- docs/rest-api/ids/ — 13 files
- docs/rest-api/partners/ — 7 files
- docs/rest-api/parcels/ — 15 files
- docs/rest-api/interchanges/ — 8 files
- docs/rest-api/callbacks/ — 8 files
- docs/rest-api/carbon-copies/ — 5 files
- docs/rest-api/certificates/ — 5 files
- docs/rest-api/comms/ — 8 files
- docs/rest-api/users/ — 16 files
- docs/rest-api/keys/ — 4 files
- docs/rest-api/portals/ — 2 files
- docs/rest-api/reports/ — 8 files
- docs/rest-api/status-lists/ — 1 file

### SOAP API (~86 files)
- docs/soap-api/_category_.json + overview.md
- docs/soap-api/auth/ — 6 files
- docs/soap-api/networks/ — 8 files
- docs/soap-api/mailboxes/ — 9 files
- docs/soap-api/ids/ — 9 files
- docs/soap-api/partners/ — 8 files (InterconnectXxx methods)
- docs/soap-api/parcels/ — 8 files (Ex variants collapsed)
- docs/soap-api/interchanges/ — 7 files (Ex variants collapsed)
- docs/soap-api/callbacks/ — 7 files
- docs/soap-api/carbon-copies/ — 6 files
- docs/soap-api/certificates/ — 5 files
- docs/soap-api/comms/ — 8 files
- docs/soap-api/users/ — 10 files
- docs/soap-api/keys/ — 5 files
- docs/soap-api/reports/ — 5 files
- NOTE: Migrations section removed (deprecated)

### Common Operations (13 files)
- docs/common-operations/_category_.json + overview.md + 11 task pages

### Appendix (5 files)
- docs/appendix/_category_.json
- docs/appendix/interchange-status-codes.md
- docs/appendix/parcel-status-codes.md
- docs/appendix/enums.md
- docs/appendix/error-codes.md

### Code Samples (8 files)
- docs/code-samples/_category_.json + overview.md + 6 sample pages

### Changelog (3 files)
- docs/changelog/_category_.json
- docs/changelog/rest-changelog.md
- docs/changelog/soap-revision-history.md

---

## Per-Page Template Pattern (Stripe-style)

Each REST and SOAP reference page follows:

1. Endpoint / Method Name + one-line description
2. REST Endpoint OR SOAP Method signature
3. Request parameters table (name, type, required, description, validation)
4. Request object JSON/XML example
5. Response object table (field, type, description)
6. Response example
7. ENUMs used (with values)
8. C# code example (.NET 10)

---

## REST vs SOAP Section Alignment

| REST Section | SOAP Section | Notes |
|---|---|---|
| Auth | Auth & Sessions | Different auth model |
| Networks | Networks | Full parity |
| Mailboxes | Mailboxes | Full parity |
| IDs | IDs | Full parity |
| Partners | Partners | REST=Partners tag, SOAP=InterconnectXxx |
| Parcels | Parcels | REST 15 endpoints, SOAP 8 collapsed |
| Interchanges | Interchanges | Full parity |
| Callbacks & Webhooks | Callbacks & Webhooks | Full parity |
| Carbon Copies | Carbon Copies | Full parity |
| Certificates | Certificates | Full parity |
| Comms | Comms | Full parity |
| Users | Users | REST 16 endpoints, SOAP 10 collapsed |
| Keys | Keys | Full parity |
| Portals | (REST only) | New capability, no SOAP equivalent |
| Reports | Reports | Full parity |
| Status Lists | (Appendix only) | REST has live endpoint |
| (future) | Migrations removed | Deprecated, not documented |

---

## Build Phases

- **Phase 1** — Docusaurus scaffold: config, sidebars, intro, template pages
- **Phase 2** — Full REST API reference (121 endpoints from Swagger JSON)
- **Phase 3** — Full SOAP API reference (~85 pages from WSDL)
- **Phase 4** — Common Operations, Guides, Getting Started, Appendix
- **Phase 5** — Code Samples (.NET 10), custom domain DNS, GitHub Actions deploy

---

## Docusaurus Setup Notes

- Plugin needed: `docusaurus-plugin-openapi-docs` for native OpenAPI rendering
- Theme: `@docusaurus/theme-classic` with custom ECGrid brand colors
- GitHub Actions workflow: build on push to main, deploy to `gh-pages` branch
- Custom domain: CNAME record pointing `developers.ecgrid.com` to `lorendata.github.io`

---

## Change Log

| Date | Change |
|---|---|
| 2026-05-07 | Initial plan created. Migrations removed from SOAP (deprecated). |
