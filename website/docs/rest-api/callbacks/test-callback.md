---
title: Test Callback
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of test-callback REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Test Callback

Send a test POST to your registered callback endpoint and return the HTTP response received from your server.

## Endpoint

```http
POST /v2/callbacks/test
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `callbackId` | int | Yes | — | The unique ID of the callback to test. |

```json
{
  "callbackId": 7001
}
```

:::tip
Use this endpoint immediately after [creating a callback](./create-callback) to verify that your endpoint is reachable and responding correctly before relying on it in production.
:::

## Response

Returns the test result, including the HTTP status code returned by your webhook endpoint and any response body received.

```json
{
  "success": true,
  "data": {
    "callbackId": 7001,
    "url": "https://app.example.com/webhooks/ecgrid",
    "httpStatus": 200,
    "responseBody": "OK",
    "testedAt": "2026-05-07T11:00:00Z"
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/callbacks/test" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "callbackId": 7001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — fire a test delivery to verify the callback endpoint is reachable
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new { callbackId = 7001 };

var response = await client.PostAsJsonAsync("/v2/callbacks/test", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CallbackTestResult>>();
if (result.Data.HttpStatus is >= 200 and < 300)
{
    Console.WriteLine($"Callback endpoint is reachable. HTTP {result.Data.HttpStatus}: {result.Data.ResponseBody}");
}
else
{
    Console.WriteLine($"Callback endpoint returned HTTP {result.Data.HttpStatus}. Check your endpoint configuration.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"callbackId\": 7001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/test"))
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
const url = 'https://rest.ecgrid.io/v2/callbacks/test';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "callbackId": 7001 }),
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
url = "https://rest.ecgrid.io/v2/callbacks/test"

response = requests.post(
    url,
    json={ "callbackId": 7001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Create Callback](./create-callback)
- [Update Callback](./update-callback)
- [Get Queue by ID](./get-queue-by-id)
- [Configure Callbacks Guide](../../common-operations/configure-callbacks)
