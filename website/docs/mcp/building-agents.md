{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Building agents guide - Greg Kolinski
*/}
---
title: Building Agents
sidebar_position: 6
---

# Building Agents

Guide for developers building AI-powered features — chatbots, agents, or automated workflows — that call ECGrid services via the MCP Server.

## Prerequisites

- An ECGrid API key — from the [ECGrid Developer Portal](https://api.ecgridos.io/)
- Familiarity with HTTP and JSON
- Any language or HTTP client — no SDK or Node.js required

## Server Details

| Item | Value |
|---|---|
| Base URL | `https://mcp.ecgrid.io/mcp` |
| Protocol | MCP over HTTP (JSON-RPC 2.0) |
| MCP Version | `2024-11-05` |
| Auth Header | `X-APIKey: YOUR_API_KEY_HERE` |
| Content-Type | `application/json` |
| Accept Header | `application/json, text/event-stream` (required — 406 without it) |

:::caution API Key Security
In all code examples in this guide, `YOUR_API_KEY_HERE` is a placeholder. In production, load your API key from an environment variable or a secrets manager — never hard-code it in source files, and never pass it through a chat conversation. The key should only appear in your application's runtime environment or config file.
:::

## Response Format

The ECGrid MCP Server returns all responses as **Server-Sent Events (SSE)**. This is the only supported response format — plain JSON is not available.

Every response arrives as an SSE envelope:

```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

**Required `Accept` header:** The server requires that your request declares both media types. Sending only `Accept: application/json` returns a `406 Not Acceptable` error:

```
Accept: application/json, text/event-stream
```

**Parsing the response:** Read the body as text, find the line starting with `data: `, strip the prefix, and parse the remainder as JSON:

```
body text → split lines → find "data: ..." → strip "data: " → JSON.parse()
```

All code examples in this guide implement this pattern. MCP-compatible AI tools handle SSE automatically — this only affects developers making direct HTTP calls.

:::tip New to SSE?
Server-Sent Events is a standard W3C protocol for streaming data over HTTP. The [MDN SSE reference](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) covers the full format spec, `event:` and `data:` line structure, reconnection behavior, and client implementations. The [WHATWG SSE spec](https://html.spec.whatwg.org/multipage/server-sent-events.html) is the authoritative technical reference.
:::

:::note Note on `"` in raw output
When reading the raw SSE stream, quote characters inside string values appear as `"` rather than `"`. This is standard HTML-safe encoding and is expected — both forms are valid JSON and decode identically. Parse with any JSON library and the values will read correctly.
:::

### Tool Result Structure

ECGrid MCP tools return **structured JSON data** intended for AI agent and developer consumption. Every tool returns a structured JSON object as its result. The AI interprets this structured data and formats the response for the end user — the raw JSON is not presented directly.

The MCP protocol wraps the tool result as a JSON string inside `content[0].text`. Parsing happens in two steps:

**Step 1 — Unwrap the SSE and JSON-RPC envelope:**
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"message\":\"Hello, Greg...\",\"loginName\":\"...\"}"
      }
    ]
  }
}
```

**Step 2 — Parse `content[0].text` as JSON to get the structured data:**
```json
{
  "message": "Hello, Greg, from ECGrid MCP server.",
  "loginName": "gkolinski@ld.com",
  "authLevel": "TechOps",
  "networkId": "47",
  "mailboxId": "0",
  "serverTimeUtc": "2026-07-06T14:00:00Z"
}
```

Full parse chain:
```
SSE data: line → JSON.parse() → JSON-RPC result → result.content[0].text → JSON.parse() → structured data
```

For error responses, `isError: true` is set on the result and `content[0].text` contains a JSON object with `code`, `message`, `userMessage`, and `suggestedAction` fields — the same two-step parse applies.

### Interactive UI Components

A subset of ECGrid MCP tools additionally render an **interactive UI component** in compatible AI clients (Claude Desktop and Claude.ai). The UI component is a visual, browsable widget that appears alongside the AI's response — presenting the structured ECGrid data in a formatted, interactive view rather than as plain text.

**This does not affect developer integrations.** The tool call, parameters, and structured JSON response are identical regardless of whether a UI component renders in the end-user's AI client. The UI component is a presentation layer; your agent code receives and handles the same structured JSON in all environments.

Tools that render interactive UI components include: `mailbox_list-mailboxes`, `mailbox_get-mailbox-by-id`, `ecgrid-id_list-ecgrid-ids-by-mailbox`, `ecgrid-id_get-ecgrid-id-by-id`, `ecgrid-id_find-edi-ids`, `partner_list-partners`, `partner_get-partner-by-id`, `transaction_search-transactions`, `interchange_get-interchange-by-id`, and `parcel_get-parcel-by-id`.

## Request Lifecycle

Every agent session follows this sequence:

```
1. Initialize   →   Handshake with the server, confirm protocol version
2. tools/list   →   Discover available tools and their schemas
3. tools/call   →   Call tools as needed
```

The server is **stateless** — each request carries the full credential and context. There is no session token to manage. You can call tools directly without re-initializing on every request, but your agent should initialize at least once on startup to confirm the server version and available capabilities.

## Step 1 — Initialize

Send `initialize` once at agent startup. Confirm the `protocolVersion` matches `2024-11-05`.

```
POST https://mcp.ecgrid.io/mcp
Content-Type: application/json
Accept: application/json, text/event-stream
X-APIKey: YOUR_API_KEY_HERE
```

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "your-agent-name",
      "version": "1.0"
    }
  }
}
```

**Expected response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "logging": {},
      "tools": {}
    },
    "serverInfo": {
      "name": "ECGrid.Mcp.Server",
      "version": "1.0.0.0"
    }
  }
}
```

Validate that `result.protocolVersion` matches what you sent. If the server returns a different version, log it — a version mismatch may indicate a server update.

## Step 2 — Discover Tools

Call `tools/list` at startup and cache the result. Re-call it periodically to pick up new tools — new tools are added regularly.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

Each tool in the response includes:
- `name` — the tool identifier used in `tools/call`
- `description` — plain-language description of what the tool does
- `inputSchema` — JSON Schema defining the required and optional parameters

Use the `inputSchema` to validate inputs before calling, and to dynamically generate UI or prompts for your agent.

## Step 3 — Call Tools

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "TOOL_NAME",
    "arguments": {
      "request": {
        "fieldName": "value"
      }
    }
  }
}
```

