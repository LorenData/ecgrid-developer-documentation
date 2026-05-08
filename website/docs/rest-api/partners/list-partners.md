---
title: List Partners
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/partners/list REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Partners

Returns a paginated list of interconnects associated with an ECGrid ID, optionally filtered by status.

## Endpoint

```http
POST /v2/partners/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridId` | integer | Yes | Must be a valid ECGrid ID | The ECGrid ID to list interconnects for |
| `status` | string | No | See `Status` enum | Filter by interconnect lifecycle status |
| `pageNo` | integer | No | Starts at 1 | Page number for pagination |
| `recordsPerPage` | integer | No | — | Number of records per page |

```json
{
  "ecGridId": 123456,
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 25
}
```

## Response

Returns a paginated array of `InterconnectIDInfo` objects.

```json
{
  "success": true,
  "data": [
    {
      "interconnectId": 9001,
      "ecGridIdFrom": 123456,
      "ecGridIdTo": 654321,
      "status": "Active",
      "created": "2024-01-15T08:30:00Z",
      "modified": "2024-03-22T14:00:00Z"
    },
    {
      "interconnectId": 9002,
      "ecGridIdFrom": 123456,
      "ecGridIdTo": 789012,
      "status": "Active",
      "created": "2024-02-20T09:00:00Z",
      "modified": "2024-02-20T09:00:00Z"
    }
  ]
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
curl -X POST "https://rest.ecgrid.io/v2/partners/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridId": 123456, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — list all active interconnects for a given ECGrid ID, paged
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridId = 123456,
    status = "Active",
    pageNo = 1,
    recordsPerPage = 25
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/partners/list", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<InterconnectIDInfo>>>();
Console.WriteLine($"Found {result!.Data.Count} interconnects");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridId\": 123456, \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 25 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners/list"))
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
const url = 'https://rest.ecgrid.io/v2/partners/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridId": 123456, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }),
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
url = "https://rest.ecgrid.io/v2/partners/list"

response = requests.post(
    url,
    json={ "ecGridId": 123456, "status": "Active", "pageNo": 1, "recordsPerPage": 25 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Partner](get-partner)
- [Count Partners](count-partners)
- [Create Partner](create-partner)
