---
title: Delete Key
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Keys / Delete Key REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Delete Key

Permanently deletes an API key by its key ID.

:::caution Immediate Revocation
Deleting a key immediately invalidates it. Any integration, application, or automation using this key will be unable to authenticate as soon as the deletion completes. Ensure all dependent systems are updated before proceeding.
:::

## Endpoint

```http
DELETE /v2/keys
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `keyId` | int | Yes | Must be a valid, existing key ID | The ID of the key to permanently delete |

```json
{
  "keyId": 9001
}
```

## Response

Returns a boolean indicating whether the deletion was successful.

```json
{
  "success": true,
  "data": true
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `success` | bool | `true` if the key was deleted; `false` if the operation failed |
| `data` | bool | Mirrors the deletion result |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X DELETE "https://rest.ecgrid.io/v2/keys" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Delete an API key by ID using a DELETE request with a JSON body
using System.Net.Http.Json;

var request = new { keyId = 9001 };

// HttpClient does not support a body on DELETE by default — use a custom request message
var message = new HttpRequestMessage(HttpMethod.Delete, "https://rest.ecgrid.io/v2/keys")
{
    Content = JsonContent.Create(request)
};

var response = await httpClient.SendAsync(message);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();

if (result?.Data == true)
{
    Console.WriteLine("Key deleted successfully.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/keys"))
    .header("X-API-Key", apiKey)
    .DELETE()
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
const url = 'https://rest.ecgrid.io/v2/keys';

const response = await fetch(url, {
  method: 'DELETE',
  headers: { 'X-API-Key': apiKey },
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
url = "https://rest.ecgrid.io/v2/keys"

response = requests.delete(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Key](./get-key)
- [List Keys](./list-keys)
- [Create Key](./create-key)
- [KeyVisibility Enum](../../appendix/enums#keyvisibility)
