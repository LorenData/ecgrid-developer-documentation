---
title: Quick Start — REST API
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API quick start page - Greg Kolinski */}
{/* 2026-05-07: Rewrote with multi-language tabbed examples (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Quick Start — REST API

This guide walks you through the most common ECGrid workflow — checking your inbox, downloading a file, and confirming delivery — using the REST API. Examples are shown in cURL, C#, Java, Node.js, and Python.

## Prerequisites

- An ECGrid API key (see [Authentication & API Keys](./authentication.md))
- Base URL: `https://rest.ecgrid.io`

## Step 1 — Verify Connectivity

The version endpoint requires no authentication and confirms you can reach the API.

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl https://rest.ecgrid.io/v2/auth/version
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
var version = await http.GetFromJsonAsync<JsonDocument>("/v2/auth/version");
Console.WriteLine(version?.RootElement.ToString());
```

</TabItem>
<TabItem value="java" label="Java">

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/version"))
    .GET()
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const response = await fetch('https://rest.ecgrid.io/v2/auth/version');
const data = await response.json();
console.log(data);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import requests
response = requests.get('https://rest.ecgrid.io/v2/auth/version')
print(response.json())
```

</TabItem>
</Tabs>

Expected response:

```json
{
  "success": true,
  "data": { "version": "2.6.x", "build": "..." }
}
```

## Step 2 — Authenticate

Add your API key to every request using the `X-API-Key` header.

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Set once; all subsequent curl commands include it
export ECGRID_API_KEY="your-api-key-here"

curl https://rest.ecgrid.io/v2/auth/version \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// Register once in DI; the factory adds the header to every request
services.AddHttpClient("ecgrid", client =>
{
    client.BaseAddress = new Uri("https://rest.ecgrid.io");
    client.DefaultRequestHeaders.Add(
        "X-API-Key",
        configuration["ECGrid:ApiKey"]);
});
```

</TabItem>
<TabItem value="java" label="Java">

```java
String apiKey = System.getenv("ECGRID_API_KEY");
HttpClient client = HttpClient.newHttpClient();

// Add to every request:
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/version"))
    .header("X-API-Key", apiKey)
    .GET()
    .build();
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const API_KEY = process.env.ECGRID_API_KEY;
const BASE_URL = 'https://rest.ecgrid.io';

// Reuse this headers object on every request
const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY
};
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

BASE_URL = 'https://rest.ecgrid.io'
HEADERS = {'X-API-Key': os.environ['ECGRID_API_KEY']}

# Pass headers= to every requests call
```

</TabItem>
</Tabs>

:::tip Bearer JWT
You can also authenticate with a short-lived JWT via `POST /v2/auth/login`. API Key auth is simpler for server-to-server workflows. See [Authentication & API Keys](./authentication.md) for details.
:::

## Step 3 — Check Your Inbox

`POST /v2/parcels/pending-inbox-list` returns all parcels that have not yet been downloaded.

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
var response = await http.PostAsJsonAsync("/v2/parcels/pending-inbox-list", new { });
response.EnsureSuccessStatusCode();
var inbox = await response.Content.ReadFromJsonAsync<JsonDocument>();
```

</TabItem>
<TabItem value="java" label="Java">

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/pending-inbox-list"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString("{}"))
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const response = await fetch(`${BASE_URL}/v2/parcels/pending-inbox-list`, {
  method: 'POST',
  headers
});
const { data: parcels } = await response.json();
```

</TabItem>
<TabItem value="python" label="Python">

```python
parcels = requests.post(
    f'{BASE_URL}/v2/parcels/pending-inbox-list',
    headers=HEADERS
).json()['data']
```

</TabItem>
</Tabs>

Response — a list of `ParcelIDInfo` records:

```json
{
  "success": true,
  "data": [
    {
      "parcelId": 123456,
      "fileName": "invoice_850.edi",
      "bytes": 4096,
      "status": "InBoxReady",
      ".....":"......"
    }
  ]
}
```

## Step 4 — Download a Parcel

`POST /v2/parcels/download` returns the raw EDI file as a base64-encoded string in the `content` field.

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST https://rest.ecgrid.io/v2/parcels/download \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"parcelId": 123456}'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
var response = await http.PostAsJsonAsync("/v2/parcels/download", new { parcelId = 123456L });
response.EnsureSuccessStatusCode();
var result = await response.Content.ReadFromJsonAsync<JsonDocument>();
var content = result!.RootElement.GetProperty("data").GetProperty("content").GetString();
var ediBytes = Convert.FromBase64String(content!);
await File.WriteAllBytesAsync("invoice_850.edi", ediBytes);
```

</TabItem>
<TabItem value="java" label="Java">

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/download"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString("{\"parcelId\": 123456}"))
    .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

// Parse JSON and decode base64 content using your preferred JSON library
var mapper = new com.fasterxml.jackson.databind.ObjectMapper();
var data = mapper.readTree(response.body()).get("data");
byte[] ediBytes = java.util.Base64.getDecoder().decode(data.get("content").asText());
java.nio.file.Files.write(java.nio.file.Path.of(data.get("fileName").asText()), ediBytes);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const response = await fetch(`${BASE_URL}/v2/parcels/download`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ parcelId: 123456 })
});
const { data } = await response.json();
const ediBytes = Buffer.from(data.content, 'base64');
await fs.promises.writeFile(data.fileName, ediBytes);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import base64

data = requests.post(
    f'{BASE_URL}/v2/parcels/download',
    headers=HEADERS,
    json={'parcelId': 123456}
).json()['data']

edi_bytes = base64.b64decode(data['content'])
open(data['fileName'], 'wb').write(edi_bytes)
```

</TabItem>
</Tabs>

## Step 5 — Confirm the Download

`POST /v2/parcels/confirm` marks the parcel as transferred so it no longer appears in inbox polls. **Always confirm after saving the file.** Un-confirmed parcels remain on the next poll cycle.

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST https://rest.ecgrid.io/v2/parcels/confirm \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"parcelId": 123456}'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
var response = await http.PostAsJsonAsync("/v2/parcels/confirm", new { parcelId = 123456L });
response.EnsureSuccessStatusCode();
```

</TabItem>
<TabItem value="java" label="Java">

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/confirm"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString("{\"parcelId\": 123456}"))
    .build();
client.send(request, HttpResponse.BodyHandlers.ofString());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
await fetch(`${BASE_URL}/v2/parcels/confirm`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ parcelId: 123456 })
});
```

</TabItem>
<TabItem value="python" label="Python">

```python
requests.post(
    f'{BASE_URL}/v2/parcels/confirm',
    headers=HEADERS,
    json={'parcelId': 123456}
)
```

</TabItem>
</Tabs>

## Complete Example

A full poll → download → confirm workflow in each language.

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
#!/usr/bin/env bash
# Requires: curl, jq
set -euo pipefail

BASE="https://rest.ecgrid.io"

# Poll for pending parcels
INBOX=$(curl -s -X POST "$BASE/v2/parcels/pending-inbox-list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}')

COUNT=$(echo "$INBOX" | jq '.data | length')
echo "Found $COUNT parcel(s) waiting."

echo "$INBOX" | jq -c '.data[]' | while read -r PARCEL; do
  ID=$(echo "$PARCEL" | jq '.parcelId')
  NAME=$(echo "$PARCEL" | jq -r '.fileName')
  echo "Downloading parcel $ID: $NAME"

  DOWNLOAD=$(curl -s -X POST "$BASE/v2/parcels/download" \
    -H "X-API-Key: $ECGRID_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"parcelId\": $ID}")

  OUT=$(echo "$DOWNLOAD" | jq -r '.data.fileName')
  echo "$DOWNLOAD" | jq -r '.data.content' | base64 -d > "$OUT"
  echo "  Saved $OUT"

  curl -s -X POST "$BASE/v2/parcels/confirm" \
    -H "X-API-Key: $ECGRID_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"parcelId\": $ID}" > /dev/null

  echo "  Confirmed parcel $ID"
done
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — full poll → download → confirm workflow
// API key loaded from IConfiguration; IHttpClientFactory manages connections

using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((ctx, services) =>
    {
        services.AddHttpClient("ecgrid", client =>
        {
            client.BaseAddress = new Uri("https://rest.ecgrid.io");
            client.DefaultRequestHeaders.Add(
                "X-API-Key",
                ctx.Configuration["ECGrid:ApiKey"]
                    ?? throw new InvalidOperationException("ECGrid:ApiKey not configured."));
        });
        services.AddTransient<EcGridWorkflow>();
    })
    .Build();

await host.Services.GetRequiredService<EcGridWorkflow>().RunAsync();

public class EcGridWorkflow(IHttpClientFactory factory)
{
    public async Task RunAsync()
    {
        var http = factory.CreateClient("ecgrid");

        var inboxResp = await http.PostAsJsonAsync("/v2/parcels/pending-inbox-list", new { });
        inboxResp.EnsureSuccessStatusCode();
        using var inboxDoc = await JsonDocument.ParseAsync(
            await inboxResp.Content.ReadAsStreamAsync());

        var parcels = inboxDoc.RootElement.GetProperty("data").EnumerateArray().ToList();
        Console.WriteLine($"Found {parcels.Count} parcel(s) waiting.");

        foreach (var parcel in parcels)
        {
            var id   = parcel.GetProperty("parcelId").GetInt64();
            var name = parcel.GetProperty("fileName").GetString();
            Console.WriteLine($"Downloading parcel {id}: {name}");

            var dlResp = await http.PostAsJsonAsync("/v2/parcels/download", new { parcelId = id });
            dlResp.EnsureSuccessStatusCode();
            using var dlDoc = await JsonDocument.ParseAsync(
                await dlResp.Content.ReadAsStreamAsync());
            var data     = dlDoc.RootElement.GetProperty("data");
            var fileName = data.GetProperty("fileName").GetString()!;
            var ediBytes = Convert.FromBase64String(data.GetProperty("content").GetString()!);
            await File.WriteAllBytesAsync(fileName, ediBytes);
            Console.WriteLine($"  Saved {ediBytes.Length:N0} bytes to {fileName}");

            var cfResp = await http.PostAsJsonAsync("/v2/parcels/confirm", new { parcelId = id });
            cfResp.EnsureSuccessStatusCode();
            Console.WriteLine($"  Confirmed parcel {id}.");
        }
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — full poll → download → confirm workflow
// Requires Jackson for JSON parsing: com.fasterxml.jackson.core:jackson-databind

import java.net.URI;
import java.net.http.*;
import java.nio.file.*;
import java.util.Base64;
import com.fasterxml.jackson.databind.*;

public class EcGridQuickStart {

    private static final String BASE = "https://rest.ecgrid.io";
    private static final String API_KEY = System.getenv("ECGRID_API_KEY");
    private static final HttpClient CLIENT = HttpClient.newHttpClient();
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        // Step 1: Poll for pending parcels
        var inboxRes = post("/v2/parcels/pending-inbox-list", "{}");
        var parcels  = MAPPER.readTree(inboxRes).get("data");
        System.out.printf("Found %d parcel(s) waiting.%n", parcels.size());

        for (var parcel : parcels) {
            long   id   = parcel.get("parcelId").asLong();
            String name = parcel.get("fileName").asText();
            System.out.printf("Downloading parcel %d: %s%n", id, name);

            // Step 2: Download
            String dlBody = String.format("{\"parcelId\": %d}", id);
            var dlTree    = MAPPER.readTree(post("/v2/parcels/download", dlBody)).get("data");
            byte[] edi    = Base64.getDecoder().decode(dlTree.get("content").asText());
            Files.write(Path.of(dlTree.get("fileName").asText()), edi);
            System.out.printf("  Saved %d bytes%n", edi.length);

            // Step 3: Confirm
            post("/v2/parcels/confirm", String.format("{\"parcelId\": %d}", id));
            System.out.printf("  Confirmed parcel %d%n", id);
        }
    }

    private static String post(String path, String body) throws Exception {
        var request = HttpRequest.newBuilder()
            .uri(URI.create(BASE + path))
            .header("X-API-Key", API_KEY)
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString()).body();
    }
}
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — native fetch, no dependencies
import { promises as fs } from 'fs';

const BASE    = 'https://rest.ecgrid.io';
const HEADERS = {
  'Content-Type': 'application/json',
  'X-API-Key':    process.env.ECGRID_API_KEY
};

async function post(path, body = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`${path} → ${res.status}`);
  return res.json();
}

// Step 1: Poll for pending parcels
const { data: parcels } = await post('/v2/parcels/pending-inbox-list');
console.log(`Found ${parcels.length} parcel(s) waiting.`);

for (const parcel of parcels) {
  console.log(`Downloading parcel ${parcel.parcelId}: ${parcel.fileName}`);

  // Step 2: Download
  const { data: dl } = await post('/v2/parcels/download', { parcelId: parcel.parcelId });
  const ediBytes = Buffer.from(dl.content, 'base64');
  await fs.writeFile(dl.fileName, ediBytes);
  console.log(`  Saved ${ediBytes.length} bytes to ${dl.fileName}`);

  // Step 3: Confirm
  await post('/v2/parcels/confirm', { parcelId: parcel.parcelId });
  console.log(`  Confirmed parcel ${parcel.parcelId}.`);
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python 3.8+ — pip install requests
import os, base64, requests
from pathlib import Path

BASE    = 'https://rest.ecgrid.io'
HEADERS = {'X-API-Key': os.environ['ECGRID_API_KEY']}

def post(path, body=None):
    r = requests.post(f'{BASE}{path}', headers=HEADERS, json=body or {})
    r.raise_for_status()
    return r.json()

# Step 1: Poll for pending parcels
parcels = post('/v2/parcels/pending-inbox-list')['data']
print(f'Found {len(parcels)} parcel(s) waiting.')

for parcel in parcels:
    print(f'Downloading parcel {parcel["parcelId"]}: {parcel["fileName"]}')

    # Step 2: Download
    dl       = post('/v2/parcels/download', {'parcelId': parcel['parcelId']})['data']
    edi_bytes = base64.b64decode(dl['content'])
    Path(dl['fileName']).write_bytes(edi_bytes)
    print(f'  Saved {len(edi_bytes)} bytes to {dl["fileName"]}')

    # Step 3: Confirm
    post('/v2/parcels/confirm', {'parcelId': parcel['parcelId']})
    print(f'  Confirmed parcel {parcel["parcelId"]}.')
```

</TabItem>
</Tabs>

## Next Steps

- [Authentication & API Keys](./authentication.md) — manage credentials and auth methods
- [REST API Reference](../rest-api/overview.md) — full endpoint documentation for all 121 endpoints
- [Common Operations](../common-operations/overview.md) — end-to-end workflow guides
- [Code Samples](../code-samples/overview.md) — complete .NET 10 sample projects
