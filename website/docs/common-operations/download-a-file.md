---
title: Download a File
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create download-a-file common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Download a File

Retrieve the raw bytes of an inbound EDI parcel from your ECGrid mailbox and save them to disk (or pass them directly to your EDI parser).

## Overview

After [polling the inbox](./poll-inbound-files) and getting a list of `InBoxReady` parcels, call the download endpoint for each `parcelId`. ECGrid returns the file content as a Base64-encoded payload (REST) or a byte array (SOAP). Decode it, write it to your destination, then immediately [confirm the download](./confirm-download) so ECGrid marks the parcel as delivered.

Sequence:
1. Poll inbox — obtain a list of parcel IDs *(see [Poll for Inbound Files](./poll-inbound-files))*.
2. Download each parcel by ID — receive file bytes.
3. Save the bytes to disk or hand them to your EDI processor.
4. Confirm the download *(see [Confirm a Download](./confirm-download))*.

:::warning Always Confirm After Saving
If you download a parcel but do not confirm it, ECGrid will re-deliver the same file on the next poll. See [Confirm a Download](./confirm-download).
:::

---

## REST

**Endpoint:** `POST /v2/parcels/download`

**Auth:** `X-API-Key: <key>` header

### Step 1 — Request the parcel content

```http
POST https://rest.ecgrid.io/v2/parcels/download
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "parcelId": 98765
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `parcelId` | integer (long) | Yes | The parcel ID from the inbox list response. |

### Step 2 — Handle the response

```json
{
  "success": true,
  "data": {
    "parcelId": 98765,
    "fileName": "850_order.edi",
    "content": "SVNBKDE...",
    "contentEncoding": "Base64",
    "size": 4096
  }
}
```

Decode `content` from Base64 to obtain the raw EDI bytes, then write them to your destination path.

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -s -X POST https://rest.ecgrid.io/v2/parcels/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"parcelId":98765}' \
  | jq -r '.data.content' | base64 -d > parcel-98765.edi
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — download a parcel and save to disk using IHttpClientFactory
// "ECGrid" named client is registered with base address and X-API-Key header

using System.Net.Http.Json;

public record DownloadRequest(long ParcelId);

public record ParcelContent(
    long ParcelId,
    string FileName,
    string Content,          // Base64-encoded file bytes
    string ContentEncoding,
    long Size);

public record DownloadResponse(bool Success, ParcelContent Data);

public class ECGridParcelDownloader
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridParcelDownloader> _logger;

    public ECGridParcelDownloader(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridParcelDownloader> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Downloads a parcel by ID and writes its content to the specified output path.
    /// Returns the local file path on success. Throws on API or I/O error.
    /// </summary>
    public async Task<string> DownloadToFileAsync(
        long parcelId,
        string outputDirectory,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        var response = await http.PostAsJsonAsync(
            "/v2/parcels/download",
            new DownloadRequest(parcelId),
            cancellationToken);

        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<DownloadResponse>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from download endpoint.");

        if (!result.Success)
            throw new InvalidOperationException($"Download failed for parcelId={parcelId}.");

        // Decode Base64 content to raw bytes
        byte[] fileBytes = Convert.FromBase64String(result.Data.Content);

        // Build a safe output path — use the server-supplied filename
        string safeFileName = Path.GetFileName(result.Data.FileName); // strip any path components
        string outputPath   = Path.Combine(outputDirectory, safeFileName);

        await File.WriteAllBytesAsync(outputPath, fileBytes, cancellationToken);

        _logger.LogInformation(
            "Saved parcel {ParcelId} → {Path} ({Bytes} bytes)",
            parcelId, outputPath, fileBytes.Length);

        return outputPath;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — download a parcel and decode Base64 content
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
long parcelId = 98765L;

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/download"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"parcelId\":" + parcelId + "}"))
    .build();

var response = http.send(request, HttpResponse.BodyHandlers.ofString());
JsonNode root = new ObjectMapper().readTree(response.body());
String base64 = root.path("data").path("content").asText();
String fileName = root.path("data").path("fileName").asText("parcel.edi");

byte[] bytes = Base64.getDecoder().decode(base64);
Files.write(Path.of(fileName), bytes);
System.out.println("Saved " + fileName + " (" + bytes.length + " bytes)");
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — download a parcel and save to disk
import { writeFile } from 'fs/promises';

const apiKey = process.env.ECGRID_API_KEY;
const parcelId = 98765;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ parcelId })
});

const { data } = await response.json();
const bytes = Buffer.from(data.content, 'base64');
await writeFile(data.fileName, bytes);
console.log(`Saved ${data.fileName} (${bytes.length} bytes)`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, base64, requests
from pathlib import Path

api_key = os.environ["ECGRID_API_KEY"]
parcel_id = 98765

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/download",
    headers={"X-API-Key": api_key},
    json={"parcelId": parcel_id}
)
resp.raise_for_status()

data = resp.json()["data"]
file_bytes = base64.b64decode(data["content"])
out_path = Path(data["fileName"])
out_path.write_bytes(file_bytes)
print(f"Saved {out_path} ({len(file_bytes)} bytes)")
```

