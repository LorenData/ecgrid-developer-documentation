# ECGrid MCP Documentation Section — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete MCP documentation section to the ECGrid Developer Documentation Portal covering the ECGrid MCP Server, 36 live tools, and all supporting reference pages.

**Architecture:** New `website/docs/mcp/` directory with top-level reference pages + a `tools/` subsection (one page per tool, one subdirectory per category). All tool content sourced from live `tools/list` data in `tools07062026.md`. Site config, sidebar, and homepage updated to surface MCP as a first-class API option at nav position 4.

**Tech Stack:** Docusaurus 3, TypeScript config, Markdown, React/TSX homepage, Node.js 20 LTS

**Branch:** `feature/mcp-docs-section`

**Source files:**
- `tools07062026.md` — live tool names, descriptions, inputSchema (root of repo)
- `C:\local docs\ECGrid-MCP\README.md` — setup, auth, protocol, troubleshooting
- `C:\local docs\ECGrid-MCP\ECGrid-MCP-Agent-Guide.md` — developer patterns, chat loops
- `C:\local docs\ECGrid-MCP\ECGrid-MCP-Release-Notes.md` — release history, response shapes

---

## File Map

### Files to modify
| File | Change |
|---|---|
| `website/sidebars.ts` | Add `mcpSidebar` entry |
| `website/docusaurus.config.ts` | Add MCP navbar item + footer entries |
| `website/src/pages/index.tsx` | Add MCP card, button, badge, quick link |
| `website/src/css/custom.css` | Add `mcpPill` CSS class |
| `website/src/pages/index.module.css` | Add `cardMcp`, `badgeMcp` CSS classes |
| `website/docs/soap-api/_category_.json` | position: 4 → 5 |
| `website/docs/common-operations/_category_.json` | position: 5 → 6 |
| `website/docs/appendix/_category_.json` | position: 6 → 7 |
| `website/docs/code-samples/_category_.json` | position: 7 → 8 |
| `website/docs/changelog/_category_.json` | position: 8 → 9 |

### Files to create (~68 new files)
All under `website/docs/mcp/` unless noted.

```
_category_.json
overview.md
quick-start.md
authentication.md
protocol-reference.md
building-agents.md
resources-and-prompts.md
other-ai-platforms.md
troubleshooting.md
connecting/_category_.json
connecting/claude-desktop.md
connecting/cursor-windsurf.md
connecting/developer-http.md
tools/_category_.json
tools/overview.md
tools/system/_category_.json
tools/system/hello-world.md
tools/system/get-version.md
tools/system/get-status-list.md
tools/users/_category_.json
tools/users/get-user-me.md
tools/users/get-user-by-id.md
tools/users/get-user-by-login.md
tools/users/list-users.md
tools/network/_category_.json
tools/network/get-network-by-id.md
tools/mailboxes/_category_.json
tools/mailboxes/get-mailbox-by-id.md
tools/mailboxes/list-mailboxes.md
tools/mailboxes/get-mailbox-by-name.md
tools/ecgrid-ids/_category_.json
tools/ecgrid-ids/get-ecgrid-id-by-id.md
tools/ecgrid-ids/find-edi-ids.md
tools/ecgrid-ids/list-ecgrid-ids-by-mailbox.md
tools/partners/_category_.json
tools/partners/get-partner-by-id.md
tools/partners/list-partners.md
tools/partners/check-partner-config.md
tools/partners/test-partner-delivery.md
tools/partners/get-partner-document-counts.md
tools/comms/_category_.json
tools/comms/get-comm-by-id.md
tools/comms/list-comms.md
tools/comms/find-comms.md
tools/comms/test-comm.md
tools/comms/check-ftp-access.md
tools/parcels/_category_.json
tools/parcels/get-parcel-by-id.md
tools/parcels/list-inbox-parcels.md        (stub)
tools/parcels/list-outbox-parcels.md       (stub)
tools/parcels/list-pending-inbox-parcels.md (stub)
tools/interchanges/_category_.json
tools/interchanges/get-interchange-by-id.md
tools/interchanges/get-document-counts-by-status.md
tools/transactions/_category_.json
tools/transactions/search-transactions.md
tools/callbacks/_category_.json
tools/callbacks/get-callback-event-by-id.md
tools/callbacks/get-callback-queue-by-id.md
tools/callbacks/list-callback-events.md
tools/callbacks/list-callback-queue.md
tools/carbon-copies/_category_.json
tools/carbon-copies/get-carbon-copy-by-id.md
tools/carbon-copies/list-carbon-copies.md
tools/keys/_category_.json
tools/keys/get-key.md
tools/keys/list-keys.md
website/docs/changelog/mcp-release-notes.md
```

---

## Task 1: Shift existing sidebar positions

**Files:**
- Modify: `website/docs/soap-api/_category_.json`
- Modify: `website/docs/common-operations/_category_.json`
- Modify: `website/docs/appendix/_category_.json`
- Modify: `website/docs/code-samples/_category_.json`
- Modify: `website/docs/changelog/_category_.json`

- [ ] **Step 1: Update soap-api position**

Read current content of `website/docs/soap-api/_category_.json`, then update `position` to 5:
```json
{
  "label": "SOAP API",
  "position": 5,
  "link": {
    "type": "generated-index"
  }
}
```

- [ ] **Step 2: Update common-operations position**

Read current content of `website/docs/common-operations/_category_.json`, then update `position` to 6.

- [ ] **Step 3: Update appendix position**

Read current content of `website/docs/appendix/_category_.json`, then update `position` to 7.

- [ ] **Step 4: Update code-samples position**

Read current content of `website/docs/code-samples/_category_.json`, then update `position` to 8.

- [ ] **Step 5: Update changelog position**

Read current content of `website/docs/changelog/_category_.json`, then update `position` to 9.

- [ ] **Step 6: Verify build still passes**

```bash
cd website && npm run build 2>&1 | tail -20
```
Expected: `Generated static files in "build".` with no ERR lines.

- [ ] **Step 7: Commit**

```bash
git add website/docs/soap-api/_category_.json website/docs/common-operations/_category_.json website/docs/appendix/_category_.json website/docs/code-samples/_category_.json website/docs/changelog/_category_.json
git commit -m "docs: shift sidebar positions to make room for MCP at position 4"
```

---

## Task 2: Add MCP to sidebars.ts and docusaurus.config.ts

**Files:**
- Modify: `website/sidebars.ts`
- Modify: `website/docusaurus.config.ts`

- [ ] **Step 1: Add mcpSidebar to sidebars.ts**

Read `website/sidebars.ts` first. Add `mcpSidebar` after `soapApiSidebar`:

```typescript
mcpSidebar: [
  {
    type: 'autogenerated',
    dirName: 'mcp',
  },
],
```

- [ ] **Step 2: Add MCP navbar item to docusaurus.config.ts**

Read `website/docusaurus.config.ts` first. In the `navbar.items` array, add the MCP entry after the SOAP API item and before the Common Operations item:

```typescript
{
  type: "docSidebar",
  sidebarId: "mcpSidebar",
  position: "left",
  label: "MCP",
},
```

- [ ] **Step 3: Add MCP footer entries to docusaurus.config.ts**

In the `footer.links` array, add `MCP` to the Documentation column items (after SOAP API entry):

```typescript
{ label: "MCP", to: "/docs/mcp/overview" },
```

Add to the Live References column items:

```typescript
{
  label: "ECGrid MCP Server",
  href: "https://mcp.ecgrid.io",
},
```

- [ ] **Step 4: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```
Expected: build succeeds (MCP sidebar will be empty but that's not a build error).

- [ ] **Step 5: Commit**

```bash
git add website/sidebars.ts website/docusaurus.config.ts
git commit -m "config: add MCP sidebar, navbar item, and footer entries"
```

---

## Task 3: Update homepage — CSS and index.tsx

**Files:**
- Modify: `website/src/css/custom.css`
- Modify: `website/src/pages/index.module.css`
- Modify: `website/src/pages/index.tsx`

- [ ] **Step 1: Add mcpPill to custom.css**

Read `website/src/css/custom.css` first. Add the MCP pill class alongside the existing pill classes:

```css
.mcpPill {
  background: #F26522;
  color: #fff;
  border-radius: 4px;
  padding: 2px 10px;
  font-size: 0.78rem;
  font-weight: 600;
  margin: 0 4px;
  white-space: nowrap;
}
```

- [ ] **Step 2: Add cardMcp and badgeMcp to index.module.css**

Read `website/src/pages/index.module.css` first. Add MCP card and badge variant classes alongside the existing `cardNew`, `cardCatalog`, `badgeNew`, `badgeCatalog` classes. Follow the exact same pattern already used for those classes — read the file to find the exact CSS, then add:

```css
.cardMcp {
  border-top: 4px solid #F26522;
}

.badgeMcp {
  background: #F26522;
  color: #fff;
}
```

- [ ] **Step 3: Update index.tsx — add mcpPill to hero badge strip**

Read `website/src/pages/index.tsx` first. In the `Hero` function, locate the `heroBadge` paragraph and add the MCP pill after the Catalog pill:

```tsx
<span className={styles.mcpPill}>ECGrid MCP — New</span>
```

- [ ] **Step 4: Update index.tsx — add MCP hero button**

In the `heroButtons` div, add the MCP button after the SOAP API Reference button and before Transformation API:

```tsx
<Link className="button button--outline button--lg" to="/docs/mcp/overview">
  ECGrid MCP
