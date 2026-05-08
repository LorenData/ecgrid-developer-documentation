---
title: Download Parcel
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/download-parcel.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Download Parcel

Download the EDI content of an inbound parcel by its ID.

## Endpoint

```http
POST /v2/parcels/download
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `parcelId` | long | Yes | | Unique identifier of the parcel to download |

```json
{
  "parcelId": 987654321
}
```

## Response

Returns the parcel metadata along with the Base64-encoded file content.

:::tip Confirm After Download
Always call [Confirm Download](./confirm-download) (`POST /v2/parcels/confirm`) after successfully saving the file. Without confirmation, ECGrid treats the parcel as undelivered and will re-deliver it on the next polling cycle.
:::

```json
{
  "success": true,
  "data": {
    "parcelId": 987654321,
    "fileName": "invoice_batch_20260507.edi",
    "content": "SVFU4OiogU2VuZGluZyBFREkgZGF0YSB2aWEgRUNHcmlk...",
    "bytes": 14872
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/download" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "parcelId": 987654321 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — download a parcel and write the EDI file to disk
using System.Net.Http.Json;

var downloadRequest = new { parcelId = 987654321L };

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/download",
    downloadRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ParcelDownload>>();
var download = result!.Data;

// Decode and save the EDI content
var ediBytes = Convert.FromBase64String(download.Content);
await File.WriteAllBytesAsync(download.FileName, ediBytes);

// Confirm delivery so ECGrid marks the parcel as transferred
var confirmRequest = new { parcelId = download.ParcelId };
var confirmResponse = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/confirm",
    confirmRequest);
confirmResponse.EnsureSuccessStatusCode();

Console.WriteLine($"Downloaded and confirmed parcel {download.ParcelId} — {download.FileName}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"parcelId\": 987654321 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/download"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(body))
    .build();

HttpClient client = HttpClient.newHttpClient();
HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString());

System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const apiKey = process.env.ECGRID_API_KEY;
const url = 'https://rest.ecgrid.io/v2/parcels/download';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "parcelId": 987654321 }),
});

const data = await response.json();
console.log(data);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
headers = {"X-API-Key": api_key}
url = "https://rest.ecgrid.io/v2/parcels/download"

response = requests.post(
    url,
    json={ "parcelId": 987654321 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Confirm Download](./confirm-download) — must be called after every successful download
- [Inbox List](./inbox-list) — list available inbound parcels
- [Pending Inbox List](./pending-inbox-list) — efficiently check for new unread parcels
- [Get Parcel](./get-parcel) — retrieve parcel metadata without downloading content
