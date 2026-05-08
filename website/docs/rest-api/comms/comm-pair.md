---
title: Comm Pair
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Comm Pair REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Comm Pair

Returns the communication path between two ECGrid IDs, showing which Comm channels are used for routing EDI traffic from one trading partner to another.

## Endpoint

```http
POST /v2/comms/pair
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridIdFrom` | integer | Yes | Must be a valid ECGrid ID | The source ECGrid ID (sender) |
| `ecGridIdTo` | integer | Yes | Must be a valid ECGrid ID | The destination ECGrid ID (receiver) |

```json
{
  "ecGridIdFrom": 100001,
  "ecGridIdTo": 200002
}
```

## Response

Returns an array of `CommIDInfo` objects representing the communication path between the two ECGrid IDs.

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
    },
    {
      "commId": 5099,
      "mailboxId": 202,
      "commType": "as2",
      "identifier": "PARTNER-AS2",
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
curl -X POST "https://rest.ecgrid.io/v2/comms/pair" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridIdFrom": 100001, "ecGridIdTo": 200002 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Look up the communication path between two trading partners
var request = new
{
    ecGridIdFrom = 100001,
    ecGridIdTo = 200002
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/pair",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<CommIdInfo>>>();
Console.WriteLine($"Communication path has {result.Data.Count} channel(s):");

foreach (var comm in result.Data)
{
    Console.WriteLine($"  Comm {comm.CommId}: {comm.CommType} — {comm.Identifier}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridIdFrom\": 100001, \"ecGridIdTo\": 200002 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/pair"))
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
const url = 'https://rest.ecgrid.io/v2/comms/pair';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridIdFrom": 100001, "ecGridIdTo": 200002 }),
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
url = "https://rest.ecgrid.io/v2/comms/pair"

response = requests.post(
    url,
    json={ "ecGridIdFrom": 100001, "ecGridIdTo": 200002 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Set Pair](./set-pair)
- [Get Comm](./get-comm)
- [Find Comm](./find-comm)
- [List Comms](./list-comms)
