---
title: Update Config
sidebar_position: 16
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Update Config documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Config

Updates advanced configuration settings for a specified user account, including notification preferences, cell phone contact information, and other user-level options.

## Endpoint

```http
POST /v2/users/update-config
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | integer | Yes | Must be an existing user | ID of the user whose configuration to update |

Additional configuration fields are passed alongside `userId`. Omit any field to leave its current value unchanged.

```json
{
  "userId": 1042
}
```

## Response

Returns a boolean indicating whether the configuration was successfully updated.

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
curl -X POST "https://rest.ecgrid.io/v2/users/update-config" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 1042 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Update advanced user configuration settings using IHttpClientFactory
public async Task<bool> UpdateUserConfigAsync(
    IHttpClientFactory httpClientFactory,
    int userId,
    object? additionalConfig = null)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    // Merge userId with any additional config fields provided by the caller
    var requestBody = new System.Text.Json.Nodes.JsonObject
    {
        ["userId"] = userId
    };

    if (additionalConfig is not null)
    {
        var extraJson = System.Text.Json.JsonSerializer.SerializeToNode(additionalConfig);
        if (extraJson is System.Text.Json.Nodes.JsonObject extraObj)
        {
            foreach (var prop in extraObj)
            {
                requestBody[prop.Key] = prop.Value?.DeepClone();
            }
        }
    }

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/update-config",
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

String body = "{ \"userId\": 1042 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/update-config"))
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
const url = 'https://rest.ecgrid.io/v2/users/update-config';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 1042 }),
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
url = "https://rest.ecgrid.io/v2/users/update-config"

response = requests.post(
    url,
    json={ "userId": 1042 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Update User](./update-user) — update core profile fields (name, email)
- [Set Role](./set-role) — change the user's AuthLevel
- [Set Network Mailbox](./set-network-mailbox) — change the user's network or mailbox context
- [Send SMS](./send-sms) — send a message using the cell carrier configured here