</TabItem>
</Tabs>

**Usage in your polling loop:**

```csharp
foreach (var parcel in readyParcels)
{
    var savedPath = await downloader.DownloadToFileAsync(
        parcel.ParcelId,
        outputDirectory: "/data/edi/inbound",
        cancellationToken);

    // Process EDI content here, then confirm
    await confirmer.ConfirmAsync(parcel.ParcelId, cancellationToken);
}
```

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Method:** `ParcelDownload(SessionID, ParcelID)` → `byte[]`

### Step 1 — Call ParcelDownload

```csharp
var result = await client.ParcelDownloadAsync(sessionId, parcelId);
byte[] fileBytes = result.ParcelDownloadResult;
```

The method returns the raw file bytes directly — no Base64 decoding required.

### Step 2 — Save to disk

```csharp
await File.WriteAllBytesAsync(outputPath, fileBytes);
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Reference: https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

using ECGridOS;

public static async Task DownloadParcelAsync(
    ECGridOSAPIClient client,
    string sessionId,
    int parcelId,
    string outputDirectory)
{
    // Fetch parcel metadata first to get the filename
    var infoResult = await client.ParcelInfoAsync(sessionId, parcelId);
    var info = infoResult.ParcelInfoResult;
    string safeFileName = Path.GetFileName(info.FileName);

    // Download the raw bytes
    var download = await client.ParcelDownloadAsync(sessionId, parcelId);
    byte[] fileBytes = download.ParcelDownloadResult;

    string outputPath = Path.Combine(outputDirectory, safeFileName);
    await File.WriteAllBytesAsync(outputPath, fileBytes);

    Console.WriteLine($"Saved: {outputPath}  ({fileBytes.Length} bytes)");

    // Confirm immediately after saving — see confirm-download.md
    await client.ParcelDownloadConfirmAsync(sessionId, parcelId);
    Console.WriteLine($"Confirmed parcelId={parcelId}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP ParcelDownload via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
String parcelId  = "98765";

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:ParcelDownload>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:ParcelID>" + parcelId + "</ecg:ParcelID>"
    + "</ecg:ParcelDownload></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/ParcelDownload\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Extract Base64 ParcelDownloadResult from XML, then decode
// var bytes = Base64.getDecoder().decode(extractedBase64);
// Files.write(Path.of("parcel-" + parcelId + ".edi"), bytes);
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP ParcelDownload via raw HTTP
import { writeFile } from 'fs/promises';

const sessionId = 'YOUR_SESSION_ID';
const parcelId  = '98765';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelDownload>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:ParcelID>${parcelId}</ecg:ParcelID>
  </ecg:ParcelDownload></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelDownload"'
  },
  body: envelope
});
const xml = await response.text();
// Parse ParcelDownloadResult from XML, decode Base64, write to file
console.log(xml);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import requests
from pathlib import Path
import base64

session_id = "YOUR_SESSION_ID"  # obtain from Login
parcel_id  = "98765"

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelDownload>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:ParcelID>' + parcel_id + '</ecg:ParcelID>'
    '</ecg:ParcelDownload></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelDownload"'}
)
resp.raise_for_status()
# Parse ParcelDownloadResult from resp.text, decode Base64, write to file
print(resp.text)
```

</TabItem>
</Tabs>

---

## Related

- [Poll for Inbound Files](./poll-inbound-files)
- [Confirm a Download](./confirm-download)
- [REST — Parcels: Download](../rest-api/parcels/download-parcel)
- [SOAP — ParcelDownload](../soap-api/parcels/parcel-download)
