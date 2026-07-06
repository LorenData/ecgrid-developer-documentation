{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: get-version tool reference - Greg Kolinski
*/}
---
title: get-version
---

# get-version

Return the ECGrid REST API and ECGridOS backend version strings. Use for smoke tests, integration diagnostics, or to confirm which API/backend build the caller is talking to — e.g. 'what version of ECGrid is this?', 'is the backend reachable?'. Takes no input arguments. Returns `rest` (the REST API version + build, e.g. `v2.6 (Build 1042)`) and `ecgridOs` (the SOAP backend version, or `Unknown` if that lookup failed). Not the caller's own identity — for that use `connectivity_user_get-user-me`.

## Tool Name

`connectivity_system_get-version`

## Auth Level Required

Any

## Parameters

None. Pass an empty `request` object: `"arguments": { "request": {} }`.

## Response

Structured JSON — `rest` (REST API version + build string), `ecgridOs` (ECGridOS backend version string).

```json
{
  "rest": "v2.6 (Build 1042)",
  "ecgridOs": "v4.1.0"
}
```

## Response Fields

| Field | Description |
|---|---|
| `rest` | ECGrid REST API version and build number |
| `ecgridOs` | ECGridOS SOAP backend version (`Unknown` if that lookup failed) |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_system_get-version",
    "arguments": { "request": {} }
  }
}
```

## See Also

- [hello-world](./hello-world.md) — verify identity and connectivity
- [Protocol Reference](../../protocol-reference.md)
