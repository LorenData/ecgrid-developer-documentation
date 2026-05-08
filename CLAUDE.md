# Claude Code Instructions — ecgrid-developer-portal

## Project Context

This repo is the ECGrid Developer Documentation Portal — a unified public-facing documentation site covering the ECGrid REST API (v2.6, active) and ECGridOS SOAP API (v4.1, legacy). It is built with Docusaurus 3 and hosted on GitHub Pages under the LorenData GitHub organization. The repo also contains .NET sample projects for REST and SOAP integration under `/samples`.

---

## Stack

- **Docs site:** Docusaurus 3 (Node.js, TypeScript config)
- **OpenAPI plugin:** `docusaurus-plugin-openapi-docs` for native REST endpoint rendering
- **Samples language:** C# (.NET 10) existing sample and source from GitHub for SOAP
- **Sample frameworks:** Console, ASP.NET Core Web API (Minimal API + MVC), Worker Service
- **SOAP client:** `dotnet-svcutil` generated proxy or manual `HttpClient`
- **Hosting:** GitHub Pages (`gh-pages` branch) via GitHub Actions
- **No database, no Entity Framework, no SQL**

---

## Repo Structure

```
ecgrid-developer-portal/
├── CLAUDE.md                          ← This file
├── README.md
├── website/                           ← Docusaurus 3 site
│   ├── docs/                          ← All markdown content (~244 files)
│   │   ├── intro.md
│   │   ├── getting-started/
│   │   ├── guides/
│   │   ├── rest-api/
│   │   ├── soap-api/
│   │   ├── common-operations/
│   │   ├── appendix/
│   │   ├── code-samples/
│   │   └── changelog/
│   ├── static/
│   ├── src/css/custom.css
│   ├── docusaurus.config.ts
│   └── sidebars.ts
└── samples/
    ├── README.md
    ├── rest/
    │   ├── ECGrid-REST-dotnet10-Console/
    │   ├── ECGrid-REST-dotnet10-AspNetCore-MVC/
    │   ├── ECGrid-REST-dotnet10-WorkerService/
    │   └── ECGrid-REST-dotnet10-MinimalAPI/
    └── soap/
        ├── ECGrid-SOAP-dotnet10-Console-HttpClient/
        └── ECGrid-SOAP-dotnet10-Console-SvcUtil/
```

---

## Source Data — Always Fetch Live

Do not hardcode API shapes from memory. Always fetch these live sources when generating docs:

| Asset | URL |
|---|---|
| REST Swagger JSON | `https://rest.ecgrid.io/swagger/v2/swagger.json` |
| REST Swagger UI | `https://rest.ecgrid.io/swagger/index.html` |
| SOAP Service | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx` |
| WSDL | `https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL` |
| Existing Wiki | `https://github.com/LorenData/ECGrid-API/wiki` |
| Existing Repo | `https://github.com/LorenData/ECGrid-API` |

---

## Site Navigation — Full Structure

This is the canonical nav. Generate docs in this exact order and structure.

