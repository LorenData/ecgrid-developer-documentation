---
title: Set Pair
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Set Pair REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Set Pair

Sets or updates the preferred communication channel pairing between two ECGrid IDs, directing how EDI traffic is routed between them.

## Endpoint

```http
POST /v2/comms/set-pair
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridIdFrom` | integer | Yes | Must be a valid ECGrid ID | The source ECGrid ID (sender) |
| `ecGridIdTo` | integer | Yes | Must be a valid ECGrid ID | The destination ECGrid ID (receiver) |
| `commId` | integer | No | Must be a valid Comm ID | Preferred Comm channel to use for this pairing |

```json
{
  "ecGridIdFrom": 100001,
  "ecGridIdTo": 200002,
  "commId": 5001
}
```

## Response

Returns an updated array of `CommIDInfo` objects reflecting the new pairing.

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

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/comms/set-pair" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridIdFrom": 100001, "ecGridIdTo": 200002, "commId": 5001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Set the preferred comm channel between two trading partners
var request = new
{
    ecGridIdFrom = 100001,
    ecGridIdTo = 200002,
    commId = 5001
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/set-pair",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<CommIdInfo>>>();
Console.WriteLine($"Comm pair updated. Active channel: {result.Data.FirstOrDefault()?.Identifier}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridIdFrom\": 100001, \"ecGridIdTo\": 200002, \"commId\": 5001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/set-pair"))
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
const url = 'https://rest.ecgrid.io/v2/comms/set-pair';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridIdFrom": 100001, "ecGridIdTo": 200002, "commId": 5001 }),
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
url = "https://rest.ecgrid.io/v2/comms/set-pair"

response = requests.post(
    url,
    json={ "ecGridIdFrom": 100001, "ecGridIdTo": 200002, "commId": 5001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Comm Pair](./comm-pair)
- [Get Comm](./get-comm)
- [Create Comm](./create-comm)
- [Update Comm](./update-comm)
