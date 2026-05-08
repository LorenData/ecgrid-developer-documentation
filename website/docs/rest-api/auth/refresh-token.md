---
title: Refresh Token
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST Auth refresh-token endpoint page created - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Refresh Token

Refresh an expiring JWT Bearer token to obtain a new one without re-authenticating with a username and password.

## Endpoint

```http
POST /v2/auth/refresh
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `token` | string | Yes | Valid JWT | The current Bearer token to refresh |

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Response

Returns a new JWT Bearer token and its updated expiry time.

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2026-05-07T20:00:00Z",
    "userId": 4821
  },
  "errorCode": "",
  "message": ""
}
```

| Field | Type | Description |
|---|---|---|
| `token` | string | New JWT Bearer token to use for subsequent requests |
| `expiresAt` | datetime (ISO 8601) | UTC timestamp when the new token expires |
| `userId` | integer | Internal ECGrid user ID for the authenticated account |

:::note
The original token is invalidated after a successful refresh. Update your stored token immediately with the value returned in `data.token`.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/auth/refresh" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Refresh an expiring token and update the HttpClient authorization header
using System.Net.Http.Json;

/// <summary>
/// Refreshes the current Bearer token and updates the client's default auth header.
/// </summary>
async Task RefreshTokenAsync(HttpClient httpClient, string currentToken)
{
    var response = await httpClient.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/auth/refresh",
        new { token = currentToken });

    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<TokenData>>();

    if (result?.Success == true && result.Data is not null)
    {
        httpClient.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", result.Data.Token);
    }
}

record TokenData(string Token, DateTime ExpiresAt, int UserId);
record ApiResponse<T>(bool Success, T? Data, string ErrorCode, string Message);
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/refresh"))
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
const url = 'https://rest.ecgrid.io/v2/auth/refresh';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }),
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
url = "https://rest.ecgrid.io/v2/auth/refresh"

response = requests.post(
    url,
    json={ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Login](./login.md) — obtain an initial Bearer token
- [Logout](./logout.md) — invalidate the current session
- [Session](./session.md) — check the current token's session details
