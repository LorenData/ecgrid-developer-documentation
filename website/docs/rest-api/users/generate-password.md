---
title: Generate Password
sidebar_position: 12
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API Users - Generate Password documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Generate Password

Generates a random password that meets ECGrid complexity requirements, ready to use with [Update Password](./update-password) or [Create User](./create-user).

## Endpoint

```http
POST /v2/users/generate-password
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `length` | integer | No | Defaults to `12` | Desired length of the generated password |

```json
{
  "length": 16
}
```

## Response

Returns the generated password string. The returned password is guaranteed to satisfy the ECGrid password complexity pattern:

`^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

```json
{
  "success": true,
  "data": "Xk7#mQpL2rNv!dYw"
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/users/generate-password" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "length": 16 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Generate a compliant random password using IHttpClientFactory
public async Task<string?> GeneratePasswordAsync(
    IHttpClientFactory httpClientFactory,
    int length = 12)
{
    var http = httpClientFactory.CreateClient("ECGridRest");

    var requestBody = new { length };

    var response = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/users/generate-password",
        requestBody);
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<string>>();
    return result?.Data;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"length\": 16 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/generate-password"))
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
const url = 'https://rest.ecgrid.io/v2/users/generate-password';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "length": 16 }),
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
url = "https://rest.ecgrid.io/v2/users/generate-password"

response = requests.post(
    url,
    json={ "length": 16 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Update Password](./update-password) — apply the generated password to a user account
- [Create User](./create-user) — supply the generated password when creating a new user
