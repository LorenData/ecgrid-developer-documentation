---
title: Create User
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Create User documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create User

Creates a new user account within the specified network and mailbox context.

## Endpoint

```http
POST /v2/users
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `login` | string | Yes | Unique within the network | Username for authentication |
| `password` | string | Yes | See password pattern below | Initial password for the user |
| `email` | string | Yes | Valid email format | User's email address |
| `firstName` | string | No | — | User's first name |
| `lastName` | string | No | — | User's last name |
| `networkId` | integer | No | Defaults to caller's network | Network to create the user under |
| `mailboxId` | integer | No | Defaults to caller's mailbox | Mailbox to associate with the user |
| `authLevel` | AuthLevel | No | Defaults to `MailboxUser` | Permission level to assign |

**Password pattern:** `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

Must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.

```json
{
  "login": "jsmith",
  "password": "Passw0rd!",
  "email": "jsmith@example.com",
  "firstName": "John",
  "lastName": "Smith",
  "networkId": 1,
  "mailboxId": 101,
  "authLevel": "MailboxAdmin"
}
```

## Response

Returns the newly created `UserIDInfo` object.

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
    "created": "2026-05-07T14:30:00Z"
  }
}
```

## ENUMs

This endpoint uses the following ENUM in its request body. See [Appendix: ENUMs](../../appendix/enums) for full value lists.

- `AuthLevel` — permission level to assign to the new user

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "login": "jsmith", "password": "Passw0rd!", "email": "jsmith@example.com", "firstName": "John", "lastName": "Smith", "networkId": 1, "mailboxId": 101, "authLevel": "MailboxAdmin" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Create a new user using IHttpClientFactory
public async Task<UserIdInfo?> CreateUserAsync(
    IHttpClientFactory httpClientFactory,
    string login,
    string password,
    string email,
    string firstName,
    string lastName,
    int networkId,
    int mailboxId,
    string authLevel = "MailboxUser")
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        login,
        password,
        email,
        firstName,
        lastName,
        networkId,
        mailboxId,
        authLevel
    };

    var response = await http.PostAsJsonAsync("https://rest.ecgrid.io/v2/users", requestBody);
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

String body = "{ \"login\": \"jsmith\", \"password\": \"Passw0rd!\", \"email\": \"jsmith@example.com\", \"firstName\": \"John\", \"lastName\": \"Smith\", \"networkId\": 1, \"mailboxId\": 101, \"authLevel\": \"MailboxAdmin\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users"))
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
const url = 'https://rest.ecgrid.io/v2/users';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "login": "jsmith", "password": "Passw0rd!", "email": "jsmith@example.com", "firstName": "John", "lastName": "Smith", "networkId": 1, "mailboxId": 101, "authLevel": "MailboxAdmin" }),
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

response = requests.post(
    url,
    json={ "login": "jsmith", "password": "Passw0rd!", "email": "jsmith@example.com", "firstName": "John", "lastName": "Smith", "networkId": 1, "mailboxId": 101, "authLevel": "MailboxAdmin" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — retrieve user details after creation
- [Update User](./update-user) — modify a user's information
- [Set Role](./set-role) — change a user's AuthLevel after creation
- [Update Password](./update-password) — change a user's password
