---
title: Version
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: REST Auth version endpoint page created - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Version

Returns the current ECGrid REST API version string. No authentication is required, making this endpoint useful for connectivity testing and health checks.

## Endpoint

```http
GET /v2/auth/version
```

:::info No authentication required
This endpoint does not require an `X-API-Key` or `Authorization` header. It is safe to call from any context to verify reachability of the API.
:::

## Response

Returns the API version as a string.

```json
{
  "success": true,
  "data": {
    "version": "2.6"
  },
  "errorCode": "",
  "message": ""
}
```

| Field | Type | Description |
|---|---|---|
| `version` | string | The current REST API version (e.g., `"2.6"`) |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/auth/version" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Verify API connectivity and retrieve the current version
using System.Net.Http.Json;

/// <summary>
/// Fetches the API version as a lightweight connectivity and health check.
/// No authentication header needed.
/// </summary>
async Task<string?> GetApiVersionAsync(HttpClient httpClient)
{
    var response = await httpClient.GetAsync(
        "https://rest.ecgrid.io/v2/auth/version");

    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<VersionData>>();
    return result?.Data?.Version;
}

record VersionData(string Version);
record ApiResponse<T>(bool Success, T? Data, string ErrorCode, string Message);
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/version"))
    .header("X-API-Key", apiKey)
    .GET()
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
const url = 'https://rest.ecgrid.io/v2/auth/version';

const response = await fetch(url, {
  method: 'GET',
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
url = "https://rest.ecgrid.io/v2/auth/version"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [REST API Overview](../overview.md) — full endpoint listing for v2.6
- [Login](./login.md) — authenticate to start a session
