---
title: Delete Callback
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of delete-callback REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Delete Callback

Permanently remove a callback registration and stop all future event deliveries to its endpoint.

## Endpoint

```http
DELETE /v2/callbacks
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `callbackId` | int | Yes | — | The unique ID of the callback to delete. |

```json
{
  "callbackId": 7001
}
```

## Response

Returns a boolean indicating whether the deletion was successful.

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
curl -X DELETE "https://rest.ecgrid.io/v2/callbacks" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — permanently remove a callback registration
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new { callbackId = 7001 };

// DELETE with a request body requires an explicit HttpRequestMessage
var request = new HttpRequestMessage(HttpMethod.Delete, "/v2/callbacks")
{
    Content = JsonContent.Create(requestBody)
};

var response = await client.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result.Data)
{
    Console.WriteLine("Callback successfully deleted.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks"))
    .header("X-API-Key", apiKey)
    .DELETE()
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
const url = 'https://rest.ecgrid.io/v2/callbacks';

const response = await fetch(url, {
  method: 'DELETE',
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
url = "https://rest.ecgrid.io/v2/callbacks"

response = requests.delete(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Create Callback](./create-callback)
- [Update Callback](./update-callback)
- [Queue List](./queue-list)
