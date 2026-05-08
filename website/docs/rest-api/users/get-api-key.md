---
title: Get API Key
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Get API Key documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get API Key

Retrieves the current API key for a specific user by their User ID.

## Endpoint

```http
GET /v2/users/key/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The User ID whose API key to retrieve |

:::note
This operation requires `NetworkAdmin` or higher `AuthLevel`. Users may retrieve their own API key via [Get Me](./get-me) and [Generate API Key](./generate-api-key).
:::

## Response

Returns the API key string for the specified user.

```json
{
  "success": true,
  "data": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/users/key/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve a user's API key using IHttpClientFactory
// Requires NetworkAdmin or higher auth level
public async Task<string?> GetApiKeyAsync(IHttpClientFactory httpClientFactory, int userId)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var response = await http.GetAsync($"https://rest.ecgrid.io/v2/users/key/{userId}");
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<string>>();
    return result?.Data;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/users/key/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/users/key/${id}`;

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
id = 0  # replace with actual id
url = f"https://rest.ecgrid.io/v2/users/key/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Generate API Key](./generate-api-key) — generate a new API key, invalidating the current one
- [Get Me](./get-me) — retrieve your own user context and confirm which key is active
- [Authentication](../../getting-started/authentication) — how to use API keys in requests
