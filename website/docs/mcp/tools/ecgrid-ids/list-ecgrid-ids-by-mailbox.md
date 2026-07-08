---
title: list-ecgrid-ids-by-mailbox
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: list-ecgrid-ids-by-mailbox tool reference - Greg Kolinski
*/}

# list-ecgrid-ids-by-mailbox

List ECGrid trading-partner ID records registered under a specific mailbox. Use to enumerate the roster of EDI IDs under a known mailbox — for example an operator wants every partner ID, qualifier, and status currently registered there. Only `mailboxId` is required: when `networkId` is omitted the tool resolves the owning network automatically. Supply `networkId` explicitly to skip that extra lookup when the network is already known. Returns a `count` and an `ecgridIds` array; an empty array (count = 0) means the mailbox has no registered EDI IDs matching the filter — a successful outcome, NOT NOT_FOUND.

> ℹ️ **Interactive UI Component:** This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.

## Tool Name

`connectivity_ecgrid-id_list-ecgrid-ids-by-mailbox`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.mailboxId` | integer | Yes | Internal numeric mailbox ID. Non-negative integer >= 0. `0` refers to the network's root mailbox (not a sentinel for "all"). Example: 142. Values < 0 are rejected as VALIDATION_ERROR. |
| `request.networkId` | integer \| null | No | Internal numeric network ID. Positive integer >= 1. When omitted, resolved automatically from `mailboxId`. Supply explicitly to skip that lookup when the network is already known. Example: 7. |
| `request.showInactive` | boolean \| null | No | Include inactive (Suspended, Terminated) records. Default `false` — only Active and Pending records returned. Pass `true` to retrieve the full roster including Suspended and Terminated records, for example when auditing historical assignments. |

## Response

Returns a count and array of ECGrid ID records registered under the mailbox.

```json
{
  "count": 3,
  "ecgridIds": [
    {
      "ecgridId": 12345,
      "networkId": 7,
      "networkName": "Loren Data Corp",
      "mailboxId": 142,
      "mailboxName": "acme-prod@example.com",
      "qualifier": "ZZ",
      "id": "ACMECORP",
      "description": "ACME Corporation Production",
      "dataEmail": "edi@acme.example.com",
      "mailboxDefault": true,
      "status": "Active",
      "useType": "Production"
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Number of ECGrid ID records returned |
| `ecgridIds` | array | Array of ECGrid ID records registered under the mailbox (may be empty) |
| `ecgridIds[].ecgridId` | integer | Internal numeric ECGrid ID (primary key) |
| `ecgridIds[].networkId` | integer | ECGrid network that owns this ID |
| `ecgridIds[].networkName` | string | Human-readable name of the owning network |
| `ecgridIds[].mailboxId` | integer | ECGrid mailbox this ID is registered under |
| `ecgridIds[].mailboxName` | string | Human-readable name of the owning mailbox |
| `ecgridIds[].qualifier` | string | X12 partner-ID qualifier (ISA05/ISA07), e.g. `ZZ`, `01` |
| `ecgridIds[].id` | string | Wire-level EDI identifier exchanged in X12 ISA06/ISA08 |
| `ecgridIds[].description` | string | Free-form human-readable description of the trading partner |
| `ecgridIds[].dataEmail` | string | Email address for data-notification delivery |
| `ecgridIds[].mailboxDefault` | boolean | `true` if this is the default ECGrid ID for its mailbox |
| `ecgridIds[].status` | string | Lifecycle status — Active, Inactive, Pending, Suspended, or Terminated (see [Status enum](../../../appendix/enums.md)) |
| `ecgridIds[].useType` | string | Use type — Test, Production, or TestAndProduction (see [UseType enum](../../../appendix/enums.md)) |

## UI Component

When this tool is called from Claude Desktop or Claude.ai, the response includes a visual widget rendered from `ui://ecgrid-id/by-mailbox.html` displaying the ECGrid ID roster alongside the AI's text response.

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_ecgrid-id_list-ecgrid-ids-by-mailbox",
    "arguments": {
      "request": { "mailboxId": 142 }
    }
  }
}
```

## Example Prompts

- `List all EDI IDs for mailbox 142`
- `What trading partner IDs does mailbox 500 have?`
- `Show me all ECGrid IDs registered under mailbox 142, including inactive ones`

## See Also

- [get-ecgrid-id-by-id](./get-ecgrid-id-by-id.md) — look up a single record by its internal numeric ECGrid ID
- [find-edi-ids](./find-edi-ids.md) — search by wire-level EDI identifier string or description substring
- [get-mailbox-by-id](../mailboxes/get-mailbox-by-id.md) — look up mailbox metadata for the parent mailbox
