---
title: List IDs
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids/list REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List IDs

Returns a paginated list of ECGrid IDs filtered by mailbox, network, and/or status.

## Endpoint

```http
POST /v2/ids/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | No | — | Filter by mailbox ID |
| `networkId` | integer | No | — | Filter by network ID |
| `status` | string | No | See `Status` enum | Filter by lifecycle status |
| `pageNo` | integer | No | Starts at 1 | Page number for pagination |
| `recordsPerPage` | integer | No | — | Number of records per page |

```json
{
  "mailboxId": 1001,
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 25
}
```

## Response

Returns a paginated array of `ECGridIDInfo` objects.

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
    },
    {
      "ecGridId": 123457,
      "mailboxId": 1001,
      "networkId": 42,
      "qualifier": "ZZ",
      "id": "PARTNER002",
      "description": "Beta Logistics",
      "status": "Active",
      "routingGroup": "ProductionA",
      "ediStandard": "X12"
    }
  ]
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

See [Enums reference](../../appendix/enums) for complete enum definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/ids/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 1001, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — list all active ECGrid IDs for a given mailbox, paged
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    mailboxId = 1001,
    status = "Active",
    pageNo = 1,
    recordsPerPage = 25
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/ids/list", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ECGridIDInfo>>>();
Console.WriteLine($"Found {result!.Data.Count} ECGrid IDs");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 1001, \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 25 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/list"))
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
const url = 'https://rest.ecgrid.io/v2/ids/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 1001, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }),
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
url = "https://rest.ecgrid.io/v2/ids/list"

response = requests.post(
    url,
    json={ "mailboxId": 1001, "status": "Active", "pageNo": 1, "recordsPerPage": 25 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Find ID](find-id)
- [Create ID](create-id)
