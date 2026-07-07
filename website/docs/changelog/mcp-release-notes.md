{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP release notes - Greg Kolinski
*/}
---
title: MCP Release Notes
sidebar_position: 3
---

# ECGrid MCP Release Notes

Track new tools and changes to the ECGrid MCP Server (`mcp.ecgrid.io`).

Call `tools/list` to always get the current complete tool list at runtime. See the [Tools Reference](../mcp/tools/overview.md) for full documentation on every tool.

---

## Response Modes: Structured JSON and Interactive UI Components

All ECGrid MCP tools return **structured JSON data** designed for AI agent and developer consumption. The AI interprets the structured data and presents it to the user in plain language. Developers integrating via the HTTP API receive the same structured JSON for use in their own applications.

A subset of tools additionally render an **interactive UI component** in compatible AI clients (Claude Desktop and Claude.ai). The UI component is a visual, browsable widget that appears alongside the AI's response — presenting the structured ECGrid data in a formatted, interactive view rather than as plain text. Both modes use the identical tool call and return the identical data; the UI component is a presentation layer available in supported clients.

**Tools with interactive UI components:**

| Tool | UI Component |
|---|---|
| `mailbox_list-mailboxes` | Interactive mailbox browser |
| `mailbox_get-mailbox-by-id` | Mailbox profile card |
| `ecgrid-id_list-ecgrid-ids-by-mailbox` | EDI ID roster |
| `ecgrid-id_get-ecgrid-id-by-id` | EDI ID detail card |
| `ecgrid-id_find-edi-ids` | EDI ID search results |
| `partner_list-partners` | Trading partner list |
| `partner_get-partner-by-id` | Interconnect detail card |
| `transaction_search-transactions` | Transaction search and browse |
| `interchange_get-interchange-by-id` | Interchange detail card |
| `parcel_get-parcel-by-id` | Parcel detail with interchange manifest |

---

## 2026-07-01 — Interchange / Transaction Tools + Interactive UI Components

*PRs 3360, 3362*

### New Tools

#### `connectivity_interchange_get-interchange-by-id`

Look up a single EDI interchange (X12 ISA...IEA or EDIFACT UNB...UNZ envelope) by its numeric interchange ID. Returns routing, status, EDI identity, raw ISA header, and the list of parcel IDs carrying it.

**Returns:** Structured JSON — interchangeId, interchangeControlId, standard, documentType, bytes, interchangeDateTime, processDate, status (code, description, statusDate), from/to routing (networkId, networkName, mailboxId), raw header, tpFrom/tpTo EDI identity summaries (ecgridId, qualifier, id, description), parcelIds, parcelCount.

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.interchangeId` *(integer, required)* — numeric interchange ID

---

#### `connectivity_transaction_search-transactions`

Search EDI transactions the way the Customer Portal Transactions page does — by direction, type (Interchange or File), date window, ECGrid ID or qualifier+EDI ID filters, and view. Use for portal-style traffic lookup, monitoring, and troubleshooting.

**Returns:** Structured JSON — applied filters, rows array (each with transactionId, type, direction, timestamps, status, controlNumber, standard, documentType, bytes, parcelIds, from/to routing and EDI identity), leg totals, and totalRecords.

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Key parameters:**
- `request.type` *(string, required)* — `Interchange` or `File`
- `request.direction` *(string, required)* — `Inbound`, `Outbound`, or `Both`
- `request.networkId` *(integer, optional)* — defaults to caller's own network
- `request.mailboxId` *(integer, optional)* — defaults to -1 (all mailboxes)
- `request.beginDate`, `request.endDate` *(ISO 8601, optional)* — defaults to last 24 hours
- `request.view` *(string, optional)* — `Archive` (default), `Blocked`, `Pending`, `NoRoute`, `PendingDownload`, `DeliveryError`

---

### App Resources Added

Interactive UI resources registered for parcel, partner, ECGrid ID, and mailbox objects — enabling the UI component rendering behavior in compatible AI clients for the full set of applicable tools.

---

## 2026-06-24 — LLM Documentation Guidance

*PR 3299*

### Enhancement

ECGrid docs portal fallback instruction added to server metadata — AI agents that encounter an unknown ECGrid term or capability are directed to the ECGrid Developer Portal for authoritative reference.

---

## 2026-06-22 — Resources and Prompts

*PR 3283*

### MCP Resources Added

Resources are server-side reference data that AI agents can consult during a session. They do not appear in `tools/list` but are available to MCP clients that request them.

| Resource | Description |
|---|---|
| `Glossary` | ECGrid terminology reference — qualifier codes, status code meanings, object type definitions |
| `InterchangeStatus` | Complete interchange status code catalog with descriptions and severity levels |
| `ParcelStatus` | Complete parcel status code catalog with descriptions and severity levels |

### MCP Prompts Added

Prompts are guided multi-step sequences exposed by the server. They do not appear in `tools/list` but are available to MCP clients that request them.

| Prompt | Description |
|---|---|
| `InvestigatePartner` | Guided sequence for diagnosing a trading partner relationship — checks config, traffic history, and delivery status in order |
| `TriageStuckInterchange` | Guided sequence for triaging a stuck or pending interchange — walks through parcel status, route config, and retry state |

---

## 2026-06-10 — Callbacks, Carbon Copy, Keys, and FindComms

### New Tools

#### `connectivity_callback_get-callback-event-by-id`

Look up a single callback (webhook) event registration by its numeric ID, including its recent delivery/retry queue. Returns registration config (URL, direction, frequency, maxCalls, status, httpAuthType) and queue entries with per-attempt delivery logs.

**Returns:** Structured JSON — callBackEventId, registration config, queue array (each entry: status, callsRemaining, nextCall, delivery log). HTTP auth credentials are never returned.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.callBackEventId` *(integer, required)* — numeric callback event ID
- `request.queueCount` *(integer, optional)* — max queue entries to embed; defaults to 25

