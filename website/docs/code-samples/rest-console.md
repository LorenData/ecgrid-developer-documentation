---
title: REST Console Sample
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created REST Console sample documentation page - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs to REST console sample key patterns - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# REST Console Sample

The `ECGrid-REST-dotnet10-Console` project is the simplest starting point for ECGrid REST integration. It walks through a complete file exchange workflow using a .NET 10 console application with top-level statements.

## Project Location

```
samples/rest/ECGrid-REST-dotnet10-Console/
```

## What It Demonstrates

This sample covers the core EDI file exchange workflow end to end:

1. **Check version** — confirm connectivity and API version
2. **Check inbox** — list parcels waiting for download
3. **Download parcel** — retrieve the EDI file content
4. **Confirm download** — acknowledge receipt so ECGrid marks the parcel delivered
5. **Upload file** — send an outbound EDI file to a trading partner

## Key Files

| File | Purpose |
|---|---|
| `Program.cs` | Entry point — all workflow logic using top-level statements |
| `appsettings.json` | Base configuration (base URL, mailbox ID, etc.) |
| `appsettings.Development.json` | Local overrides (excluded from source control) |

## Configuration

The API key and connection settings are loaded from `IConfiguration`. Add your API key via user-secrets to avoid committing credentials:

```bash
cd samples/rest/ECGrid-REST-dotnet10-Console
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
```

The `appsettings.json` structure used by the sample:

```json
{
  "ECGrid": {
    "BaseUrl": "https://rest.ecgrid.io",
    "ApiKey": "",
    "MailboxId": 0
  }
}
```

## Key Patterns

### HttpClient Setup

The sample configures `HttpClient` through the host builder so the API key is applied to every request automatically:

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# cURL passes the API key as a header on every request — no setup phase needed
# Export the key once in your shell session
export ECGRID_API_KEY="your-api-key-here"

# Every request uses it like this:
curl -s \
  -H "X-API-Key: $ECGRID_API_KEY" \
  https://rest.ecgrid.io/v2/auth/version | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// Program.cs — .NET 10 top-level statements
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = Host.CreateApplicationBuilder(args);

host.Services.AddHttpClient("ecgrid", (sp, client) =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    client.BaseAddress = new Uri(config["ECGrid:BaseUrl"]!);
    // API key authentication — key loaded from IConfiguration, never hardcoded
    client.DefaultRequestHeaders.Add("X-API-Key", config["ECGrid:ApiKey"]!);
});

var app = host.Build();
var httpFactory = app.Services.GetRequiredService<IHttpClientFactory>();
var http = httpFactory.CreateClient("ecgrid");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — reusable HttpClient with API key applied to every request
// Use a request factory helper since Java's HttpClient doesn't support default headers
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;

class EcGridClient {
    private final HttpClient http = HttpClient.newHttpClient();
    private final String apiKey;
    private final String baseUrl;

    EcGridClient(String apiKey, String baseUrl) {
        this.apiKey   = apiKey;
        this.baseUrl  = baseUrl;
    }

    HttpRequest.Builder request(String path) {
        return HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + path))
            .header("Content-Type", "application/json")
            .header("X-API-Key", apiKey);
    }

    // Usage: http.send(client.request("/v2/auth/version").GET().build(), BodyHandlers.ofString())
}
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — reusable fetch wrapper with API key header
const BASE_URL = 'https://rest.ecgrid.io';
const API_KEY  = process.env.ECGRID_API_KEY;

function ecgridFetch(path, options = {}) {
  return fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY,
      ...options.headers
    }
  });
}

// Usage: const resp = await ecgridFetch('/v2/auth/version');
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — requests.Session with API key applied to every request
import os, requests

api_key = os.environ["ECGRID_API_KEY"]

session = requests.Session()
session.headers.update({
    "X-API-Key": api_key,
    "Content-Type": "application/json"
})
session.base_url = "https://rest.ecgrid.io"