All tool arguments are wrapped in a `request` object. Parameter names and types for each tool are defined in the `inputSchema` returned by `tools/list`.

## Error Handling

### JSON-RPC Errors

Application-level errors return a standard JSON-RPC error object:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32600,
    "message": "Description of the error"
  }
}
```

### HTTP Errors

| Code | Meaning | Agent Action |
|---|---|---|
| `400` | Malformed JSON or invalid JSON-RPC | Fix the request structure |
| `401` | Missing or invalid API key | Check `X-APIKey` header |
| `406` | Missing or invalid `Accept` header | Set `Accept: application/json, text/event-stream` |
| `413` | Request body over 64 KB | Reduce payload size |
| `415` | Body is not JSON | Set `Content-Type: application/json` |
| `429` | Per-IP rate limit exceeded | Retry after `Retry-After` seconds (60s) |
| `503` | Global concurrency cap reached | Retry after `Retry-After` seconds (1s) |

### Retry Pattern for Rate Limiting

Both `429` and `503` include `"retryable": true` in the response body and a `Retry-After` header. Implement exponential backoff with jitter for production agents:

```
On 429: wait Retry-After (60s), then retry
On 503: wait Retry-After (1s), then retry with backoff
Max retries: 3 recommended before surfacing error to user
```

## Auth Levels

Your agent can inspect the `authLevel` returned by any tool to understand what the API key can access. All values are camelCase strings as returned by the server.

| Auth Level | Access Type | Description |
|---|---|---|
| `TPUser` | Read-only | Trading partner — read-only access scoped to a single trading partner relationship. |
| `MailboxUser` | Standard | Mailbox-level user — standard access to a specific mailbox within a network. |
| `MailboxAdmin` | Admin | Mailbox-level admin — elevated access to manage a specific mailbox. |
| `NetworkUser` | Standard | Network-level user — standard access across all mailboxes within your ECGrid network. |
| `NetworkAdmin` | Admin | Network-level admin — full administrative access across your ECGrid network. |

If a tool call fails due to insufficient permissions, surface a clear message to the user and link them to the [ECGrid Developer Portal](https://api.ecgridos.io/) to review their account access, or to [ECGrid Support](https://ecgrid.freshdesk.com/support/home).

## Health Checks

Integrate the health probes into your agent's startup or monitoring:

```
GET https://mcp.ecgrid.io/health/live   →  200 if process is up
GET https://mcp.ecgrid.io/health/ready  →  200 if ready, 503 if not
```

No authentication required. Both probes are exempt from rate limiting. Call `/health/ready` before your first `initialize` to avoid initializing against an unavailable server.

## Available Tools

Call `tools/list` at agent startup and cache the result. Re-call it periodically — new tools are added regularly.

The server currently provides tools across these categories:

| Category | Tools | Interactive UI Component |
|---|---|---|
| System | `get-version`, `get-status-list`, `hello-world` | None |
| User | `user_get-user-me`, `user_get-user-by-id`, `user_get-user-by-login`, `user_list-users` | None |
| Network | `network_get-network-by-id` | None |
| Mailbox | `mailbox_get-mailbox-by-id`, `mailbox_list-mailboxes`, `mailbox_get-mailbox-by-name` | `mailbox_get-mailbox-by-id`, `mailbox_list-mailboxes` |
| ECGrid IDs | `ecgrid-id_get-ecgrid-id-by-id`, `ecgrid-id_find-edi-ids`, `ecgrid-id_list-ecgrid-ids-by-mailbox` | All three |
| Trading Partners | `partner_get-partner-by-id`, `partner_list-partners`, `partner_check-partner-config`, `partner_test-partner-delivery`, `partner_get-partner-document-counts` | `partner_get-partner-by-id`, `partner_list-partners` |
| Communication Channels | `comm_get-comm-by-id`, `comm_list-comms`, `comm_find-comms`, `comm_test-comm`, `comm_check-ftp-access` | None |
| Parcels | `parcel_get-parcel-by-id`, `parcel_list-inbox-parcels`, `parcel_list-outbox-parcels`, `parcel_list-pending-inbox-parcels` | `parcel_get-parcel-by-id` |
| Interchanges | `interchange_get-interchange-by-id`, `interchange_get-document-counts-by-status` | `interchange_get-interchange-by-id` |
| Transactions | `transaction_search-transactions` | `transaction_search-transactions` |
| Callbacks | `callback_get-callback-event-by-id`, `callback_get-callback-queue-by-id`, `callback_list-callback-events`, `callback_list-callback-queue` | None |
| Carbon Copy | `carbon-copy_get-carbon-copy-by-id`, `carbon-copy_list-carbon-copies` | None |
| Keys | `key_get-key`, `key_list-keys` | None |
| Resources & Prompts | Glossary, InterchangeStatus, ParcelStatus resources; InvestigatePartner, TriageStuckInterchange prompts | N/A — not tools |

All tools return structured JSON data. The interactive UI component column identifies which tools additionally render a visual widget in compatible AI clients — this does not affect agent code or HTTP integrations.

## Complete Example — C#

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

public class EcGridMcpClient
{
    private readonly HttpClient _http;
    private readonly string _baseUrl = "https://mcp.ecgrid.io/mcp";
    private int _requestId = 0;

    public EcGridMcpClient(string apiKey)
    {
        _http = new HttpClient();
        _http.DefaultRequestHeaders.Add("X-APIKey", apiKey);
        _http.DefaultRequestHeaders.Add("Accept", "application/json, text/event-stream"); // required by server
    }

    private async Task<JsonElement> PostAsync(object payload)
    {
        var json = JsonSerializer.Serialize(payload);
        var response = await _http.PostAsync(_baseUrl,
            new StringContent(json, Encoding.UTF8, "application/json"));
        response.EnsureSuccessStatusCode();
        // Step 1 — unwrap SSE: extract the data: line and parse JSON-RPC envelope
        var body = await response.Content.ReadAsStringAsync();
        var dataLine = body.Split('\n')
            .FirstOrDefault(l => l.StartsWith("data: "))
            ?.Substring(6) ?? body;
        var envelope = JsonDocument.Parse(dataLine).RootElement;
        if (envelope.TryGetProperty("error", out var error))
            throw new Exception($"MCP error: {error}");
        // Step 2 — parse content[0].text as JSON to get the structured data object
        var resultText = envelope.GetProperty("result")
            .GetProperty("content")[0]
            .GetProperty("text").GetString()!;
        return JsonDocument.Parse(resultText).RootElement;
    }

    public async Task<JsonElement> InitializeAsync() =>
        await PostAsync(new {
            jsonrpc = "2.0", id = ++_requestId, method = "initialize",
            @params = new {
                protocolVersion = "2024-11-05",
                capabilities = new { },
                clientInfo = new { name = "my-ecgrid-agent", version = "1.0" }
            }
        });

    public async Task<JsonElement> ListToolsAsync() =>
        await PostAsync(new {
            jsonrpc = "2.0", id = ++_requestId,
            method = "tools/list", @params = new { }
        });

    public async Task<JsonElement> CallToolAsync(string toolName, object arguments) =>
        await PostAsync(new {
            jsonrpc = "2.0", id = ++_requestId, method = "tools/call",
            @params = new { name = toolName, arguments }
        });
}

// Usage
var client = new EcGridMcpClient("YOUR_API_KEY_HERE");
await client.InitializeAsync();
var tools = await client.ListToolsAsync();
var result = await client.CallToolAsync("hello-world",
    new { request = new { name = "My Agent" } });
Console.WriteLine(result);
```

