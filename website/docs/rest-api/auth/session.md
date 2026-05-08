---
title: Session
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST Auth session endpoint page created - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Session

Retrieve information about the currently authenticated session, including the user identity, network and mailbox context, and token expiry.

## Endpoint

```http
POST /v2/auth/session
```

## Request Body

No request body is required. Session details are resolved from the `Authorization` or `X-API-Key` header.

## Response

Returns the session context for the currently authenticated principal.

```json
{
  "success": true,
  "data": {
    "userId": 4821,
    "login": "jsmith@example.com",
    "networkId": 1,
    "mailboxId": 101,
    "authLevel": "MailboxAdmin",
    "expiresAt": "2026-05-07T18:30:00Z"
  },
  "errorCode": "",
  "message": ""
}
```

| Field | Type | Description |
|---|---|---|
| `userId` | integer | Internal ECGrid user ID |
| `login` | string | Username / login identifier |
| `networkId` | integer | ECGrid network ID the user belongs to |
| `mailboxId` | integer | Primary mailbox ID associated with the session |
| `authLevel` | string | Current authorization level — see `AuthLevel` ENUM below |
| `expiresAt` | datetime (ISO 8601) | UTC expiry time of the current token or session |

## ENUMs

### AuthLevel

| Value | Description |
|---|---|
| `NoChange` | No change to current level |
| `Root` | System root access |
| `TechOps` | Technical operations |
| `NetOps` | Network operations |
| `NetworkAdmin` | Full network administration |
| `NetworkUser` | Standard network user |
| `MailboxAdmin` | Full mailbox administration |
| `MailboxUser` | Standard mailbox user |
| `TPUser` | Trading partner user |
| `General` | General read-only access |

See [Appendix — ENUMs](../../appendix/enums.md) for the full `AuthLevel` reference.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/auth/session" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "success": true, "data": { "userId": 4821, "login": "jsmith@example.com", "networkId": 1, "mailboxId": 101, "authLevel": "MailboxAdmin", "expiresAt": "2026-05-07T18:30:00Z" }, "errorCode": "", "message": "" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve and inspect the current session
using System.Net.Http.Json;

/// <summary>
/// Fetches the current session details to verify authentication and check the auth level.
/// </summary>
async Task<SessionData?> GetSessionAsync(HttpClient httpClient)
{
    var response = await httpClient.PostAsync(
        "https://rest.ecgrid.io/v2/auth/session",
        content: null);

    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<SessionData>>();
    return result?.Data;
}

record SessionData(
    int UserId,
    string Login,
    int NetworkId,
    int MailboxId,
    string AuthLevel,
    DateTime ExpiresAt);

record ApiResponse<T>(bool Success, T? Data, string ErrorCode, string Message);
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"success\": true, \"data\": { \"userId\": 4821, \"login\": \"jsmith@example.com\", \"networkId\": 1, \"mailboxId\": 101, \"authLevel\": \"MailboxAdmin\", \"expiresAt\": \"2026-05-07T18:30:00Z\" }, \"errorCode\": \"\", \"message\": \"\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/session"))
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
const url = 'https://rest.ecgrid.io/v2/auth/session';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "success": true, "data": { "userId": 4821, "login": "jsmith@example.com", "networkId": 1, "mailboxId": 101, "authLevel": "MailboxAdmin", "expiresAt": "2026-05-07T18:30:00Z" }, "errorCode": "", "message": "" }),
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
url = "https://rest.ecgrid.io/v2/auth/session"

response = requests.post(
    url,
    json={ "success": true, "data": { "userId": 4821, "login": "jsmith@example.com", "networkId": 1, "mailboxId": 101, "authLevel": "MailboxAdmin", "expiresAt": "2026-05-07T18:30:00Z" }, "errorCode": "", "message": "" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Login](./login.md) — obtain a session token
- [Refresh Token](./refresh-token.md) — extend the session before `expiresAt`
- [Logout](./logout.md) — terminate the current session
- [Appendix — ENUMs](../../appendix/enums.md)
