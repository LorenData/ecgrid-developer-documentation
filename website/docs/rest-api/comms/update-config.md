---
title: Update Comm Config
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Update Comm Config REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Comm Config

Updates the extended configuration settings of a communication channel, such as connection parameters, authentication details, and protocol-specific options.

## Endpoint

```http
PUT /v2/comms/update-config
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be an existing Comm ID | Unique identifier of the communication channel to configure |

Additional configuration fields vary by `commType`. Submit only the fields applicable to the channel's protocol. Omitted fields retain their current values.

```json
{
  "commId": 5001
}
```

## Response

Returns a success boolean confirming the configuration was updated.

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
curl -X PUT "https://rest.ecgrid.io/v2/comms/update-config" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Update comm configuration settings
// Include only the fields that need to change; omitted fields are unchanged
var request = new
{
    commId = 5001
    // Add protocol-specific configuration fields as needed
};

using var response = await httpClient.PutAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/update-config",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();

if (result.Data)
{
    Console.WriteLine($"Comm {5001} configuration updated successfully.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/update-config"))
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
const url = 'https://rest.ecgrid.io/v2/comms/update-config';

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001 }),
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
url = "https://rest.ecgrid.io/v2/comms/update-config"

response = requests.put(
    url,
    json={ "commId": 5001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Comm](./get-comm)
- [Create Comm](./create-comm)
- [Update Comm](./update-comm)
- [Add Private Certificate](../certificates/add-private)
- [Add Public Certificate](../certificates/add-public)