# Usage: resp = session.get(session.base_url + "/v2/auth/version")
```

</TabItem>
</Tabs>

### Inbox Check and Download Loop

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Check inbox and print parcel IDs
curl -s -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"mailboxId":0,"pageNo":1,"recordsPerPage":25}' | jq '.data[].parcelId'

# Download a specific parcel (replace 12345)
curl -s -X POST https://rest.ecgrid.io/v2/parcels/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"parcelID":12345}' -o parcel-12345.edi

# Confirm receipt
curl -s -X POST https://rest.ecgrid.io/v2/parcels/confirm \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"parcelID":12345}'
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// Check inbox and process each waiting parcel
var inboxResponse = await http.PostAsJsonAsync(
    "v2/parcels/pending-inbox-list", new { mailboxId, pageNo = 1, recordsPerPage = 25 });
var inbox = await inboxResponse.Content.ReadFromJsonAsync<ApiResponse<List<ParcelSummary>>>();

foreach (var parcel in inbox?.Data ?? [])
{
    // Download the parcel content
    var download = await http.GetAsync($"/v2/parcels/{parcel.ParcelId}/download");
    var ediContent = await download.Content.ReadAsByteArrayAsync();

    // Save locally — production code would route to a processor
    await File.WriteAllBytesAsync($"parcel-{parcel.ParcelId}.edi", ediContent);

    // Confirm receipt so ECGrid marks the parcel as delivered
    await http.PostAsync($"/v2/parcels/{parcel.ParcelId}/confirm", null);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — inbox check and download loop
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String base = "https://rest.ecgrid.io";

// Get inbox list
var inboxResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/pending-inbox-list"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"mailboxId\":0,\"pageNo\":1,\"recordsPerPage\":25}"))
    .build(), BodyHandlers.ofString());
// Parse parcel list from inboxResp.body() and iterate...

// For each parcel — download
long parcelId = 12345L;
var downloadResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/download"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"parcelID\":" + parcelId + "}"))
    .build(), BodyHandlers.ofByteArray());
Files.write(Path.of("parcel-" + parcelId + ".edi"), downloadResp.body());

// Confirm receipt
http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/confirm"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"parcelID\":" + parcelId + "}"))
    .build(), BodyHandlers.discarding());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — inbox check and download loop
import fs from 'node:fs/promises';

const apiKey = process.env.ECGRID_API_KEY;
const base = 'https://rest.ecgrid.io';
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Get inbox list
const inboxResp = await fetch(`${base}/v2/parcels/pending-inbox-list`, {
  method: 'POST', headers,
  body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
});
const inbox = await inboxResp.json();

for (const parcel of inbox.data ?? []) {
  // Download parcel
  const dlResp = await fetch(`${base}/v2/parcels/download`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
  const bytes = Buffer.from(await dlResp.arrayBuffer());
  await fs.writeFile(`parcel-${parcel.parcelId}.edi`, bytes);

  // Confirm receipt
  await fetch(`${base}/v2/parcels/confirm`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
  console.log(`Parcel ${parcel.parcelId} saved and confirmed.`);
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — inbox check and download loop
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})
base = "https://rest.ecgrid.io"

inbox = session.post(f"{base}/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25}).json()

for parcel in inbox.get("data", []):
    parcel_id = parcel["parcelId"]

    # Download
    data = session.post(f"{base}/v2/parcels/download",
        json={"parcelID": parcel_id}).content
    with open(f"parcel-{parcel_id}.edi", "wb") as f:
        f.write(data)

    # Confirm receipt
    session.post(f"{base}/v2/parcels/confirm", json={"parcelID": parcel_id})
    print(f"Parcel {parcel_id} saved and confirmed.")
```

</TabItem>
</Tabs>

### Upload

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Upload an outbound EDI file
curl -s -X POST https://rest.ecgrid.io/v2/parcels/upload \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @outbound.edi | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// Upload an outbound EDI file
var fileBytes = await File.ReadAllBytesAsync("outbound.edi");
using var content = new ByteArrayContent(fileBytes);
content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

var uploadResult = await http.PostAsync("/v2/parcels/upload", content);
uploadResult.EnsureSuccessStatusCode();
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — upload an outbound EDI file
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

byte[] fileBytes = Files.readAllBytes(Path.of("outbound.edi"));

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
    .header("Content-Type", "application/octet-stream")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofByteArray(fileBytes))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // parse JSON for parcel ID
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — upload an outbound EDI file
import fs from 'node:fs/promises';

const apiKey = process.env.ECGRID_API_KEY;
const fileBytes = await fs.readFile('outbound.edi');

const response = await fetch('https://rest.ecgrid.io/v2/parcels/upload', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/octet-stream',
    'X-API-Key': apiKey
  },
  body: fileBytes
});

const result = await response.json();
console.log('Uploaded parcel ID:', result.data?.parcelId);
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — upload an outbound EDI file
import os, requests

api_key = os.environ["ECGRID_API_KEY"]

with open("outbound.edi", "rb") as f:
    file_bytes = f.read()

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/upload",
    data=file_bytes,
    headers={
        "Content-Type": "application/octet-stream",
        "X-API-Key": api_key
    }
)
resp.raise_for_status()
print("Uploaded parcel ID:", resp.json()["data"]["parcelId"])
```

</TabItem>
</Tabs>

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-Console
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
dotnet run
```

## See Also

- [REST API Overview](../rest-api/overview.md)
- [Parcels — Pending Inbox List](../rest-api/parcels/pending-inbox-list.md)
- [Parcels — Download](../rest-api/parcels/download-parcel.md)
- [Parcels — Confirm Download](../rest-api/parcels/confirm-download.md)
- [Parcels — Upload](../rest-api/parcels/upload-parcel.md)
- [Poll Inbound Files](../common-operations/poll-inbound-files.md)