## Complete Example — JavaScript

```javascript
class EcGridMcpClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = "https://mcp.ecgrid.io/mcp";
    this.requestId = 0;
  }

  async post(payload) {
    const res = await fetch(this.baseUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream", // required by server
        "X-APIKey": this.apiKey,
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    // Step 1 — unwrap SSE: extract the data: line and parse JSON-RPC envelope
    const raw = await res.text();
    const dataLine = raw.split("\n").find(l => l.startsWith("data: "));
    const envelope = JSON.parse(dataLine.slice(6));
    if (envelope.error) throw new Error(`MCP error: ${JSON.stringify(envelope.error)}`);
    // Step 2 — parse content[0].text as JSON to get the structured data object
    return JSON.parse(envelope.result.content[0].text);
  }

  initialize() {
    return this.post({
      jsonrpc: "2.0", id: ++this.requestId, method: "initialize",
      params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: { name: "my-ecgrid-agent", version: "1.0" },
      },
    });
  }

  listTools() {
    return this.post({
      jsonrpc: "2.0", id: ++this.requestId,
      method: "tools/list", params: {},
    });
  }

  callTool(name, args) {
    return this.post({
      jsonrpc: "2.0", id: ++this.requestId, method: "tools/call",
      params: { name, arguments: args },
    });
  }
}

// Usage
const client = new EcGridMcpClient("YOUR_API_KEY_HERE");
await client.initialize();
const tools = await client.listTools();
const result = await client.callTool("hello-world",
  { request: { name: "My Agent" } });
console.log(result);
```

## Complete Example — Python

```python
import httpx
import json

class EcGridMcpClient:
    def __init__(self, api_key: str):
        self.base_url = "https://mcp.ecgrid.io/mcp"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",  # required by server
            "X-APIKey": api_key,
        }
        self._request_id = 0

    def _post(self, payload: dict) -> dict:
        self._request_id += 1
        payload["id"] = self._request_id
        response = httpx.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        # Step 1 — unwrap SSE: extract the data: line and parse JSON-RPC envelope
        for line in response.text.splitlines():
            if line.startswith("data: "):
                envelope = json.loads(line[6:])
                if "error" in envelope:
                    raise Exception(f"MCP error: {envelope['error']}")
                # Step 2 — parse content[0].text as JSON to get structured data
                return json.loads(envelope["result"]["content"][0]["text"])
        raise ValueError("No data line found in SSE response")

    def initialize(self) -> dict:
        return self._post({
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "my-ecgrid-agent", "version": "1.0"},
            },
        })

    def list_tools(self) -> dict:
        return self._post({
            "jsonrpc": "2.0", "method": "tools/list", "params": {},
        })

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self._post({
            "jsonrpc": "2.0", "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })

# Usage
client = EcGridMcpClient("YOUR_API_KEY_HERE")
client.initialize()
tools = client.list_tools()
result = client.call_tool("hello-world", {"request": {"name": "My Agent"}})
print(result)
```

## Testing Your Agent

**MCP Inspector** — use the official inspector tool to explore tools interactively before writing code:

```bash
npx @modelcontextprotocol/inspector "https://mcp.ecgrid.io/mcp" --header "X-APIKey:YOUR_API_KEY_HERE"
```

This opens a browser UI to browse tools, inspect schemas, and call them manually. Note that the MCP Inspector renders structured JSON responses only — interactive UI components are available exclusively in Claude Desktop and Claude.ai.

## Building a Chat Agent with ECGrid

The client examples above handle the ECGrid side of the integration. This section shows how to wire ECGrid tool calls into a full conversational AI chat loop using the Anthropic API.

**The pattern:**
1. User sends a message
2. You call the LLM with the user message and a system prompt that describes the available ECGrid tools
3. The LLM decides whether to call an ECGrid tool or respond directly
4. If it calls a tool, you execute the tool against the ECGrid MCP Server, return the structured JSON result to the LLM
5. The LLM interprets the structured data and composes a natural language response for the user
6. Repeat

### System Prompt

The system prompt tells the LLM what ECGrid tools are available and how to use them. Build it dynamically from `tools/list` at startup and refresh it periodically — new tools are added regularly.

A representative starting prompt for an ECGrid support agent:

