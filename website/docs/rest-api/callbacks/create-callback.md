---
title: Create Callback
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of create-callback REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Callback

Register a new webhook callback so ECGrid posts a JSON notification to your endpoint when a specified event occurs.

## Endpoint

```http
POST /v2/callbacks/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `url` | string | Yes | HTTPS only | The webhook URL ECGrid will POST to when the event fires. |
| `event` | Objects | Yes | See ENUMs | The ECGrid event type that triggers this callback. |
| `mailboxId` | int | No | — | Scope the callback to a specific mailbox. Omit for network-wide. |
| `networkId` | int | No | — | Scope the callback to a specific network. |
| `httpAuthType` | HTTPAuthType | No | See ENUMs | Authentication method ECGrid uses when calling your endpoint. |
| `username` | string | No | — | Username for HTTP authentication (required if `httpAuthType` is not `None`). |
| `password` | string | No | — | Password for HTTP authentication (required if `httpAuthType` is not `None`). |

```json
{
  "url": "https://app.example.com/webhooks/ecgrid",
  "event": "Parcel",
  "mailboxId": 12345,
  "httpAuthType": "Basic",
  "username": "webhook_user",
  "password": "s3cr3t!"
}
```

:::note
The callback URL must use **HTTPS**. ECGrid will POST a JSON payload to this URL whenever the specified event fires on the scoped mailbox or network.
:::

## Response

Returns the newly created callback record, including the assigned `callbackId`.

```json
{
  "success": true,
  "data": {
    "callbackId": 7001,
    "url": "https://app.example.com/webhooks/ecgrid",
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

| Value | Description |
|---|---|
| `Parcel` | Triggered on parcel events (received, sent, error) |
| `Interchange` | Triggered on interchange-level events |
| `Interconnect` | Triggered on partner interconnect status changes |
| `User` | Triggered on user account events |
| `Mailbox` | Triggered on mailbox configuration changes |
| `Network` | Triggered on network-level events |

See [Enums Reference](../../appendix/enums) for the complete `Objects` ENUM.

### HTTPAuthType

| Value | Description |
|---|---|
| `None` | No authentication — endpoint is open |
| `Basic` | HTTP Basic authentication |
| `Digest` | HTTP Digest authentication |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/callbacks/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://app.example.com/webhooks/ecgrid", "event": "Parcel", "mailboxId": 12345, "httpAuthType": "Basic", "username": "webhook_user", "password": "s3cr3t!" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — register a new webhook callback for parcel events
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new
{
    url = "https://app.example.com/webhooks/ecgrid",
    @event = "Parcel",
    mailboxId = 12345,
    httpAuthType = "Basic",
    username = configuration["Webhook:Username"],
    password = configuration["Webhook:Password"]
};

var response = await client.PostAsJsonAsync("/v2/callbacks/create", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CallbackInfo>>();
Console.WriteLine($"Callback created with ID: {result.Data.CallbackId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"url\": \"https://app.example.com/webhooks/ecgrid\", \"event\": \"Parcel\", \"mailboxId\": 12345, \"httpAuthType\": \"Basic\", \"username\": \"webhook_user\", \"password\": \"s3cr3t!\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/create"))
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
const url = 'https://rest.ecgrid.io/v2/callbacks/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "url": "https://app.example.com/webhooks/ecgrid", "event": "Parcel", "mailboxId": 12345, "httpAuthType": "Basic", "username": "webhook_user", "password": "s3cr3t!" }),
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
url = "https://rest.ecgrid.io/v2/callbacks/create"

response = requests.post(
    url,
    json={ "url": "https://app.example.com/webhooks/ecgrid", "event": "Parcel", "mailboxId": 12345, "httpAuthType": "Basic", "username": "webhook_user", "password": "s3cr3t!" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Update Callback](./update-callback)
- [Delete Callback](./delete-callback)
- [Test Callback](./test-callback)
- [Queue List](./queue-list)
- [Configure Callbacks Guide](../../common-operations/configure-callbacks)
