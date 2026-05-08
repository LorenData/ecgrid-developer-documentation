---
title: Reset Sessions
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Reset Sessions documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Reset Sessions

Invalidates all open JWT sessions for a specified user, forcing them to re-authenticate on their next request.

## Endpoint

```http
POST /v2/users/reset/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The User ID whose sessions should be invalidated |

This endpoint is particularly useful for security incidents — for example, if a user's credentials are suspected to be compromised, calling this endpoint immediately revokes all active bearer tokens without requiring an API key rotation.

## Response

Returns a boolean indicating whether the session reset was successful.

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
curl -X POST "https://rest.ecgrid.io/v2/users/reset/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Invalidate all JWT sessions for a user using IHttpClientFactory
// Use this during security incidents to force re-authentication
public async Task<bool> ResetSessionsAsync(IHttpClientFactory httpClientFactory, int userId)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    // POST with no body — the user ID is in the path
    var response = await http.PostAsync(
        $"https://rest.ecgrid.io/v2/users/reset/{userId}",
        content: null);
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
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/users/reset/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/users/reset/${id}`;

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
url = f"https://rest.ecgrid.io/v2/users/reset/{id}"

response = requests.post(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Generate API Key](./generate-api-key) — rotate the user's API key in addition to revoking sessions
- [Terminate User](./terminate-user) — permanently disable the account if the security concern is severe
- [Authentication](../../guides/authentication-session-management) — details on JWT session lifecycle