</Link>
```

- [ ] **Step 5: Update index.tsx — add ApiCard badgeVariant and cardVariantClass**

In the `ApiCard` component, update the `cardVariantClass` and `badgeVariantClass` ternary chains to include `'mcp'`:

```tsx
const cardVariantClass =
  badgeVariant === 'active'  ? styles.cardActive :
  badgeVariant === 'new'     ? styles.cardNew :
  badgeVariant === 'catalog' ? styles.cardCatalog :
  badgeVariant === 'mcp'     ? styles.cardMcp :
  styles.cardLegacy;

const badgeVariantClass =
  badgeVariant === 'legacy'  ? styles.badgeLegacy :
  badgeVariant === 'new'     ? styles.badgeNew :
  badgeVariant === 'catalog' ? styles.badgeCatalog :
  badgeVariant === 'mcp'     ? styles.badgeMcp :
  undefined;
```

Also update the `ApiCardProps` type to include `'mcp'` in the `badgeVariant` union:

```tsx
badgeVariant: 'active' | 'legacy' | 'new' | 'catalog' | 'mcp';
```

- [ ] **Step 6: Update index.tsx — add MCP API card**

In the `apiCards` array, add the MCP card after the Catalog card:

```tsx
{
  badge: 'New',
  badgeVariant: 'mcp',
  title: 'ECGrid MCP',
  description: 'Connect any MCP-compatible AI tool directly to your ECGrid account. Natural language access to your network, mailboxes, trading partners, and transactions — no custom integration code.',
  bullets: [
    '36 tools across 13 categories',
    'Claude Desktop, Cursor, Windsurf, and any HTTP agent',
    'X-APIKey authentication · mcp.ecgrid.io',
    'Interactive UI components in Claude Desktop and Claude.ai',
  ],
  to: '/docs/mcp/overview',
  linkLabel: 'MCP Reference →',
},
```

- [ ] **Step 7: Update index.tsx — add MCP quick link**

In the `quickLinks` array, add:

```tsx
{ label: 'Quick Start — MCP', to: '/docs/mcp/quick-start' },
```

- [ ] **Step 8: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```
Expected: build succeeds with no TypeScript errors.

- [ ] **Step 9: Commit**

```bash
git add website/src/css/custom.css website/src/pages/index.module.css website/src/pages/index.tsx
git commit -m "feat: add MCP card, button, badge, and quick link to homepage"
```

---

## Task 4: Create MCP section — _category_.json and overview pages

**Files:** `website/docs/mcp/` (create directory and top-level pages)

- [ ] **Step 1: Create _category_.json**

```json
{
  "label": "MCP",
  "position": 4,
  "link": {
    "type": "generated-index",
    "description": "Connect any MCP-compatible AI tool to your ECGrid account. Natural language access to your network, mailboxes, trading partners, and transactions."
  }
}
```
Save to `website/docs/mcp/_category_.json`.

- [ ] **Step 2: Create overview.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Initial MCP section overview - Greg Kolinski -->
---
title: MCP Overview
sidebar_position: 1
---

# ECGrid MCP

**You create the experience. We power the connections.**

The ECGrid MCP Server brings ECGrid's full B2B connectivity layer directly into AI agents, AI assistants, and AI-powered applications via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

## What Is MCP?

The Model Context Protocol is an open standard that lets AI tools connect to external services as native capabilities. Once the ECGrid MCP Server is connected, your AI can call ECGrid operations directly — no custom integration code required per operation.

## The ECGrid MCP Server

| Item | Value |
|---|---|
| Server URL | `https://mcp.ecgrid.io/mcp` |
| Protocol | MCP over HTTP (JSON-RPC 2.0) |
| MCP Version | `2024-11-05` |
| Authentication | `X-APIKey` header (your ECGrid API key) |
| Tools | 36 tools across 13 categories |

## Who This Is For

**ECGrid customers** — connect Claude Desktop (or any MCP-compatible AI tool) to your ECGrid account in about 5 minutes. Ask your AI about trading partners, transaction history, mailboxes, and network status in plain language instead of logging into the portal.

**Developers** — add ECGrid B2B capabilities to any AI agent, chatbot, or automation workflow. All tools return structured JSON for programmatic consumption. A subset of tools additionally render an interactive UI component in Claude Desktop and Claude.ai.

## Next Steps

- **New to MCP?** → [Quick Start](./quick-start.md)
- **Setting up Claude Desktop?** → [Connect Your AI Tool](./connecting/claude-desktop.md)
- **Building an agent?** → [Building Agents](./building-agents.md)
- **Looking up a specific tool?** → [Tools Reference](./tools/overview.md)
```
Save to `website/docs/mcp/overview.md`.

- [ ] **Step 3: Create quick-start.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Initial MCP quick start - Greg Kolinski -->
---
title: Quick Start
sidebar_position: 2
---

# Quick Start

Connect the ECGrid MCP Server to your AI tool in four steps.

## Step 1 — Get Your ECGrid API Key

Go to the [ECGrid Developer Portal](https://api.ecgridos.io/), log in, and copy your API key from account settings. This is the same key used for the REST and SOAP APIs — no new account needed.

## Step 2 — Check Node.js (Claude Desktop only)

> **Developers calling the MCP server directly over HTTP:** skip this step. Node.js is not required for HTTP integrations.

Open a terminal and run:

```bash
node --version
```

You need **v18 or later**. If Node.js is missing or too old, install the LTS version from [nodejs.org](https://nodejs.org).

> Node.js is required by Claude Desktop as a local bridge to remote MCP servers — not by ECGrid. This is a one-time install.

## Step 3 — Add the Config Block

Add the following to your `claude_desktop_config.json` (replace `YOUR_API_KEY_HERE`):

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

Config file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Or open it directly: Claude Desktop → hamburger menu (☰) → Settings → Developer → Edit Config.

Fully restart Claude Desktop after saving.

## Step 4 — Test the Connection

Type this prompt in your AI tool:

```
Test the ECGrid MCP connection
```

A successful response returns your ECGrid login name, auth level, network ID, and current server time.

## Need More Detail?

- [Full Claude Desktop setup](./connecting/claude-desktop.md) — merge instructions, hidden folder tips, troubleshooting
- [Cursor, Windsurf, and other tools](./connecting/cursor-windsurf.md)
- [Direct HTTP connection (developers)](./connecting/developer-http.md)
```
Save to `website/docs/mcp/quick-start.md`.

- [ ] **Step 4: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```
Expected: build succeeds.

- [ ] **Step 5: Commit**

```bash
git add website/docs/mcp/
git commit -m "docs(mcp): scaffold section with _category_.json, overview, and quick-start"
```

---

## Task 5: Create authentication.md and protocol-reference.md

**Files:** `website/docs/mcp/authentication.md`, `website/docs/mcp/protocol-reference.md`

- [ ] **Step 1: Create authentication.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: MCP authentication reference - Greg Kolinski -->
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
```
Save to `website/docs/mcp/authentication.md`.

- [ ] **Step 2: Create protocol-reference.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: MCP protocol reference - Greg Kolinski -->
---
title: Protocol Reference
sidebar_position: 4
---

# Protocol Reference

Technical reference for developers calling the ECGrid MCP Server directly over HTTP.

## HTTP Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/mcp` | JSON-RPC 2.0 entry point — `initialize`, `tools/list`, `tools/call` |
| `GET` | `/mcp` | Server-sent event stream for server-initiated notifications |
| `GET` | `/health/live` | Liveness probe — `200 {"status":"healthy"}` if the process is running |
| `GET` | `/health/ready` | Readiness probe — `200` when healthy, `503` when not ready |

Health probes are anonymous and exempt from rate limiting. POST body size is capped at **64 KB**.

## Required Headers

Every POST to `/mcp` requires:

```
Content-Type: application/json
Accept: application/json, text/event-stream
X-APIKey: YOUR_API_KEY_HERE
```

Omitting or incorrectly setting `Accept` returns `406 Not Acceptable`.

## Response Format — Server-Sent Events

All responses arrive as SSE envelopes:

```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

**To parse:** read the body as text, find the line starting with `data: `, strip the prefix, and parse the remainder as JSON.

> MCP-compatible AI tools (Claude Desktop, Cursor, Windsurf) handle SSE automatically. This only affects developers making direct HTTP calls.

## Tool Result — Two-Step Parse

Tool results are wrapped as a JSON string inside `content[0].text`. Parsing happens in two steps:

```
SSE data: line
  → JSON.parse() → JSON-RPC result
    → result.content[0].text  (this is a JSON string)
      → JSON.parse() → { fieldName: value, ... }
```

```csharp
// Step 1 — unwrap SSE and JSON-RPC envelope
var body = await response.Content.ReadAsStringAsync();
var dataLine = body.Split('\n').FirstOrDefault(l => l.StartsWith("data: "))?.Substring(6) ?? body;
var envelope = JsonDocument.Parse(dataLine).RootElement;

