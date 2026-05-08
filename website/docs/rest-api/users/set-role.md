---
title: Set Role
sidebar_position: 13
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Set Role documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Set Role

Updates the `AuthLevel` (permission role) for a specified user, optionally scoping the role to a specific network or mailbox.

:::caution
Elevating a user's `AuthLevel` grants them additional access to networks, mailboxes, and ECGrid IDs. The `Root` and `TechOps` roles provide the broadest system access and should be assigned only to fully trusted administrators. Confirm the correct User ID and intended role before calling this endpoint.
:::

## Endpoint

```http
POST /v2/users/role
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | integer | Yes | Must be an existing user | ID of the user whose role to change |
| `authLevel` | AuthLevel | Yes | — | The new permission level to assign |
| `networkId` | integer | No | — | Scope the role to this network |
| `mailboxId` | integer | No | — | Scope the role to this mailbox |

```json
{
  "userId": 1042,
  "authLevel": "NetworkAdmin",
  "networkId": 1
}
```

## Response

Returns the updated `UserIDInfo` object reflecting the new role.

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
    "authLevel": "NetworkAdmin",
    "status": "Active",
    "created": "2024-03-15T10:22:00Z"
  }
}
```

## ENUMs

This endpoint uses the following ENUM in its request body. See [Appendix: ENUMs](../../appendix/enums) for full value lists.

- `AuthLevel` — the permission level to assign, from highest to lowest: `Root`, `TechOps`, `NetOps`, `NetworkAdmin`, `NetworkUser`, `MailboxAdmin`, `MailboxUser`, `TPUser`, `General`

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users/role" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 1042, "authLevel": "NetworkAdmin", "networkId": 1 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Change a user's permission role using IHttpClientFactory
// Use sparingly for Root and TechOps — these roles have broad system access
public async Task<UserIdInfo?> SetRoleAsync(
    IHttpClientFactory httpClientFactory,
    int userId,
    string authLevel,
    int? networkId = null,
    int? mailboxId = null)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        userId,
        authLevel,
        networkId,
        mailboxId
    };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/role",
        requestBody);
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

String body = "{ \"userId\": 1042, \"authLevel\": \"NetworkAdmin\", \"networkId\": 1 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/role"))
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
const url = 'https://rest.ecgrid.io/v2/users/role';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 1042, "authLevel": "NetworkAdmin", "networkId": 1 }),
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
url = "https://rest.ecgrid.io/v2/users/role"

response = requests.post(
    url,
    json={ "userId": 1042, "authLevel": "NetworkAdmin", "networkId": 1 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — confirm the user's current role before making changes
- [List Users](./list-users) — filter users by AuthLevel to audit role assignments
- [Update User](./update-user) — update other profile fields without changing the role
