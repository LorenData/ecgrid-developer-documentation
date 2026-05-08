---
title: Add VAN
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids/tp-add-van REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Add VAN

Associates a VAN (Value Added Network) qualifier and ID with an existing ECGrid ID to enable cross-network EDI routing.

## Endpoint

```http
POST /v2/ids/tp-add-van
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridId` | integer | Yes | Must be a valid ECGrid ID | The ECGrid ID to associate the VAN entry with |
| `vanQualifier` | string | Yes | ISA qualifier code used by the VAN | VAN-side ISA qualifier |
| `vanId` | string | Yes | ISA ID used by the VAN | VAN-side ISA identifier |

```json
{
  "ecGridId": 123456,
  "vanQualifier": "01",
  "vanId": "VANPARTNER001"
}
```

## Response

Returns a success boolean confirming the VAN association was added.

```json
{
  "success": true,
  "data": true
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/ids/tp-add-van" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridId": 123456, "vanQualifier": "01", "vanId": "VANPARTNER001" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — add a VAN qualifier/ID mapping to an ECGrid ID for cross-network routing
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridId = 123456,
    vanQualifier = "01",
    vanId = "VANPARTNER001"
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/ids/tp-add-van", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
Console.WriteLine($"VAN association added: {result!.Data}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridId\": 123456, \"vanQualifier\": \"01\", \"vanId\": \"VANPARTNER001\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/tp-add-van"))
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
const url = 'https://rest.ecgrid.io/v2/ids/tp-add-van';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridId": 123456, "vanQualifier": "01", "vanId": "VANPARTNER001" }),
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
url = "https://rest.ecgrid.io/v2/ids/tp-add-van"

response = requests.post(
    url,
    json={ "ecGridId": 123456, "vanQualifier": "01", "vanId": "VANPARTNER001" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Create ID](create-id)
- [Create Partner (Interconnect)](../partners/create-partner)