// Step 2 — parse content[0].text as JSON
var resultText = envelope.GetProperty("result").GetProperty("content")[0].GetProperty("text").GetString()!;
var data = JsonDocument.Parse(resultText).RootElement;
```

## Initialization

Every MCP client must send `initialize` before calling tools. MCP-compatible tools handle this automatically.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": { "name": "your-client", "version": "1.0" }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "logging": {}, "tools": {} },
    "serverInfo": { "name": "ECGrid.Mcp.Server", "version": "1.0.0.0" }
  }
}
```

## Rate Limiting

| Limit | Value | Response | `Retry-After` |
|---|---|---|---|
| Per-IP request rate | 100 req/min | `429 Too Many Requests` | 60 seconds |
| Global concurrency | 500 simultaneous | `503 Service Unavailable` | 1 second |

Both responses include `{"code":"RATE_LIMITED","retryable":true}`.

## Error Codes

| HTTP | Meaning |
|---|---|
| `200` | Success |
| `400` | Malformed JSON or invalid JSON-RPC |
| `401` | Missing, invalid, or ambiguous credential |
| `406` | `Accept` header missing or invalid |
| `413` | POST body exceeds 64 KB |
| `415` | POST body is not JSON |
| `429` | Per-IP rate limit exceeded |
| `503` | Global concurrency cap reached |

JSON-RPC application errors use the standard error object:
```json
{ "jsonrpc": "2.0", "id": 1, "error": { "code": -32600, "message": "description" } }
```

## Health Probes

```bash
# Liveness — is the process up?
GET https://mcp.ecgrid.io/health/live
# → 200 {"status":"healthy"}

# Readiness — is it accepting traffic?
GET https://mcp.ecgrid.io/health/ready
# → 200 healthy/degraded, 503 not ready
```

No authentication required. Exempt from rate limiting.

## MCP Inspector

