---
title: Direct HTTP (Developers)
sidebar_position: 3
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Developer HTTP connection guide - Greg Kolinski
*/}

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
- [Building Agents](../building-agents) — chat loop patterns, multi-LLM examples