```
You are an ECGrid assistant. You help users interact with their ECGrid B2B connectivity account.

You have access to ECGrid tools across the following categories:
- System: get-version, get-status-list, hello-world
- User: user_get-user-me, user_get-user-by-id, user_get-user-by-login, user_list-users
- Network: network_get-network-by-id
- Mailbox: mailbox_get-mailbox-by-id, mailbox_list-mailboxes, mailbox_get-mailbox-by-name
- ECGrid IDs: ecgrid-id_get-ecgrid-id-by-id, ecgrid-id_find-edi-ids, ecgrid-id_list-ecgrid-ids-by-mailbox
- Trading Partners: partner_get-partner-by-id, partner_list-partners, partner_check-partner-config, partner_test-partner-delivery, partner_get-partner-document-counts
- Communication Channels: comm_get-comm-by-id, comm_list-comms, comm_find-comms, comm_test-comm, comm_check-ftp-access
- Parcels: parcel_get-parcel-by-id, parcel_list-inbox-parcels, parcel_list-outbox-parcels, parcel_list-pending-inbox-parcels
- Interchanges: interchange_get-interchange-by-id, interchange_get-document-counts-by-status
- Transactions: transaction_search-transactions
- Callbacks: callback_get-callback-event-by-id, callback_get-callback-queue-by-id, callback_list-callback-events, callback_list-callback-queue
- Carbon Copy: carbon-copy_get-carbon-copy-by-id, carbon-copy_list-carbon-copies
- Keys: key_get-key, key_list-keys

When a user asks about their ECGrid account, select the most appropriate tool and call it.
Chain multiple tools when needed — for example, list mailboxes first, then look up a specific mailbox, then check its trading partners.
All tools return structured JSON data. Present results in plain language — never show raw JSON to the user.
For unfamiliar ECGrid terms, consult the Glossary resource before responding.
```

### JavaScript — Minimal Chat Loop

```javascript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const ecgrid = new EcGridMcpClient(process.env.ECGRID_API_KEY); // from earlier in this guide

// Tool registry — built from tools/list at startup; update as new tools are added
// All tools return structured JSON data; a subset also render interactive UI components
// in compatible AI clients (Claude Desktop, Claude.ai) — agent code is identical either way
const ECGRID_TOOLS = [
  {
    name: "hello-world",
    description: "Verifies the ECGrid connection and returns the user's identity, auth level, network ID, and mailbox ID. Returns structured JSON.",
    input_schema: {
      type: "object",
      properties: { name: { type: "string", description: "Optional display name" } }
    }
  },
  {
    name: "user_get-user-me",
    description: "Returns the identity, auth level, network, and mailbox of the current API key holder. Returns structured JSON.",
    input_schema: { type: "object", properties: {} }
  },
  {
    name: "mailbox_list-mailboxes",
    description: "Lists all mailboxes on a network. Omit networkId to list the caller's own network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: { networkId: { type: "integer", description: "Optional — defaults to caller's home network" } }
    }
  },
  {
    name: "mailbox_get-mailbox-by-id",
    description: "Returns the full profile for a mailbox including contacts, config, and AS2 ID. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: { mailboxId: { type: "integer", description: "Numeric mailbox ID" } },
      required: ["mailboxId"]
    }
  },
  {
    name: "partner_list-partners",
    description: "Lists trading-partner interconnects for a mailbox or network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: {
        mailboxId: { type: "integer", description: "List all partners for this mailbox" },
        networkId: { type: "integer" },
        status: { type: "string", description: "Pending, Completed, Canceled, Delayed, Problem, AuthorizationRequired, or NoStatusChange" }
      }
    }
  },
  {
    name: "partner_check-partner-config",
    description: "Health-checks a trading-partner interconnect for setup completeness, traffic history, active IDs, and scheduled moves. Returns structured JSON with isHealthy and issues list.",
    input_schema: {
      type: "object",
      properties: { interconnectId: { type: "integer", description: "Numeric interconnect ID" } },
      required: ["interconnectId"]
    }
  },
  {
    name: "transaction_search-transactions",
    description: "Searches EDI transactions by direction, type, date range, ECGrid ID, and view (Archive, Pending, Blocked, DeliveryError, etc.). Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: {
        type: { type: "string", enum: ["Interchange", "File"], description: "Required" },
        direction: { type: "string", enum: ["Inbound", "Outbound", "Both"], description: "Required" },
        networkId: { type: "integer" },
        mailboxId: { type: "integer", description: "Use -1 for all mailboxes" },
        beginDate: { type: "string", description: "ISO 8601" },
        endDate: { type: "string", description: "ISO 8601" },
        view: { type: "string", description: "Archive, Blocked, Pending, NoRoute, PendingDownload, or DeliveryError" }
      },
      required: ["type", "direction"]
    }
  },
  {
    name: "parcel_get-parcel-by-id",
    description: "Returns the full detail of a parcel including status, routing, and the interchange manifest. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: { parcelId: { type: "integer", description: "Numeric parcel ID" } },
      required: ["parcelId"]
    }
  },
  {
    name: "interchange_get-interchange-by-id",
    description: "Returns the full detail of an EDI interchange including routing, status, raw ISA header, and carrying parcel IDs. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: { interchangeId: { type: "integer", description: "Numeric interchange ID" } },
      required: ["interchangeId"]
    }
  },
  {
    name: "ecgrid-id_find-edi-ids",
    description: "Finds ECGrid trading-partner ID records by wire EDI identifier string or description substring. Use to resolve an EDI ID to its owning mailbox. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
    input_schema: {
      type: "object",
      properties: {
        id: { type: "string", description: "Wire EDI identifier (e.g. ISA06/ISA08 value)" },
        description: { type: "string", description: "Description substring — takes precedence over id when both supplied" },
        networkId: { type: "integer" },
        qualifier: { type: "string", description: "X12 qualifier (e.g. ZZ, 01) — defaults to wildcard" }
      }
    }
  }
  // Add additional tools from tools/list as needed
];

const SYSTEM_PROMPT = `You are an ECGrid assistant. Help users interact with their B2B connectivity account.
When a user asks about their account, select the most appropriate ECGrid tool and call it.
Chain tools when needed — for example, list mailboxes first, then look up a specific one, then check its partners.
All tools return structured JSON data. Present results in plain language — never show raw JSON to the user.`;

async function chat(conversationHistory, userMessage) {
  conversationHistory.push({ role: "user", content: userMessage });

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    system: SYSTEM_PROMPT,
    tools: ECGRID_TOOLS,
    messages: conversationHistory,
  });

  if (response.stop_reason === "tool_use") {
    const toolUse = response.content.find(b => b.type === "tool_use");
    const toolResult = await ecgrid.callTool(toolUse.name, toolUse.input);

    conversationHistory.push({ role: "assistant", content: response.content });
    conversationHistory.push({
      role: "user",
      content: [{ type: "tool_result", tool_use_id: toolUse.id, content: JSON.stringify(toolResult) }]
    });

    const finalResponse = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      system: SYSTEM_PROMPT,
      tools: ECGRID_TOOLS,
      messages: conversationHistory,
    });

    const reply = finalResponse.content.find(b => b.type === "text").text;
    conversationHistory.push({ role: "assistant", content: reply });
    return reply;
  }

  const reply = response.content.find(b => b.type === "text").text;
  conversationHistory.push({ role: "assistant", content: reply });
  return reply;
}

// Usage
const history = [];
await ecgrid.initialize();

console.log(await chat(history, "What is my ECGrid auth level?"));
// → "Your ECGrid account is authenticated as TechOps on network 47."

console.log(await chat(history, "Show me the mailboxes on my network."));
// → "Network 47 has the following mailboxes: ..."

console.log(await chat(history, "Are there any transactions retrying right now?"));
// → "Yes — there are currently 6 outbound interchanges in E3010 Delay: Interchange Retry status ..."
```

