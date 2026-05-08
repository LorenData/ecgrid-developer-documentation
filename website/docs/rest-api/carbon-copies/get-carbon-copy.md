---
title: Get Carbon Copy
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Get Carbon Copy REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Carbon Copy

Retrieves the details of a specific carbon copy rule by its unique ID.

## Endpoint

```http
GET /v2/carboncopies/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | Unique identifier of the carbon copy rule |

## Response

Returns the carbon copy rule details including source and destination mailboxes, direction, and status.

```json
{
  "success": true,
  "data": {
    "ccId": 1042,
    "fromMailboxId": 101,
    "toMailboxId": 202,
    "status": "Active",
    "direction": "InBox",
    "created": "2025-01-15T10:30:00Z"
  }
}
```

## ENUMs

This endpoint returns values from the `Direction` and `Status` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/carboncopies/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve a carbon copy rule by ID
using var response = await httpClient.GetAsync($"https://rest.ecgrid.io/v2/carboncopies/{ccId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CarbonCopyInfo>>();
Console.WriteLine($"CC Rule {result.Data.CcId}: {result.Data.Direction} from mailbox {result.Data.FromMailboxId} to {result.Data.ToMailboxId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/carboncopies/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/carboncopies/${id}`;

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
url = f"https://rest.ecgrid.io/v2/carboncopies/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Create Carbon Copy](./create-carbon-copy)
- [List Carbon Copies](./list-carbon-copies)
- [Update Carbon Copy](./update-carbon-copy)
- [Delete Carbon Copy](./delete-carbon-copy)
- [ENUMs Reference](../../appendix/enums)
