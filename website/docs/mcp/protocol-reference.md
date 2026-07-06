{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: MCP protocol reference - Greg Kolinski
*/}
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
