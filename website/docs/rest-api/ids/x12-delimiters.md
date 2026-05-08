---
title: X12 Delimiters
sidebar_position: 13
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids/tp-x12-delimiters REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# X12 Delimiters

Sets custom X12 EDI delimiter characters for a trading partner ECGrid ID.

## Endpoint

```http
POST /v2/ids/tp-x12-delimiters
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridId` | integer | Yes | Must be a valid ECGrid ID | The ECGrid ID to configure |
| `elementDelimiter` | string | Yes | Single character | ISA element delimiter (e.g. `"*"`) |
| `subElementDelimiter` | string | Yes | Single character | ISA sub-element delimiter (e.g. `":"`) |
| `segmentTerminator` | string | Yes | Single character | Segment terminator (e.g. `"~"`) |

```json
{
  "ecGridId": 123456,
  "elementDelimiter": "*",
  "subElementDelimiter": ":",
  "segmentTerminator": "~"
}
```

## Response

Returns a success boolean confirming the delimiter configuration was applied.

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
curl -X POST "https://rest.ecgrid.io/v2/ids/tp-x12-delimiters" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridId": 123456, "elementDelimiter": "*", "subElementDelimiter": ":", "segmentTerminator": "~" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — set custom X12 delimiter characters for a trading partner ID
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridId = 123456,
    elementDelimiter = "*",
    subElementDelimiter = ":",
    segmentTerminator = "~"
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/ids/tp-x12-delimiters", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
Console.WriteLine($"X12 delimiters configured: {result!.Data}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridId\": 123456, \"elementDelimiter\": \"*\", \"subElementDelimiter\": \":\", \"segmentTerminator\": \"~\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/tp-x12-delimiters"))
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
const url = 'https://rest.ecgrid.io/v2/ids/tp-x12-delimiters';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridId": 123456, "elementDelimiter": "*", "subElementDelimiter": ":", "segmentTerminator": "~" }),
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
url = "https://rest.ecgrid.io/v2/ids/tp-x12-delimiters"

response = requests.post(
    url,
    json={ "ecGridId": 123456, "elementDelimiter": "*", "subElementDelimiter": ":", "segmentTerminator": "~" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Update Config](update-config)
- [Mailbox X12 Delimiters](../mailboxes/x12-delimiters)
