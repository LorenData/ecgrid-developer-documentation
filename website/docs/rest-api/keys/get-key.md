---
title: Get Key
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Keys / Get Key REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Key

Retrieves a specific API key record for a user by user ID.

## Endpoint

```http
POST /v2/keys/get-key
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | int | Yes | Must be a valid user ID | The ID of the user whose key should be retrieved |

```json
{
  "userId": 12345
}
```

## Response

Returns the key record associated with the specified user, including the key string and visibility level.

```json
{
  "success": true,
  "data": {
    "keyId": 9001,
    "userId": 12345,
    "key": "ek_live_abc123xyz789...",
    "visibility": "Private",
    "created": "2025-01-15T10:30:00Z"
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `keyId` | int | Unique identifier for this key record |
| `userId` | int | The user this key belongs to |
| `key` | string | The API key string used for authentication |
| `visibility` | string | Scope of the key — see `KeyVisibility` enum |
| `created` | datetime | UTC timestamp when the key was created |

## ENUMs

### KeyVisibility

See [KeyVisibility in the Appendix](../../appendix/enums#keyvisibility) for the full list of values.

| Value | Description |
|---|---|
| `Private` | Key is accessible only to the owning user |
| `Shared` | Key is shared within the mailbox or network |
| `Public` | Key is publicly accessible |
| `Session` | Key is tied to a single session |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/keys/get-key" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 12345 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve an API key for a given user
using System.Net.Http.Json;

var request = new { userId = 12345 };

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/keys/get-key",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<KeyInfo>>();
Console.WriteLine($"Key: {result?.Data?.Key}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"userId\": 12345 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/keys/get-key"))
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
const url = 'https://rest.ecgrid.io/v2/keys/get-key';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 12345 }),
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
url = "https://rest.ecgrid.io/v2/keys/get-key"

response = requests.post(
    url,
    json={ "userId": 12345 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Keys](./list-keys)
- [Create Key](./create-key)
- [Delete Key](./delete-key)
- [Get API Key (Users)](../users/get-api-key)
- [KeyVisibility Enum](../../appendix/enums#keyvisibility)