---

#### `connectivity_callback_get-callback-queue-by-id`

Look up a single callback delivery/retry queue entry by its numeric queue ID. Returns attempt status, calls remaining, next call time, delivery log, and a lite reference to the parent callback event.

**Returns:** Structured JSON — callBackQueueId, status, callsRemaining, nextCall, log array, lite event reference.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.callBackQueueId` *(integer, required)* — numeric callback queue entry ID (not a callBackEventId)

---

#### `connectivity_callback_list-callback-events`

List all callback registrations under a specific (networkId, mailboxId) pair. Returns registration config for each entry; delivery queue data is not embedded — use `callback_get-callback-event-by-id` for queue detail.

**Returns:** Structured JSON — count, events array (each: callBackEventId, systemObject, direction, frequency, maxCalls, status, url, httpAuthType).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, required)* — use 0 for the network root mailbox
- `request.showInactive` *(boolean, optional)* — include Suspended/Terminated registrations; defaults to false

---

#### `connectivity_callback_list-callback-queue`

List the callback delivery/retry queue for a mailbox. `pending` view returns attempts awaiting delivery; `failed` view returns errored attempts within a lookback window.

**Returns:** Structured JSON — count, queue array (each: status, callsRemaining, nextCall, delivery log, lite event reference).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, required)*
- `request.view` *(string, optional)* — `pending` (default) or `failed`
- `request.maxDays` *(integer, required when view=failed)* — lookback window in days

---

#### `connectivity_carbon-copy_get-carbon-copy-by-id`

Look up a single carbon copy routing rule by its numeric ID. Returns the four endpoint summaries (originalFrom, originalTo, ccFrom, ccTo), GS envelope filters, transaction set filter, status, and timestamps.

**Returns:** Structured JSON — carbonCopyId, networkId, mailboxId, four endpoint summaries (each: ecgridId, qualifier, id, description), gsFrom, gsTo, transactionSet, status, created, modified.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.carbonCopyId` *(integer, required)*

---

#### `connectivity_carbon-copy_list-carbon-copies`

List carbon copy routing rules. Scoped to a specific (networkId, mailboxId) pair, or across the full APIKey when both are omitted. Optional ECGrid ID filters narrow to rules involving a specific sender or receiver.

**Returns:** Structured JSON — count, carbonCopies array (each: carbonCopyId, networkId, mailboxId, four endpoint summaries, gsFrom, gsTo, transactionSet, status, timestamps).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId`, `request.mailboxId` *(integer, optional — must be supplied together)*
- `request.ecgridIdFrom`, `request.ecgridIdTo` *(integer, optional)* — filter by original sender/receiver
- `request.showInactive` *(boolean, optional)*

---

#### `connectivity_key_get-key`

Fetch a single ECGrid key/value record by its exact key name, object class, and visibility scope.

**Returns:** Structured JSON — key, value (verbatim, not redacted), meta, visibility, created, expires.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.systemObject` *(string, required)* — object class (e.g., Mailbox, Network, User)
- `request.objectId` *(integer, required)*
- `request.key` *(string, required)* — exact key name
- `request.visibility` *(string, required)* — `Private`, `Shared`, `Public`, or `Session`

