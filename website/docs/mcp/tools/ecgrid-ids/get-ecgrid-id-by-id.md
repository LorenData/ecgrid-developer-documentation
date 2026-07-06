{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-ecgrid-id-by-id tool reference - Greg Kolinski
*/}
---
title: get-ecgrid-id-by-id
---

# get-ecgrid-id-by-id

Look up a single ECGrid trading-partner ID record by its numeric ECGrid ID (the internal int32 primary key). Use when the caller already has the integer ECGrid ID — for example from a previous `connectivity_partner_get-partner-by-id` result, a `connectivity_ecgrid-id_find-edi-ids` match, a ticket, or an admin reference. For lookup by the wire-level EDI identifier string (the value partners exchange in X12 ISA06/ISA08, paired with a qualifier such as `ZZ` or `01`) use `connectivity_ecgrid-id_find-edi-ids` instead. Returns NOT_FOUND when no record matches the integer ID. Results are scoped to the caller's APIKey.

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::

## Tool Name

`connectivity_ecgrid-id_get-ecgrid-id-by-id`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.ecgridId` | integer | Yes | The numeric ECGrid ID — the internal int32 primary key of the trading-partner ID record. Positive integer >= 1. Example: 12345. This is NOT the wire-level EDI identifier string; for that use `connectivity_ecgrid-id_find-edi-ids`. |

## Response

Returns the ECGrid ID record's full profile including the wire-level EDI identifier pair, owner mailbox, lifecycle status, and use type.

```json
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
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `ecgridId` | integer | The internal numeric ECGrid ID (primary key) |
| `networkId` | integer | ECGrid network that owns this ID |
| `networkName` | string | Human-readable name of the owning network |
| `mailboxId` | integer | ECGrid mailbox this ID is registered under |
| `mailboxName` | string | Human-readable name of the owning mailbox |
| `qualifier` | string | X12 partner-ID qualifier (ISA05/ISA07), e.g. `ZZ`, `01` |
| `id` | string | Wire-level EDI identifier exchanged in X12 ISA06/ISA08 |
| `description` | string | Free-form human-readable description of the trading partner |
| `dataEmail` | string | Email address for data-notification delivery |
| `mailboxDefault` | boolean | `true` if this is the default ECGrid ID for its mailbox |
| `status` | string | Lifecycle status (see [Status enum](../../../appendix/enums.md)) |
| `useType` | string | Use type — Test, Production, or TestAndProduction (see [UseType enum](../../../appendix/enums.md)) |

## UI Component

When this tool is called from Claude Desktop or Claude.ai, the response includes a visual widget rendered from `ui://ecgrid-id/detail.html` displaying the ECGrid ID profile alongside the AI's text response.

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_ecgrid-id_get-ecgrid-id-by-id",
    "arguments": {
      "request": { "ecgridId": 12345 }
    }
  }
}
```

## Example Prompts

- `Show me ECGrid ID 12345`
- `What mailbox owns ECGrid ID 99999?`
- `Look up the trading-partner ID record 12345`

## See Also

- [find-edi-ids](./find-edi-ids.md) — search by wire-level EDI identifier string or description substring
- [list-ecgrid-ids-by-mailbox](./list-ecgrid-ids-by-mailbox.md) — list all ECGrid IDs registered under a mailbox
- [get-mailbox-by-id](../mailboxes/get-mailbox-by-id.md) — look up the owning mailbox
