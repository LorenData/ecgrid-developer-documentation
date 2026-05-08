---
title: Generate API Key
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Generate API Key documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Generate API Key

Generates a new API key for a specific user, immediately invalidating their previous key.

:::caution
Generating a new API key **immediately invalidates the user's existing key**. Any integrations, scripts, or services still using the old key will stop authenticating until they are updated with the new key. Coordinate key rotation carefully before calling this endpoint.
:::

## Endpoint

```http
POST /v2/users/key-generate/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The User ID for whom to generate a new API key |

## Response

Returns the newly generated API key string.

```json
{
  "success": true,
  "data": "f9e8d7c6-b5a4-3210-fedc-ba9876543210"
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users/key-generate/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Generate a new API key for a user using IHttpClientFactory
// WARNING: The previous API key is invalidated immediately upon success.
public async Task<string?> GenerateApiKeyAsync(IHttpClientFactory httpClientFactory, int userId)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    // POST with no body — the user ID is in the path
    var response = await http.PostAsync(
        $"https://rest.ecgrid.io/v2/users/key-generate/{userId}",
        content: null);
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
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/users/key-generate/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/users/key-generate/${id}`;

const response = await fetch(url, {
  method: 'POST',
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
url = f"https://rest.ecgrid.io/v2/users/key-generate/{id}"

response = requests.post(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get API Key](./get-api-key) — retrieve the current API key for a user without rotating it
- [Reset Sessions](./reset-sessions) — invalidate JWT sessions without rotating the API key
- [Authentication](../../getting-started/authentication) — how API keys are used in requests