---

#### `connectivity_key_list-keys`

List all key/value records attached to an ECGrid system object across all visibility levels. Use to discover what keys exist on an object — for example, FTP setup keys on a mailbox.

**Returns:** Structured JSON — count, keys array (each: key, value, meta, visibility, created, expires).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.systemObject` *(string, required)* — object class
- `request.objectId` *(integer, required)*

---

#### `connectivity_comm_find-comms`

Find communication channel records by wire identifier (e.g. an AS2 ID or FTP login) for a given protocol type, without needing to know the owning mailbox first. Use to answer "which mailbox owns this AS2 ID?"

**Returns:** Structured JSON — count, comms array (each: commId, type, identifier, url, sign/encrypt/compress flags, receipt policy, httpAuthType, status, usage window, owner, certificate metadata).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.identifier` *(string, required)* — wire identifier (e.g. AS2 ID, FTP login)
- `request.commType` *(string, required)* — protocol (e.g. `as2`, `ftp`, `sftp`)

---

## 2026-06-08 — Parcel Tools

### New Tools

#### `connectivity_parcel_get-parcel-by-id`

Look up a single parcel by its numeric parcel ID. Returns full parcel detail including identification, status, routing, and the interchange manifest with per-interchange status.

**Returns:** Structured JSON — parcelId, parcelDate, parcelBytes, fileName, mailbagControlId, status (code, description, statusDate), from/to routing (networkId, networkName, mailboxId, mailboxName), interchanges array (each: interchangeId, statusCode, statusDescription, statusDate, documentType), interchangeCount.

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.parcelId` *(integer, required)* — numeric parcel ID (int64)

---

#### `connectivity_parcel_list-pending-inbox-parcels`

List parcels currently sitting in the inbox awaiting download, scoped to a network and mailbox. Use to answer "what is pending for this mailbox right now?"

**Returns:** Structured JSON — count, parcels array (each: parcelId, parcelDate, parcelBytes, fileName, status, from/to routing, interchangeCount).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, required)*

---

#### `connectivity_parcel_list-inbox-parcels`

List inbound parcels by date range for a mailbox.

**Returns:** Structured JSON — count, parcels array with parcel identification, status, routing, and interchange counts.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, required)*
- `request.beginDate`, `request.endDate` *(ISO 8601, required)*

---

#### `connectivity_parcel_list-outbox-parcels`

List outbound parcels by date range for a mailbox.

**Returns:** Structured JSON — count, parcels array with parcel identification, status, routing, and interchange counts.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, required)*
- `request.beginDate`, `request.endDate` *(ISO 8601, required)*

---

## 2026-06-01 — Diagnostics: Config, FTP, Comms, and ECGrid IDs

*PRs 3184, 3186*

### New Tools

#### `connectivity_partner_check-partner-config`

Health-check a single interconnect (trading-partner relationship) for completeness and correctness. Runs four checks: setup complete, traffic has flowed, both ECGrid IDs active, and whether either ID has a scheduled future-dated move.

**Returns:** Structured JSON — isHealthy (boolean), setupComplete, hasTraffic, tp1/tp2.isActive, tp1/tp2.scheduledMove, lastTraffic timestamps, issues array (plain-language problem and warning descriptions).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.interconnectId` *(integer, required)*

---

#### `connectivity_comm_check-ftp-access`

Diagnose why an (S)FTP connection to ECGrid is being refused. Reads FTP setup keys on the mailbox or network and reports account configuration, ECGrid user lockout and session state, and optional IP allowlist check.

**Returns:** Structured JSON — account section (ftpConfigured, status, loginName, hasCertificate), optional ip section (allowed), optional user section (lockedOut, status, openSessions).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, optional)* — reads from mailbox when supplied, network when omitted
- `request.ip` *(string, optional)* — IPv4 or IPv6 address to check against the FTP allowlist

---

