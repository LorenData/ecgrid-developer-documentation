---
title: List Users
sidebar_position: 10
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - List Users documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Users

Returns a paginated list of users filtered by network, mailbox, auth level, and status.

## Endpoint

```http
POST /v2/users/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `networkId` | integer | No | — | Filter by network ID |
| `mailboxId` | integer | No | — | Filter by mailbox ID |
| `authLevel` | AuthLevel | No | — | Filter by user permission level |
| `status` | Status | No | — | Filter by user lifecycle status |
| `pageNo` | integer | No | Defaults to 1 | Page number for pagination |
| `recordsPerPage` | integer | No | Defaults to 25 | Number of results per page |

```json
{
  "networkId": 1,
  "mailboxId": 101,
  "authLevel": "MailboxUser",
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 25
}
```

## Response

Returns a paginated array of `UserIDInfo` objects matching the filter criteria.

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
      "authLevel": "MailboxUser",
      "status": "Active",
      "created": "2024-03-15T10:22:00Z"
    },
    {
      "userId": 1043,
      "login": "ajones",
      "email": "ajones@example.com",
      "firstName": "Alice",
      "lastName": "Jones",
      "networkId": 1,
      "mailboxId": 101,
      "authLevel": "MailboxUser",
      "status": "Active",
      "created": "2024-04-01T08:00:00Z"
    }
  ]
}
```

## ENUMs

This endpoint uses the following ENUMs in its request and response. See [Appendix: ENUMs](../../appendix/enums) for full value lists.

- `AuthLevel` — filter and display user permission levels
- `Status` — filter by user lifecycle state (e.g., `Active`, `Suspended`, `Terminated`)

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "networkId": 1, "mailboxId": 101, "authLevel": "MailboxUser", "status": "Active", "pageNo": 1, "recordsPerPage": 25 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — List users with optional filters using IHttpClientFactory
public async Task<List<UserIdInfo>?> ListUsersAsync(
    IHttpClientFactory httpClientFactory,
    int? networkId = null,
    int? mailboxId = null,
    string? authLevel = null,
    string? status = "Active",
    int pageNo = 1,
    int recordsPerPage = 25)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new
    {
        networkId,
        mailboxId,
        authLevel,
        status,
        pageNo,
        recordsPerPage
    };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/list",
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

String body = "{ \"networkId\": 1, \"mailboxId\": 101, \"authLevel\": \"MailboxUser\", \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 25 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/list"))
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
const url = 'https://rest.ecgrid.io/v2/users/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "networkId": 1, "mailboxId": 101, "authLevel": "MailboxUser", "status": "Active", "pageNo": 1, "recordsPerPage": 25 }),
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
url = "https://rest.ecgrid.io/v2/users/list"

response = requests.post(
    url,
    json={ "networkId": 1, "mailboxId": 101, "authLevel": "MailboxUser", "status": "Active", "pageNo": 1, "recordsPerPage": 25 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get User](./get-user) — retrieve a single user by ID
- [Get User by Name](./get-by-name) — search by login name
- [Set Role](./set-role) — change a user's AuthLevel
- [Terminate User](./terminate-user) — permanently remove a user account
