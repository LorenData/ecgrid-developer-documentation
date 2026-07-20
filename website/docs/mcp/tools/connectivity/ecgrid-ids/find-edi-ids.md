---
title: find-edi-ids
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: find-edi-ids tool reference - Greg Kolinski
*/}

# find-edi-ids

Find ECGrid trading-partner ID records by EDI identifier string (the wire-level X12 ISA06/ISA08 value) or by a substring of the record description, with optional scope filters. Use when the caller has an EDI identifier string and wants to resolve it to the owning record — for example an inbound X12 envelope shows partner ID `7704344400` and they want to know which mailbox owns it — or when the caller knows a partner-name substring (e.g. `acme`) and wants matching records. Supply at least one of `id` or `description`. When `description` is supplied the backend routes to a description-based search and the `id`/`qualifier` filter is ignored. Returns a `count` and an `ediIds` array; an empty array (count = 0) is a successful outcome, NOT an error.

> ℹ️ **Interactive UI Component:** This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.

## Tool Name

`connectivity_ecgrid-id_find-edi-ids`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.id` | string \| null | Conditional | Wire-level EDI identifier string as exchanged on the X12 wire (ISA06/ISA08, GS02/GS03). Max 35 characters. Required when `description` is not supplied; at least one of `id` or `description` must be present. When both are supplied, `description` takes precedence and `id`/`qualifier` are ignored. Example: `7704344400`. |
| `request.description` | string \| null | Conditional | Case-insensitive substring filter on the record's free-form description. Max 128 characters. When supplied, routes to description-based search and `id`/`qualifier` are ignored. Use for human-readable partner-name lookup. Example: `acme`. |
| `request.qualifier` | string \| null | No | X12 partner-ID qualifier prefix (ISA05/ISA07). Max 4 characters. Typical values: `ZZ` (mutually defined), `01` (DUNS), `12` (phone), `14` (DUNS+suffix). Default `%` matches all qualifiers. Combine with `id` to narrow to a unique record. Ignored when `description` is supplied. |
| `request.networkId` | integer \| null | No | Restricts search to records on the given network. Sentinel: `-1` = all networks (default). Example: 42. |
| `request.mailboxId` | integer \| null | No | Restricts search to records on the given mailbox within `networkId`. Sentinel: `-1` = all mailboxes (default), `0` = network root mailbox. Example: 1234. |
| `request.showInactive` | boolean \| null | No | Include inactive (Suspended, Terminated) records. Default `true` — all lifecycle states returned. Pass `false` to restrict to Active and Pending only. |

## Response

Returns a count and array of matching ECGrid ID records. An empty `ediIds` array with `count = 0` means no match — this is success, not an error.

```json
{
  "count": 2,
  "ediIds": [
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
| `count` | integer | Number of matching records returned |
| `ediIds` | array | Array of matching ECGrid ID records (may be empty) |
| `ediIds[].ecgridId` | integer | Internal numeric ECGrid ID (primary key) |
| `ediIds[].networkId` | integer | ECGrid network that owns this ID |
| `ediIds[].networkName` | string | Human-readable name of the owning network |
| `ediIds[].mailboxId` | integer | ECGrid mailbox this ID is registered under |
| `ediIds[].mailboxName` | string | Human-readable name of the owning mailbox |
| `ediIds[].qualifier` | string | X12 partner-ID qualifier (ISA05/ISA07), e.g. `ZZ`, `01` |
| `ediIds[].id` | string | Wire-level EDI identifier exchanged in X12 ISA06/ISA08 |
| `ediIds[].description` | string | Free-form human-readable description of the trading partner |
| `ediIds[].dataEmail` | string | Email address for data-notification delivery |
| `ediIds[].mailboxDefault` | boolean | `true` if this is the default ECGrid ID for its mailbox |
| `ediIds[].status` | string | Lifecycle status (see [Status enum](../../../../appendix/enums.md)) |
| `ediIds[].useType` | string | Use type — Test, Production, or TestAndProduction (see [UseType enum](../../../../appendix/enums.md)) |

## UI Component

When this tool is called from Claude Desktop or Claude.ai, the response includes a visual widget rendered from `ui://ecgrid-id/find.html` displaying the search results alongside the AI's text response.

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_ecgrid-id_find-edi-ids",
    "arguments": {
      "request": {
        "id": "9998887776",
        "qualifier": "ZZ"
      }
    }
  }
}
```

## Example Prompts

- `Find the ECGrid ID for EDI identifier 9998887776`
- `Which mailbox owns EDI ID "ACMECORP" with qualifier ZZ?`
- `Find all EDI IDs with "acme" in their description`

## See Also

- [get-ecgrid-id-by-id](./get-ecgrid-id-by-id.md) — look up a single record by its internal numeric ECGrid ID
- [list-ecgrid-ids-by-mailbox](./list-ecgrid-ids-by-mailbox.md) — list all ECGrid IDs registered under a mailbox
- [get-mailbox-by-id](../mailboxes/get-mailbox-by-id.md) — look up the owning mailbox once you have the mailbox ID