```
Getting Started                          position: 1
  platform-overview.md
  authentication-api-keys.md
  quick-start-rest.md
  quick-start-soap.md

Guides                                   position: 2
  rest-vs-soap.md
  authentication-session-management.md
  connecting-via-soap.md
  error-handling-troubleshooting.md
  migrating-soap-to-rest.md

REST API  (v2.6 — Active)                position: 3
  overview.md
  auth/
    login.md
    refresh-token.md
    logout.md
    session.md
    change-password.md
    version.md
  networks/
    get-network.md
    list-networks.md
    update-network.md
    get-contact.md
    update-config.md
    x12-delimiters.md
  mailboxes/
    get-mailbox.md
    create-mailbox.md
    list-mailboxes.md
    update-mailbox.md
    update-config.md
    x12-delimiters.md
    delete-mailbox.md
  ids/
    get-id.md
    create-id.md
    update-id.md
    delete-id.md
    find-id.md
    list-ids.md
    update-config.md
    add-van.md
    get-mailbox-default.md
    move-tp.md
    update-data-email.md
    update-description.md
    x12-delimiters.md
  partners/
    get-partner.md
    create-partner.md
    delete-partner.md
    count-partners.md
    list-partners.md
    add-note.md
    list-notes.md
  parcels/
    get-parcel.md
    upload-parcel.md
    download-parcel.md
    confirm-download.md
    inbox-list.md
    outbox-list.md
    pending-inbox-list.md
    cancel-parcel.md
    reset-to-inbox.md
    get-manifest.md
    update-parcel.md
    set-mailbag-control-id.md
    find-mailbag-control-id.md
    acknowledgment-note.md
    send-test-file.md
  interchanges/
    get-interchange.md
    cancel-interchange.md
    get-manifest.md
    resend-interchange.md
    get-date.md
    get-header.md
    inbox-list.md
    outbox-list.md
  callbacks/
    create-callback.md
    update-callback.md
    delete-callback.md
    get-queue-by-id.md
    event-list.md
    get-event-by-id.md
    queue-list.md
    test-callback.md
  carbon-copies/
    get-carbon-copy.md
    create-carbon-copy.md
    list-carbon-copies.md
    update-carbon-copy.md
    delete-carbon-copy.md
  certificates/
    add-private.md
    add-public.md
    create-certificate.md
    renew-certificate.md
    terminate-certificate.md
  comms/
    get-comm.md
    find-comm.md
    list-comms.md
    comm-pair.md
    set-pair.md
    create-comm.md
    update-comm.md
    update-config.md
  users/
    get-user.md
    create-user.md
    update-user.md
    terminate-user.md
    get-me.md
    get-api-key.md
    generate-api-key.md
    reset-sessions.md
    get-by-name.md
    list-users.md
    update-password.md
    generate-password.md
    set-role.md
    send-sms.md
    set-network-mailbox.md
    update-config.md
  keys/
    get-key.md
    list-keys.md
    create-key.md
    delete-key.md
  portals/
    get-portal-by-mailbox.md
    create-portal.md
  reports/
    mailbox-interchange-stats.md
    mailbox-stats.md
    report-list.md
    report-by-date.md
    instant-stats.md
    interchange-stats.md
    monthly-report.md
    traffic-stats.md
  status-lists/
    get-status-lists.md

SOAP API  (v4.1 — Legacy)               position: 4
  overview.md
  auth/
    login.md
    logout.md
    whoami.md
    session-info.md
    session-log.md
    version.md
  networks/
    network-info.md
    network-list.md
    network-add.md
    network-update.md
    network-set-status.md
    network-gateway.md
    network-vpn.md
    network-status-summary.md
  mailboxes/
    mailbox-info.md
    mailbox-list.md
    mailbox-add.md
    mailbox-config.md
    mailbox-description.md
    mailbox-delete-on-download.md
    mailbox-inbox-timeout.md
    mailbox-x12-delimiters.md
    mailbox-managed.md
  ids/
    ecgrid-id-info.md
    tp-info.md
    tp-list.md
    tp-add.md
    tp-search.md
    tp-move.md
    tp-add-van.md
    tp-update-description.md
    tp-update-data-email.md
  partners/
    interconnect-info.md
    interconnect-add.md
    interconnect-list-by-status.md
    interconnect-list-by-ecgrid-id.md
    interconnect-update.md
    interconnect-cancel.md
    interconnect-count.md
    interconnect-note.md
  parcels/
    parcel-inbox.md
    parcel-outbox.md
    parcel-upload.md
    parcel-download.md
    parcel-download-confirm.md
    parcel-info.md
    parcel-note.md
    parcel-resend.md
  interchanges/
    interchange-inbox.md
    interchange-outbox.md
    interchange-info.md
    interchange-manifest.md
    interchange-header-info.md
    interchange-resend.md
    interchange-cancel.md
  callbacks/
    callback-add.md
    callback-event-info.md
    callback-event-list.md
    callback-pending-list.md
    callback-failed-list.md
    callback-queue-info.md
    callback-test.md
  carbon-copies/
    carbon-copy-add.md
    carbon-copy-info.md
    carbon-copy-list.md
    carbon-copy-activate.md
    carbon-copy-suspend.md
    carbon-copy-terminate.md
  certificates/
    certificate-add-public.md
    certificate-add-private.md
    certificate-create-private.md
    certificate-renew-private.md
    certificate-terminate.md
  comms/
    comm-info.md
    comm-list.md
    comm-find.md
    comm-add.md
    comm-update.md
    comm-pair.md
    comm-set-pair.md
    comm-default-mailbox.md
  users/
    user-info.md
    user-list.md
    user-add.md
    user-update.md
    user-set-auth-level.md
    user-get-api-key.md
    user-password.md
    user-reset.md
    user-suspend.md
    user-terminate.md
  keys/
    key-get.md
    key-set.md
    key-list.md
    key-remove.md
    generate-api-key.md
  reports/
    report-instant-stats.md
    report-interchange-stats.md
    report-mailbox-stats.md
    report-traffic-stats.md
    report-monthly.md

Common Operations                        position: 5
  overview.md
  poll-inbound-files.md
  download-a-file.md
  confirm-download.md
  upload-a-file.md
  send-edi-to-trading-partner.md
  create-a-mailbox.md
  onboard-trading-partner.md
  setup-interconnect.md
  configure-callbacks.md
  manage-users-permissions.md
  work-with-carbon-copies.md

Appendix                                 position: 6
  interchange-status-codes.md
  parcel-status-codes.md
  enums.md
  error-codes.md

Code Samples                             position: 7
  overview.md
  rest-console.md
  rest-aspnet-mvc.md
  rest-worker-service.md
  rest-minimal-api.md
  soap-httpclient.md
  soap-svcutil.md

Changelog                                position: 8
  rest-changelog.md
  soap-revision-history.md
```

