---
title: Get Event by ID
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of get-event-by-id REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Event by ID

Retrieve the full details of a specific callback event, including the payload delivered, delivery status, and attempt history.

## Endpoint

```http
POST /v2/callbacks/get-event-by-id
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `callbackEventId` | int | Yes | — | The unique ID of the callback event to retrieve. |

```json
{
  "callbackEventId": 88001
}
```

## Response

Returns the full callback event record, including the JSON payload that was posted to your endpoint, the delivery status, and the number of delivery attempts made.

```json
{
  "success": true,
  "data": {
    "callbackEventId": 88001,
    "callbackId": 7001,
    "event": "Parcel",
    "mailboxId": 12345,
    "objectId": 5550001,
    "payload": "{\"parcelId\":5550001,\"status\":\"InBoxReady\",\"created\":\"2026-05-03T08:22:00Z\"}",
    "status": "Active",
    "attempts": 1,
    "created": "2026-05-03T08:22:00Z",
    "lastAttempt": "2026-05-03T08:22:05Z",
    "delivered": "2026-05-03T08:22:05Z",
    "httpStatus": 200
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/callbacks/get-event-by-id" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "callbackEventId": 88001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — fetch full details of a callback event including payload and attempt count
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new { callbackEventId = 88001 };

var response = await client.PostAsJsonAsync("/v2/callbacks/get-event-by-id", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CallbackEventDetail>>();
Console.WriteLine($"Event {result.Data.CallbackEventId}: {result.Data.Event}");
Console.WriteLine($"  Attempts: {result.Data.Attempts} | Last HTTP: {result.Data.HttpStatus}");
Console.WriteLine($"  Payload: {result.Data.Payload}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"callbackEventId\": 88001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/get-event-by-id"))
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
const url = 'https://rest.ecgrid.io/v2/callbacks/get-event-by-id';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "callbackEventId": 88001 }),
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
url = "https://rest.ecgrid.io/v2/callbacks/get-event-by-id"

response = requests.post(
    url,
    json={ "callbackEventId": 88001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Event List](./event-list)
- [Queue List](./queue-list)
- [Get Queue by ID](./get-queue-by-id)
- [Create Callback](./create-callback)
