---
title: Send EDI to a Trading Partner
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create send-edi-to-trading-partner common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Send EDI to a Trading Partner

Look up a trading partner's ECGrid ID by their ISA qualifier and ID, then deliver an EDI document directly to their mailbox.

## Overview

Sending EDI to a specific trading partner is a two-step process: first locate the partner's `ECGridID` in the ECGrid network, then upload the EDI file with that ID as the `toECGridId`. The lookup step is optional if your EDI file already contains the correct ISA08 qualifier/ID pair and the partner is registered — ECGrid can route automatically from the interchange header.

Sequence:
1. *(Optional)* Find the trading partner's ECGrid ID using their ISA qualifier and ID.
2. Build or load your outbound EDI file.
3. Upload the file with `toECGridId` set.
4. Store the returned `parcelId` for tracking.

---

## REST

### Step 1 — Find the trading partner's ECGrid ID

If you know the partner's ISA qualifier (e.g. `"01"`) and ISA ID (e.g. `"PARTNERCO"`), use the ID find endpoint to look them up:

```http
GET https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO
X-API-Key: YOUR_API_KEY
```

```json
{
  "success": true,
  "data": [
    {
      "ecGridId": 789012,
      "qualifier": "01",
      "id": "PARTNERCO       ",
      "description": "Partner Company LLC",
      "networkId": 55,
      "mailboxId": 301
    }
  ]
}
```

Take the `ecGridId` value — `789012` in this example — and use it as `toECGridId` in the upload call.

:::tip When to Skip the Lookup
If your EDI file already has the correct ISA06/ISA08 segments and you have an active interconnect with the partner, you can omit `toECGridId` in the upload body and let ECGrid route from the interchange header. The explicit lookup is recommended when you need to validate the partner is reachable before uploading.
:::

### Step 2 — Upload the EDI file to that partner

```http
POST https://rest.ecgrid.io/v2/parcels/upload
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "fileName": "856_asn_20260507.edi",
  "content": "SVNBKDE...",
  "fromECGridId": 123456,
  "toECGridId": 789012
}
```

