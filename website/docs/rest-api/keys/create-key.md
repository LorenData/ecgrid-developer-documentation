---
title: Create Key
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Keys / Create Key REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Key

Generates a new API key for the specified user with the given visibility level.

:::tip Store the Key Immediately
The full key string is only returned once at creation time. Store it securely (such as in a secrets manager or environment variable) before discarding the response — it cannot be retrieved in full afterward.
:::

## Endpoint

```http
POST /v2/keys/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `userId` | int | Yes | Must be a valid user ID | The ID of the user for whom the key is being created |
| `visibility` | string | Yes | Must be a valid `KeyVisibility` value | Determines the scope in which this key can be used |

```json
{
  "userId": 12345,
  "visibility": "Private"
}
```

## Response

Returns the full key record, including the newly generated key string.

```json
{
  "success": true,
  "data": {
    "keyId": 9003,
    "userId": 12345,
    "key": "ek_live_newkey987zyxwvu...",
    "visibility": "Private",
    "created": "2026-05-07T08:45:00Z"
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `keyId` | int | Unique identifier for the new key record |
| `userId` | int | The user this key belongs to |
| `key` | string | The newly generated API key string — save this now |
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
curl -X POST "https://rest.ecgrid.io/v2/keys/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "userId": 12345, "visibility": "Private" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Create a new Private API key for a user and persist it to configuration
using System.Net.Http.Json;

var request = new
{
    userId = 12345,
    visibility = "Private"
};

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/keys/create",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<KeyInfo>>();

// Store result?.Data?.Key in a secrets manager or environment variable immediately.
// It will not be returned in full by any subsequent API call.
Console.WriteLine($"New key created — KeyId: {result?.Data?.KeyId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"userId\": 12345, \"visibility\": \"Private\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/keys/create"))
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
const url = 'https://rest.ecgrid.io/v2/keys/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "userId": 12345, "visibility": "Private" }),
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
url = "https://rest.ecgrid.io/v2/keys/create"

response = requests.post(
    url,
    json={ "userId": 12345, "visibility": "Private" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Key](./get-key)
- [List Keys](./list-keys)
- [Delete Key](./delete-key)
- [Generate API Key (Users)](../users/generate-api-key)
- [KeyVisibility Enum](../../appendix/enums#keyvisibility)
