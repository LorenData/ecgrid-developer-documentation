---
title: List Notes
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/partners/notelist REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Notes

Retrieves all audit notes attached to an interconnect record.

## Endpoint

```http
POST /v2/partners/notelist
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `interconnectId` | integer | Yes | Must be a valid interconnect ID | The interconnect to retrieve notes for |

```json
{
  "interconnectId": 9001
}
```

## Response

Returns an array of note objects, each containing the note text, timestamp, and the user who created it.

```json
{
  "success": true,
  "data": [
    {
      "text": "Approved by network admin on 2024-06-01. Test EDI verified.",
      "timestamp": "2024-06-01T14:35:00Z",
      "userId": 501
    },
    {
      "text": "Production go-live confirmed by trading partner contact.",
      "timestamp": "2024-06-03T09:10:00Z",
      "userId": 502
    }
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/partners/notelist" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "interconnectId": 9001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve all audit notes for an interconnect record
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    interconnectId = 9001
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/partners/notelist", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<InterconnectNote>>>();
foreach (var note in result!.Data)
{
    Console.WriteLine($"[{note.Timestamp:u}] User {note.UserId}: {note.Text}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"interconnectId\": 9001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners/notelist"))
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
const url = 'https://rest.ecgrid.io/v2/partners/notelist';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "interconnectId": 9001 }),
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
url = "https://rest.ecgrid.io/v2/partners/notelist"

response = requests.post(
    url,
    json={ "interconnectId": 9001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Add Note](add-note)
- [Get Partner](get-partner)