#### `connectivity_comm_get-comm-by-id`

Look up a single communication channel by its numeric comm ID. Includes SSL/TLS certificate inspection with computed validity status and days until expiry.

**Returns:** Structured JSON — commId, type (protocol), identifier, url, sign/encrypt/compress flags, receipt policy, httpAuthType, sslClientAuthentication, useType, status, usage window, timestamps, owner (userId, loginName, authLevel), certificates array (each: subject, issuer, thumbprint, serialNumber, notBefore/notAfter, status, validityStatus, isCurrentlyValid, daysUntilExpiry).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.commId` *(integer, required)*

---

#### `connectivity_comm_list-comms`

List communication channels registered under a specific (networkId, mailboxId) pair for one transport protocol. Set `withCerts: true` to include certificate validity and expiry data across all channels.

**Returns:** Structured JSON — count, comms array (same shape as `comm_get-comm-by-id`; certificates empty unless `withCerts: true`).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.mailboxId` *(integer, required)*
- `request.commType` *(string, required)* — protocol filter (e.g. `as2`, `ftp`, `sftp`)
- `request.withCerts` *(boolean, optional)* — include certificate metadata; defaults to false

---

#### `connectivity_comm_test-comm`

Actively test whether ECGrid can deliver to a customer's own configured AS2 or FTP channel by sending a throwaway test parcel and reading the delivery status. Non-blocking and two-step: call without `parcelId` to initiate, then pass the returned `parcelId` to poll.

**Returns:** Structured JSON — reachable (true/false/null), verdict (delivered/failed/aborted/pending), statusCode, statusDescription, parcelId, loopbackEcgridId.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.ecgridId` *(integer, required)* — the RECEIVE-side ECGrid ID to test
- `request.commType` *(string, required)* — `Ftp` or `As2`
- `request.parcelId` *(integer, optional)* — omit to initiate; supply to poll

---

#### `connectivity_ecgrid-id_get-ecgrid-id-by-id`

Look up a single trading-partner ID record by its internal numeric ECGrid ID.

**Returns:** Structured JSON — ecgridId, networkId, networkName, mailboxId, mailboxName, qualifier, id (wire EDI identifier), description, dataEmail, mailboxDefault, status, useType.

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.ecgridId` *(integer, required)*

---

#### `connectivity_ecgrid-id_find-edi-ids`

Find trading-partner ID records by wire-level EDI identifier string (X12 ISA06/ISA08) or by description substring. Use to resolve an inbound EDI ID to its owning mailbox and network, or to look up partners by name.

**Returns:** Structured JSON — count, ediIds array (same shape as `ecgrid-id_get-ecgrid-id-by-id`).

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.id` *(string, optional)* — wire EDI identifier; required when `description` is omitted
- `request.description` *(string, optional)* — description substring; takes precedence over `id` when both supplied
- `request.qualifier` *(string, optional)* — X12 qualifier (e.g. `ZZ`, `01`); defaults to wildcard
- `request.networkId`, `request.mailboxId` *(integer, optional)* — scope filters
- `request.showInactive` *(boolean, optional)* — defaults to true

---

#### `connectivity_ecgrid-id_list-ecgrid-ids-by-mailbox`

List all trading-partner ID records registered under a specific mailbox. Returns the full roster of EDI IDs, qualifiers, statuses, and use types.

**Returns:** Structured JSON — count, ecgridIds array (same shape as `ecgrid-id_get-ecgrid-id-by-id`).

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.mailboxId` *(integer, required)*
- `request.networkId` *(integer, optional)* — resolved automatically from mailboxId when omitted
- `request.showInactive` *(boolean, optional)*

---

#### `connectivity_partner_test-partner-delivery`

Actively test whether EDI delivery works across an interconnect by sending a throwaway test parcel through the grid and reading its delivery status. Non-blocking and two-step: call without `parcelId` to initiate, then pass the returned `parcelId` to poll.

