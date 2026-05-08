---
title: Get Me
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Get Me documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Me

Returns the `UserIDInfo` for the currently authenticated user based on the API key or JWT token in the request.

## Endpoint

```http
GET /v2/users/me
```

## Response

Returns the `UserIDInfo` object for the caller's user account.

This endpoint is useful for confirming which user context an API key belongs to, verifying the effective `AuthLevel`, and troubleshooting authentication issues without needing to know a specific User ID.

```json
{
  "success": true,
  "data": {
    "userId": 1042,
    "login": "jsmith",
    "email": "jsmith@example.com",
    "firstName": "John",
    "lastName": "Smith",
    "networkId": 1,
    "mailboxId": 101,
    "authLevel": "MailboxAdmin",
    "status": "Active",
    "created": "2024-03-15T10:22:00Z"
  }
}
```

## ENUMs

This endpoint returns the following ENUMs in its response. See [Appendix: ENUMs](../../appendix/enums) for full value lists.

- `AuthLevel` — the permission level of the authenticated user
- `Status` — the lifecycle state of the authenticated user

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/users/me" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve the authenticated user's own profile using IHttpClientFactory
public async Task<UserIdInfo?> GetMeAsync(IHttpClientFactory httpClientFactory)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var response = await http.GetAsync("https://rest.ecgrid.io/v2/users/me");
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<UserIdInfo>>();
    return result?.Data;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/me"))
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
const url = 'https://rest.ecgrid.io/v2/users/me';

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
url = "https://rest.ecgrid.io/v2/users/me"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — retrieve a specific user by ID
- [Get API Key](./get-api-key) — retrieve the API key for a user
- [Authentication](../../getting-started/authentication) — details on API key and JWT authentication