### Python — Minimal Chat Loop

```python
import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
ecgrid = EcGridMcpClient(os.environ["ECGRID_API_KEY"])  # from earlier in this guide

# Tool registry — built from tools/list at startup; update as new tools are added
# All tools return structured JSON data; a subset also render interactive UI components
# in compatible AI clients (Claude Desktop, Claude.ai) — agent code is identical either way
ECGRID_TOOLS = [
    {
        "name": "hello-world",
        "description": "Verifies the ECGrid connection and returns the user's identity, auth level, network ID, and mailbox ID. Returns structured JSON.",
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Optional display name"}}
        }
    },
    {
        "name": "user_get-user-me",
        "description": "Returns the identity, auth level, network, and mailbox of the current API key holder. Returns structured JSON.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "mailbox_list-mailboxes",
        "description": "Lists all mailboxes on a network. Omit networkId to list the caller's own network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        "input_schema": {
            "type": "object",
            "properties": {"networkId": {"type": "integer", "description": "Optional — defaults to caller's home network"}}
        }
    },
    {
        "name": "partner_list-partners",
        "description": "Lists trading-partner interconnects for a mailbox or network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mailboxId": {"type": "integer"},
                "networkId": {"type": "integer"},
                "status": {"type": "string"}
            }
        }
    },
    {
        "name": "partner_check-partner-config",
        "description": "Health-checks a trading-partner interconnect for setup completeness, traffic history, active IDs, and scheduled moves. Returns structured JSON with isHealthy and issues list.",
        "input_schema": {
            "type": "object",
            "properties": {"interconnectId": {"type": "integer"}},
            "required": ["interconnectId"]
        }
    },
    {
        "name": "transaction_search-transactions",
        "description": "Searches EDI transactions by direction, type, date range, and view. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        "input_schema": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["Interchange", "File"]},
                "direction": {"type": "string", "enum": ["Inbound", "Outbound", "Both"]},
                "networkId": {"type": "integer"},
                "mailboxId": {"type": "integer"},
                "view": {"type": "string"}
            },
            "required": ["type", "direction"]
        }
    },
    {
        "name": "interchange_get-interchange-by-id",
        "description": "Returns the full detail of an EDI interchange including routing, status, raw ISA header, and carrying parcel IDs. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        "input_schema": {
            "type": "object",
            "properties": {"interchangeId": {"type": "integer"}},
            "required": ["interchangeId"]
        }
    },
    {
        "name": "parcel_get-parcel-by-id",
        "description": "Returns the full detail of a parcel including status, routing, and the interchange manifest. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        "input_schema": {
            "type": "object",
            "properties": {"parcelId": {"type": "integer"}},
            "required": ["parcelId"]
        }
    },
    {
        "name": "ecgrid-id_find-edi-ids",
        "description": "Finds ECGrid trading-partner ID records by wire EDI identifier or description substring. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "description": {"type": "string"},
                "networkId": {"type": "integer"},
                "qualifier": {"type": "string"}
            }
        }
    }
    # Add additional tools from tools/list as needed
]

SYSTEM_PROMPT = (
    "You are an ECGrid assistant. Help users interact with their B2B connectivity account. "
    "When a user asks about their account, select the most appropriate ECGrid tool and call it. "
    "Chain tools when needed — for example, list mailboxes first, then look up a specific one, then check its partners. "
    "All tools return structured JSON data. Present results in plain language — never show raw JSON to the user."
)

def chat(conversation_history: list, user_message: str) -> str:
    conversation_history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=ECGRID_TOOLS,
        messages=conversation_history,
    )

    if response.stop_reason == "tool_use":
        tool_use = next(b for b in response.content if b.type == "tool_use")
        tool_result = ecgrid.call_tool(tool_use.name, tool_use.input)

        conversation_history.append({"role": "assistant", "content": response.content})
        conversation_history.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": json.dumps(tool_result)}]
        })

        final = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=ECGRID_TOOLS,
            messages=conversation_history,
        )

        reply = next(b.text for b in final.content if b.type == "text")
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    reply = next(b.text for b in response.content if b.type == "text")
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

# Usage
history = []
ecgrid.initialize()

print(chat(history, "What is my ECGrid auth level?"))
# → "Your ECGrid account is authenticated as TechOps on network 47."

print(chat(history, "Show me the mailboxes on my network."))
# → "Network 47 has the following mailboxes: ..."

print(chat(history, "Are there any transactions retrying right now?"))
# → "Yes — there are currently 6 outbound interchanges in E3010 Delay: Interchange Retry status ..."
```