```json
{
  "success": true,
  "data": {
    "parcelId": 334455,
    "status": "OutBoxQueued"
  }
}
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — find the trading partner's ECGrid ID
curl -s "https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO" \
  -H "X-API-Key: $ECGRID_API_KEY" | jq '.data[0].ecGridId'

# Step 2 — upload the EDI file (replace TO_ECGRID_ID with value from step 1)
B64=$(base64 -w 0 /path/to/856_asn.edi)
curl -s -X POST https://rest.ecgrid.io/v2/parcels/upload \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"fileName\":\"856_asn.edi\",\"content\":\"$B64\",\"fromECGridId\":123456,\"toECGridId\":$TO_ECGRID_ID}" | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — find a trading partner by ISA qualifier/ID then upload an EDI file
// "ECGrid" named client is registered with base address and X-API-Key header

using System.Net.Http.Json;

// --- DTOs ---

public record ECGridIdRecord(
    int ECGridId,
    string Qualifier,
    string Id,
    string Description,
    int NetworkId,
    int MailboxId);

public record FindIdResponse(bool Success, List<ECGridIdRecord> Data);

public record UploadRequest(
    string FileName,
    string Content,       // Base64-encoded bytes
    int FromECGridId,
    int ToECGridId);

public record UploadData(long ParcelId, string FileName, string Status, long Size);
public record UploadResponse(bool Success, UploadData Data);

// --- Service ---

public class ECGridEdiSender
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridEdiSender> _logger;

    public ECGridEdiSender(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridEdiSender> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Looks up a trading partner by ISA qualifier and ID, then sends them an EDI file.
    /// Returns the assigned parcelId. Throws if the partner cannot be found.
    /// </summary>
    public async Task<long> SendToPartnerAsync(
        string isaQualifier,
        string isaId,
        string filePath,
        int fromECGridId,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        // Step 1 — resolve partner's ECGrid ID
        int toECGridId = await FindPartnerECGridIdAsync(
            http, isaQualifier, isaId, cancellationToken);

        _logger.LogInformation(
            "Resolved {Qualifier}/{Id} → ECGridId={ToId}", isaQualifier, isaId, toECGridId);

        // Step 2 — read and encode the file
        byte[] fileBytes      = await File.ReadAllBytesAsync(filePath, cancellationToken);
        string base64Content  = Convert.ToBase64String(fileBytes);
        string fileName       = Path.GetFileName(filePath);

        // Step 3 — upload
        var uploadRequest = new UploadRequest(fileName, base64Content, fromECGridId, toECGridId);
        var uploadResponse = await http.PostAsJsonAsync(
            "/v2/parcels/upload", uploadRequest, cancellationToken);

        uploadResponse.EnsureSuccessStatusCode();

        var uploadResult = await uploadResponse.Content
            .ReadFromJsonAsync<UploadResponse>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from upload endpoint.");

        if (!uploadResult.Success)
            throw new InvalidOperationException($"Upload failed for '{fileName}'.");

        _logger.LogInformation(
            "Sent '{FileName}' to ECGridId={ToId} → parcelId={ParcelId}",
            fileName, toECGridId, uploadResult.Data.ParcelId);

        return uploadResult.Data.ParcelId;
    }

    /// <summary>
    /// Finds the ECGrid ID for a trading partner by ISA qualifier and ID.
    /// Throws <see cref="KeyNotFoundException"/> if the partner is not registered.
    /// </summary>
    private static async Task<int> FindPartnerECGridIdAsync(
        HttpClient http,
        string qualifier,
        string id,
        CancellationToken cancellationToken)
    {
        var response = await http.GetFromJsonAsync<FindIdResponse>(
            $"/v2/ids/find?qualifier={Uri.EscapeDataString(qualifier)}&id={Uri.EscapeDataString(id)}",
            cancellationToken);

        if (response is null || response.Data.Count == 0)
            throw new KeyNotFoundException(
                $"No ECGrid ID found for qualifier='{qualifier}' id='{id}'.");

        // If multiple results are returned, prefer the first active match
        return response.Data[0].ECGridId;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — find trading partner by ISA ID, then upload EDI file
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;
import com.fasterxml.jackson.databind.*;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — find partner's ECGrid ID
var findReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO"))
    .header("X-API-Key", key)
    .GET().build();
var findResp = http.send(findReq, HttpResponse.BodyHandlers.ofString());
JsonNode idNode = mapper.readTree(findResp.body()).path("data").get(0);
int toId = idNode.path("ecGridId").asInt();

// Step 2 — encode and upload
byte[] bytes  = Files.readAllBytes(Path.of("/data/edi/outbound/856_asn.edi"));
String base64 = Base64.getEncoder().encodeToString(bytes);
String body   = String.format(
    "{\"fileName\":\"856_asn.edi\",\"content\":\"%s\",\"fromECGridId\":123456,\"toECGridId\":%d}",
    base64, toId);

var upReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(body)).build();

var upResp = http.send(upReq, HttpResponse.BodyHandlers.ofString());
System.out.println(upResp.body()); // parcelId
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — find trading partner then upload EDI file
import { readFile } from 'fs/promises';
import { basename } from 'path';

const apiKey   = process.env.ECGRID_API_KEY;
const headers  = { 'X-API-Key': apiKey };
const filePath = '/data/edi/outbound/856_asn.edi';

// Step 1 — find partner ECGrid ID
const findResp = await fetch(
  'https://rest.ecgrid.io/v2/ids/find?qualifier=01&id=PARTNERCO',
  { headers });
const { data: [partner] } = await findResp.json();
const toECGridId = partner.ecGridId;

// Step 2 — upload
const bytes   = await readFile(filePath);
const content = bytes.toString('base64');
const response = await fetch('https://rest.ecgrid.io/v2/parcels/upload', {
  method: 'POST',
  headers: { ...headers, 'Content-Type': 'application/json' },
  body: JSON.stringify({ fileName: basename(filePath), content, fromECGridId: 123456, toECGridId })
});
const { data } = await response.json();
console.log(`Sent as parcelId=${data.parcelId}`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, base64, requests
from pathlib import Path

api_key  = os.environ["ECGRID_API_KEY"]
session  = requests.Session()
session.headers.update({"X-API-Key": api_key})
file_path = Path("/data/edi/outbound/856_asn.edi")

# Step 1 — find trading partner ECGrid ID
find = session.get("https://rest.ecgrid.io/v2/ids/find",
                   params={"qualifier": "01", "id": "PARTNERCO"})
find.raise_for_status()
to_ecgrid_id = find.json()["data"][0]["ecGridId"]

# Step 2 — encode and upload
content = base64.b64encode(file_path.read_bytes()).decode()
resp = session.post(
    "https://rest.ecgrid.io/v2/parcels/upload",
    json={"fileName": file_path.name, "content": content,
          "fromECGridId": 123456, "toECGridId": to_ecgrid_id}
)
resp.raise_for_status()
print(f"Sent as parcelId={resp.json()['data']['parcelId']}")
```

</TabItem>
</Tabs>

**Usage:**

```csharp
long parcelId = await sender.SendToPartnerAsync(
    isaQualifier: "01",
    isaId:        "PARTNERCO",
    filePath:     "/data/edi/outbound/856_asn_20260507.edi",
    fromECGridId: 123456,
    cancellationToken: ct);

Console.WriteLine($"Delivered as parcelId={parcelId}");
```

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

