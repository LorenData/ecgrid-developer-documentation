---
title: Get ID
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create GET /v2/ids/{id} REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get ID

Retrieves a single ECGrid ID (Trading Partner ID) by its numeric identifier.

## Endpoint

```http
GET /v2/ids/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The numeric ECGrid ID to retrieve |

## Response

Returns an `ECGridIDInfo` object for the requested ECGrid ID.

```json
{
  "success": true,
  "data": {
    "ecGridId": 123456,
    "mailboxId": 1001,
    "networkId": 42,
    "qualifier": "01",
    "id": "PARTNER001",
    "description": "Acme Corp Production",
    "status": "Active",
    "routingGroup": "ProductionA",
    "ediStandard": "X12"
  }
}
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | ID is in development/testing phase |
| `Active` | ID is live and routing EDI traffic |
| `Preproduction` | ID is staged but not yet live |
| `Suspended` | ID is temporarily disabled |
| `Terminated` | ID has been permanently deactivated |

See [Enums reference](../../appendix/enums) for full details on `RoutingGroup` and `EDIStandard`.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/ids/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve an ECGrid ID record by its numeric ID
using var client = httpClientFactory.CreateClient("ECGrid");

var response = await client.GetAsync($"https://rest.ecgrid.io/v2/ids/{ecGridId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ECGridIDInfo>>();
Console.WriteLine($"Qualifier: {result!.Data.Qualifier}, ID: {result.Data.Id}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/ids/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/ids/${id}`;

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
url = f"https://rest.ecgrid.io/v2/ids/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List IDs](list-ids)
- [Find ID](find-id)
- [Create ID](create-id)
