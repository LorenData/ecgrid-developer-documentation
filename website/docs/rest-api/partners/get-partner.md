---
title: Get Partner
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create GET /v2/partners/{id} REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Partner

Retrieves a single interconnect (partner relationship) record by its numeric ID.

## Endpoint

```http
GET /v2/partners/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The numeric Interconnect/Partner ID to retrieve |

## Response

Returns an `InterconnectIDInfo` object describing the partner relationship.

```json
{
  "success": true,
  "data": {
    "interconnectId": 9001,
    "ecGridIdFrom": 123456,
    "ecGridIdTo": 654321,
    "status": "Active",
    "created": "2024-01-15T08:30:00Z",
    "modified": "2024-03-22T14:00:00Z"
  }
}
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | Interconnect is in development/testing phase |
| `Active` | Interconnect is live; EDI routing is permitted |
| `Preproduction` | Interconnect is staged but not yet live |
| `Suspended` | Interconnect is temporarily disabled |
| `Terminated` | Interconnect has been permanently ended |

See [Enums reference](../../appendix/enums) for complete enum definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/partners/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve a partner interconnect record by its ID
using var client = httpClientFactory.CreateClient("ECGrid");

var response = await client.GetAsync(
    $"https://rest.ecgrid.io/v2/partners/{interconnectId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<InterconnectIDInfo>>();
Console.WriteLine($"Interconnect {result!.Data.InterconnectId}: " +
    $"{result.Data.EcGridIdFrom} ↔ {result.Data.EcGridIdTo} ({result.Data.Status})");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/partners/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/partners/${id}`;

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
url = f"https://rest.ecgrid.io/v2/partners/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Partners](list-partners)
- [Create Partner](create-partner)
- [Delete Partner](delete-partner)