### Step 1 — Find the partner's ECGrid ID with TPSearch

```csharp
var searchResult = await client.TPSearchAsync(
    sessionId,
    qualifier: "01",
    id:        "PARTNERCO");

var partners = searchResult.TPSearchResult;
if (partners is null || partners.Length == 0)
    throw new KeyNotFoundException("Trading partner not found.");

int toECGridId = partners[0].ECGridID;
```

### Step 2 — Upload the EDI file with ParcelUpload

```csharp
byte[] fileBytes = await File.ReadAllBytesAsync(filePath);
string fileName  = Path.GetFileName(filePath);

var upload = await client.ParcelUploadAsync(
    sessionId,
    fileName,
    fileBytes,
    content: "application/edi-x12");

long parcelId = upload.ParcelUploadResult;
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Reference: https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

using ECGridOS;

public static async Task<long> SendEdiToPartnerAsync(
    ECGridOSAPIClient client,
    string sessionId,
    string isaQualifier,
    string isaId,
    string filePath)
{
    // Step 1 — look up the trading partner
    var searchResult = await client.TPSearchAsync(sessionId, isaQualifier, isaId);
    var partners = searchResult.TPSearchResult;

    if (partners is null || partners.Length == 0)
        throw new KeyNotFoundException(
            $"No ECGrid partner found for qualifier='{isaQualifier}' id='{isaId}'.");

    int toECGridId = partners[0].ECGridID;
    Console.WriteLine($"Found partner ECGridId={toECGridId}: {partners[0].Description}");

    // Step 2 — read file and upload
    byte[] fileBytes = await File.ReadAllBytesAsync(filePath);
    string fileName  = Path.GetFileName(filePath);

    var upload = await client.ParcelUploadAsync(
        sessionId,
        fileName,
        fileBytes,
        content: "application/edi-x12");

    long parcelId = upload.ParcelUploadResult;
    Console.WriteLine($"Uploaded '{fileName}' → parcelId={parcelId}");
    return parcelId;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP TPSearch + ParcelUpload via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

// Step 1 — TPSearch for the partner's ECGrid ID (parse result from XML)
String searchEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:TPSearch>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>"
    + "</ecg:TPSearch></soap:Body></soap:Envelope>";

var searchReq = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/TPSearch\"")
    .POST(BodyPublishers.ofString(searchEnv)).build();
var searchResp = http.send(searchReq, HttpResponse.BodyHandlers.ofString());
// Extract ECGridID from searchResp.body() XML, then call ParcelUpload
System.out.println(searchResp.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP TPSearch + ParcelUpload via raw HTTP
import { readFile } from 'fs/promises';
import { basename } from 'path';

const sessionId = 'YOUR_SESSION_ID';

// Step 1 — find partner ECGrid ID via TPSearch
const searchEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:TPSearch>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:Qualifier>01</ecg:Qualifier>
    <ecg:ID>PARTNERCO</ecg:ID>
  </ecg:TPSearch></soap:Body>
</soap:Envelope>`;

const searchResp = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/TPSearch"' },
  body: searchEnv
});
// Parse ECGridID from XML, then call ParcelUpload
console.log(await searchResp.text());
```

</TabItem>
<TabItem value="python" label="Python">

```python
import base64, requests
from pathlib import Path

session_id = "YOUR_SESSION_ID"  # obtain from Login
file_path  = Path("/data/edi/outbound/856_asn.edi")

# Step 1 — find partner ECGrid ID via TPSearch
search_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:TPSearch>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>'
    '</ecg:TPSearch></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=search_env.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/TPSearch"'}
)
resp.raise_for_status()
# Parse ECGridID from resp.text, then call ParcelUpload
print(resp.text)
```

</TabItem>
</Tabs>

---

## Prerequisites

Before you can deliver EDI to a trading partner through ECGrid, the following must be in place:

1. **Trading partner is registered** — they have an ECGrid ID. Use the lookup endpoint to verify.
2. **Interconnect exists** — your mailbox must have an active interconnect (partner relationship) with the recipient's mailbox. See [Set Up an Interconnect](./setup-interconnect).
3. **Comm configuration** — both parties must have compatible communications settings. ECGrid handles routing once the interconnect is active.

---

## Related

- [Upload a File](./upload-a-file)
- [Set Up an Interconnect](./setup-interconnect)
- [Onboard a Trading Partner](./onboard-trading-partner)
- [REST — IDs: Find ID](../rest-api/ids/find-id)
- [REST — Parcels: Upload](../rest-api/parcels/upload-parcel)
- [SOAP — TPSearch](../soap-api/ids/tp-search)
- [SOAP — ParcelUpload](../soap-api/parcels/parcel-upload)
