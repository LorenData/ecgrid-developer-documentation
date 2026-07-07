---
title: get-status-list
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-status-list tool reference - Greg Kolinski
*/}

# get-status-list

Return the ECGrid status-code catalog — the reference table that maps every numeric status code to its meaning. Use to resolve or explain a status code seen elsewhere: the `statusCode` on a parcel (`connectivity_parcel_get-parcel-by-id`) or the `InterchangeStatus` on report rows (`connectivity_interchange_get-document-counts-by-status`). Also useful to enumerate all possible statuses. Takes no input arguments. Returns a `codes` array (each: code, qualifier, message, level) and a `count`. This is tenant-agnostic reference data and changes rarely; results are cached per caller. To look up a specific parcel's current status use `connectivity_parcel_get-parcel-by-id`, not this catalog.

## Tool Name

`connectivity_system_get-status-list`

## Auth Level Required

Any

## Parameters

None. Pass an empty `request` object: `"arguments": { "request": {} }`.

## Response

Structured JSON — `count`, `codes` array (each: `code`, `qualifier`, `message`, `level`). Results are cached per caller.

```json
{
  "count": 42,
  "codes": [
    { "code": 1000, "qualifier": "E", "message": "Interchange Received", "level": "Info" },
    { "code": 3010, "qualifier": "E", "message": "Interchange Delay: Retry", "level": "Warning" }
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `count` | integer | Total number of status codes |
| `codes[].code` | integer | Numeric status code |
| `codes[].qualifier` | string | Code qualifier |
| `codes[].message` | string | Human-readable description |
| `codes[].level` | string | Severity: Info, Warning, Error |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_system_get-status-list",
    "arguments": { "request": {} }
  }
}
```

## Example Prompts

- `What does status code 3010 mean?`
- `List all ECGrid error-level status codes`

## See Also

- [Resources & Prompts](../../resources-and-prompts.md) — InterchangeStatus and ParcelStatus MCP Resources
- [get-interchange-by-id](../interchanges/get-interchange-by-id)
- [get-parcel-by-id](../parcels/get-parcel-by-id)
