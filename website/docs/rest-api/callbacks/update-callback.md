---
title: Update Callback
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of update-callback REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Callback

Modify the URL, event type, status, or authentication settings of an existing callback registration.

## Endpoint

```http
POST /v2/callbacks/update
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `callbackId` | int | Yes | — | The unique ID of the callback to update. |
| `url` | string | No | HTTPS only | New webhook URL to deliver events to. |
| `event` | Objects | No | See ENUMs | Updated event type that triggers this callback. |
| `status` | Status | No | See ENUMs | New status for the callback (e.g., `Suspended` to pause delivery). |
| `httpAuthType` | HTTPAuthType | No | See ENUMs | Updated authentication method for your endpoint. |
| `username` | string | No | — | Updated username for HTTP authentication. |
| `password` | string | No | — | Updated password for HTTP authentication. |

```json
{
  "callbackId": 7001,
  "url": "https://app.example.com/webhooks/ecgrid-v2",
  "status": "Active",
  "httpAuthType": "Basic",
  "username": "webhook_user",
  "password": "n3wP@ssword!"
}
```

## Response

Returns the updated callback record.

```json
{
  "success": true,
  "data": {
    "callbackId": 7001,
    "url": "https://app.example.com/webhooks/ecgrid-v2",
    "event": "Parcel",
    "mailboxId": 12345,
    "networkId": 0,
    "httpAuthType": "Basic",
    "status": "Active"
  }
}
```

## ENUMs

### Objects

See [Enums Reference](../../appendix/enums) for the complete `Objects` ENUM.

### HTTPAuthType

| Value | Description |
|---|---|
| `None` | No authentication |
| `Basic` | HTTP Basic authentication |
| `Digest` | HTTP Digest authentication |

### Status

| Value | Description |
|---|---|
| `Active` | Callback is active and delivering events |
| `Suspended` | Callback is paused — events are not delivered |
| `Terminated` | Callback is permanently disabled |

See [Enums Reference](../../appendix/enums) for the complete `Status` ENUM.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/callbacks/update" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "callbackId": 7001, "url": "https://app.example.com/webhooks/ecgrid-v2", "status": "Active", "httpAuthType": "Basic", "username": "webhook_user", "password": "n3wP@ssword!" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — update an existing callback's URL and credentials
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new
{
    callbackId = 7001,
    url = "https://app.example.com/webhooks/ecgrid-v2",
    status = "Active",
    httpAuthType = "Basic",
    username = configuration["Webhook:Username"],
    password = configuration["Webhook:Password"]
};

var response = await client.PostAsJsonAsync("/v2/callbacks/update", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CallbackInfo>>();
Console.WriteLine($"Callback {result.Data.CallbackId} updated. URL: {result.Data.Url}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"callbackId\": 7001, \"url\": \"https://app.example.com/webhooks/ecgrid-v2\", \"status\": \"Active\", \"httpAuthType\": \"Basic\", \"username\": \"webhook_user\", \"password\": \"n3wP@ssword!\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/update"))
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
const url = 'https://rest.ecgrid.io/v2/callbacks/update';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "callbackId": 7001, "url": "https://app.example.com/webhooks/ecgrid-v2", "status": "Active", "httpAuthType": "Basic", "username": "webhook_user", "password": "n3wP@ssword!" }),
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
url = "https://rest.ecgrid.io/v2/callbacks/update"

response = requests.post(
    url,
    json={ "callbackId": 7001, "url": "https://app.example.com/webhooks/ecgrid-v2", "status": "Active", "httpAuthType": "Basic", "username": "webhook_user", "password": "n3wP@ssword!" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Create Callback](./create-callback)
- [Delete Callback](./delete-callback)
- [Test Callback](./test-callback)
- [Configure Callbacks Guide](../../common-operations/configure-callbacks)
