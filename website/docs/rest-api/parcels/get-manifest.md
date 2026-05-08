---
title: Get Manifest
sidebar_position: 10
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/get-manifest.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Manifest

Return the list of EDI interchanges contained within a parcel.

## Endpoint

```http
GET /v2/parcels/manifest/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | Unique identifier of the parcel |

## Response

Returns an array of `ManifestInfo` objects, one for each EDI interchange found in the parcel.

```json
{
  "success": true,
  "data": [
    {
      "interchangeId": 555001,
      "sender": "112233",
      "receiver": "445566",
      "documentType": "810",
      "count": 3
    },
    {
      "interchangeId": 555002,
      "sender": "112233",
      "receiver": "445566",
      "documentType": "850",
      "count": 7
    }
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/parcels/manifest/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — inspect the interchange contents of a parcel before downloading
using System.Net.Http.Json;

var parcelId = 987654321L;

var response = await http.GetAsync(
    $"https://rest.ecgrid.io/v2/parcels/manifest/{parcelId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ManifestInfo>>>();

foreach (var interchange in result!.Data)
{
    Console.WriteLine(
        $"Interchange {interchange.InterchangeId}: " +
        $"{interchange.DocumentType} — {interchange.Count} document(s) " +
        $"from {interchange.Sender} to {interchange.Receiver}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/parcels/manifest/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/parcels/manifest/${id}`;

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
url = f"https://rest.ecgrid.io/v2/parcels/manifest/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Parcel](./get-parcel) — retrieve the parcel header metadata
- [Download Parcel](./download-parcel) — download the full parcel content
- [Interchanges — Get Interchange](../interchanges/get-interchange) — retrieve individual interchange details
