---
title: Find ID
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids/find REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Find ID

Searches for ECGrid IDs by ISA qualifier and ISA ID value.

## Endpoint

```http
POST /v2/ids/find
```

:::tip
Use this endpoint to look up a trading partner's ECGrid ID before creating an interconnect. The qualifier and ID correspond directly to the ISA-05/ISA-06 (sender) or ISA-07/ISA-08 (receiver) fields in an X12 interchange envelope.
:::

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `qualifier` | string | Yes | Valid ISA qualifier (e.g. `"01"`, `"ZZ"`) | EDI ISA qualifier to search |
| `id` | string | Yes | ISA ID value | EDI ISA identifier to search |

```json
{
  "qualifier": "01",
  "id": "PARTNER001"
}
```

## Response

Returns an array of matching `ECGridIDInfo` objects. Multiple results may be returned if the same qualifier/ID combination is registered in different networks.

```json
{
  "success": true,
  "data": [
    {
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
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/ids/find" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "qualifier": "01", "id": "PARTNER001" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — find a trading partner's ECGrid ID by qualifier and ISA ID
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    qualifier = "01",
    id = "PARTNER001"
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/ids/find", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ECGridIDInfo>>>();
foreach (var ecgridId in result!.Data)
{
    Console.WriteLine($"Found ECGrid ID {ecgridId.EcGridId}: {ecgridId.Description}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"qualifier\": \"01\", \"id\": \"PARTNER001\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/find"))
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
const url = 'https://rest.ecgrid.io/v2/ids/find';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "qualifier": "01", "id": "PARTNER001" }),
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
url = "https://rest.ecgrid.io/v2/ids/find"

response = requests.post(
    url,
    json={ "qualifier": "01", "id": "PARTNER001" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [List IDs](list-ids)
- [Create Partner (Interconnect)](../partners/create-partner)
