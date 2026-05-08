---
title: Get Interchange Manifest
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of interchanges get-manifest REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Interchange Manifest

Returns the manifest of EDI functional groups and transaction sets contained within an interchange.

## Endpoint

```http
GET /v2/interchanges/get-manifest/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | The unique ECGrid Interchange ID. |

## Response

Returns an array of `ManifestInfo` objects, each describing a functional group within the interchange — including the functional group ID, transaction set type, and transaction counts.

```json
{
  "success": true,
  "data": [
    {
      "functionalGroup": "PO",
      "transactionSetType": "850",
      "transactionSetCount": 3,
      "groupControlNumber": "100001"
    },
    {
      "functionalGroup": "IN",
      "transactionSetType": "810",
      "transactionSetCount": 1,
      "groupControlNumber": "100002"
    }
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/interchanges/get-manifest/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve the functional group manifest for an interchange
using var client = httpClientFactory.CreateClient("ECGrid");

var response = await client.GetAsync($"/v2/interchanges/get-manifest/{interchangeId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ManifestInfo>>>();
foreach (var group in result.Data)
{
    Console.WriteLine($"Group: {group.FunctionalGroup} | Type: {group.TransactionSetType} | Count: {group.TransactionSetCount}");
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
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/interchanges/get-manifest/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/interchanges/get-manifest/${id}`;

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
url = f"https://rest.ecgrid.io/v2/interchanges/get-manifest/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Interchange](./get-interchange)
- [Get Parcel Manifest](../parcels/get-manifest)
- [Inbox List](./inbox-list)
