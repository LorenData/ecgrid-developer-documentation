---
title: Count Partners
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/partners/count REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Count Partners

Returns the total count of interconnects associated with an ECGrid ID, optionally filtered by status.

## Endpoint

```http
POST /v2/partners/count
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridId` | integer | Yes | Must be a valid ECGrid ID | The ECGrid ID to count interconnects for |
| `status` | string | No | See `Status` enum | Filter by interconnect lifecycle status |

```json
{
  "ecGridId": 123456,
  "status": "Active"
}
```

## Response

Returns the total count as an integer.

```json
{
  "success": true,
  "data": 14
}
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | Interconnects in development/testing phase |
| `Active` | Live interconnects with active routing |
| `Preproduction` | Staged but not yet live |
| `Suspended` | Temporarily disabled |
| `Terminated` | Permanently ended |

See [Enums reference](../../appendix/enums) for complete enum definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/partners/count" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridId": 123456, "status": "Active" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — count the active interconnects for a given ECGrid ID
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridId = 123456,
    status = "Active"
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/partners/count", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<int>>();
Console.WriteLine($"Active interconnects: {result!.Data}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridId\": 123456, \"status\": \"Active\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners/count"))
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
const url = 'https://rest.ecgrid.io/v2/partners/count';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridId": 123456, "status": "Active" }),
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
url = "https://rest.ecgrid.io/v2/partners/count"

response = requests.post(
    url,
    json={ "ecGridId": 123456, "status": "Active" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Partners](list-partners)
- [Get Partner](get-partner)
