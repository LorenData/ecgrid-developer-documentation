---
title: Get User by Name
sidebar_position: 9
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Get By Name documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get User by Name

Searches for users matching a given login name and returns all matching `UserIDInfo` records.

## Endpoint

```http
POST /v2/users/by-name
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `login` | string | Yes | — | The login name to search for |

```json
{
  "login": "jsmith"
}
```

## Response

Returns an array of `UserIDInfo` objects matching the provided login name. Multiple results may be returned if the same login exists across different networks.

```json
{
  "success": true,
  "data": [
    {
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
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users/by-name" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "login": "jsmith" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Find users by login name using IHttpClientFactory
public async Task<List<UserIdInfo>?> GetUsersByNameAsync(
    IHttpClientFactory httpClientFactory,
    string login)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new { login };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/by-name",
        requestBody);
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<UserIdInfo>>>();
    return result?.Data;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"login\": \"jsmith\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/by-name"))
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
const url = 'https://rest.ecgrid.io/v2/users/by-name';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "login": "jsmith" }),
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
url = "https://rest.ecgrid.io/v2/users/by-name"

response = requests.post(
    url,
    json={ "login": "jsmith" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — retrieve a user by their numeric User ID
- [List Users](./list-users) — paginated search with filters for network, mailbox, and auth level
