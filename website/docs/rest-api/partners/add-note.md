---
title: Add Note
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/partners/note REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Add Note

Adds an audit note to an interconnect record for tracking changes, approvals, or support history.

## Endpoint

```http
POST /v2/partners/note
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `interconnectId` | integer | Yes | Must be a valid interconnect ID | The interconnect to add the note to |
| `note` | string | Yes | — | The note text to append to the interconnect record |

```json
{
  "interconnectId": 9001,
  "note": "Approved by network admin on 2024-06-01. Test EDI verified."
}
```

## Response

Returns a success boolean confirming the note was added.

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
curl -X POST "https://rest.ecgrid.io/v2/partners/note" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "interconnectId": 9001, "note": "Approved by network admin on 2024-06-01. Test EDI verified." }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — append an audit note to an interconnect record
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    interconnectId = 9001,
    note = "Approved by network admin on 2024-06-01. Test EDI verified."
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/partners/note", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
Console.WriteLine($"Note added: {result!.Data}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"interconnectId\": 9001, \"note\": \"Approved by network admin on 2024-06-01. Test EDI verified.\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners/note"))
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
const url = 'https://rest.ecgrid.io/v2/partners/note';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "interconnectId": 9001, "note": "Approved by network admin on 2024-06-01. Test EDI verified." }),
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
url = "https://rest.ecgrid.io/v2/partners/note"

response = requests.post(
    url,
    json={ "interconnectId": 9001, "note": "Approved by network admin on 2024-06-01. Test EDI verified." },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Notes](list-notes)
- [Get Partner](get-partner)