**Returns:** Structured JSON — reachable (true/false/null), verdict (delivered/failed/aborted/pending/not_tested), statusCode, statusDescription, parcelId, fromEcgridId, toEcgridId, notes.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.interconnectId` *(integer, required)*
- `request.direction` *(string, optional)* — `Tp1ToTp2` (default) or `Tp2ToTp1`
- `request.parcelId` *(integer, optional)* — omit to initiate; supply to poll

---

## 2026-05-26 — Build Tools: IDs and Traffic

### New Tools

#### `connectivity_interchange_get-document-counts-by-status`

Count EDI documents (interchanges) processed over a date range (max 30 days), grouped by caller-side ECGrid ID and split by direction (FROM/TO), with a per-status histogram inside each direction. Use for status-distribution count questions — not for listing or identifying individual interchanges.

**Returns:** Structured JSON — scope (networkId, networkName, mailboxId, mailboxName), startDate, endDate, total, customers array (each: ecgridId, customer, qid, total, byDirection with `from` and `to` buckets each carrying `total` and `byStatus` (statusCode → count)).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.ecgridId` *(integer, optional)* — takes precedence over networkId/mailboxId when supplied (Mode A)
- `request.networkId`, `request.mailboxId` *(integer, required when ecgridId omitted — Mode B)*
- `request.startDate`, `request.endDate` *(ISO 8601, required)* — max 30-day window

---

#### `connectivity_partner_get-partner-document-counts`

Report how many interchanges one specific ECGrid ID exchanged with each of its trading partners over a date range (max 30 days), with byte volumes. Results ranked by total interchanges descending.

**Returns:** Structured JSON — scope (ecgridId, customer, qid, networkId, networkName, mailboxId, mailboxName), startDate, endDate, totalInterchanges, totalBytes, truncation flags, partners array (each: tradingPartner, tradingPartnerQid, totalInterchanges, totalBytes).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.ecgridId` *(integer, required)*
- `request.startDate`, `request.endDate` *(ISO 8601, required)* — max 30-day window
- `request.topN` *(integer, optional)* — max partner rows returned; defaults to 50, max 500

---

## 2026-05-21 — Customer, Network, Mailbox, and Partner

*PR 3147*

### New Tools

#### `connectivity_network_get-network-by-id`

Look up a single ECGrid network by its numeric network ID.

**Returns:** Structured JSON — networkId, name, status, runStatus, outageStatus, primary contacts, associated user account IDs (owner, routing, errors, interconnects, billing), public website URLs, owner-side routing metadata, created/modified timestamps.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*

---

#### `connectivity_mailbox_get-mailbox-by-id`

Look up a single mailbox by its numeric mailbox ID.

**Returns:** Structured JSON — mailboxId, networkId, name, description, status, useType, managed, ecgridAccount, defaultAs2Id, created, modified, seven role-based contact users (owner, errors, interconnects, notices, reports, customerService, accounting — each as userId + loginName + authLevel), delivery and X12 envelope config, billing metadata (pricelistId, contractId).

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.mailboxId` *(integer, required)*

---

#### `connectivity_mailbox_list-mailboxes`

List every mailbox in a network. Omit `networkId` to list the caller's own network.

**Returns:** Structured JSON — count, mailboxes array (same shape as `mailbox_get-mailbox-by-id`).

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, optional)* — defaults to caller's home network

---

#### `connectivity_mailbox_get-mailbox-by-name`

Look up mailboxes inside a network by name or email substring. Both `networkId` and `name` are required — there is no all-networks mode.

**Returns:** Structured JSON — count, mailboxes array (same shape as `mailbox_get-mailbox-by-id`).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, required)*
- `request.name` *(string, required)* — case-insensitive substring

---

#### `connectivity_partner_get-partner-by-id`

Look up a single interconnect (trading-partner relationship) by its numeric interconnect ID.

**Returns:** Structured JSON — interconnectId, uniqueId, lifecycle timestamps (created, modified, completed, lastTraffic, lastTrafficInbound, lastTrafficOutbound), status, contactName, contactEmail, reference1, reference2, as2Id1, as2Id2, tp1/tp2 ECGrid ID summaries (ecgridId, networkId, networkName, mailboxId, mailboxName, qualifier, id, description, status, useType), compact user references (requestorUser, contactUser, netOps — each as userId + loginName).

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.partnerId` *(integer, required)* — numeric interconnect ID

---

#### `connectivity_partner_list-partners`

List interconnects (trading-partner relationships) with optional filtering by ECGrid ID pair, status, network, mailbox, and traffic recency.

**Returns:** Structured JSON — count, partners array (same shape as `partner_get-partner-by-id`).

**Also renders:** Interactive UI component in compatible AI clients (Claude Desktop, Claude.ai).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.mailboxId` *(integer, optional)* — list all partners for a mailbox in a single call
- `request.networkId` *(integer, optional)*
- `request.status` *(string, optional)* — `Pending`, `Completed`, `Canceled`, `Delayed`, `Problem`, `AuthorizationRequired`, `NoStatusChange` (default — no filter)
- `request.ecgridId1`, `request.ecgridId2` *(integer, optional)* — filter by ECGrid ID pair
- `request.maxDays` *(integer, optional)* — traffic recency window; -1 = no limit (default)

