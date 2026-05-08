---
title: Get User
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Get User documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get User

Retrieves detailed information about a specific user by their User ID.

## Endpoint

```http
GET /v2/users/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The unique User ID to retrieve |

## Response

Returns a `UserIDInfo` object for the specified user.

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

This endpoint uses the following ENUMs in its response. See [Appendix: ENUMs](../../appendix/enums) for full value lists.

- `AuthLevel` — permission level of the user (e.g., `NetworkAdmin`, `MailboxAdmin`, `MailboxUser`)
- `Status` — lifecycle state of the user (e.g., `Active`, `Suspended`, `Terminated`)

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/users/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve a user by ID using IHttpClientFactory
public async Task<UserIdInfo?> GetUserAsync(IHttpClientFactory httpClientFactory, int userId)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var response = await http.GetAsync($"https://rest.ecgrid.io/v2/users/{userId}");
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
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/users/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/users/${id}`;

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
url = f"https://rest.ecgrid.io/v2/users/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Users](./list-users) — search and filter all users
- [Get Me](./get-me) — retrieve the currently authenticated user
- [Create User](./create-user) — add a new user
- [Update User](./update-user) — modify user details
