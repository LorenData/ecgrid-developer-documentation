---
title: Update User
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Update User documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update User

Updates profile information for an existing user account.

## Endpoint

```http
PUT /v2/users
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | integer | Yes | Must be an existing user | ID of the user to update |
| `email` | string | No | Valid email format | Updated email address |
| `firstName` | string | No | — | Updated first name |
| `lastName` | string | No | — | Updated last name |

```json
{
  "userId": 1042,
  "email": "john.smith@example.com",
  "firstName": "John",
  "lastName": "Smith"
}
```

## Response

Returns the updated `UserIDInfo` object reflecting the saved changes.

```json
{
  "success": true,
  "data": {
    "userId": 1042,
    "login": "jsmith",
    "email": "john.smith@example.com",
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

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X PUT "https://rest.ecgrid.io/v2/users" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 1042, "email": "john.smith@example.com", "firstName": "John", "lastName": "Smith" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Update user profile details using IHttpClientFactory
public async Task<UserIdInfo?> UpdateUserAsync(
    IHttpClientFactory httpClientFactory,
    int userId,
    string? email = null,
    string? firstName = null,
    string? lastName = null)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        userId,
        email,
        firstName,
        lastName
    };

    var response = await http.PutAsJsonAsync("https://rest.ecgrid.io/v2/users", requestBody);
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

String body = "{ \"userId\": 1042, \"email\": \"john.smith@example.com\", \"firstName\": \"John\", \"lastName\": \"Smith\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .PUT(HttpRequest.BodyPublishers.ofString(body))
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
const url = 'https://rest.ecgrid.io/v2/users';

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 1042, "email": "john.smith@example.com", "firstName": "John", "lastName": "Smith" }),
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
url = "https://rest.ecgrid.io/v2/users"

response = requests.put(
    url,
    json={ "userId": 1042, "email": "john.smith@example.com", "firstName": "John", "lastName": "Smith" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — retrieve current user details
- [Update Password](./update-password) — change the user's password
- [Set Role](./set-role) — update the user's AuthLevel
- [Set Network Mailbox](./set-network-mailbox) — change the user's network or mailbox context
- [Update Config](./update-config) — update advanced user configuration settings