### C# — Minimal Chat Loop

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using Anthropic.SDK;
using Anthropic.SDK.Messaging;

var anthropicClient = new AnthropicClient(Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY"));
var ecgrid = new EcGridMcpClient(Environment.GetEnvironmentVariable("ECGRID_API_KEY")); // from earlier in this guide

// Tool registry — built from tools/list at startup; update as new tools are added
// All tools return structured JSON data; a subset also render interactive UI components
// in compatible AI clients (Claude Desktop, Claude.ai) — agent code is identical either way
var ecgridTools = new List<Tool>
{
    new Tool
    {
        Name = "hello-world",
        Description = "Verifies the ECGrid connection and returns the user's identity, auth level, network ID, and mailbox ID. Returns structured JSON.",
        InputSchema = new InputSchema
        {
            Type = "object",
            Properties = new Dictionary<string, Property>
            {
                ["name"] = new Property { Type = "string", Description = "Optional display name" }
            }
        }
    },
    new Tool
    {
        Name = "user_get-user-me",
        Description = "Returns the identity, auth level, network, and mailbox of the current API key holder. Returns structured JSON.",
        InputSchema = new InputSchema { Type = "object", Properties = new Dictionary<string, Property>() }
    },
    new Tool
    {
        Name = "mailbox_list-mailboxes",
        Description = "Lists all mailboxes on a network. Omit networkId to list the caller's own network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        InputSchema = new InputSchema
        {
            Type = "object",
            Properties = new Dictionary<string, Property>
            {
                ["networkId"] = new Property { Type = "integer", Description = "Optional — defaults to caller's home network" }
            }
        }
    },
    new Tool
    {
        Name = "partner_list-partners",
        Description = "Lists trading-partner interconnects for a mailbox or network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        InputSchema = new InputSchema
        {
            Type = "object",
            Properties = new Dictionary<string, Property>
            {
                ["mailboxId"] = new Property { Type = "integer" },
                ["networkId"] = new Property { Type = "integer" },
                ["status"] = new Property { Type = "string", Description = "Pending, Completed, Canceled, Delayed, Problem, AuthorizationRequired, or NoStatusChange" }
            }
        }
    },
    new Tool
    {
        Name = "transaction_search-transactions",
        Description = "Searches EDI transactions by direction, type, date range, and view. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        InputSchema = new InputSchema
        {
            Type = "object",
            Properties = new Dictionary<string, Property>
            {
                ["type"] = new Property { Type = "string", Description = "Interchange or File — required" },
                ["direction"] = new Property { Type = "string", Description = "Inbound, Outbound, or Both — required" },
                ["networkId"] = new Property { Type = "integer" },
                ["mailboxId"] = new Property { Type = "integer" },
                ["view"] = new Property { Type = "string", Description = "Archive, Blocked, Pending, NoRoute, PendingDownload, or DeliveryError" }
            },
            Required = new List<string> { "type", "direction" }
        }
    },
    new Tool
    {
        Name = "interchange_get-interchange-by-id",
        Description = "Returns full detail of an EDI interchange including routing, status, raw ISA header, and parcel IDs. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        InputSchema = new InputSchema
        {
            Type = "object",
            Properties = new Dictionary<string, Property>
            {
                ["interchangeId"] = new Property { Type = "integer", Description = "Numeric interchange ID" }
            },
            Required = new List<string> { "interchangeId" }
        }
    },
    new Tool
    {
        Name = "parcel_get-parcel-by-id",
        Description = "Returns full detail of a parcel including status, routing, and interchange manifest. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        InputSchema = new InputSchema
        {
            Type = "object",
            Properties = new Dictionary<string, Property>
            {
                ["parcelId"] = new Property { Type = "integer", Description = "Numeric parcel ID" }
            },
            Required = new List<string> { "parcelId" }
        }
    }
    // Add additional tools from tools/list as needed
};

const string SystemPrompt =
    "You are an ECGrid assistant. Help users interact with their B2B connectivity account. " +
    "When a user asks about their account, select the most appropriate ECGrid tool and call it. " +
    "Chain tools when needed — for example, list mailboxes first, then look up a specific one, then check its partners. " +
    "All tools return structured JSON data. Present results in plain language — never show raw JSON to the user.";

async Task<string> Chat(List<Message> history, string userMessage)
{
    history.Add(new Message { Role = RoleType.User, Content = userMessage });

    var response = await anthropicClient.Messages.GetClaudeMessageAsync(new MessageParameters
    {
        Model = AnthropicModels.Claude35Sonnet,
        MaxTokens = 1024,
        System = new List<SystemMessage> { new SystemMessage(SystemPrompt) },
        Tools = ecgridTools,
        Messages = history
    });

    if (response.StopReason == StopReason.ToolUse)
    {
        var toolUse = response.Content.OfType<ToolUseContent>().First();
        var toolResult = await ecgrid.CallToolAsync(toolUse.Name,
            JsonSerializer.Deserialize<Dictionary<string, object>>(toolUse.Input));

        history.Add(new Message { Role = RoleType.Assistant, Content = response.Content });
        history.Add(new Message
        {
            Role = RoleType.User,
            Content = new List<ContentBase>
            {
                new ToolResultContent
                {
                    ToolUseId = toolUse.Id,
                    Content = JsonSerializer.Serialize(toolResult)
                }
            }
        });

        var final = await anthropicClient.Messages.GetClaudeMessageAsync(new MessageParameters
        {
            Model = AnthropicModels.Claude35Sonnet,
            MaxTokens = 1024,
            System = new List<SystemMessage> { new SystemMessage(SystemPrompt) },
            Tools = ecgridTools,
            Messages = history
        });

        var reply = final.Content.OfType<TextContent>().First().Text;
        history.Add(new Message { Role = RoleType.Assistant, Content = reply });
        return reply;
    }

    var directReply = response.Content.OfType<TextContent>().First().Text;
    history.Add(new Message { Role = RoleType.Assistant, Content = directReply });
    return directReply;
}

// Usage
var conversationHistory = new List<Message>();
await ecgrid.InitializeAsync();

Console.WriteLine(await Chat(conversationHistory, "What is my ECGrid auth level?"));
// → "Your ECGrid account is authenticated as TechOps on network 47."

Console.WriteLine(await Chat(conversationHistory, "Show me the mailboxes on my network."));
// → "Network 47 has the following mailboxes: ..."

Console.WriteLine(await Chat(conversationHistory, "Are there any transactions retrying right now?"));
// → "Yes — there are currently 6 outbound interchanges in E3010 Delay: Interchange Retry status ..."
```

> This example uses the [Anthropic.SDK](https://www.nuget.org/packages/Anthropic.SDK) NuGet package. Install with: `dotnet add package Anthropic.SDK`

### Key Points

- **Conversation history** is maintained client-side and passed on every LLM call — the LLM has no memory between calls
- **Tool registry** should be built dynamically from `tools/list` so new ECGrid tools are picked up automatically without code changes
- **The LLM decides** when to call a tool — you don't need to parse the user's message yourself
- **ECGrid results go back to the LLM** as `tool_result` messages — the LLM interprets the structured JSON data and writes the user-facing response
- **The user never sees raw JSON** — that's the AI's job
- **Interactive UI components** render automatically in Claude Desktop and Claude.ai for the applicable tools — your agent code does not change; the same structured JSON is returned regardless of whether a UI component renders in the client
- For production use, add error handling around both the LLM call and the ECGrid tool call, and handle `max_tokens` exceeded gracefully
- **As more ECGrid tools ship**, extend the tool registry by refreshing `tools/list` and updating your system prompt to describe the new tools — the chat loop itself does not change
- **These examples use the Anthropic API** but the pattern applies to any LLM with tool/function calling support (OpenAI, Gemini, etc.) — replace the LLM client and tool schema format, keep the ECGrid client and the conversation history structure

> For Anthropic API documentation including tool use, conversation management, and model options see [docs.anthropic.com](https://docs.anthropic.com).

## Using ECGrid with Other LLMs

The ECGrid MCP client is identical regardless of which LLM you use. Only the LLM client and tool schema format change. This section covers the differences for OpenAI and provides a schema translation reference for other platforms.

### Tool Schema Translation

ECGrid tools are discovered via `tools/list` and return a standard JSON Schema `inputSchema`. Each LLM platform expects a slightly different format when you register tools:

| | Anthropic | OpenAI | Gemini |
|---|---|---|---|
| Tools array param | `tools` | `tools` | `tools` |
| Schema key | `input_schema` | `parameters` | `parameters` |
| Tool type field | `type: "custom"` (implicit) | `type: "function"` | `function_declarations` |
| Stop reason | `tool_use` | `tool_calls` | `functionCall` in content |
| Tool result role | `user` with `tool_result` content | `tool` role message | `user` with `functionResponse` content |
| Tool use ID field | `tool_use_id` | `tool_call_id` | not required |

When building the tool registry from `tools/list`, map `inputSchema` to `parameters` for OpenAI and Gemini instead of `input_schema`. Tool descriptions should note structured JSON return format and interactive UI component availability regardless of platform — the LLM uses this to set user expectations correctly.

### OpenAI — Minimal Chat Loop

The ECGrid client from earlier in this guide is unchanged. Only the LLM call and tool handling differ.

**JavaScript:**

```javascript
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const ecgrid = new EcGridMcpClient(process.env.ECGRID_API_KEY); // from earlier in this guide

// Tool registry — note: OpenAI uses "parameters" not "input_schema"
const ECGRID_TOOLS = [
  {
    type: "function",
    function: {
      name: "hello-world",
      description: "Verifies the ECGrid connection and returns the user's identity, auth level, network ID, and mailbox ID. Returns structured JSON.",
      parameters: {
        type: "object",
        properties: { name: { type: "string", description: "Optional display name" } }
      }
    }
  },
  {
    type: "function",
    function: {
      name: "mailbox_list-mailboxes",
      description: "Lists all mailboxes on a network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
      parameters: {
        type: "object",
        properties: { networkId: { type: "integer", description: "Optional — defaults to caller's home network" } }
      }
    }
  },
  {
    type: "function",
    function: {
      name: "transaction_search-transactions",
      description: "Searches EDI transactions by direction, type, date range, and view. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
      parameters: {
        type: "object",
        properties: {
          type: { type: "string", enum: ["Interchange", "File"] },
          direction: { type: "string", enum: ["Inbound", "Outbound", "Both"] },
          networkId: { type: "integer" },
          mailboxId: { type: "integer" },
          view: { type: "string" }
        },
        required: ["type", "direction"]
      }
    }
  }
  // Add additional tools from tools/list as needed
];

const SYSTEM_PROMPT = "You are an ECGrid assistant. Help users interact with their B2B connectivity account. " +
  "When a user asks about their account, call the appropriate ECGrid tool. " +
  "All tools return structured JSON data. Present results in plain language — never show raw JSON to the user.";

async function chat(conversationHistory, userMessage) {
  conversationHistory.push({ role: "user", content: userMessage });

  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "system", content: SYSTEM_PROMPT }, ...conversationHistory],
    tools: ECGRID_TOOLS,
    tool_choice: "auto",
  });

  const message = response.choices[0].message;

  if (message.tool_calls?.length) {
    conversationHistory.push(message);

    for (const toolCall of message.tool_calls) {
      const args = JSON.parse(toolCall.function.arguments);
      const toolResult = await ecgrid.callTool(toolCall.function.name, args);

      conversationHistory.push({
        role: "tool",
        tool_call_id: toolCall.id,
        content: JSON.stringify(toolResult),
      });
    }

    const final = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "system", content: SYSTEM_PROMPT }, ...conversationHistory],
      tools: ECGRID_TOOLS,
    });

    const reply = final.choices[0].message.content;
    conversationHistory.push({ role: "assistant", content: reply });
    return reply;
  }

  conversationHistory.push({ role: "assistant", content: message.content });
  return message.content;
}

