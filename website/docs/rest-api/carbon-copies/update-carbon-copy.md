---
title: Update Carbon Copy
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Update Carbon Copy REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Carbon Copy

Updates the status or direction of an existing carbon copy rule.

## Endpoint

```http
PUT /v2/carboncopies/update
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ccId` | integer | Yes | Must be an existing CC rule | Unique identifier of the carbon copy rule to update |
| `status` | Status | No | See ENUMs | New status for the rule (e.g., `Active`, `Suspended`) |
| `direction` | Direction | No | See ENUMs | New traffic direction for the rule |

```json
{
  "ccId": 1042,
  "status": "Suspended",
  "direction": "OutBox"
}
```

## Response

Returns the updated carbon copy rule.

```json
{
  "success": true,
  "data": {
    "ccId": 1042,
    "fromMailboxId": 101,
    "toMailboxId": 202,
    "status": "Suspended",
    "direction": "OutBox",
    "created": "2025-01-15T10:30:00Z"
  }
}
```

## ENUMs

This endpoint uses the `Status` and `Direction` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X PUT "https://rest.ecgrid.io/v2/carboncopies/update" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ccId": 1042, "status": "Suspended", "direction": "OutBox" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Suspend a carbon copy rule
var request = new
{
    ccId = 1042,
    status = "Suspended"
};

using var response = await httpClient.PutAsJsonAsync(
    "https://rest.ecgrid.io/v2/carboncopies/update",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CarbonCopyInfo>>();
Console.WriteLine($"CC Rule {result.Data.CcId} updated — Status: {result.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ccId\": 1042, \"status\": \"Suspended\", \"direction\": \"OutBox\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/carboncopies/update"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .PUT(HttpRequest.BodyPublishers.ofString(body))
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
const url = 'https://rest.ecgrid.io/v2/carboncopies/update';

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ccId": 1042, "status": "Suspended", "direction": "OutBox" }),
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
url = "https://rest.ecgrid.io/v2/carboncopies/update"

response = requests.put(
    url,
    json={ "ccId": 1042, "status": "Suspended", "direction": "OutBox" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Carbon Copy](./get-carbon-copy)
- [Create Carbon Copy](./create-carbon-copy)
- [List Carbon Copies](./list-carbon-copies)
- [Delete Carbon Copy](./delete-carbon-copy)
- [ENUMs Reference](../../appendix/enums)
