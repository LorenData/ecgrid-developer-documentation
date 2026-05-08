---
title: Create Partner
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/partners REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Partner

Creates a new interconnect (partner relationship) that permits EDI routing between two ECGrid IDs.

## Endpoint

```http
POST /v2/partners
```

:::note
Both ECGrid IDs must already exist before creating an interconnect. Use [Find ID](../ids/find-id) to look up a trading partner's ECGrid ID by their ISA qualifier and ISA ID. The interconnect defines a bidirectional routing permission — once created, EDI can flow in either direction between the two IDs.
:::

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridIdFrom` | integer | Yes | Must be a valid ECGrid ID | The originating trading partner ECGrid ID |
| `ecGridIdTo` | integer | Yes | Must be a valid ECGrid ID | The destination trading partner ECGrid ID |

```json
{
  "ecGridIdFrom": 123456,
  "ecGridIdTo": 654321
}
```

## Response

Returns the newly created `InterconnectIDInfo` object.

```json
{
  "success": true,
  "data": {
    "interconnectId": 9001,
    "ecGridIdFrom": 123456,
    "ecGridIdTo": 654321,
    "status": "Active",
    "created": "2024-06-01T10:00:00Z",
    "modified": "2024-06-01T10:00:00Z"
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/partners" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridIdFrom": 123456, "ecGridIdTo": 654321 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — create an interconnect to authorize EDI routing between two trading partners
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridIdFrom = 123456,
    ecGridIdTo = 654321
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/partners", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<InterconnectIDInfo>>();
Console.WriteLine($"Created interconnect ID: {result!.Data.InterconnectId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridIdFrom\": 123456, \"ecGridIdTo\": 654321 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners"))
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
const url = 'https://rest.ecgrid.io/v2/partners';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridIdFrom": 123456, "ecGridIdTo": 654321 }),
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
url = "https://rest.ecgrid.io/v2/partners"

response = requests.post(
    url,
    json={ "ecGridIdFrom": 123456, "ecGridIdTo": 654321 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Find ID](../ids/find-id)
- [Get Partner](get-partner)
- [Delete Partner](delete-partner)
- [Onboard Trading Partner](../../common-operations/onboard-trading-partner)
