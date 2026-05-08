---
title: Update Password
sidebar_position: 11
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Update Password documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Password

Sets a new password for a specified user account.

## Endpoint

```http
POST /v2/users/password
```

:::note
This is an administrative operation that requires `NetworkAdmin` or higher `AuthLevel`. Use [Generate Password](./generate-password) to create a compliant random password before calling this endpoint if needed.
:::

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | integer | Yes | Must be an existing user | ID of the user whose password to change |
| `newPassword` | string | Yes | See password pattern below | The new password to set |

**Password pattern:** `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

Must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.

```json
{
  "userId": 1042,
  "newPassword": "NewPassw0rd!"
}
```

## Response

Returns a boolean indicating whether the password was successfully updated.

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
curl -X POST "https://rest.ecgrid.io/v2/users/password" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 1042, "newPassword": "NewPassw0rd!" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Set a new password for a user using IHttpClientFactory
// Requires NetworkAdmin or higher auth level
public async Task<bool> UpdatePasswordAsync(
    IHttpClientFactory httpClientFactory,
    int userId,
    string newPassword)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        userId,
        newPassword
    };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/password",
        requestBody);
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

String body = "{ \"userId\": 1042, \"newPassword\": \"NewPassw0rd!\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/password"))
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
const url = 'https://rest.ecgrid.io/v2/users/password';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 1042, "newPassword": "NewPassw0rd!" }),
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
url = "https://rest.ecgrid.io/v2/users/password"

response = requests.post(
    url,
    json={ "userId": 1042, "newPassword": "NewPassw0rd!" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Generate Password](./generate-password) — create a random password that meets complexity requirements
- [Reset Sessions](./reset-sessions) — invalidate active sessions after a password change
- [Update User](./update-user) — update other user profile fields
