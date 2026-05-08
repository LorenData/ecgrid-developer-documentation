---
title: Find Comm
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Find Comm REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Find Comm

Searches for communication channels by identifier string, optionally filtered by channel type.

## Endpoint

```http
POST /v2/comms/find
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `identifier` | string | Yes | — | AS2 ID, FTP username, or other channel-specific identifier to search for |
| `commType` | NetworkGatewayCommChannel | No | See ENUMs | Narrow results to a specific communication channel type |

```json
{
  "identifier": "MYCOMPANY-AS2",
  "commType": "as2"
}
```

## Response

Returns an array of matching `CommIDInfo` objects.

```json
{
  "success": true,
  "data": [
    {
      "commId": 5001,
      "mailboxId": 101,
      "commType": "as2",
      "identifier": "MYCOMPANY-AS2",
      "status": "Active",
      "useType": "Production",
      "privateKeyRequired": true,
      "withCerts": true
    }
  ]
}
```

## ENUMs

This endpoint uses the `NetworkGatewayCommChannel` ENUM. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/comms/find" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "identifier": "MYCOMPANY-AS2", "commType": "as2" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Search for a comm channel by its AS2 identifier
var request = new
{
    identifier = "MYCOMPANY-AS2",
    commType = "as2"
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/find",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<CommIdInfo>>>();

foreach (var comm in result.Data)
{
    Console.WriteLine($"Found Comm {comm.CommId}: {comm.CommType} — {comm.Identifier} [{comm.Status}]");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"identifier\": \"MYCOMPANY-AS2\", \"commType\": \"as2\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/find"))
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
const url = 'https://rest.ecgrid.io/v2/comms/find';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "identifier": "MYCOMPANY-AS2", "commType": "as2" }),
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
url = "https://rest.ecgrid.io/v2/comms/find"

response = requests.post(
    url,
    json={ "identifier": "MYCOMPANY-AS2", "commType": "as2" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Comm](./get-comm)
- [List Comms](./list-comms)
- [Create Comm](./create-comm)
- [ENUMs Reference](../../appendix/enums)