---

#### `connectivity_user_get-user-by-id`

Look up a single ECGrid user by their numeric user ID.

**Returns:** Structured JSON — userId, loginName, firstName, lastName, company, email, phone, timeZoneOffset, authLevel, lockoutStatus, networkId, mailboxId, lastLogin, openSessions, timeOut, created, modified.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.userId` *(integer, required)*

---

#### `connectivity_user_get-user-by-login`

Look up a single ECGrid user by their login name or email address.

**Returns:** Structured JSON — same shape as `user_get-user-by-id`.

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.loginName` *(string, required)* — full login name or email address

---

#### `connectivity_user_get-user-me`

Return the session and profile record for the caller — the user identity behind the current APIKey. Use for connectivity verification, auth level inspection, and session diagnostics.

**Returns:** Structured JSON — same shape as `user_get-user-by-id`, plus ecgridOsVersion, sessionId, sessionEventId.

**Auth level required:** Any

**Parameters:** None

---

#### `connectivity_user_list-users`

List ECGrid users matching supplied filters, scoped to network, mailbox, or name substring. Supports a `lockedOut` post-filter to surface locked-out accounts. At least one scope filter (networkId, mailboxId, or name) is required.

**Returns:** Structured JSON — count, users array (same shape as `user_get-user-by-id`).

**Auth level required:** Any (scoped to caller's APIKey)

**Parameters:**
- `request.networkId` *(integer, optional)* — scope filter
- `request.mailboxId` *(integer, optional)* — scope filter
- `request.name` *(string, optional)* — login/email substring; scope filter
- `request.lockedOut` *(boolean, optional)* — post-filter; requires at least one scope filter alongside it

---

## 2026-05-19 — Foundation

### New Tools

#### `connectivity_system_hello-world`

Verifies your connection and returns your authenticated ECGrid identity. Use this to confirm your API key is valid and your integration is working.

**Returns:** Structured JSON — message (greeting), loginName, authLevel, networkId, mailboxId, serverTimeUtc.

**Auth level required:** Any

**Parameters:**
- `request.name` *(string, optional)* — display name; falls back to your `loginName` if omitted

---

#### `connectivity_system_get-version`

Return the ECGrid REST API and ECGridOS backend version strings. Use for smoke tests and integration diagnostics.

**Returns:** Structured JSON — rest (REST API version + build string), ecgridOs (ECGridOS backend version string).

**Auth level required:** Any

**Parameters:** None

---

#### `connectivity_system_get-status-list`

Return the complete ECGrid status-code catalog — maps every numeric status code to its meaning, qualifier, and severity level. Use to resolve status codes seen on parcels or interchanges. Results are cached per caller.

**Returns:** Structured JSON — count, codes array (each: code, qualifier, message, level).

**Auth level required:** Any

**Parameters:** None

---

## Response Modes Reference

All tools in this document return **structured JSON data** intended for AI agent and developer consumption. Ten tools additionally render an **interactive UI component** in compatible AI clients. The table at the top of this document lists all tools with interactive UI components.

**Structured JSON** is the primary return format for all tools — consistent across all MCP clients, HTTP integrations, Claude Desktop, and Claude.ai. The AI interprets the structured data and presents it to the user in plain language; developers use it directly in their applications.

**Interactive UI components** are a presentation layer available in Claude Desktop and Claude.ai. When a supported tool is called in a compatible client, the structured JSON data is also rendered as a browsable visual widget alongside the AI's text response. The tool call, parameters, and JSON response are identical regardless of whether a UI component renders.

---

## See Also

- [MCP Server Overview](../mcp/overview.md)
- [Tools Reference](../mcp/tools/overview.md)
- [REST API Changelog](./rest-changelog)
- [SOAP API Revision History](./soap-revision-history)
- [ECGrid Developer Portal](https://api.ecgridos.io/)