// Usage
const history = [];
await ecgrid.initialize();
console.log(await chat(history, "What is my ECGrid auth level?"));
```

**Python:**

```python
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
ecgrid = EcGridMcpClient(os.environ["ECGRID_API_KEY"])  # from earlier in this guide

# Tool registry — note: OpenAI uses "parameters" not "input_schema"
ECGRID_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "hello-world",
            "description": "Verifies the ECGrid connection and returns the user's identity, auth level, network ID, and mailbox ID. Returns structured JSON.",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Optional display name"}}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mailbox_list-mailboxes",
            "description": "Lists all mailboxes on a network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
            "parameters": {
                "type": "object",
                "properties": {"networkId": {"type": "integer", "description": "Optional — defaults to caller's home network"}}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transaction_search-transactions",
            "description": "Searches EDI transactions by direction, type, date range, and view. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["Interchange", "File"]},
                    "direction": {"type": "string", "enum": ["Inbound", "Outbound", "Both"]},
                    "networkId": {"type": "integer"},
                    "mailboxId": {"type": "integer"},
                    "view": {"type": "string"}
                },
                "required": ["type", "direction"]
            }
        }
    }
    # Add additional tools from tools/list as needed
]

SYSTEM_PROMPT = (
    "You are an ECGrid assistant. Help users interact with their B2B connectivity account. "
    "When a user asks about their account, call the appropriate ECGrid tool. "
    "All tools return structured JSON data. Present results in plain language — never show raw JSON to the user."
)