Use the official [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to explore tools interactively:

```bash
npx @modelcontextprotocol/inspector "https://mcp.ecgrid.io/mcp" --header "X-APIKey:YOUR_API_KEY_HERE"
```
```
Save to `website/docs/mcp/protocol-reference.md`.

- [ ] **Step 3: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```

- [ ] **Step 4: Commit**

```bash
git add website/docs/mcp/authentication.md website/docs/mcp/protocol-reference.md
git commit -m "docs(mcp): add authentication and protocol reference pages"
```

---

## Task 6: Create connecting/ subsection

**Files:** `website/docs/mcp/connecting/`

- [ ] **Step 1: Create connecting/_category_.json**

```json
{
  "label": "Connect Your AI Tool",
  "position": 5
}
```

- [ ] **Step 2: Create claude-desktop.md**

Source content from `C:\local docs\ECGrid-MCP\README.md` sections: "Step 3 — Connect Your AI Tool → Claude Desktop", "Let Claude Install It For You", and "Step 3a" hidden folder instructions. Reformat for Docusaurus page style with AI attribution header.

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Claude Desktop connection guide - Greg Kolinski -->
---
title: Claude Desktop
sidebar_position: 1
---

# Connect Claude Desktop

Full setup guide for connecting the ECGrid MCP Server to Claude Desktop on macOS and Windows.

## Let Claude Install It For You

The fastest way — paste one of these prompts into Claude and let it handle the setup.

### Option A — Claude Desktop (Fully Automated)

> Use this if you are already inside Claude Desktop. Claude Desktop has computer use capabilities — it can open a terminal, check for Node.js, locate and edit your config file, and verify the connection.

Copy and paste into Claude Desktop:

```
I want to connect the ECGrid MCP server to Claude Desktop. Please set it up for me by doing the following — ask my permission before taking any action that changes my system:

1. Ask me for my ECGrid API key (I can get it from https://api.ecgridos.io/ → account settings if I don't have it handy)
2. Open a terminal and run `node --version` to check if Node.js is installed
   - If Node.js v18 or higher is installed: confirm it and continue
   - If Node.js is missing or below v18: tell me what you found, ask my permission, then download and run the LTS installer from https://nodejs.org
3. Locate my claude_desktop_config.json file and open it
4. Add the ECGrid MCP block in the correct location, safely merging with any existing content
5. Fill in my API key in the X-APIKey line — no spaces around the colon
6. Show me the final file contents before saving and ask my permission to save
7. After I confirm, save the file and ask me to fully restart Claude Desktop
8. After I restart, test the connection by running: Test the ECGrid MCP connection

The ECGrid MCP server URL is https://mcp.ecgrid.io/mcp. Authentication uses the X-APIKey header. The mcpServers block to add is:
{
  "ecgrid-mcp": {
    "command": "npx",
    "args": ["-y","mcp-remote","https://mcp.ecgrid.io/mcp","--header","X-APIKey:PLACEHOLDER","--transport","http-only"]
  }
}
```

### Option B — Claude.ai Web or Mobile (Step-by-Step Guidance)

Copy and paste into any Claude conversation for guided manual setup.

```
I want to connect the ECGrid MCP server to Claude Desktop. Please guide me through setup step by step. Ask me for my ECGrid API key, my OS, then walk me through Node.js check/install, finding the config file, and adding the ECGrid MCP block with my key filled in. Server URL: https://mcp.ecgrid.io/mcp, auth header: X-APIKey.
```

---

## Manual Setup

### Step 1 — Check and Install Node.js

Open a terminal and run:

```
node --version
```

You need **v18 or later**. Install from [nodejs.org](https://nodejs.org) if missing or too old.

:::tip macOS — opening Terminal
Press `Cmd + Space`, type `Terminal`, press Enter.
:::

:::tip Windows — opening Command Prompt
Press the Windows key, type `cmd`, press Enter.
:::

### Step 2 — Find Your Config File

The fastest way: Claude Desktop → hamburger menu (☰) → **Settings** → **Developer** → **Edit Config**.

Manual paths:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

:::caution macOS — Library folder is hidden
Use **Go** → **Go to Folder** (Cmd+Shift+G) and paste `~/Library/Application Support/Claude/`.
:::

:::caution Windows — AppData folder is hidden
Paste `%APPDATA%\Claude\` directly into the File Explorer address bar.
:::

### Step 3 — Add the Config Block

**New file or empty file** — paste this exactly:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.ecgrid.io/mcp",
        "--header",
        "X-APIKey:YOUR_API_KEY_HERE",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

**File already has content** — add the `"ecgrid-mcp"` block inside the existing `"mcpServers"` section. Never duplicate the outer `{}` or add a second `"mcpServers"` key. Validate with [jsonlint.com](https://jsonlint.com) if unsure.

### Step 4 — Restart and Test

Fully close and reopen Claude Desktop, then type:

```
Test the ECGrid MCP connection
```

A successful response returns your ECGrid login name, auth level, and network ID.

## Troubleshooting

See the [Troubleshooting](../troubleshooting.md) page for a full table of error causes and fixes.
```
Save to `website/docs/mcp/connecting/claude-desktop.md`.

- [ ] **Step 3: Create cursor-windsurf.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Cursor/Windsurf connection guide - Greg Kolinski -->
---
title: Cursor, Windsurf & Others
sidebar_position: 2
---

# Cursor, Windsurf & Other MCP Tools

Many MCP-compatible tools support remote MCP servers natively — no Node.js required.

## Cursor

Add to `~/.cursor/mcp.json` or via **Settings → MCP**:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "url": "https://mcp.ecgrid.io/mcp",
      "headers": {
        "X-APIKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## Windsurf

Add via **Settings → MCP Servers → Add Server**, or edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "ecgrid-mcp": {
      "serverUrl": "https://mcp.ecgrid.io/mcp",
      "headers": {
        "X-APIKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## Other MCP-Compatible Tools

Use the same server URL and header for any tool that supports remote MCP servers:

| Item | Value |
|---|---|
| Server URL | `https://mcp.ecgrid.io/mcp` |
| Auth header | `X-APIKey: YOUR_API_KEY_HERE` |
| Transport | HTTP (SSE response) |

Config formats vary by tool version — check your tool's documentation. You can also paste the [ECGrid MCP README](https://api.ecgridos.io/docs/mcp/overview) into your AI and ask: *"How do I add this MCP server to [tool name]?"*

## Verify the Connection

After configuring, test with:

```
Test the ECGrid MCP connection
```

Expected: your ECGrid login name, auth level, network ID, and server time.
```
Save to `website/docs/mcp/connecting/cursor-windsurf.md`.

- [ ] **Step 4: Create developer-http.md**

Source from `C:\local docs\ECGrid-MCP\README.md` "Developer Reference" section and `ECGrid-MCP-Agent-Guide.md`.

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Developer HTTP connection guide - Greg Kolinski -->
---
title: Direct HTTP (Developers)
sidebar_position: 3
---

# Direct HTTP Connection

Call the ECGrid MCP Server directly over HTTP from any language or framework. No Node.js, no SDK, no local bridge.

## Server Details

| Item | Value |
|---|---|
| URL | `https://mcp.ecgrid.io/mcp` |
| Protocol | MCP over HTTP (JSON-RPC 2.0) |
| Auth | `X-APIKey: YOUR_API_KEY_HERE` |
| Accept | `application/json, text/event-stream` (required — 406 without it) |
| Response format | Server-Sent Events (SSE) |

## Quick Test — curl

```bash
curl -s -X POST https://mcp.ecgrid.io/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "X-APIKey: YOUR_API_KEY_HERE" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"connectivity_system_hello-world","arguments":{"request":{"name":"Test"}}}}'
```

## Request Lifecycle

```
1. POST initialize  →  confirm protocol version
2. POST tools/list  →  discover available tools and their schemas
3. POST tools/call  →  call tools
```

The server is **stateless** — each request carries the full credential. No session token to manage.

## C# Example

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

var client = new HttpClient();
client.DefaultRequestHeaders.Add("X-APIKey", "YOUR_API_KEY_HERE");
client.DefaultRequestHeaders.Add("Accept", "application/json, text/event-stream");

var baseUrl = "https://mcp.ecgrid.io/mcp";

async Task<JsonElement> PostAsync(object payload)
{
    var json = JsonSerializer.Serialize(payload);
    var response = await client.PostAsync(baseUrl,
        new StringContent(json, Encoding.UTF8, "application/json"));
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    var dataLine = body.Split('\n')
        .FirstOrDefault(l => l.StartsWith("data: "))?.Substring(6) ?? body;
    var envelope = JsonDocument.Parse(dataLine).RootElement;
    var resultText = envelope.GetProperty("result")
        .GetProperty("content")[0].GetProperty("text").GetString()!;
    return JsonDocument.Parse(resultText).RootElement;
}

var result = await PostAsync(new {
    jsonrpc = "2.0", id = 1, method = "tools/call",
    @params = new {
        name = "connectivity_system_hello-world",
        arguments = new { request = new { name = "My Agent" } }
    }
});
Console.WriteLine(result);
```

## See Also

- [Protocol Reference](../protocol-reference.md) — full SSE format, two-step parse, error codes
- [Building Agents](../building-agents.md) — chat loop patterns, multi-LLM examples
```
Save to `website/docs/mcp/connecting/developer-http.md`.

- [ ] **Step 5: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```

- [ ] **Step 6: Commit**

```bash
git add website/docs/mcp/connecting/
git commit -m "docs(mcp): add connecting subsection — Claude Desktop, Cursor/Windsurf, developer HTTP"
```

---

## Task 7: Create building-agents.md and remaining top-level pages

**Files:** `website/docs/mcp/building-agents.md`, `resources-and-prompts.md`, `other-ai-platforms.md`, `troubleshooting.md`

- [ ] **Step 1: Create building-agents.md**

Source: `C:\local docs\ECGrid-MCP\ECGrid-MCP-Agent-Guide.md` — use full content, reformatted. Include: request lifecycle, system prompt guidance, complete C#/JS/Python chat loops (Anthropic API), OpenAI examples, tool schema translation table.

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Building agents guide - Greg Kolinski -->
---
title: Building Agents
sidebar_position: 6
---

# Building Agents

Guide for developers building AI-powered features — chatbots, agents, or automated workflows — that call ECGrid services via the MCP Server.
```

Then include the full content from `ECGrid-MCP-Agent-Guide.md`, reformatted into Docusaurus markdown sections. Key sections to preserve:
- Request Lifecycle (stateless, initialize/list/call flow)
- Response Format (SSE, two-step parse)
- Tool Result Structure (content[0].text)
- Interactive UI Components
- Error Handling (JSON-RPC errors, HTTP errors, retry pattern)
- Auth Levels
- Health Checks
- Complete C# / JavaScript / Python examples
- Building a Chat Agent (system prompt, Anthropic API chat loop in JS, Python, C#)
- Using ECGrid with Other LLMs (OpenAI examples, schema translation table)

Save to `website/docs/mcp/building-agents.md`.

- [ ] **Step 2: Create resources-and-prompts.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: MCP resources and prompts reference - Greg Kolinski -->
---
title: Resources & Prompts
sidebar_position: 7
---

# Resources & Prompts

The ECGrid MCP Server exposes MCP Resources and MCP Prompts in addition to tools. These do **not** appear in `tools/list` — they are available to MCP clients that request them via `resources/list` and `prompts/list`.

## MCP Resources

Resources are server-side reference data that AI agents can read during a session.

| Resource | Description |
|---|---|
| `Glossary` | ECGrid terminology reference — qualifier codes, status code meanings, object type definitions |
| `InterchangeStatus` | Complete interchange status code catalog with descriptions and severity levels |
| `ParcelStatus` | Complete parcel status code catalog with descriptions and severity levels |

> MCP-compatible AI tools (Claude Desktop, Cursor, Windsurf) load resources automatically when the AI needs them. Developers can request them via `resources/read`.

## MCP Prompts

Prompts are guided multi-step sequences exposed by the server.

| Prompt | Description |
|---|---|
| `InvestigatePartner` | Guided sequence for diagnosing a trading partner relationship — checks config, traffic history, and delivery status in order |
| `TriageStuckInterchange` | Guided sequence for triaging a stuck or pending interchange — walks through parcel status, route config, and retry state |

> Use prompts by asking your AI: *"Investigate this trading partner"* or *"Triage this stuck interchange"* — the AI will invoke the guided sequence automatically if your MCP client supports prompts.

## Status Code Reference

The `connectivity_system_get-status-list` tool returns the complete ECGrid status-code catalog at runtime — use it to resolve any status code seen on parcels or interchanges.

See also: [get-status-list](./tools/system/get-status-list.md)
```
Save to `website/docs/mcp/resources-and-prompts.md`.

- [ ] **Step 3: Create other-ai-platforms.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: Other AI platforms page - Greg Kolinski -->
---
title: Other AI Platforms
sidebar_position: 8
---

# Other AI Platforms

The ECGrid MCP Server uses the open MCP standard. Any AI tool or platform that supports MCP natively can connect using the server URL and API key — no additional setup required.

## Platforms Without Native MCP Support

For platforms that do not yet support MCP natively — including ChatGPT, Grok, and others — direct MCP connection is not currently available. ECGrid provides a full REST API that any platform can call directly:

- **ECGrid REST API**: [rest.ecgrid.io](https://rest.ecgrid.io/index.html) — full interactive documentation
- **OpenAPI / Swagger spec**: [rest.ecgrid.io/swagger/v2/swagger.json](https://rest.ecgrid.io/swagger/v2/swagger.json) — import into ChatGPT Custom Actions, LangChain, or any OpenAPI-compatible toolchain

The REST API uses the same ECGrid API key (`X-APIKey` header) and covers the full breadth of ECGrid operations.

## Using ECGrid Tools with OpenAI and Other LLMs

The ECGrid MCP client HTTP code is identical regardless of which LLM you use. Only the LLM client and tool schema format change. See the [Building Agents](./building-agents.md) page for the OpenAI chat loop examples and the Anthropic/OpenAI/Gemini tool schema translation table.
```
Save to `website/docs/mcp/other-ai-platforms.md`.

- [ ] **Step 4: Create troubleshooting.md**

Source from `C:\local docs\ECGrid-MCP\README.md` "Troubleshooting" section — full table.

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: MCP troubleshooting page - Greg Kolinski -->
---
title: Troubleshooting
sidebar_position: 9
---

# Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or missing API key | Verify `X-APIKey` value — no spaces around the colon |
| `406 Not Acceptable` | Missing or incorrect `Accept` header | Set `Accept: application/json, text/event-stream` on every request |
| `429 Too Many Requests` | Per-IP rate limit hit | Wait 60 seconds and retry — check `Retry-After` header |
| `503 Service Unavailable` | Server concurrency cap reached | Wait 1 second and retry — this is transient |
| `Connection refused` | Incorrect server URL | Use `https://mcp.ecgrid.io/mcp` exactly |
| Tool not appearing in AI assistant | Config not loaded | Fully restart the AI application after saving the config file |
| Can't find the config file | Unsure of location | Claude Desktop → hamburger menu → Settings → Developer → Edit Config |
| Can't find the config file on macOS | Library folder is hidden | Use Go → Go to Folder, paste `~/Library/Application Support/Claude/` |
| Can't find the config file on Windows | AppData folder is hidden | Paste `%APPDATA%\Claude\` into the File Explorer address bar |
| `node: command not found` | Node.js not installed | See [Quick Start](./quick-start.md) Step 2 — Claude Desktop users only |
| Node.js version too old | Version below v18 | Install the LTS version from [nodejs.org](https://nodejs.org) |
| JSON parse error on config file | Malformed JSON | Paste your config into [jsonlint.com](https://jsonlint.com) to find the error |
| ECGrid block not working despite no error | `mcpServers` block placed outside main object | The block must be inside the single outer `{}` — see [Claude Desktop setup](./connecting/claude-desktop.md) |
| `loginName` shows unexpected value | Wrong API key | Confirm the key at the [ECGrid Developer Portal](https://api.ecgridos.io/) |
| `413 Payload Too Large` | Request body over 64 KB | Reduce request payload size |
| Empty `tools/list` response | Server unreachable or bad auth | Check API key and network connectivity; verify URL |

> **Still stuck?** Paste the [ECGrid MCP Overview](./overview.md) into Claude or any AI assistant and describe what you're seeing. The AI can help diagnose the issue step by step. Or contact [ECGrid Support](https://ecgrid.freshdesk.com/support/home).
```
Save to `website/docs/mcp/troubleshooting.md`.

- [ ] **Step 5: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```

- [ ] **Step 6: Commit**

```bash
git add website/docs/mcp/building-agents.md website/docs/mcp/resources-and-prompts.md website/docs/mcp/other-ai-platforms.md website/docs/mcp/troubleshooting.md
git commit -m "docs(mcp): add building-agents, resources-and-prompts, other-ai-platforms, troubleshooting"
```

---

## Task 8: Create tools/ structure, overview, and system tools

**Files:** `website/docs/mcp/tools/`

The tool page template below is used for **every** tool page in Tasks 8–20. The content for each tool — description, parameters, response shape — comes from `tools07062026.md` at the line numbers listed per task.

**Tool page template:**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: [tool display name] MCP tool reference - Greg Kolinski -->
---
title: [display name]
---

# [display name]

[Description from tools07062026.md — verbatim]

:::info Interactive UI Component
This tool renders a visual widget in Claude Desktop and Claude.ai alongside the AI's response.
:::
[omit the :::info block if the tool has no _meta.ui.resourceUri in tools07062026.md]

## Tool Name

```
connectivity_[category]_[slug]
```

## Auth Level Required

Any (scoped to caller's APIKey)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
[rows from inputSchema.properties.request.properties in tools07062026.md]

## Response

[One sentence from release notes describing return value]

```json
[Example response from release notes]
```

## Response Fields

| Field | Type | Description |
|---|---|---|
[rows from release notes return shape]

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_[category]_[slug]",
    "arguments": {
      "request": {
        [example field from inputSchema]
      }
    }
  }
}
```

## Example Prompts

[2-3 natural language prompts that invoke this tool — omit for system/diagnostic tools]

## See Also

[Links to related tools and REST equivalent where applicable]
```

- [ ] **Step 1: Create tools/_category_.json**

```json
{ "label": "Tools Reference", "position": 10 }
```

- [ ] **Step 2: Create tools/overview.md**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: MCP tools overview - Greg Kolinski -->
---
title: Tools Overview
sidebar_position: 1
---

# Tools Reference

The ECGrid MCP Server exposes 36 tools across 13 categories. All tools are prefixed `connectivity_` and return structured JSON data.

Call `tools/list` at startup to get the current complete tool list with full input schemas — new tools are added regularly and the response is always authoritative.

## Tool Categories

| Category | Tools | Interactive UI |
|---|---|---|
| [System](./system/) | `hello-world`, `get-version`, `get-status-list` | — |
| [Users](./users/) | `get-user-me`, `get-user-by-id`, `get-user-by-login`, `list-users` | — |
| [Network](./network/) | `get-network-by-id` | — |
| [Mailboxes](./mailboxes/) | `get-mailbox-by-id`, `list-mailboxes`, `get-mailbox-by-name` | `get-mailbox-by-id`, `list-mailboxes` |
| [ECGrid IDs](./ecgrid-ids/) | `get-ecgrid-id-by-id`, `find-edi-ids`, `list-ecgrid-ids-by-mailbox` | All three |
| [Partners](./partners/) | `get-partner-by-id`, `list-partners`, `check-partner-config`, `test-partner-delivery`, `get-partner-document-counts` | `get-partner-by-id`, `list-partners` |
| [Comms](./comms/) | `get-comm-by-id`, `list-comms`, `find-comms`, `test-comm`, `check-ftp-access` | — |
| [Parcels](./parcels/) | `get-parcel-by-id` (+ 3 coming soon) | `get-parcel-by-id` |
| [Interchanges](./interchanges/) | `get-interchange-by-id`, `get-document-counts-by-status` | `get-interchange-by-id` |
| [Transactions](./transactions/) | `search-transactions` | `search-transactions` |
| [Callbacks](./callbacks/) | `get-callback-event-by-id`, `get-callback-queue-by-id`, `list-callback-events`, `list-callback-queue` | — |
| [Carbon Copies](./carbon-copies/) | `get-carbon-copy-by-id`, `list-carbon-copies` | — |
| [Keys](./keys/) | `get-key`, `list-keys` | — |

## Response Modes

**Structured JSON** — all 36 tools return a structured JSON data object. The AI interprets this and presents it to the user in plain language. Developers use it directly in their applications.

**Interactive UI components** — 10 tools additionally render a visual, browsable widget in Claude Desktop and Claude.ai alongside the AI's text response. The tool call, parameters, and JSON response are identical regardless of whether a UI component renders. Identified in the table above.

## Future Tools

Simplify and Catalog MCP tools will be documented here when released.
```

- [ ] **Step 3: Create tools/system/_category_.json**

```json
{ "label": "System", "position": 2 }
```

- [ ] **Step 4: Create tools/system/hello-world.md**

Source from `tools07062026.md` lines 1111–1140 (description and inputSchema).

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: hello-world tool reference - Greg Kolinski -->
---
title: hello-world
---

# hello-world

Greets the caller and returns their identity from the ECGrid backend. Use as a first test after setup, or as a connectivity check in your application.

## Tool Name

```
connectivity_system_hello-world
```

## Auth Level Required

Any

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `request.name` | string \| null | No | Optional display name; falls back to the caller's loginName. Max 256 characters. |

## Response

Structured JSON — greeting message, loginName, authLevel, networkId, mailboxId, serverTimeUtc.

```json
{
  "message": "Hello, Your Name, from ECGrid MCP server.",
  "loginName": "your-login",
  "authLevel": "NetworkUser",
  "networkId": "47",
  "mailboxId": "0",
  "serverTimeUtc": "2026-07-06T14:00:00Z"
}
```

## Response Fields

| Field | Description |
|---|---|
| `message` | Greeting confirming the name passed in (or your loginName) |
| `loginName` | Your ECGrid account login name |
| `authLevel` | Your account's permission tier — see [Authentication](../../authentication.md) |
| `networkId` | The ECGrid network your account belongs to |
| `mailboxId` | Your mailbox ID (0 = network-level account) |
| `serverTimeUtc` | Current ECGrid server time in UTC |

## Example Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "connectivity_system_hello-world",
    "arguments": {
      "request": { "name": "Your Name" }
    }
  }
}
```

## Example Prompts

- `Test the ECGrid MCP connection`
- `What is my ECGrid auth level?`
- `What network ID does ECGrid return for me?`

## See Also

- [get-version](./get-version.md) — confirm API and backend versions
- [Authentication](../../authentication.md) — auth levels explained
```

- [ ] **Step 5: Create tools/system/get-version.md**

Source from `tools07062026.md` lines 971–987.

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: get-version tool reference - Greg Kolinski -->
---
title: get-version
---

# get-version

Return the ECGrid REST API and ECGridOS backend version strings. Use for smoke tests, integration diagnostics, or to confirm which API/backend build the caller is talking to.

## Tool Name

```
connectivity_system_get-version
```

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
```

- [ ] **Step 6: Create tools/system/get-status-list.md**

Source from `tools07062026.md` lines 896–912.

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: get-status-list tool reference - Greg Kolinski -->
---
title: get-status-list
---

# get-status-list

Return the ECGrid status-code catalog — the reference table that maps every numeric status code to its meaning. Use to resolve or explain a status code seen on a parcel or interchange.

## Tool Name

```
connectivity_system_get-status-list
```

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

- [Resources & Prompts](../../resources-and-prompts.md) — `InterchangeStatus` and `ParcelStatus` MCP Resources
- [get-interchange-by-id](../interchanges/get-interchange-by-id.md)
- [get-parcel-by-id](../parcels/get-parcel-by-id.md)
```

- [ ] **Step 7: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```

- [ ] **Step 8: Commit**

```bash
git add website/docs/mcp/tools/
git commit -m "docs(mcp): add tools overview and system tools (hello-world, get-version, get-status-list)"
```

---

## Task 9: Users tools

**Files:** `website/docs/mcp/tools/users/`

Source: `tools07062026.md` at lines: `get-user-me` (99–114), `get-user-by-id` (838–866), `get-user-by-login` (1024–1051), `list-users` (4–61).

- [ ] **Step 1: Create tools/users/_category_.json**

```json
{ "label": "Users", "position": 3 }
```

- [ ] **Step 2: Create get-user-me.md**

Tool name: `connectivity_user_get-user-me`. Description from line 99. No parameters (empty request). Returns: userId, loginName, firstName, lastName, company, email, phone, timeZoneOffset, authLevel, lockoutStatus, networkId, mailboxId, lastLogin, openSessions, timeOut, created, modified, plus ecgridOsVersion, sessionId, sessionEventId.

Example prompts: `Who am I?`, `What's my ECGrid account?`, `What auth level does my API key have?`

- [ ] **Step 3: Create get-user-by-id.md**

Tool name: `connectivity_user_get-user-by-id`. Source line 838. Parameter: `request.userId` (integer, required, >= 1). Returns same shape as `get-user-me` minus session fields.

Example prompts: `Look up user 12345`, `Show me the profile for user ID 9876`

- [ ] **Step 4: Create get-user-by-login.md**

Tool name: `connectivity_user_get-user-by-login`. Source line 1024. Parameter: `request.loginName` (string, required, 8–128 chars). Returns same shape as `get-user-by-id`.

Example prompts: `Look up user jane.smith@example.com`, `Find the ECGrid user with this email address`

- [ ] **Step 5: Create list-users.md**

Tool name: `connectivity_user_list-users`. Source lines 4–61. Parameters: `networkId` (integer|null, optional), `mailboxId` (integer|null, optional), `name` (string|null, optional, max 40 chars), `lockedOut` (boolean|null, optional post-filter). At least one of networkId/mailboxId/name required. Returns: `count`, `users` array (same shape as `get-user-by-id`). Cache bypass — always reflects current state.

Example prompts: `List all users on network 7`, `Show locked-out users on network 7`, `Find users with acme in their login`

- [ ] **Step 6: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/users/
git commit -m "docs(mcp): add users tools (get-user-me, get-user-by-id, get-user-by-login, list-users)"
```

---

## Task 10: Network tool

**Files:** `website/docs/mcp/tools/network/`

Source: `tools07062026.md` line 1082.

- [ ] **Step 1: Create tools/network/_category_.json**

```json
{ "label": "Network", "position": 4 }
```

- [ ] **Step 2: Create get-network-by-id.md**

Tool name: `connectivity_network_get-network-by-id`. Source line 1082. Parameter: `request.networkId` (integer, required, >= 1). Returns: networkId, name, status, runStatus, outageStatus, primary contacts (owner/errors/interconnects/billing — each as userId+loginName+authLevel), public website URLs, owner-side routing metadata, created/modified timestamps.

Example prompts: `Show me network 47`, `What's the status of my ECGrid network?`

- [ ] **Step 3: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/network/
git commit -m "docs(mcp): add network tool (get-network-by-id)"
```

---

## Task 11: Mailboxes tools

**Files:** `website/docs/mcp/tools/mailboxes/`

Source: `tools07062026.md` at lines: `get-mailbox-by-id` (63–96), `list-mailboxes` (370–407), `get-mailbox-by-name` (335–369). All three checked against `_meta.ui.resourceUri` — `get-mailbox-by-id` and `list-mailboxes` have UI components.

- [ ] **Step 1: Create tools/mailboxes/_category_.json**

```json
{ "label": "Mailboxes", "position": 5 }
```

- [ ] **Step 2: Create get-mailbox-by-id.md**

Tool name: `connectivity_mailbox_get-mailbox-by-id`. Has `_meta.ui.resourceUri: "ui://mailbox/detail.html"` — include `:::info Interactive UI Component` block. Source line 63. Parameter: `request.mailboxId` (integer, required, >= 1). Returns: mailboxId, networkId, name, description, status, useType, managed, ecgridAccount, defaultAs2Id, created, modified, seven role-based contacts (owner/errors/interconnects/notices/reports/customerService/accounting — each: userId+loginName+authLevel), delivery + X12 config, billing metadata.

Example prompts: `Show me mailbox 142`, `What's the configuration of mailbox 500?`

- [ ] **Step 3: Create list-mailboxes.md**

Tool name: `connectivity_mailbox_list-mailboxes`. Has UI component. Source line 370. Parameter: `request.networkId` (integer|null, optional — defaults to caller's home network). Returns: `count`, `mailboxes` array (same shape as `get-mailbox-by-id`).

Example prompts: `List all mailboxes on my network`, `How many mailboxes does network 47 have?`

- [ ] **Step 4: Create get-mailbox-by-name.md**

Tool name: `connectivity_mailbox_get-mailbox-by-name`. Source line 335. No UI component. Parameters: `request.networkId` (integer, required), `request.name` (string, required, case-insensitive substring). Returns: `count`, `mailboxes` array.

Example prompts: `Find mailboxes with "acme" in their name on network 47`

- [ ] **Step 5: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/mailboxes/
git commit -m "docs(mcp): add mailboxes tools (get-mailbox-by-id, list-mailboxes, get-mailbox-by-name)"
```

---

## Task 12: ECGrid IDs tools

**Files:** `website/docs/mcp/tools/ecgrid-ids/`

Source: `tools07062026.md` at lines: `get-ecgrid-id-by-id` (989–1022), `find-edi-ids` (408–488), `list-ecgrid-ids-by-mailbox` (2195+). All three have UI components.

- [ ] **Step 1: Create tools/ecgrid-ids/_category_.json**

```json
{ "label": "ECGrid IDs", "position": 6 }
```

- [ ] **Step 2: Create get-ecgrid-id-by-id.md**

Tool name: `connectivity_ecgrid-id_get-ecgrid-id-by-id`. Has UI component (`ui://ecgrid-id/detail.html`). Source line 989. Parameter: `request.ecgridId` (integer, required, >= 1). Returns: ecgridId, networkId, networkName, mailboxId, mailboxName, qualifier, id (wire EDI identifier), description, dataEmail, mailboxDefault, status, useType.

- [ ] **Step 3: Create find-edi-ids.md**

Tool name: `connectivity_ecgrid-id_find-edi-ids`. Has UI component (`ui://ecgrid-id/find.html`). Source line 408. Parameters: `request.id` (string|null, optional — wire EDI identifier), `request.description` (string|null, optional — substring, takes precedence over id), `request.qualifier` (string|null, optional — X12 qualifier), `request.networkId` (integer|null, optional), `request.mailboxId` (integer|null, optional), `request.showInactive` (boolean|null, optional). At least one of id/description required. Returns: `count`, `ediIds` array (same shape as `get-ecgrid-id-by-id`).

Example prompts: `Find the ECGrid ID for EDI identifier 9998887776`, `Which mailbox owns the EDI ID "ACMECORP" with qualifier ZZ?`

- [ ] **Step 4: Create list-ecgrid-ids-by-mailbox.md**

Tool name: `connectivity_ecgrid-id_list-ecgrid-ids-by-mailbox`. Has UI component (`ui://ecgrid-id/by-mailbox.html`). Source line 2195. Parameters: `request.mailboxId` (integer, required), `request.networkId` (integer|null, optional), `request.showInactive` (boolean|null, optional). Returns: `count`, `ecgridIds` array.

Example prompts: `List all EDI IDs for mailbox 142`, `What trading partner IDs does mailbox 500 have?`

- [ ] **Step 5: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/ecgrid-ids/
git commit -m "docs(mcp): add ECGrid ID tools (get-ecgrid-id-by-id, find-edi-ids, list-ecgrid-ids-by-mailbox)"
```

---

## Task 13: Partners tools

**Files:** `website/docs/mcp/tools/partners/`

Source: `tools07062026.md` at lines: `get-partner-by-id` (1224–1258), `list-partners` (553–639), `check-partner-config` (1053–1081), `test-partner-delivery` (914–969), `get-partner-document-counts` (640–693). `get-partner-by-id` and `list-partners` have UI components.

- [ ] **Step 1: Create tools/partners/_category_.json**

```json
{ "label": "Partners", "position": 7 }
```

- [ ] **Step 2: Create get-partner-by-id.md**

Tool name: `connectivity_partner_get-partner-by-id`. Has UI component (`ui://partner/detail.html`). Source line 1224. Parameter: `request.partnerId` (integer, required, >= 1). Returns: interconnectId, uniqueId, lifecycle timestamps, status, contactName, contactEmail, reference1/2, as2Id1/2, tp1/tp2 ECGrid ID summaries, compact user references.

- [ ] **Step 3: Create list-partners.md**

Tool name: `connectivity_partner_list-partners`. Has UI component (`ui://partner/list.html`). Source line 553. Parameters: `request.mailboxId`, `request.networkId`, `request.status` (Pending/Completed/Canceled/Delayed/Problem/AuthorizationRequired/NoStatusChange), `request.ecgridId1`/`ecgridId2`, `request.maxDays` — all optional. Returns: `count`, `partners` array.

- [ ] **Step 4: Create check-partner-config.md**

Tool name: `connectivity_partner_check-partner-config`. Source line 1053. Parameter: `request.interconnectId` (integer, required). Returns: `isHealthy`, `setupComplete`, `hasTraffic`, tp1/tp2 active flags, scheduled move flags, last-traffic timestamps, `issues` array (plain-language problem descriptions).

Example prompts: `Is trading partner 12345 set up correctly?`, `Why is traffic not flowing with interconnect 99999?`

- [ ] **Step 5: Create test-partner-delivery.md**

Tool name: `connectivity_partner_test-partner-delivery`. Source line 914. Two-step tool — call without `parcelId` to initiate, then with `parcelId` to poll. Parameters: `request.interconnectId` (integer, required), `request.direction` (Tp1ToTp2/Tp2ToTp1, optional), `request.parcelId` (integer|null, optional), `request.documentType` (string|null, optional). Returns: `reachable`, `verdict`, `statusCode`, `statusDescription`, `parcelId`, `fromEcgridId`, `toEcgridId`, `notes`.

Include the two-step pattern in the page:
```
Step 1 — initiate: call without parcelId → get parcelId + verdict "pending"
Step 2 — poll: call with parcelId → get final verdict (delivered/failed/aborted)
```

- [ ] **Step 6: Create get-partner-document-counts.md**

Tool name: `connectivity_partner_get-partner-document-counts`. Source line 640. Parameters: `request.ecgridId` (integer, required), `request.startDate`/`endDate` (ISO 8601, required, max 30-day window), `request.topN` (integer, optional, default 50, max 500). Returns: scope, totalInterchanges, totalBytes, `partners` array (each: tradingPartner, tradingPartnerQid, totalInterchanges, totalBytes), ranked by total descending.

- [ ] **Step 7: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/partners/
git commit -m "docs(mcp): add partners tools (5 tools including check-config and test-delivery)"
```

---

## Task 14: Comms tools

**Files:** `website/docs/mcp/tools/comms/`

Source: `tools07062026.md` at lines: `get-comm-by-id` (2166+), `list-comms` (229–296), `find-comms` (2115+), `test-comm` (781–837), `check-ftp-access` (1142–1187). No UI components for comms tools.

- [ ] **Step 1: Create tools/comms/_category_.json**

```json
{ "label": "Comms", "position": 8 }
```

- [ ] **Step 2: Create get-comm-by-id.md**

Tool name: `connectivity_comm_get-comm-by-id`. Source line 2166. Parameter: `request.commId` (integer, required). Returns: commId, type, identifier, url, sign/encrypt/compress flags, receipt policy, httpAuthType, sslClientAuthentication, useType, status, usage window, timestamps, owner (userId+loginName+authLevel), certificates array (subject, issuer, thumbprint, serialNumber, notBefore/notAfter, status, validityStatus, isCurrentlyValid, daysUntilExpiry).

- [ ] **Step 3: Create list-comms.md**

Tool name: `connectivity_comm_list-comms`. Source line 229. Parameters: `request.networkId` (integer, required), `request.mailboxId` (integer, required), `request.commType` (string, required — as2/ftp/sftp/etc.), `request.withCerts` (boolean, optional — default false; set true to inspect certificate validity/expiry), `request.showInactive` (boolean, optional), `request.useType` (string, optional), `request.privateKeyRequired` (boolean, optional). Returns: `count`, `comms` array.

Include note: "Set `withCerts: true` to inspect certificate validity, expiry, and issuer across all channels in a mailbox."

- [ ] **Step 4: Create find-comms.md**

Tool name: `connectivity_comm_find-comms`. Source line 2115. Parameters: `request.identifier` (string, required — wire identifier e.g. AS2 ID), `request.commType` (string, required). Returns: `count`, `comms` array. Use case: "Which mailbox owns this AS2 ID?"

- [ ] **Step 5: Create test-comm.md**

Tool name: `connectivity_comm_test-comm`. Source line 781. Two-step tool. Parameters: `request.ecgridId` (integer, required — the RECEIVE-side ECGrid ID), `request.commType` (string, required — Ftp or As2), `request.parcelId` (integer|null, optional). Returns: `reachable`, `verdict`, `statusCode`, `statusDescription`, `parcelId`, `loopbackEcgridId`.

Include two-step pattern (same as test-partner-delivery).

- [ ] **Step 6: Create check-ftp-access.md**

Tool name: `connectivity_comm_check-ftp-access`. Source line 1142. Parameters: `request.networkId` (integer, required), `request.mailboxId` (integer|null, optional), `request.ip` (string|null, optional — IPv4 or IPv6). Returns: `data` envelope with `account` section (ftpConfigured, status, loginName, hasCertificate), optional `ip` section (allowed), optional `user` section (lockedOut, status, openSessions). `partial` flag + `warnings` if user-status lookup degrades.

Example prompts: `Why is the FTP login for mailbox 142 being refused?`, `Is IP 203.0.113.5 allowed for FTP on network 7?`

- [ ] **Step 7: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/comms/
git commit -m "docs(mcp): add comms tools (5 tools including test-comm and check-ftp-access)"
```

---

## Task 15: Parcels tools

**Files:** `website/docs/mcp/tools/parcels/`

Source: `tools07062026.md` line 694 for `get-parcel-by-id`. The three list tools are stubs — not yet deployed on live server.

- [ ] **Step 1: Create tools/parcels/_category_.json**

```json
{ "label": "Parcels", "position": 9 }
```

- [ ] **Step 2: Create get-parcel-by-id.md**

Tool name: `connectivity_parcel_get-parcel-by-id`. Has UI component (`ui://parcel/detail.html`). Source line 694. Parameter: `request.parcelId` (integer, required, >= 1, int64). Returns: parcelId, parcelDate, parcelBytes, fileName, mailbagControlId, status (code+description+statusDate), from/to routing (networkId+networkName+mailboxId+mailboxName), `interchanges` array (each: interchangeId, statusCode, statusDescription, statusDate, documentType), interchangeCount.

Example prompts: `Show me parcel 987654321`, `What's the status of this parcel?`, `Which interchanges does parcel 12345 contain?`

- [ ] **Step 3: Create list-inbox-parcels.md (stub)**

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: list-inbox-parcels stub - Greg Kolinski -->
---
title: list-inbox-parcels
---

# list-inbox-parcels

:::caution Coming Soon
This tool is in development and not yet available on the ECGrid MCP Server. This page will be updated when the tool ships. Use `tools/list` to confirm availability.
:::

List inbound parcels by date range for a mailbox.

**Planned tool name:** `connectivity_parcel_list-inbox-parcels`
```

- [ ] **Step 4: Create list-outbox-parcels.md (stub)**

Same pattern as Step 3. Planned tool name: `connectivity_parcel_list-outbox-parcels`. Description: List outbound parcels by date range for a mailbox.

- [ ] **Step 5: Create list-pending-inbox-parcels.md (stub)**

Same pattern. Planned tool name: `connectivity_parcel_list-pending-inbox-parcels`. Description: List parcels currently sitting in the inbox awaiting download.

- [ ] **Step 6: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/parcels/
git commit -m "docs(mcp): add parcels tools (get-parcel-by-id + 3 coming-soon stubs)"
```

---

## Task 16: Interchanges tools

**Files:** `website/docs/mcp/tools/interchanges/`

Source: `tools07062026.md` at lines: `get-interchange-by-id` (1189–1223), `get-document-counts-by-status` (489–552). `get-interchange-by-id` has UI component.

- [ ] **Step 1: Create tools/interchanges/_category_.json**

```json
{ "label": "Interchanges", "position": 10 }
```

- [ ] **Step 2: Create get-interchange-by-id.md**

Tool name: `connectivity_interchange_get-interchange-by-id`. Has UI component (`ui://interchange/detail.html`). Source line 1189. Parameter: `request.interchangeId` (integer, required, >= 1). Returns: interchangeId, interchangeControlId, standard, documentType, bytes, interchangeDateTime, processDate, nested `status`, `from`/`to` routing, raw `header`, compact `tpFrom`/`tpTo` EDI-identity summaries, `parcelIds`, `parcelCount`.

Example prompts: `Show me interchange 123456789`, `Who sent interchange 99999 and what's its status?`

- [ ] **Step 3: Create get-document-counts-by-status.md**

Tool name: `connectivity_interchange_get-document-counts-by-status`. Source line 489. Two modes: Mode A (`ecgridId` supplied) or Mode B (`networkId` + `mailboxId` required). Parameters: `request.ecgridId` (integer, optional — takes precedence), `request.networkId` (integer), `request.mailboxId` (integer), `request.startDate`/`endDate` (ISO 8601, required, max 30 days). Returns: scope, startDate, endDate, total, `customers` array (each: ecgridId, customer, qid, total, byDirection: {from, to} each with {total, byStatus: {statusCode → count}}).

Include note: "Use for status-distribution count questions, not for listing individual interchanges. Use `search-transactions` for listing."

- [ ] **Step 4: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/interchanges/
git commit -m "docs(mcp): add interchanges tools (get-interchange-by-id, get-document-counts-by-status)"
```

---

## Task 17: Transactions tool

**Files:** `website/docs/mcp/tools/transactions/`

Source: `tools07062026.md` line 1410. Has UI component.

- [ ] **Step 1: Create tools/transactions/_category_.json**

```json
{ "label": "Transactions", "position": 11 }
```

- [ ] **Step 2: Create search-transactions.md**

Tool name: `connectivity_transaction_search-transactions`. Has UI component (`ui://transaction/search.html`). Source line 1410. 

Parameters: `request.type` (string, required — `Interchange` or `File`), `request.direction` (string, required — `Inbound`/`Outbound`/`Both`), `request.networkId` (integer, optional — defaults to caller's network), `request.mailboxId` (integer, optional — defaults to -1 all mailboxes), `request.beginDate`/`endDate` (ISO 8601, optional — defaults to last 24 hours), `request.view` (string, optional — `Archive`/`Blocked`/`Pending`/`NoRoute`/`PendingDownload`/`DeliveryError`).

Returns: applied filters, `rows` array (each: transactionId, type, direction, timestamps, status, controlNumber, standard, documentType, bytes, parcelIds, from/to routing and EDI identity), leg totals, totalRecords.

Example prompts:
- `Show me all inbound interchanges from the last 24 hours`
- `Are there any transactions currently blocked?`
- `Show pending inbound files for mailbox 142`
- `Find all delivery errors from yesterday`

- [ ] **Step 3: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/transactions/
git commit -m "docs(mcp): add transactions tool (search-transactions)"
```

---

## Task 18: Callbacks tools

**Files:** `website/docs/mcp/tools/callbacks/`

Source: `tools07062026.md` at lines: `get-callback-event-by-id` (299–334), `get-callback-queue-by-id` (1313+), `list-callback-events` (189–228), `list-callback-queue` (729–780). No UI components.

- [ ] **Step 1: Create tools/callbacks/_category_.json**

```json
{ "label": "Callbacks", "position": 12 }
```

- [ ] **Step 2: Create get-callback-event-by-id.md**

Tool name: `connectivity_callback_get-callback-event-by-id`. Source line 299. Parameters: `request.callBackEventId` (integer, required), `request.queueCount` (integer, optional — default 25, caps embedded queue entries). Returns: registration config (systemObject, direction, frequency, maxCalls, status, url, httpAuthType) + `queue` array (each: status, callsRemaining, nextCall, delivery log). HTTP auth credentials never returned.

- [ ] **Step 3: Create get-callback-queue-by-id.md**

Tool name: `connectivity_callback_get-callback-queue-by-id`. Source line 1313. Parameter: `request.callBackQueueId` (integer, required — queue entry ID, NOT a callBackEventId). Returns: callBackQueueId, status, callsRemaining, nextCall, log array, lite event reference.

Include note distinguishing callBackQueueId from callBackEventId.

- [ ] **Step 4: Create list-callback-events.md**

Tool name: `connectivity_callback_list-callback-events`. Source line 189. Parameters: `request.networkId` (integer, required, >= 1), `request.mailboxId` (integer, required, >= 0), `request.showInactive` (boolean, optional — default false). Returns: `count`, `events` array (registration config only — queue NOT embedded). Empty array = no callbacks, not an error.

- [ ] **Step 5: Create list-callback-queue.md**

Tool name: `connectivity_callback_list-callback-queue`. Source line 729. Parameters: `request.networkId` (integer, required), `request.mailboxId` (integer, required), `request.view` (string, optional — `pending` default or `failed`), `request.maxDays` (integer, required when view=failed). Returns: `count`, `queue` array.

- [ ] **Step 6: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/callbacks/
git commit -m "docs(mcp): add callbacks tools (4 tools)"
```

---

## Task 19: Carbon Copies and Keys tools

**Files:** `website/docs/mcp/tools/carbon-copies/`, `website/docs/mcp/tools/keys/`

Source: `tools07062026.md` at lines: `get-carbon-copy-by-id` (867–895), `list-carbon-copies` (1342+), `get-key` (117–186), `list-keys` (1259+). No UI components.

- [ ] **Step 1: Create tools/carbon-copies/_category_.json**

```json
{ "label": "Carbon Copies", "position": 13 }
```

- [ ] **Step 2: Create get-carbon-copy-by-id.md**

Tool name: `connectivity_carbon-copy_get-carbon-copy-by-id`. Source line 867. Parameter: `request.carbonCopyId` (integer, required). Returns: carbonCopyId, networkId, mailboxId, four endpoint summaries (originalFrom, originalTo, ccFrom, ccTo — each: ecgridId, qualifier, id, description), gsFrom, gsTo, transactionSet, status, created, modified.

- [ ] **Step 3: Create list-carbon-copies.md**

Tool name: `connectivity_carbon-copy_list-carbon-copies`. Source line 1342. Parameters: `request.networkId`/`mailboxId` (integer, optional — must be supplied together), `request.ecgridIdFrom`/`ecgridIdTo` (integer, optional), `request.showInactive` (boolean, optional). Returns: `count`, `carbonCopies` array.

- [ ] **Step 4: Create tools/keys/_category_.json**

```json
{ "label": "Keys", "position": 14 }
```

- [ ] **Step 5: Create get-key.md**

Tool name: `connectivity_key_get-key`. Source line 117. Parameters: `request.systemObject` (string, required — enum: System/User/Network/Mailbox/EcgridId/Interconnect/Migration/Parcel/Interchange/CarbonCopy/CallBackEvent/As2/Comm/Gisb/InterconnectNote/PriceList/Contract/Invoice), `request.objectId` (integer, required, >= 1), `request.key` (string, required, 1–512 chars), `request.visibility` (string, required — Private/Shared/Public/Session). Returns: key, value (verbatim), meta, visibility, created, expires. Not cached.

- [ ] **Step 6: Create list-keys.md**

Tool name: `connectivity_key_list-keys`. Source line 1259. Parameters: `request.systemObject` (string, required — same enum as get-key), `request.objectId` (integer, required). Returns: `count`, `keys` array (each: key, value, meta, visibility, created, expires).

Example prompt: `What FTP setup keys are on mailbox 142?`

- [ ] **Step 7: Verify build and commit**

```bash
cd website && npm run build 2>&1 | tail -5
git add website/docs/mcp/tools/carbon-copies/ website/docs/mcp/tools/keys/
git commit -m "docs(mcp): add carbon-copies and keys tools (4 tools)"
```

---

## Task 20: Changelog entry

**Files:** `website/docs/changelog/mcp-release-notes.md`

- [ ] **Step 1: Create mcp-release-notes.md**

Source from `C:\local docs\ECGrid-MCP\ECGrid-MCP-Release-Notes.md`. Reformat to match the style of the existing `rest-changelog.md` page. Include:
- AI attribution header
- Front matter: `title: MCP Release Notes`
- All 9 release groups (2026-05-19 Foundation through 2026-07-01 Interchange/Transaction Tools)
- Response Modes section
- Link back to [Tools Reference](../mcp/tools/overview.md)

```markdown
<!-- AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-07-06: MCP release notes - Greg Kolinski -->
---
title: MCP Release Notes
sidebar_position: 3
---

# ECGrid MCP Release Notes

Track new tools and changes to the ECGrid MCP Server (`mcp.ecgrid.io`).

Call `tools/list` to always get the current complete tool list at runtime. See the [Tools Reference](../mcp/tools/overview.md) for full documentation on every tool.

---
```

Then include all release entries from the source file, reformatted.

- [ ] **Step 2: Verify build**

```bash
cd website && npm run build 2>&1 | tail -20
```
Expected: full successful build with no broken link warnings for MCP pages.

- [ ] **Step 3: Commit**

```bash
git add website/docs/changelog/mcp-release-notes.md
git commit -m "docs(mcp): add MCP release notes to changelog section"
```

---

## Task 21: Final verification and local dev test

- [ ] **Step 1: Full build**

```bash
cd website && npm run build 2>&1
```
Expected: `Generated static files in "build".` No ERR lines. Note any broken link warnings and fix them.

- [ ] **Step 2: Start dev server and verify**

```bash
cd website && npm run start
```

Open `http://localhost:3000` and verify:
- [ ] MCP tab appears in navbar between SOAP API and Common Operations
- [ ] Home page shows MCP card in "Choose Your API" section
- [ ] Home page hero has ECGrid MCP button and badge pill
- [ ] Quick Links has "Quick Start — MCP"
- [ ] Footer has MCP under Documentation and ECGrid MCP Server under Live References
- [ ] Navigate to `/docs/mcp/overview` — page loads correctly
- [ ] Navigate to `/docs/mcp/tools/overview` — category table renders
- [ ] Navigate to `/docs/mcp/tools/system/hello-world` — tool page renders with all sections
- [ ] Navigate to `/docs/mcp/tools/mailboxes/get-mailbox-by-id` — Interactive UI Component callout renders
- [ ] Navigate to `/docs/changelog/mcp-release-notes` — page loads
- [ ] Navigate to existing REST API page — still works, no nav regression
- [ ] SOAP API sidebar position shows correctly (position 5)

- [ ] **Step 3: Fix any broken links or rendering issues found in Step 2**

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "docs(mcp): complete MCP documentation section — 36 tools, all reference pages, nav and homepage updated"
```

---

## Self-Review

**Spec coverage check:**
- [x] Nav position 4 — Task 1 (shift others) + Task 2 (add MCP sidebar/nav)
- [x] Homepage MCP card, button, badge, quick link — Task 3
- [x] Footer entries — Task 2
- [x] Top-level pages (overview, quick-start, auth, protocol) — Tasks 4–5
- [x] Connecting subsection (3 pages) — Task 6
- [x] building-agents, resources-and-prompts, other-ai-platforms, troubleshooting — Task 7
- [x] tools/overview + all 13 _category_.json + 36 tool pages — Tasks 8–19
- [x] 3 parcel stub pages — Task 15
- [x] Changelog entry — Task 20
- [x] Live tool descriptions from tools07062026.md — specified per task with source line numbers
- [x] UI component callout on 10 tools — specified per task
- [x] AI attribution on every new file — included in all file content
- [x] CSS for MCP pill and card — Task 3

**No placeholders found** — all tasks have specific file content or reference exact source line numbers in tools07062026.md.

**Type consistency** — all tool names use `connectivity_` prefix throughout, consistent with tools07062026.md.