---

## REST vs SOAP Section Alignment

SOAP and REST use the same top-level section headings. When both APIs cover the same resource, cross-reference them.

| REST Section | SOAP Section | Notes |
|---|---|---|
| Auth | Auth & Sessions | Different auth model — session vs header |
| Networks | Networks | Full parity |
| Mailboxes | Mailboxes | Full parity |
| IDs | IDs | Full parity |
| Partners | Partners | REST tag = Partners, SOAP methods = InterconnectXxx |
| Parcels | Parcels | REST 15 endpoints, SOAP 8 collapsed pages |
| Interchanges | Interchanges | Full parity |
| Callbacks & Webhooks | Callbacks & Webhooks | Full parity |
| Carbon Copies | Carbon Copies | Full parity |
| Certificates | Certificates | Full parity |
| Comms | Comms | Full parity |
| Users | Users | REST 16 endpoints, SOAP 10 collapsed |
| Keys | Keys | Full parity |
| Portals | (REST only) | New capability, no SOAP equivalent |
| Reports | Reports | Full parity |
| Status Lists | (Appendix only) | REST has live `GET /v2/status-lists` endpoint |
| (future) | Migrations removed | Deprecated — do not document |

---

## Page Templates

### REST Endpoint Page Template

Use this template for every file under `docs/rest-api/**/*.md`.
Pull all field names, types, constraints, and ENUMs directly from the live Swagger JSON.
Do not invent field names or types.

```markdown
---
title: <Human-readable endpoint name>
---

# <Human-readable endpoint name>

<One sentence from the Swagger description tag, or written from context.>

## Endpoint

```http
<METHOD> <path>
```

## Path Parameters  ← omit section if none

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | type | Yes/No | description |

## Query Parameters  ← omit section if none

| Parameter | Type | Default | Description |
|---|---|---|---|

## Request Body  ← omit section if GET/DELETE with no body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `fieldName` | type | Yes/No | constraints | description |

```json
{
  "example": "request body"
}
```

## Response

<One sentence describing what is returned.>

```json
{
  "success": true,
  "data": { }
}
```

## ENUMs  ← include only if request or response uses ENUMs

### <EnumName>

| Value | Description |
|---|---|
| `Value1` | description |

## C# Example

```csharp
// .NET 10 — HttpClient pattern
var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io<path>",
    new { field = value });

var result = await response.Content.ReadFromJsonAsync<ApiResponse>();
```

## See Also  ← omit if no natural cross-references

- [Related page](../path/to/page)
```

---

### SOAP Method Page Template

Use this template for every file under `docs/soap-api/**/*.md`.
Pull all parameter names, types, and return types from the live WSDL `?op=<MethodName>` endpoint.
Where a method has `Ex`, `ExA`, or other suffixed variants, document them all on the same page under separate `### Variant` subheadings rather than separate files.

