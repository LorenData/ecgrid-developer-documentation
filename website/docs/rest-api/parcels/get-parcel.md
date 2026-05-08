---
title: Get Parcel
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/get-parcel.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Parcel

Retrieve the metadata and status for a single parcel by its unique ID.

## Endpoint

```http
GET /v2/parcels/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | Unique identifier of the parcel |

## Response

Returns a `ParcelIDInfo` object describing the parcel's metadata and current status.

```json
{
  "success": true,
  "data": {
    "parcelId": 987654321,
    "mailboxId": 1001,
    "networkId": 42,
    "fileName": "invoice_batch_20260507.edi",
    "bytes": 14872,
    "status": "InBoxReady",
    "ecGridIdFrom": 112233,
    "ecGridIdTo": 445566,
    "created": "2026-05-07T08:00:00Z",
    "modified": "2026-05-07T08:05:00Z"
  }
}
```

## ENUMs

### ParcelStatus

See [ParcelStatus in Appendix — ENUMs](../../appendix/enums) for the full list of parcel status values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/parcels/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve parcel metadata by ID
using System.Net.Http.Json;

var parcelId = 987654321L;

var response = await http.GetAsync($"https://rest.ecgrid.io/v2/parcels/{parcelId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ParcelIdInfo>>();
Console.WriteLine($"Parcel {result!.Data.ParcelId} — Status: {result.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/parcels/%s", id)))
    .header("X-API-Key", apiKey)
    .GET()
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
const url = `https://rest.ecgrid.io/v2/parcels/${id}`;

const response = await fetch(url, {
  method: 'GET',
  headers: { 'X-API-Key': apiKey },
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
id = 0  # replace with actual id
url = f"https://rest.ecgrid.io/v2/parcels/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Download Parcel](./download-parcel) — download the EDI content of this parcel
- [Get Manifest](./get-manifest) — list interchanges contained in this parcel
- [Inbox List](./inbox-list) — search inbound parcels
