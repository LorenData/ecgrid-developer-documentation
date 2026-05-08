---
title: Upload a File
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create upload-a-file common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Upload a File

Send an EDI file from your application into ECGrid for routing and delivery to a trading partner.

## Overview

Uploading places an outbound EDI file into the ECGrid network. ECGrid examines the EDI interchange headers (ISA/GS segments) to determine the sender and recipient, routes the file to the appropriate trading partner's mailbox, and returns a `parcelId` you can use to track delivery status.

You may also explicitly provide `fromECGridId` and `toECGridId` in the request body to override header-based routing — useful when the ISA IDs are not unique within your network or when you are sending test files.

Sequence:
1. Read the EDI file from disk (or build it in memory).
2. Base64-encode the bytes.
3. POST to the upload endpoint with filename, encoded content, and optional routing IDs.
4. Store the returned `parcelId` for status tracking.

---

## REST

**Endpoint:** `POST /v2/parcels/upload`

**Auth:** `X-API-Key: <key>` header

### Step 1 — Prepare the request body

```http
POST https://rest.ecgrid.io/v2/parcels/upload
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "fileName": "850_order_20260507.edi",
  "content": "SVNBKDE...",
  "fromECGridId": 123456,
  "toECGridId": 789012
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `fileName` | string | Yes | Original filename including extension. Preserved in the parcel record. |
| `content` | string | Yes | Base64-encoded EDI file bytes. |
| `fromECGridId` | integer | No | Sender's ECGrid ID. If omitted, ECGrid derives from the ISA06 segment. |
| `toECGridId` | integer | No | Recipient's ECGrid ID. If omitted, ECGrid derives from the ISA08 segment. |

### Step 2 — Inspect the response

```json
{
  "success": true,
  "data": {
    "parcelId": 112233,
    "fileName": "850_order_20260507.edi",
    "status": "OutBoxQueued",
    "size": 8192
  }
}
```

Store `parcelId`. Use `GET /v2/parcels/{id}` to poll delivery status if needed.

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Encode the file to Base64 first, then upload
B64=$(base64 -w 0 /path/to/850_order.edi)

curl -s -X POST https://rest.ecgrid.io/v2/parcels/upload \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"fileName\":\"850_order.edi\",\"content\":\"$B64\",\"fromECGridId\":123456,\"toECGridId\":789012}" | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — read a file from disk and upload it using IHttpClientFactory
// "ECGrid" named client is registered with base address and X-API-Key header

using System.Net.Http.Json;

public record UploadRequest(
    string FileName,
    string Content,          // Base64-encoded bytes
    int FromECGridId,
    int ToECGridId);

public record UploadData(long ParcelId, string FileName, string Status, long Size);

public record UploadResponse(bool Success, UploadData Data);

public class ECGridParcelUploader
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridParcelUploader> _logger;

    public ECGridParcelUploader(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridParcelUploader> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Reads a file from disk, Base64-encodes it, and uploads it to ECGrid.
    /// Returns the assigned parcelId on success.
    /// </summary>
    public async Task<long> UploadFileAsync(
        string filePath,
        int fromECGridId,
        int toECGridId,
        CancellationToken cancellationToken = default)
    {
        if (!File.Exists(filePath))
            throw new FileNotFoundException("EDI file not found.", filePath);

        byte[] fileBytes = await File.ReadAllBytesAsync(filePath, cancellationToken);
        string base64Content = Convert.ToBase64String(fileBytes);
        string fileName = Path.GetFileName(filePath);

        var request = new UploadRequest(fileName, base64Content, fromECGridId, toECGridId);

        var http = _httpClientFactory.CreateClient("ECGrid");
        var response = await http.PostAsJsonAsync(
            "/v2/parcels/upload", request, cancellationToken);

        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<UploadResponse>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from upload endpoint.");

        if (!result.Success)
            throw new InvalidOperationException($"Upload failed for file '{fileName}'.");

        _logger.LogInformation(
            "Uploaded '{FileName}' → parcelId={ParcelId}  status={Status}",
            fileName, result.Data.ParcelId, result.Data.Status);

        return result.Data.ParcelId;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — read, Base64-encode, and upload an EDI file
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

Path filePath   = Path.of("/data/edi/outbound/850_order.edi");
byte[] bytes    = Files.readAllBytes(filePath);
String base64   = Base64.getEncoder().encodeToString(bytes);
String fileName = filePath.getFileName().toString();

String body = String.format(
    "{\"fileName\":\"%s\",\"content\":\"%s\",\"fromECGridId\":123456,\"toECGridId\":789012}",
    fileName, base64);

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = http.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // contains parcelId
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — read, Base64-encode, and upload an EDI file
import { readFile } from 'fs/promises';
import { basename } from 'path';

const apiKey   = process.env.ECGRID_API_KEY;
const filePath = '/data/edi/outbound/850_order.edi';

const bytes   = await readFile(filePath);
const content = bytes.toString('base64');
const fileName = basename(filePath);

const response = await fetch('https://rest.ecgrid.io/v2/parcels/upload', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ fileName, content, fromECGridId: 123456, toECGridId: 789012 })
});

const { data } = await response.json();
console.log(`Uploaded as parcelId=${data.parcelId}`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, base64, requests
from pathlib import Path

api_key   = os.environ["ECGRID_API_KEY"]
file_path = Path("/data/edi/outbound/850_order.edi")

file_bytes = file_path.read_bytes()
content    = base64.b64encode(file_bytes).decode()

resp = requests.post(
    "https://rest.ecgrid.io/v2/parcels/upload",
    headers={"X-API-Key": api_key},
    json={
        "fileName":     file_path.name,
        "content":      content,
        "fromECGridId": 123456,
        "toECGridId":   789012,
    }
)
resp.raise_for_status()
print(f"Uploaded as parcelId={resp.json()['data']['parcelId']}")
```

