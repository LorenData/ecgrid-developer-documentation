---
title: Terminate User
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Terminate User documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Terminate User

Permanently terminates a user account, revoking all access and invalidating all sessions and API keys.

:::danger
Terminating a user account is permanent and cannot be undone. All active sessions and API keys for the user will be immediately invalidated. Confirm the correct User ID before calling this endpoint.
:::

## Endpoint

```http
DELETE /v2/users/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The User ID of the account to terminate |

## Response

Returns a boolean indicating whether the termination was successful.

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
curl -X DELETE "https://rest.ecgrid.io/v2/users/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Terminate a user account using IHttpClientFactory
// WARNING: This action is permanent. Verify the userId before calling.
public async Task<bool> TerminateUserAsync(IHttpClientFactory httpClientFactory, int userId)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var response = await http.DeleteAsync($"https://rest.ecgrid.io/v2/users/{userId}");
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
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/users/%s", id)))
    .header("X-API-Key", apiKey)
    .DELETE()
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
const url = `https://rest.ecgrid.io/v2/users/${id}`;

const response = await fetch(url, {
  method: 'DELETE',
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
url = f"https://rest.ecgrid.io/v2/users/{id}"

response = requests.delete(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — verify user details before termination
- [Reset Sessions](./reset-sessions) — revoke active sessions without terminating the account
- [List Users](./list-users) — review users before taking action
