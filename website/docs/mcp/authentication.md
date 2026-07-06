{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP authentication reference - Greg Kolinski
*/}
---
title: Authentication
sidebar_position: 3
---

# Authentication

All requests to `https://mcp.ecgrid.io/mcp` require exactly one of the following:

| Method | Header | Format |
|---|---|---|
| API Key | `X-APIKey` | Your ECGrid API key from the [ECGrid Developer Portal](https://api.ecgridos.io/) |
| Bearer JWT | `Authorization: Bearer <token>` | HS256 JWT — contact [ECGrid Support](https://ecgrid.freshdesk.com/support/home) if your integration requires JWT auth |

Sending both headers, or neither, returns `401`. The raw API key never appears in server logs.

## Auth Levels

Your API key carries a permission tier that determines which operations are available. The `authLevel` field is returned in every tool response.

| Auth Level | Access Type | Description |
|---|---|---|
| `TPUser` | Read-only | Trading partner — read-only access scoped to a single trading partner relationship |
| `MailboxUser` | Standard | Standard access to a specific mailbox within a network |
| `MailboxAdmin` | Admin | Elevated administrative access to a specific mailbox |
| `NetworkUser` | Standard | Standard access across all mailboxes within your ECGrid network |
| `NetworkAdmin` | Admin | Full administrative access across your ECGrid network — broadest level available to customers |

All 36 tools are accessible at **Any** auth level, scoped to what your API key can see. A `NetworkAdmin` key sees all mailboxes on their network; a `MailboxUser` key sees only their assigned mailbox.

## Getting Your API Key

1. Go to the [ECGrid Developer Portal](https://api.ecgridos.io/)
2. Log in with your ECGrid account
3. Navigate to account settings
4. Copy your API key

> **Keep your API key private.** Do not share it, commit it to source control, or include it in client-side code. Treat it like a password.

## See Also

- [Quick Start](./quick-start.md) — connecting your AI tool
- [Protocol Reference](./protocol-reference.md) — HTTP headers, rate limits, error codes
