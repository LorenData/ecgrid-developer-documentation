---
title: Get Queue by ID
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of get-queue-by-id REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Queue by ID

Retrieve the current delivery queue entry and status for a specific callback.

## Endpoint

```http
GET /v2/callbacks/get-queue-by-id?callbackId={callbackId}
```

## Query Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `callbackId` | int | — (required) | The unique ID of the callback whose queue entry to retrieve. |

## Response

Returns a `CallBackQueueIDInfo` object with the callback's current queue position and delivery status details.

```json
{
  "success": true,
  "data": {
    "callbackId": 7001,
    "url": "https://app.example.com/webhooks/ecgrid",
    "event": "Parcel",
    "queuedAt": "2026-05-07T09:00:00Z",
    "lastAttempt": "2026-05-07T09:01:00Z",
    "attempts": 1,
    "status": "Active",
    "lastHttpStatus": 200
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/callbacks/get-queue-by-id?callbackId=$CALLBACK_ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — check the delivery queue status for a specific callback
using var client = httpClientFactory.CreateClient("ECGrid");

var response = await client.GetAsync($"/v2/callbacks/get-queue-by-id?callbackId={callbackId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CallBackQueueIdInfo>>();
Console.WriteLine($"Callback {result.Data.CallbackId} — Status: {result.Data.Status}, Attempts: {result.Data.Attempts}, Last HTTP: {result.Data.LastHttpStatus}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String callbackId = "0"; // replace with actual callbackId

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/callbacks/get-queue-by-id?callbackId=%s", callbackId)))
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
const url = `https://rest.ecgrid.io/v2/callbacks/get-queue-by-id?callbackId=${callbackId}`;

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
callback_id = 0  # replace with actual callback_id
url = f"https://rest.ecgrid.io/v2/callbacks/get-queue-by-id?callbackId={callback_id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Queue List](./queue-list)
- [Event List](./event-list)
- [Get Event by ID](./get-event-by-id)
- [Create Callback](./create-callback)
