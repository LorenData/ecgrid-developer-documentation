---
title: ENUMs Reference
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created ENUMs reference page for REST and SOAP APIs - Greg Kolinski */}

# ENUMs Reference

These ENUMs are used across both REST and SOAP APIs. Individual endpoint and method pages link here for full definitions.

---

## AuthLevel

User permission level. Controls what operations a user or API key may perform.

| Value | Description |
|---|---|
| `NoChange` | Retain the current AuthLevel — used in update operations to leave the level unchanged |
| `Root` | Unrestricted system-level access (Loren Data internal only) |
| `TechOps` | Technical operations access across all networks |
| `NetOps` | Network operations access |
| `NetworkAdmin` | Full administrative access within a single network |
| `NetworkUser` | Standard user access within a network |
| `MailboxAdmin` | Full administrative access within a single mailbox |
| `MailboxUser` | Standard user access within a mailbox |
| `TPUser` | Trading partner–level access |
| `General` | Minimal general-purpose access |

---

## Status

Object lifecycle status. Applies to networks, mailboxes, IDs, interconnects, users, and other resources.

| Value | Description |
|---|---|
| `Development` | Object is being configured and is not yet live |
| `Active` | Object is live and fully operational |
| `Preproduction` | Object is in a staging/testing state before going active |
| `Suspended` | Object is temporarily disabled; can be reactivated |
| `Terminated` | Object has been permanently deactivated |

---

## Direction

Message direction relative to the local mailbox.

| Value | Description |
|---|---|
| `NoDir` | No direction specified; used in queries that span both directions |
| `OutBox` | Outbound — messages sent from this mailbox to a trading partner |
| `InBox` | Inbound — messages received by this mailbox from a trading partner |

---

## EDIStandard

EDI document standard or file format.

| Value | Description |
|---|---|
| `X12` | ANSI ASC X12 (the primary EDI standard in North America) |
| `EDIFACT` | UN/EDIFACT (international EDI standard) |
| `TRADACOMS` | TRADACOMS (UK retail EDI standard) |
| `VDA` | VDA (German automotive EDI standard) |
| `XML` | XML-based document |
| `TXT` | Plain text file |
| `PDF` | PDF document |
| `Binary` | Binary file (non-EDI payload) |

---

## ParcelStatus

Parcel delivery state. A parcel is the file-level container for one or more EDI interchanges.

| Value | Description |
|---|---|
| `InBoxReady` | Parcel has been received and is ready for download by the recipient |
| `InBoxTransferred` | Parcel has been downloaded (transferred) to the recipient |
| `InBoxArchived` | Parcel has been moved to archive storage after download |
| `as2Receive` | Parcel was received via an AS2 channel |
| `as2Sent` | Parcel was delivered via an AS2 channel |
| `ftpReceived` | Parcel was received via an FTP/SFTP channel |
| `ftpSent` | Parcel was delivered via an FTP/SFTP channel |
| `outboxPending` | Parcel is queued for outbound delivery |
| `outboxSent` | Parcel has been sent and delivery is in progress |
| `outboxAcknowledged` | Delivery has been acknowledged by the receiving party |
| `outboxRetry` | Delivery failed and the system is retrying |
| `outboxFailed` | Delivery failed after all retry attempts were exhausted |
| `outboxDeliveryError` | A delivery error was encountered (may recover) |
| `outboxTransferred` | Parcel has been handed off to a downstream carrier or VAN |
| `Cancelled` | Parcel was cancelled before delivery |
| `VaultReady` | Parcel is stored in the ECGrid Vault for long-term retention |

---

## RoutingGroup

ECGrid internal routing group. Determines which production cluster or environment handles the traffic.

| Value | Description |
|---|---|
| `ProductionA` | Primary production routing cluster A |
| `ProductionB` | Primary production routing cluster B |
| `Migration1` | Migration routing group 1 (temporary, used during network migrations) |
| `Migration2` | Migration routing group 2 |
| `ManagedFileTransfer` | Managed file transfer routing path |
| `Test` | Test environment routing |
| `SuperHub` | Super-hub routing for large-volume networks |
| `Suspense1` | Suspense hold group 1 |
| `Suspense2` | Suspense hold group 2 |
| `Suspense3` | Suspense hold group 3 |
| `NetOpsOnly1` | Restricted to network operations staff only — group 1 |
| `NetOpsOnly2` | Restricted to network operations staff only — group 2 |

---

## UseType

Designates whether an ECGrid ID or resource is for test or production use.

| Value | Description |
|---|---|
| `Undefined` | No use type specified |
| `Test` | Test traffic only; not used for live production EDI |
| `Production` | Live production EDI only |
| `TestAndProduction` | Accepts both test and production traffic |

---

## NetworkContactType

Contact role for a network. Used when retrieving or updating network contact information.

