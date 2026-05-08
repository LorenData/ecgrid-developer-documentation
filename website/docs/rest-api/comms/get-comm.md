---
title: Get Comm
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Get Comm REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Comm

Retrieves the details of a specific communication channel (Comm) by its unique ID.

## Endpoint

```http
GET /v2/comms/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | Unique identifier of the communication channel |

## Response

Returns the full `CommIDInfo` object for the specified communication channel.

```json
{
  "success": true,
  "data": {
    "commId": 5001,
    "mailboxId": 101,
    "commType": "as2",
    "identifier": "MYCOMPANY-AS2",
    "status": "Active",
    "useType": "Production",
    "privateKeyRequired": true,
    "withCerts": true
  }
}
```

## ENUMs

This endpoint returns values from the `NetworkGatewayCommChannel`, `Status`, and `UseType` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/comms/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve a communication channel by ID
using var response = await httpClient.GetAsync(
    $"https://rest.ecgrid.io/v2/comms/{commId}");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Comm {result.Data.CommId}: Type={result.Data.CommType}, Identifier={result.Data.Identifier}, Status={result.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/comms/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/comms/${id}`;

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
id = 0  # replace with actual id
url = f"https://rest.ecgrid.io/v2/comms/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Find Comm](./find-comm)
- [List Comms](./list-comms)
- [Create Comm](./create-comm)
- [Update Comm](./update-comm)
- [ENUMs Reference](../../appendix/enums)
