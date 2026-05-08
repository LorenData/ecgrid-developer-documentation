---
title: Get Network
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created GET /v2/networks/{id} reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Network

Retrieves detailed information for a single ECGrid network by its numeric ID.

## Endpoint

```http
GET /v2/networks/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | Unique numeric identifier of the network |

## Response

Returns a `NetworkIDInfo` object for the requested network.

```json
{
  "success": true,
  "data": {
    "networkId": 1001,
    "uniqueId": "MYNETWORK",
    "companyName": "Acme Corporation",
    "status": "Active",
    "created": "2020-03-15T08:00:00Z",
    "modified": "2024-11-01T14:22:10Z"
  },
  "errorCode": null,
  "message": null
}
```

## ENUMs

### Status

The `status` field uses the `Status` enum. See the full value table in [Appendix: ENUMs](../../appendix/enums#status).

| Value | Description |
|---|---|
| `Development` | Account is in development/testing |
| `Active` | Account is live and operational |
| `Preproduction` | Staging state before go-live |
| `Suspended` | Temporarily disabled |
| `Terminated` | Permanently closed |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/networks/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve a network by ID
using System.Net.Http.Headers;

var networkId = 1001;
var request = new HttpRequestMessage(HttpMethod.Get, $"https://rest.ecgrid.io/v2/networks/{networkId}");
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<NetworkIdInfo>>();
Console.WriteLine($"Network: {result?.Data?.CompanyName} — Status: {result?.Data?.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/networks/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/networks/${id}`;

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
url = f"https://rest.ecgrid.io/v2/networks/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Networks](./list-networks)
- [Update Network](./update-network)
- [Appendix: ENUMs](../../appendix/enums)
