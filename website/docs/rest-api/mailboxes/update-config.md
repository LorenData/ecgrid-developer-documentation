---
title: Update Mailbox Config
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/mailboxes/update-config reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Mailbox Config

Updates the operational configuration settings for a mailbox, such as processing options and delivery behavior.

## Endpoint

```http
POST /v2/mailboxes/update-config
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | Yes | — | ID of the mailbox to configure |

> Additional configuration fields are mailbox-specific. Refer to the live [Swagger UI](https://rest.ecgrid.io/swagger/index.html) for the full field list applicable to your account tier.

```json
{
  "mailboxId": 5001
}
```

## Response

Returns a success indicator confirming the configuration was saved.

```json
{
  "success": true,
  "data": null,
  "errorCode": null,
  "message": "Mailbox configuration updated."
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/mailboxes/update-config" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 5001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — update mailbox configuration settings
var payload = new
{
    mailboxId = 5001
    // add additional config fields as returned by the Swagger spec for your account
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/mailboxes/update-config")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<object>>();
Console.WriteLine($"Config update succeeded: {result?.Success}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 5001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/update-config"))
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
const url = 'https://rest.ecgrid.io/v2/mailboxes/update-config';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 5001 }),
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
url = "https://rest.ecgrid.io/v2/mailboxes/update-config"

response = requests.post(
    url,
    json={ "mailboxId": 5001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Mailbox](./get-mailbox)
- [Update Mailbox](./update-mailbox)
- [Set X12 Delimiters](./x12-delimiters)
