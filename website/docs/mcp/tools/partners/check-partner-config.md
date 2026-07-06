{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: check-partner-config tool reference - Greg Kolinski
*/}
---
title: check-partner-config
---

# check-partner-config

Health-check a single ECGrid interconnect (trading-partner relationship) for completeness and correctness. Use when the caller asks whether a trading partner is set up correctly, ready to exchange traffic, fully configured, or wants to know why traffic is not flowing — given the integer interconnect ID. Runs four checks: setup complete (status = Completed), traffic has flowed, both ECGrid IDs are active, and whether either ID has a future-dated move scheduled. Returns NOT_FOUND when no interconnect matches the ID.

## Tool Name

`connectivity_partner_check-partner-config`

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.interconnectId` | integer | Yes | The numeric interconnect (trading-partner relationship) ID to health-check. Positive integer >= 1. Example: 12345. Same value as `InterconnectIDInfo.interconnectId` returned by `connectivity_partner_list-partners` or `connectivity_partner_get-partner-by-id`. |

## Response

Returns a health summary with individual check results and a plain-language `issues` array describing any problems found.

```json
{
  "isHealthy": false,
  "setupComplete": true,
  "hasTraffic": false,
  "tp1": {
    "isActive": true,
    "scheduledMove": false,
    "lastTraffic": null
  },
  "tp2": {
    "isActive": true,
    "scheduledMove": false,
    "lastTraffic": null
  },
  "issues": [
    "No traffic has been recorded on this interconnect. Verify both sides are sending EDI documents.",
    "TP1 has no last-traffic timestamp — the interconnect may never have been used."
  ]
}
```

## Response Fields

| Field | Type | Description |
|---|---|---|
| `isHealthy` | boolean | `true` when all critical checks pass; `false` if any issue was found |
| `setupComplete` | boolean | `true` when the interconnect status is Completed (both sides accepted) |
| `hasTraffic` | boolean | `true` when at least one EDI document has flowed across this relationship |
| `tp1` | object | Health flags for the TP1 side of the interconnect |
| `tp1.isActive` | boolean | `true` when the TP1 ECGrid ID's lifecycle status is Active |
| `tp1.scheduledMove` | boolean | `true` when the TP1 ECGrid ID has a future-dated move scheduled via `ownerInfo.effective` |
| `tp1.lastTraffic` | string \| null | ISO 8601 timestamp of the most recent traffic from the TP1 side (null if none) |
| `tp2` | object | Health flags for the TP2 side — same shape as `tp1` |
| `tp2.isActive` | boolean | `true` when the TP2 ECGrid ID's lifecycle status is Active |
| `tp2.scheduledMove` | boolean | `true` when the TP2 ECGrid ID has a future-dated move scheduled |
| `tp2.lastTraffic` | string \| null | ISO 8601 timestamp of the most recent traffic from the TP2 side (null if none) |
| `issues` | array | Plain-language list of problems and warnings to relay to the caller. Empty when `isHealthy` is `true`. |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_partner_check-partner-config",
    "arguments": {
      "request": { "interconnectId": 12345 }
    }
  }
}
```

## Example Prompts

- `Is trading partner 12345 set up correctly?`
- `Why is traffic not flowing with interconnect 99999?`
- `Check the configuration for partner 55555`

## See Also

- [get-partner-by-id](./get-partner-by-id.md) — view the raw relationship profile (contacts, AS2 IDs, references)
- [test-partner-delivery](./test-partner-delivery.md) — actively send a test parcel to verify end-to-end delivery
- [get-partner-document-counts](./get-partner-document-counts.md) — view EDI document volume to confirm traffic history
