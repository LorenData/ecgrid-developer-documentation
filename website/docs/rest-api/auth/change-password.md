---
title: Change Password
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST Auth change-password endpoint page created - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Change Password

Change the authenticated user's account password. Both the current password and the new password are required.

## Endpoint

```http
PUT /v2/auth/password
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `currentPassword` | string | Yes | Must match the current password on file | The user's existing password |
| `newPassword` | string | Yes | See password policy below | The desired new password |

**Password policy:** `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

The new password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.

```json
{
  "currentPassword": "OldP@ssword1",
  "newPassword": "NewP@ssword2!"
}
```

## Response

Returns a success confirmation when the password has been updated.

```json
{
  "success": true,
  "data": null,
  "errorCode": "",
  "message": "Password updated successfully."
}
```

:::caution Active sessions
Changing your password does not automatically invalidate existing active tokens. If you suspect a credential compromise, call [Logout](./logout.md) after changing the password to terminate the current session, and consider resetting all sessions via [Reset Sessions](../users/reset-sessions.md).
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X PUT "https://rest.ecgrid.io/v2/auth/password" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "currentPassword": "OldP@ssword1", "newPassword": "NewP@ssword2!" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Change the authenticated user's password
using System.Net.Http.Json;

/// <summary>
/// Changes the current user's password. Loads credentials from configuration,
/// never from hardcoded strings.
/// </summary>
async Task ChangePasswordAsync(HttpClient httpClient, string currentPassword, string newPassword)
{
    var response = await httpClient.PutAsJsonAsync(
        "https://rest.ecgrid.io/v2/auth/password",
        new { currentPassword, newPassword });

    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<object>>();

    if (result?.Success != true)
    {
        throw new InvalidOperationException(
            $"Password change failed: {result?.Message} ({result?.ErrorCode})");
    }
}

record ApiResponse<T>(bool Success, T? Data, string ErrorCode, string Message);
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"currentPassword\": \"OldP@ssword1\", \"newPassword\": \"NewP@ssword2!\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/password"))
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
const url = 'https://rest.ecgrid.io/v2/auth/password';

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "currentPassword": "OldP@ssword1", "newPassword": "NewP@ssword2!" }),
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
url = "https://rest.ecgrid.io/v2/auth/password"

response = requests.put(
    url,
    json={ "currentPassword": "OldP@ssword1", "newPassword": "NewP@ssword2!" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Login](./login.md) — authenticate after a password change
- [Logout](./logout.md) — invalidate the current session
- [Generate Password](../users/generate-password.md) — generate a compliant password for a user
- [Reset Sessions](../users/reset-sessions.md) — force-terminate all active sessions for a user