</TabItem>
</Tabs>

**Usage:**

```csharp
long parcelId = await uploader.UploadFileAsync(
    filePath:     "/data/edi/outbound/850_order_20260507.edi",
    fromECGridId: 123456,
    toECGridId:   789012,
    cancellationToken: ct);

Console.WriteLine($"Uploaded as parcelId={parcelId}");
```

:::tip Header-Based Routing
If your EDI files contain valid ISA/GS segments with the correct sender and receiver IDs that are already registered in ECGrid, you can omit `fromECGridId` and `toECGridId` and let ECGrid route automatically. Explicit IDs are recommended when the same ISA ID is used in multiple mailboxes or networks.
:::

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Method:** `ParcelUpload(SessionID, FileName, Bytes, Content)` → `long` (ParcelID)

| Parameter | Type | Description |
|---|---|---|
| `SessionID` | string | Active session token. |
| `FileName` | string | Original filename including extension. |
| `Bytes` | byte[] | Raw file bytes — not Base64 encoded; the SOAP stack handles encoding. |
| `Content` | string | MIME content type, e.g. `"application/edi-x12"`. |

### Step 1 — Call ParcelUpload

```csharp
byte[] fileBytes = await File.ReadAllBytesAsync(filePath);
string fileName  = Path.GetFileName(filePath);

var result = await client.ParcelUploadAsync(
    sessionId,
    fileName,
    fileBytes,
    content: "application/edi-x12");

long parcelId = result.ParcelUploadResult;
Console.WriteLine($"Uploaded parcelId={parcelId}");
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Reference: https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

using ECGridOS;

public static async Task<long> UploadEdiFileAsync(
    ECGridOSAPIClient client,
    string sessionId,
    string filePath)
{
    if (!File.Exists(filePath))
        throw new FileNotFoundException("EDI file not found.", filePath);

    byte[] fileBytes = await File.ReadAllBytesAsync(filePath);
    string fileName  = Path.GetFileName(filePath);

    // ParcelUpload handles Base64 encoding internally via the SOAP stack
    var result = await client.ParcelUploadAsync(
        sessionId,
        fileName,
        fileBytes,
        content: "application/edi-x12");

    long parcelId = result.ParcelUploadResult;
    Console.WriteLine($"Uploaded '{fileName}' → parcelId={parcelId}");
    return parcelId;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP ParcelUpload via raw HTTP (Base64 content in envelope)
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
Path filePath    = Path.of("/data/edi/outbound/850_order.edi");
byte[] bytes     = Files.readAllBytes(filePath);
String base64    = Base64.getEncoder().encodeToString(bytes);
String fileName  = filePath.getFileName().toString();

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:ParcelUpload>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:FileName>" + fileName + "</ecg:FileName>"
    + "<ecg:Bytes>" + base64 + "</ecg:Bytes>"
    + "<ecg:Content>application/edi-x12</ecg:Content>"
    + "</ecg:ParcelUpload></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/ParcelUpload\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // extract ParcelUploadResult (parcelId)
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP ParcelUpload via raw HTTP
import { readFile } from 'fs/promises';
import { basename } from 'path';

const sessionId = 'YOUR_SESSION_ID';
const filePath  = '/data/edi/outbound/850_order.edi';
const bytes     = await readFile(filePath);
const base64    = bytes.toString('base64');
const fileName  = basename(filePath);

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelUpload>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:FileName>${fileName}</ecg:FileName>
    <ecg:Bytes>${base64}</ecg:Bytes>
    <ecg:Content>application/edi-x12</ecg:Content>
  </ecg:ParcelUpload></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelUpload"'
  },
  body: envelope
});
console.log(await response.text()); // extract ParcelUploadResult (parcelId)
```

</TabItem>
<TabItem value="python" label="Python">

```python
import base64, requests
from pathlib import Path

session_id = "YOUR_SESSION_ID"  # obtain from Login
file_path  = Path("/data/edi/outbound/850_order.edi")
file_bytes = file_path.read_bytes()
b64        = base64.b64encode(file_bytes).decode()

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelUpload>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:FileName>' + file_path.name + '</ecg:FileName>'
    '<ecg:Bytes>' + b64 + '</ecg:Bytes>'
    '<ecg:Content>application/edi-x12</ecg:Content>'
    '</ecg:ParcelUpload></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelUpload"'}
)
resp.raise_for_status()
print(resp.text)  # extract ParcelUploadResult (parcelId)
```

</TabItem>
</Tabs>

---

## Routing Logic

ECGrid determines delivery routing in the following priority order:

1. **Explicit IDs** — if `fromECGridId` / `toECGridId` are provided (REST) or set on the comm configuration, they take precedence.
2. **ISA header** — ECGrid reads ISA06 (sender) and ISA08 (recipient) qualifier/ID pairs from the EDI interchange envelope.
3. **GS header** — used as a fallback or for sub-routing within an interchange.

If routing cannot be resolved, the parcel is placed in a suspense state and an error is returned.

---

## Related

- [Send EDI to a Trading Partner](./send-edi-to-trading-partner)
- [Poll for Inbound Files](./poll-inbound-files)
- [REST — Parcels: Upload](../rest-api/parcels/upload-parcel)
- [SOAP — ParcelUpload](../soap-api/parcels/parcel-upload)