def chat(conversation_history: list, user_message: str) -> str:
    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        tools=ECGRID_TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    if message.tool_calls:
        conversation_history.append(message)

        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            tool_result = ecgrid.call_tool(tool_call.function.name, args)
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result),
            })

        final = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            tools=ECGRID_TOOLS,
        )
        reply = final.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    reply = message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

# Usage
history = []
ecgrid.initialize()
print(chat(history, "What is my ECGrid auth level?"))
```

**C#:**

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;
using OpenAI;
using OpenAI.Chat;

var openaiClient = new ChatClient(model: "gpt-4o", apiKey: Environment.GetEnvironmentVariable("OPENAI_API_KEY"));
var ecgrid = new EcGridMcpClient(Environment.GetEnvironmentVariable("ECGRID_API_KEY")); // from earlier in this guide

var ecgridTools = new List<ChatTool>
{
    ChatTool.CreateFunctionTool(
        functionName: "hello-world",
        functionDescription: "Verifies the ECGrid connection and returns the user's identity, auth level, network ID, and mailbox ID. Returns structured JSON.",
        functionParameters: BinaryData.FromString("""
            {"type":"object","properties":{"name":{"type":"string","description":"Optional display name"}}}
            """)
    ),
    ChatTool.CreateFunctionTool(
        functionName: "mailbox_list-mailboxes",
        functionDescription: "Lists all mailboxes on a network. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        functionParameters: BinaryData.FromString("""
            {"type":"object","properties":{"networkId":{"type":"integer","description":"Optional — defaults to caller's home network"}}}
            """)
    ),
    ChatTool.CreateFunctionTool(
        functionName: "transaction_search-transactions",
        functionDescription: "Searches EDI transactions by direction, type, date range, and view. Returns structured JSON. Also renders an interactive UI component in compatible AI clients.",
        functionParameters: BinaryData.FromString("""
            {"type":"object","properties":{"type":{"type":"string"},"direction":{"type":"string"},"networkId":{"type":"integer"},"mailboxId":{"type":"integer"},"view":{"type":"string"}},"required":["type","direction"]}
            """)
    )
    // Add additional tools from tools/list as needed
};

const string SystemPrompt =
    "You are an ECGrid assistant. Help users interact with their B2B connectivity account. " +
    "When a user asks about their account, call the appropriate ECGrid tool. " +
    "All tools return structured JSON data. Present results in plain language — never show raw JSON to the user.";

async Task<string> Chat(List<ChatMessage> history, string userMessage)
{
    history.Add(new UserChatMessage(userMessage));

    var options = new ChatCompletionOptions();
    foreach (var tool in ecgridTools) options.Tools.Add(tool);

    ChatCompletion response = await openaiClient.CompleteChatAsync(
        new List<ChatMessage> { new SystemChatMessage(SystemPrompt) }.Concat(history).ToList(), options);

    if (response.FinishReason == ChatFinishReason.ToolCalls)
    {
        history.Add(new AssistantChatMessage(response));
        var toolResults = new List<ToolChatMessage>();
        foreach (var toolCall in response.ToolCalls)
        {
            var args = JsonSerializer.Deserialize<Dictionary<string, object>>(toolCall.FunctionArguments);
            var toolResult = await ecgrid.CallToolAsync(toolCall.FunctionName, args);
            toolResults.Add(new ToolChatMessage(toolCall.Id, JsonSerializer.Serialize(toolResult)));
        }
        history.AddRange(toolResults);

        ChatCompletion final = await openaiClient.CompleteChatAsync(
            new List<ChatMessage> { new SystemChatMessage(SystemPrompt) }.Concat(history).ToList(), options);

        var reply = final.Content[0].Text;
        history.Add(new AssistantChatMessage(reply));
        return reply;
    }

    var directReply = response.Content[0].Text;
    history.Add(new AssistantChatMessage(directReply));
    return directReply;
}

// Usage
var conversationHistory = new List<ChatMessage>();
await ecgrid.InitializeAsync();
Console.WriteLine(await Chat(conversationHistory, "What is my ECGrid auth level?"));
```

> This example uses the [OpenAI .NET SDK](https://www.nuget.org/packages/OpenAI). Install with: `dotnet add package OpenAI`

> For OpenAI API documentation including function calling and conversation management see [platform.openai.com/docs](https://platform.openai.com/docs).

## See Also

- [Protocol Reference](./protocol-reference.md) — full MCP protocol details
- [Resources & Prompts](./resources-and-prompts.md) — MCP resources and guided prompts
- [Other AI Platforms](./other-ai-platforms.md) — connecting non-MCP platforms
- [Troubleshooting](./troubleshooting.md) — common errors and fixes
- [ECGrid Developer Portal](https://api.ecgridos.io/) — API keys, full API reference
- [ECGrid Support](https://ecgrid.freshdesk.com/support/home)
