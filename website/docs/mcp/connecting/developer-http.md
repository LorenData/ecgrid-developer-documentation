---
title: Direct HTTP (Developers)
sidebar_position: 4
---

{/*
AI Attribution — Loren Data AI Use Policy §8.2
Tool: Claude Code (Anthropic)
2026-07-06: Developer HTTP connection guide - Greg Kolinski
2026-07-07: Add JavaScript and Python examples, convert to tabs - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

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

## Example

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

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
    // Step 1 — extract the data: line from the SSE envelope
    var dataLine = body.Split('\n')
        .FirstOrDefault(l => l.StartsWith("data: "))?.Substring(6) ?? body;
    var envelope = JsonDocument.Parse(dataLine).RootElement;
    // Step 2 — parse content[0].text as JSON to get the structured data
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

</TabItem>
<TabItem value="javascript" label="JavaScript">

```javascript
const BASE_URL = "https://mcp.ecgrid.io/mcp";
const API_KEY = "YOUR_API_KEY_HERE";

async function post(payload) {
  const res = await fetch(BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json, text/event-stream",
      "X-APIKey": API_KEY,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  // Step 1 — extract the data: line from the SSE envelope
  const raw = await res.text();
  const dataLine = raw.split("\n").find(l => l.startsWith("data: "));
  const envelope = JSON.parse(dataLine.slice(6));
  if (envelope.error) throw new Error(`MCP error: ${JSON.stringify(envelope.error)}`);
  // Step 2 — parse content[0].text as JSON to get the structured data
  return JSON.parse(envelope.result.content[0].text);
}

const result = await post({
  jsonrpc: "2.0", id: 1, method: "tools/call",
  params: {
    name: "connectivity_system_hello-world",
    arguments: { request: { name: "My Agent" } },
  },
});
console.log(result);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import httpx
import json

BASE_URL = "https://mcp.ecgrid.io/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "X-APIKey": "YOUR_API_KEY_HERE",
}

def post(payload: dict) -> dict:
    response = httpx.post(BASE_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    # Step 1 — extract the data: line from the SSE envelope
    for line in response.text.splitlines():
        if line.startswith("data: "):
            envelope = json.loads(line[6:])
            if "error" in envelope:
                raise Exception(f"MCP error: {envelope['error']}")
            # Step 2 — parse content[0].text as JSON to get the structured data
            return json.loads(envelope["result"]["content"][0]["text"])
    raise ValueError("No data line found in SSE response")

result = post({
    "jsonrpc": "2.0", "id": 1, "method": "tools/call",
    "params": {
        "name": "connectivity_system_hello-world",
        "arguments": {"request": {"name": "My Agent"}},
    },
})
print(result)
```

</TabItem>
</Tabs>

## See Also

- [Protocol Reference](../protocol-reference.md) — full SSE format, two-step parse, error codes
- [Building Agents](../building-agents) — chat loop patterns, multi-LLM examples