| Value | Description |
|---|---|
| `Owner` | Primary owner of the network account |
| `Errors` | Contact for error notifications and alerts |
| `Interconnects` | Contact for interconnect setup and requests |
| `Notices` | Contact for general notices and announcements |
| `Reports` | Contact for scheduled reports |
| `Accounting` | Contact for billing and accounting matters |
| `CustomerService` | Customer service contact |

---

## NetworkGatewayCommChannel

Communication channel type for network gateway connections.

| Value | Description |
|---|---|
| `none` | No channel configured |
| `ftp` | FTP (plain) |
| `sftp` | SFTP (SSH File Transfer Protocol) |
| `as2` | AS2 (Applicability Statement 2) |
| `http` | HTTP |
| `oftp` | OFTP (Odette File Transfer Protocol) |
| `x400` | X.400 messaging |
| `gisb` | GISB (Gas Industry Standards Board) |
| `rnif` | RosettaNet Implementation Framework |
| `cxml` | cXML (Commerce XML) |
| `ftpsslimplicit` | FTP over SSL with implicit TLS |
| `peppol` | PEPPOL (Pan-European Public Procurement Online) |
| `as4` | AS4 (successor to AS2 for B2B messaging) |
| `undefined` | Channel type not yet defined |

---

## KeyVisibility

Visibility and sharing scope of an API key.

| Value | Description |
|---|---|
| `Private` | Key is visible only to the owner |
| `Shared` | Key is shared within a network or mailbox group |
| `Public` | Key is publicly visible |
| `Session` | Key is tied to a session and expires when the session ends |

---

## Objects

Object type used in audit logs, callback events, and system filtering.

| Value | Description |
|---|---|
| `System` | System-level event |
| `User` | User account object |
| `Network` | Network object |
| `Mailbox` | Mailbox object |
| `ECGridID` | ECGrid trading partner ID |
| `Interconnect` | Interconnect (partner relationship) object |
| `Migration` | Migration record (legacy; deprecated) |
| `Parcel` | Parcel (file container) object |
| `Interchange` | EDI interchange object |
| `CarbonCopy` | Carbon copy routing rule object |
| `CallBackEvent` | Callback/webhook event object |
| `AS2` | AS2 connection object |
| `Comm` | Communications channel object |
| `GISB` | GISB channel object |
| `InterconnectNote` | Note attached to an interconnect |
| `PriceList` | Pricing list object |
| `Contract` | Contract object |
| `Invoice` | Invoice object |

---

## CertificateType

Type of digital certificate used for AS2 or encryption.

| Value | Description |
|---|---|
| `X509` | X.509 public-key certificate (most common for AS2 and TLS) |
| `PGP` | PGP (Pretty Good Privacy) certificate |
| `SSH` | SSH public key |

---

## CertificateUsage

Intended usage for a certificate.

| Value | Description |
|---|---|
| `SSL` | TLS/SSL transport security |
| `Encryption` | Payload encryption |
| `Signature` | Digital signature only |
| `EncryptionAndSignature` | Both encryption and digital signature |

---

## ReceiptType

AS2 Message Disposition Notification (MDN) receipt type.

| Value | Description |
|---|---|
| `None` | No receipt requested |
| `SynchronousUnsigned` | Synchronous MDN, unsigned |
| `SynchronousSigned` | Synchronous MDN, digitally signed |
| `AsynchronousUnsigned` | Asynchronous MDN, unsigned |
| `AsynchronousSigned` | Asynchronous MDN, digitally signed |

---

## HTTPAuthType

HTTP authentication method for callbacks and comm channel connections.

| Value | Description |
|---|---|
| `None` | No HTTP authentication |
| `Basic` | HTTP Basic authentication (base64-encoded credentials) |
| `Digest` | HTTP Digest authentication |

---

## StatisticsPeriod

Time period granularity for report and statistics queries.

| Value | Description |
|---|---|
| `Hour` | Hourly statistics |
| `Day` | Daily statistics |
| `Week` | Weekly statistics |
| `Month` | Monthly statistics |

---

## EMailSystem

Email transport system used for EDI-over-email delivery.

| Value | Description |
|---|---|
| `smtp` | SMTP (standard internet email) |
| `x400` | X.400 email messaging system |

---

## EMailPayload

How the EDI payload is attached to an email notification.

| Value | Description |
|---|---|
| `Body` | Payload included in the email body |
| `Attachment` | Payload included as an email attachment |

---

## CellCarrier

Mobile carrier for SMS notifications sent via the Users API.

| Value | Description |
|---|---|
| `ATTCingular` | AT&T / Cingular Wireless |
| `Verizon` | Verizon Wireless |
| `TMobile` | T-Mobile |
| `SprintPCS` | Sprint PCS |
| `Nextel` | Nextel |
| `BoostMobile` | Boost Mobile |
| `USCellular` | US Cellular |
| `MetroPCS` | Metro PCS |

:::note
Additional carriers may be available in the live API. Check the Swagger UI at [rest.ecgrid.io/swagger](https://rest.ecgrid.io/swagger/index.html) for the current complete list.
:::
