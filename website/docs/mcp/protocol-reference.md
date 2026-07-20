---
title: Protocol Reference
sidebar_position: 4
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP protocol reference - Greg Kolinski
2026-07-20: Update required headers for multi-credential model - Greg Kolinski
*/}

# Protocol Reference

Technical reference for developers calling the ECGrid MCP Server directly over HTTP.

## HTTP Endpoints

### MCP Protocol

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/mcp` | Required | JSON-RPC 2.0 entry point — `initialize`, `tools/list`, `tools/call` |
| `GET` | `/mcp` | Required | Server-sent event stream for server-initiated notifications |

POST body size is capped at **64 KB**.

### Discovery Endpoints

These endpoints are anonymous and CORS-enabled. Useful for building integrations, displaying tool catalogs, or configuring MCP clients programmatically.

| Method | Path | Content-Type | Purpose |
|---|---|---|---|
| `GET` | `/.well-known/mcp` | `application/json` | MCP discovery metadata — spec version, server info, capabilities, auth methods, rate limits, and links to tools.json and server-card.json |
| `GET` | `/.well-known/mcp/server-card.json` | `application/json` | Server card — full metadata including a summary list of every registered tool |
| `GET` | `/tools.json` | `application/json` | Tools registry — ordered list of all tools with name, description, and full input schema |
| `GET` | `/llms.txt` | `text/plain` | LLM guidance file — plain-text description of the server for LLM-based discovery |
| `GET` | `/` | `text/html` | Server landing page |
| `GET` | `/tools` | `text/html` | Interactive tools browser |

**`/.well-known/mcp` example response:**
```json
{
  "spec_version": "2026-01-24",
  "server_name": "ECGrid MCP Server",
  "server_version": "1.2.0",
  "endpoints": { "streamable_http": "https://mcp.ecgrid.io/mcp" },
  "capabilities": { "tools": true, "resources": true, "prompts": true, "sampling": false },
  "authentication": {
    "required": true,
    "methods": ["api_key"],
    "api_key": {
      "headers": {
        "X-Connectivity-API-Key": "ECGrid API key — obtain from https://api.ecgridos.io/",
        "X-DataSync-API-Key": "GPA Personal Access Token (PAT)",
        "X-Translation-API-Key": "Translation API key"
      },
    }
  },
  "rate_limits": { "requests_per_minute": 100 },
  "documentation": "https://api.ecgridos.io/",
  "tools_list": "https://mcp.ecgrid.io/tools.json",
  "server_card": "https://mcp.ecgrid.io/.well-known/mcp/server-card.json"
}
```

**`/tools.json` example response:**
```json
{
  "server": {
    "name": "ECGrid MCP Server",
    "version": "1.2.0",
    "generatedAt": "2026-07-07T12:00:00.0000000Z"
  },
  "tools": [
    {
      "name": "connectivity_interchange_get-interchange-by-id",
      "description": "Look up a single EDI interchange by its numeric interchange ID...",
      "inputSchema": { ... }
    }
  ]
}
```

### Health Probes

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/health/live` | None | Liveness probe — `200 {"status":"healthy"}` if the process is running |
| `GET` | `/health/ready` | None | Readiness probe — `200` when healthy, `503` when not ready |

Health probes are anonymous.

## Required Headers

Every POST to `/mcp` requires `Content-Type`, `Accept`, and at least one credential header:

```
Content-Type: application/json
Accept: application/json, text/event-stream
X-Connectivity-API-Key: YOUR_API_KEY_HERE
```

Supply a header for each product you want to use. A single request can carry multiple credential headers:

```
X-Connectivity-API-Key: YOUR_CONNECTIVITY_KEY
X-DataSync-API-Key: YOUR_GPA_PAT
X-Translation-API-Key: YOUR_TRANSLATION_KEY
```

Omitting or incorrectly setting `Accept` returns `406 Not Acceptable`. Sending no recognized credential returns `401`.

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

## MCP Inspector

Use the official [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to explore tools interactively:

```bash
npx @modelcontextprotocol/inspector "https://mcp.ecgrid.io/mcp" --header "X-Connectivity-API-Key:YOUR_API_KEY_HERE"
```
