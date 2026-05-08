---
title: Login
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST Auth login endpoint page created - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Login

Authenticate with an ECGrid username and password to obtain a JWT Bearer token for subsequent API calls.

## Endpoint

```http
POST /v2/auth/login
```

:::info No authentication required
This endpoint does not require an `X-API-Key` or `Authorization` header — it is the entry point for obtaining credentials.
:::

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `login` | string | Yes | — | ECGrid username or login identifier |
| `password` | string | Yes | — | Account password |

```json
{
  "login": "jsmith@example.com",
  "password": "Sup3r$ecret!"
}
```

## Response

Returns a JWT Bearer token along with its expiry time and the authenticated user's ID.

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2026-05-07T18:30:00Z",
    "userId": 4821
  },
  "errorCode": "",
  "message": ""
}
```

| Field | Type | Description |
|---|---|---|
| `token` | string | JWT Bearer token — pass as `Authorization: Bearer <token>` |
| `expiresAt` | datetime (ISO 8601) | UTC timestamp when the token expires |
| `userId` | integer | Internal ECGrid user ID for the authenticated account |

:::tip Prefer API Key for server-to-server integrations
JWT tokens expire and require refresh. For long-running services or automated pipelines, use the `X-API-Key` header with a key obtained from [Generate API Key](../users/generate-api-key.md) instead.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/auth/login" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "login": "jsmith@example.com", "password": "Sup3r$ecret!" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Login and capture the Bearer token for reuse
using System.Net.Http.Json;

var httpClient = httpClientFactory.CreateClient("ECGrid");

var loginResponse = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/auth/login",
    new { login = config["ECGrid:Login"], password = config["ECGrid:Password"] });

loginResponse.EnsureSuccessStatusCode();

var result = await loginResponse.Content.ReadFromJsonAsync<ApiResponse<LoginData>>();

if (result?.Success == true)
{
    // Store token for use in subsequent requests
    httpClient.DefaultRequestHeaders.Authorization =
        new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", result.Data.Token);
}

record LoginData(string Token, DateTime ExpiresAt, int UserId);
record ApiResponse<T>(bool Success, T? Data, string ErrorCode, string Message);
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"login\": \"jsmith@example.com\", \"password\": \"Sup3r$ecret!\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/login"))
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
const url = 'https://rest.ecgrid.io/v2/auth/login';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "login": "jsmith@example.com", "password": "Sup3r$ecret!" }),
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
url = "https://rest.ecgrid.io/v2/auth/login"

response = requests.post(
    url,
    json={ "login": "jsmith@example.com", "password": "Sup3r$ecret!" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Refresh Token](./refresh-token.md) — extend a token before it expires
- [Logout](./logout.md) — invalidate the current session
- [Session](./session.md) — inspect the current authenticated session
- [Authentication & Session Management](../../guides/authentication-session-management.md)
