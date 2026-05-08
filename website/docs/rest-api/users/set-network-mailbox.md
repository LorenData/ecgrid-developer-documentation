---
title: Set Network Mailbox
sidebar_position: 15
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Set Network Mailbox documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Set Network Mailbox

Changes the network and mailbox context associated with a user account.

## Endpoint

```http
POST /v2/users/set-network-mailbox
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | integer | Yes | Must be an existing user | ID of the user to update |
| `networkId` | integer | No | — | The network ID to associate with the user |
| `mailboxId` | integer | No | — | The mailbox ID to associate with the user |

```json
{
  "userId": 1042,
  "networkId": 2,
  "mailboxId": 205
}
```

## Response

Returns the updated `UserIDInfo` object reflecting the new network and mailbox association.

```json
{
  "success": true,
  "data": {
    "userId": 1042,
    "login": "jsmith",
    "email": "jsmith@example.com",
    "firstName": "John",
    "lastName": "Smith",
    "networkId": 2,
    "mailboxId": 205,
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
curl -X POST "https://rest.ecgrid.io/v2/users/set-network-mailbox" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 1042, "networkId": 2, "mailboxId": 205 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Reassign a user to a different network or mailbox using IHttpClientFactory
public async Task<UserIdInfo?> SetNetworkMailboxAsync(
    IHttpClientFactory httpClientFactory,
    int userId,
    int? networkId = null,
    int? mailboxId = null)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        userId,
        networkId,
        mailboxId
    };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/set-network-mailbox",
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

String body = "{ \"userId\": 1042, \"networkId\": 2, \"mailboxId\": 205 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/set-network-mailbox"))
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
const url = 'https://rest.ecgrid.io/v2/users/set-network-mailbox';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 1042, "networkId": 2, "mailboxId": 205 }),
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
url = "https://rest.ecgrid.io/v2/users/set-network-mailbox"

response = requests.post(
    url,
    json={ "userId": 1042, "networkId": 2, "mailboxId": 205 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — verify current network and mailbox before making changes
- [Set Role](./set-role) — update the user's permission level alongside the context change
- [Update User](./update-user) — update other profile fields
