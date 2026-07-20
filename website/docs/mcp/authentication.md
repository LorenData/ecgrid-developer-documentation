---
title: Authentication
sidebar_position: 3
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP authentication reference - Greg Kolinski
2026-07-20: Multi-credential auth model — Connectivity, GPA/DataSync, Translation headers - Greg Kolinski
*/}

# Authentication

All requests to `https://mcp.ecgrid.io/mcp` require at least one credential header matching the products you want to use. A single connection can carry multiple headers — one per product.

## Which Credential to Use

| Product | Header | Credential |
|---|---|---|
| ECGrid Connectivity | `X-Connectivity-API-Key` | Your ECGrid API key |
| Translation | `X-Translation-API-Key` | Your Translation API key |
| GPA (DataSync) | `X-DataSync-API-Key` | Your GPA Personal Access Token (PAT) |

Supply the header for each product you want to use. Sending no recognized credential returns `401`. The raw credential never appears in server logs.

> 🔒 **Keep credentials out of chat.** Your API key or PAT goes in the config only — not in your conversation with the AI. Once configured, your AI connects automatically without needing the credential in any prompt. Treat your key and PAT like passwords: don't paste them into chat, don't share them, don't commit them to source control.

## Auth Levels (Connectivity)

Your ECGrid API key carries a permission tier that determines which Connectivity operations are available. The `authLevel` field is returned in every Connectivity tool response.

| Auth Level | Access Type | Description |
|---|---|---|
| `TPUser` | Read-only | Trading partner — read-only access scoped to a single trading partner relationship |
| `MailboxUser` | Standard | Standard access to a specific mailbox within a network |
| `MailboxAdmin` | Admin | Elevated administrative access to a specific mailbox |
| `NetworkUser` | Standard | Standard access across all mailboxes within your ECGrid network |
| `NetworkAdmin` | Admin | Full administrative access across your ECGrid network — broadest level available to customers |

All Connectivity tools are accessible at **Any** auth level, scoped to what your API key can see. A `NetworkAdmin` key sees all mailboxes on their network; a `MailboxUser` key sees only their assigned mailbox.

## Getting Your Credential

**ECGrid API key (Connectivity):**

1. Go to your ECGrid Portal
2. Log in with your ECGrid account
3. Navigate to account settings (Profile)
4. Copy your API key

**GPA Personal Access Token — PAT (DataSync):**

Your GPA PAT is issued from the GPA administration portal. Contact your GPA administrator if you do not have one.

**Translation API key:**

Your Translation API key is provided with your Translation product subscription.

## See Also

- [Quick Start](./quick-start.md) — connecting your AI tool
- [Protocol Reference](./protocol-reference.md) — HTTP headers, rate limits, error codes
