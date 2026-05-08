---
title: Send SMS
sidebar_position: 14
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Send SMS documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Send SMS

Sends an SMS text message to a user's configured mobile phone number.

## Endpoint

```http
POST /v2/users/send-sms
```

:::note
The target user must have a cell phone number and cell carrier configured in their account. If either is missing or the carrier is unsupported, the message will not be delivered.
:::

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | integer | Yes | Must be an existing user | ID of the user to receive the SMS |
| `message` | string | Yes | — | The text message content to send |

```json
{
  "userId": 1042,
  "message": "Your ECGrid parcel download is ready."
}
```

## Response

Returns a boolean indicating whether the SMS was successfully submitted for delivery.

```json
{
  "success": true,
  "data": true
}
```

## ENUMs

The user's cell carrier configuration uses the `CellCarrier` ENUM. This is set on the user's account, not passed in this request. See [Appendix: ENUMs](../../appendix/enums) for the full list of supported carriers.

- `CellCarrier` — the mobile carrier associated with the user's phone number (e.g., `ATTCingular`, `Verizon`, `TMobile`, `SprintPCS`)

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users/send-sms" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 1042, "message": "Your ECGrid parcel download is ready." }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Send an SMS notification to a user using IHttpClientFactory
// User must have a cell number and carrier configured on their account
public async Task<bool> SendSmsAsync(
    IHttpClientFactory httpClientFactory,
    int userId,
    string message)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        userId,
        message
    };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/send-sms",
        requestBody);
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
    return result?.Data ?? false;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"userId\": 1042, \"message\": \"Your ECGrid parcel download is ready.\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/send-sms"))
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
const url = 'https://rest.ecgrid.io/v2/users/send-sms';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 1042, "message": "Your ECGrid parcel download is ready." }),
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
url = "https://rest.ecgrid.io/v2/users/send-sms"

response = requests.post(
    url,
    json={ "userId": 1042, "message": "Your ECGrid parcel download is ready." },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — verify the user's contact details before sending
- [Update Config](./update-config) — configure a user's cell phone number and carrier
