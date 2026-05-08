---
title: REST API Overview
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST API overview page created - Greg Kolinski */}

# REST API Overview

The ECGrid REST API v2.6 is the active, recommended interface for all new ECGrid integrations. It provides full access to network, mailbox, trading partner, parcel, interchange, and reporting functions over HTTPS using JSON.

## Base URL

```
https://rest.ecgrid.io
```

## Authentication

All endpoints (except `GET /v2/auth/version`) require authentication via one of two methods:

| Method | Header | Notes |
|---|---|---|
| API Key | `X-API-Key: <key>` | Recommended for server-to-server integrations |
| Bearer JWT | `Authorization: Bearer <token>` | Obtained from `POST /v2/auth/login` |

See [Authentication & Session Management](../getting-started/authentication.md) for full details.

## Request / Response Format

All requests and responses use `application/json`. Every response is wrapped in a standard envelope:

```json
{
  "success": true,
  "data": { },
  "errorCode": "",
  "message": ""
}
```

| Field | Type | Description |
|---|---|---|
| `success` | boolean | `true` if the call succeeded; `false` on error |
| `data` | object \| array \| null | The response payload |
| `errorCode` | string | Machine-readable error code when `success` is `false` |
| `message` | string | Human-readable description of the result or error |

## Endpoints by Resource Group

119 total endpoints across 16 resource groups.

| Tag | Count | Description |
|---|---|---|
| [Auth](./auth/login.md) | 6 | Login, logout, token refresh, session info, password change, version |
| [Networks](./networks/get-network.md) | 6 | Network profile, contact, configuration, X12 delimiters |
| [Mailboxes](./mailboxes/get-mailbox.md) | 7 | Mailbox CRUD, configuration, X12 delimiters |
| [IDs](./ids/get-id.md) | 13 | ECGrid ID management, trading partner CRUD, VAN routing |
| [Partners](./partners/get-partner.md) | 7 | Interconnect (partner) management, notes |
| [Parcels](./parcels/get-parcel.md) | 15 | Upload, download, inbox/outbox lists, confirmation, manifest |
| [Interchanges](./interchanges/get-interchange.md) | 8 | Interchange tracking, cancel, resend, manifest |
| [Callbacks](./callbacks/create-callback.md) | 8 | Webhook registration, event queue, testing |
| [Carbon Copies](./carbon-copies/get-carbon-copy.md) | 5 | CC routing rules CRUD |
| [Certificates](./certificates/add-private.md) | 5 | AS2/SFTP certificate management |
| [Comms](./comms/get-comm.md) | 8 | Communication channel configuration |
| [Users](./users/get-user.md) | 16 | User CRUD, roles, API keys, password management |
| [Keys](./keys/get-key.md) | 4 | API key lifecycle management |
| [Portals](./portals/get-portal-by-mailbox.md) | 2 | Portal provisioning |
| [Reports](./reports/mailbox-interchange-stats.md) | 8 | Usage statistics and traffic reports |
| [Status Lists](./status-lists/get-status-lists.md) | 1 | Reference lists for status codes and ENUMs |

## OpenAPI Specification

The full OpenAPI 3 spec is available at:

- **Swagger UI:** [https://rest.ecgrid.io/swagger/index.html](https://rest.ecgrid.io/swagger/index.html)
- **Swagger JSON:** [https://rest.ecgrid.io/swagger/v2/swagger.json](https://rest.ecgrid.io/swagger/v2/swagger.json)

## See Also

- [Quick Start — REST](../getting-started/quick-start-rest.md)
- [REST vs SOAP](../getting-started/rest-vs-soap.md)
- [Error Handling & Troubleshooting](../getting-started/error-handling-troubleshooting.md)
- [Appendix — Error Codes](../appendix/error-codes.md)
