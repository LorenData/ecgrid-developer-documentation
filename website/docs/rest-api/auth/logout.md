---
title: Logout
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST Auth logout endpoint page created - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Logout

Invalidate the current Bearer token or API session, ending the authenticated session immediately.

## Endpoint

```http
POST /v2/auth/logout
```

## Request Body

No request body is required. The session is identified from the `Authorization` or `X-API-Key` header on the request.

## Response

Returns a success confirmation. After a successful logout, the token or session used to make this call is no longer valid.

```json
{
  "success": true,
  "data": null,
  "errorCode": "",
  "message": "Session terminated."
}
```

:::caution
After calling logout, any subsequent requests using the same token will receive a `401 Unauthorized` response. If you are using API Key authentication, logout terminates the current session but does not revoke the key itself.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/auth/logout" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "success": true, "data": null, "errorCode": "", "message": "Session terminated." }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Logout and clear the authorization header
using System.Net.Http.Json;

/// <summary>
/// Logs out the current session and clears the client's authorization header.
/// </summary>
async Task LogoutAsync(HttpClient httpClient)
{
    var response = await httpClient.PostAsync(
        "https://rest.ecgrid.io/v2/auth/logout",
        content: null);

    response.EnsureSuccessStatusCode();

    // Clear the stored token so it cannot be reused accidentally
    httpClient.DefaultRequestHeaders.Authorization = null;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"success\": true, \"data\": null, \"errorCode\": \"\", \"message\": \"Session terminated.\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/logout"))
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
const url = 'https://rest.ecgrid.io/v2/auth/logout';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "success": true, "data": null, "errorCode": "", "message": "Session terminated." }),
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
url = "https://rest.ecgrid.io/v2/auth/logout"

response = requests.post(
    url,
    json={ "success": true, "data": null, "errorCode": "", "message": "Session terminated." },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Login](./login.md) — start a new session
- [Refresh Token](./refresh-token.md) — extend an active session before logout
- [Session](./session.md) — inspect the current session before logging out