```markdown
---
title: <Method name>
---

# <Method name>

<One sentence description from the WSDL or ASMX service page.>

:::caution Legacy API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](<relative link>).
:::

## Method Signature

```
<ReturnType> MethodName(string SessionID, type param1, type param2, ...)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `paramName` | type | Yes/No | description |

## Response Object — <ReturnTypeName>

| Field | Type | Description |
|---|---|---|
| `FieldName` | type | description |

```xml
<!-- Example response XML -->
<MethodResult>
  <Field>value</Field>
</MethodResult>
```

## Variants  ← include only if Ex/ExA variants exist

### MethodNameEx

<What differs from the base method.>

| Additional Parameter | Type | Description |
|---|---|---|

## ENUMs  ← include only if method uses ENUMs

## C# Example

```csharp
// .NET 10 — dotnet-svcutil generated proxy
var result = await client.MethodNameAsync(sessionID, param1, param2);
```

## REST Equivalent

See [<REST page name>](<relative link to rest-api section>).
```

---

### Common Operations Page Template

Use this template for every file under `docs/common-operations/*.md`.
Show REST and SOAP paths side by side. Do not repeat full API reference detail — link to it.

```markdown
---
title: <Task name>
---

# <Task name>

<1-2 sentences: what this operation accomplishes and when you'd use it.>

## Overview

<Short explanation of the sequence of calls involved.>

## REST

### Step 1 — <action>

```http
POST /v2/resource/action
```

```json
{ "request": "body" }
```

### Step 2 — <action>

...

### Complete C# Example

```csharp
// .NET 10
```

---

## SOAP

:::caution Legacy API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

### Step 1 — <action>

```csharp
var result = await client.MethodNameAsync(sessionID, params);
```

### Complete C# Example

```csharp
// .NET 10 — full SOAP sequence
```

---

## Related

- [REST reference page](../rest-api/...)
- [SOAP reference page](../soap-api/...)
```

---

## Coding Conventions — C# Samples

- Target framework: `.NET 10` — use `<TargetFramework>net10.0</TargetFramework>`
- Use `HttpClient` with `IHttpClientFactory` for REST calls — never `new HttpClient()` in production code
- Use `System.Text.Json` — never Newtonsoft
- Use `async`/`await` throughout — no `.Result` or `.Wait()`
- Use top-level statements in Console samples to keep them concise
- API key loaded from `IConfiguration` / environment variable — never hardcoded
- All SOAP samples use `dotnet-svcutil` generated proxy OR manual `HttpClient` — no WCF `web.config` patterns
- No Entity Framework, no SQL, no direct database access
- No third-party NuGet packages beyond what is strictly needed for the sample's purpose
- `PascalCase` for class and method names, `camelCase` for local variables
- XML doc comments (`/// <summary>`) on all public methods in sample projects

---

## Docusaurus Configuration Rules

- Use TypeScript config (`docusaurus.config.ts`, `sidebars.ts`) — not JavaScript
- Plugin `docusaurus-plugin-openapi-docs` for the REST API reference
- Theme: `@docusaurus/theme-classic`
- Brand colors from Loren Data palette:
  - Primary: `#005B99` (ECGrid blue)
  - Secondary: `#00AEEF` (ECGrid light blue)
  - Accent: `#F26522` (Loren Data orange)
- `_category_.json` files control sidebar labels and positions — always include them
- Sidebar positions: Getting Started=1, Guides=2, REST API=3, SOAP API=4, Common Operations=5, Appendix=6, Code Samples=7, Changelog=8
- Custom domain target: `developers.ecgrid.com`
- GitHub Actions deploy workflow: build on push to `main`, deploy to `gh-pages` branch

---

## SOAP Connection — Library Guidance

The SOAP docs recommend these client options. Do not recommend others.

| Library | Use Case |
|---|---|
| `dotnet-svcutil` | Recommended for new .NET 10 projects. Generates typed proxy from WSDL. |
| CoreWCF | Migrating existing WCF code to .NET 10. |
| Manual `HttpClient` | Minimal dependencies, full control. Shown in `soap-httpclient` sample. |
| SoapCore | Server-side SOAP middleware — not for consuming ECGridOS. |

---

## Authentication Summary

| API | Method | Header / Pattern |
|---|---|---|
| REST | API Key | `X-API-Key: <key>` |
| REST | JWT Bearer | `Authorization: Bearer <token>` |
| SOAP | Session ID | First param of every method call, obtained from `Login()` |

Password pattern (both APIs): `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

---

## REST API Endpoint Count Reference

121 total endpoints across 16 tags (v2.6). Use the Swagger JSON as the authoritative source.

| Tag | Count | Key Operations |
|---|---|---|
| Auth | 6 | login, logout, refresh, session, password, version |
| Networks | 6 | get, list, update, get-contact, update-config, x12-delimiters |
| Mailboxes | 7 | get, create, list, update, update-config, x12-delimiters, delete |
| IDs | 13 | get, create, update, delete, find, list, update-config, add-van, get-mailbox-default, tp-move, update-data-email, update-description, x12-delimiters |
| Partners | 7 | get, create, delete, count, list, add-note, list-notes |
| Parcels | 15 | get, upload, download, confirm, inbox-list, outbox-list, pending-inbox-list, cancel, reset-to-inbox, manifest, update, set-mailbag-id, find-mailbag-id, acknowledgment-note, send-test-file |
| Interchanges | 8 | get, cancel, manifest, resend, get-date, get-header, inbox-list, outbox-list |
| Callbacks | 8 | create, update, delete, get-queue-by-id, event-list, get-event-by-id, queue-list, test |
| CarbonCopies | 5 | get, create, list, update, delete |
| Certificates | 5 | add-private, add-public, create, renew, terminate |
| Comms | 8 | get, find, list, pair, set-pair, create, update, update-config |
| Users | 16 | get, create, update, terminate, get-me, get-key, generate-key, reset-sessions, by-name, list, password, generate-password, role, send-sms, set-network-mailbox, update-config |
| Keys | 4 | get-key, list, create, delete |
| Portals | 2 | get-by-mailbox, create |
| Reports | 8 | mailbox-interchange-stats, mailbox-stats, report-list, by-date, instant-stats, interchange-stats, monthly, traffic-stats |
| StatusLists | 1 | get-status-lists |

---

## Key ENUMs Reference

These ENUMs appear across many endpoints. Define them in `docs/appendix/enums.md` and link from each page that uses them rather than repeating the full table everywhere.

| ENUM | Values |
|---|---|
| `AuthLevel` | NoChange, Root, TechOps, NetOps, NetworkAdmin, NetworkUser, MailboxAdmin, MailboxUser, TPUser, General |
| `Status` | Development, Active, Preproduction, Suspended, Terminated |
| `Direction` | NoDir, OutBox, InBox |
| `EDIStandard` | X12, EDIFACT, TRADACOMS, VDA, XML, TXT, PDF, Binary |
| `ParcelStatus` | InBoxReady, InBoxTransferred, as2Receive, as2Sent, ftpReceived, ftpSent, outboxDeliveryError, ... (full list in Swagger) |
| `RoutingGroup` | ProductionA, ProductionB, Migration1, Migration2, ManagedFileTransfer, Test, SuperHub, Suspense1-3, NetOpsOnly1-2 |
| `UseType` | Undefined, Test, Production, TestAndProduction |
| `NetworkContactType` | Owner, Errors, Interconnects, Notices, Reports, Accounting, CustomerService |
| `NetworkGatewayCommChannel` | none, ftp, sftp, as2, http, oftp, x400, gisb, rnif, cxml, ftpsslimplicit, peppol, as4, undefined |
| `KeyVisibility` | Private, Shared, Public, Session |
| `Objects` | System, User, Network, Mailbox, ECGridID, Interconnect, Migration, Parcel, Interchange, CarbonCopy, CallBackEvent, AS2, Comm, GISB, InterconnectNote, PriceList, Contract, Invoice |
| `CertificateType` | X509, PGP, SSH |
| `CertificateUsage` | SSL, Encryption, Signature, EncryptionAndSignature |
| `ReceiptType` | None, SynchronousUnsigned, SynchronousSigned, AsynchronousUnsigned, AsynchronousSigned |
| `HTTPAuthType` | None, Basic, Digest |
| `StatisticsPeriod` | Hour, Day, Week, Month |
| `EMailSystem` | smtp, x400 |
| `EMailPayload` | Body, Attachment |
| `CellCarrier` | ATTCingular, Verizon, TMobile, SprintPCS, Nextel, BoostMobile, USCellular, MetroPCS, ... |

---

## What to Avoid

- Do not suggest Entity Framework, SQL Server, or any SQL-based storage
- Do not use Newtonsoft.Json — use `System.Text.Json` only
- Do not hardcode API keys, passwords, or credentials anywhere in samples
- Do not create a Migrations section in SOAP docs — it is deprecated and excluded by design
- Do not document deprecated or uncommon SOAP API calls (CallBackIDInfo, etc.)
- Do not generate Docusaurus JavaScript config — use TypeScript only
- Do not commit, push, or merge to any branch — that is a human responsibility per Loren Data AI Use Policy §7.2
- Do not use `new HttpClient()` directly in production sample code — use `IHttpClientFactory`
- Do not reference WCF `system.serviceModel` web.config patterns — this is .NET 10 only

---

## Security Guardrails — DO NOT MODIFY WITHOUT REVIEW

- No secrets, API keys, or credentials in any source file — samples load config from `IConfiguration` or environment variables
- Authentication and session-handling code requires human review before commit
- Do not generate code that stores or logs customer PII

---

## Build & Deploy Notes

```bash
# Install dependencies
cd website
npm install

# Local dev server
npm run start

# Production build
npm run build

# GitHub Actions deploys automatically on push to main
# Target: gh-pages branch → developers.ecgrid.com
```

---

## When You Change Files — Attribution and Comments (Automated)

When you materially modify or create any file, you MUST manage the AI Attribution comment block at the top of the file. This is a Loren Data AI Use Policy requirement (§8.1–§8.2).

### What counts as "material modification"

Attribute these:
- Creating a new file (always)
- Adding or changing methods, classes, or non-trivial code blocks
- Generating test files
- Restructuring or refactoring code in a file

Skip attribution for these:
- Renaming a variable, fixing whitespace, correcting typos
- Changes the developer explicitly says they will rewrite
- Documentation-only changes under 5 lines

### Getting the developer name and today's date

Run these once per session and reuse the values:

- **Developer name:** run `git config user.name` in the terminal
- **Today's date:** ISO format `YYYY-MM-DD`

If `git config user.name` returns empty, ask the developer for their name before proceeding.

### If the file has NO attribution block yet

For Markdown files:
```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | YYYY-MM-DD: description - developer name -->
```

For C# files:
```csharp
// ------------------------------------------------------------
// AI Attribution — per Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// YYYY-MM-DD: <one-line description> - <developer name>
// ------------------------------------------------------------
```

For JSON files (strict): skip inline attribution — PR description covers per §8.3.

### If the file ALREADY has an attribution block

Append a new dated line inside the existing block above the closing separator. Never replace existing entries.

### Inline comments in generated code

- Comment the WHY not the WHAT
- Add XML doc comments (`/// <summary>`) on all public C# methods
- Match existing file comment density — do not over-comment

### When NOT to auto-attribute

If the developer says "skip attribution for this one," respect it without argument.

---

## Related Documents

- [Claude Code Setup Guide](../General Documentation/Developer Handbook/Claude-Code-Setup-Guide.md)
- [Developer Guide Template](../General Documentation/Developer Handbook/Developer-Guide-Template.md)
- [ECGrid CI/CD Branch Standards](../General Documentation/Developer Handbook/ECGrid-CICD-Branch-Standards.md)
- [API Naming & Versioning Standard](../General Documentation/Developer Handbook/API-Naming-Versioning-Standard.md)
- [Loren Data AI Use Policy](../General Documentation/AI_Use_Policy_v1_3.docx)
- [Site Plan Document](C:\Local Docs\API Doc Site\ECGrid-Developer-Portal-Plan.md)

---

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-07 | Initial CLAUDE.md created. Full site plan, nav structure, page templates, ENUMs, coding conventions, and attribution automation merged from Loren Data Developer Handbook template. | Greg |
