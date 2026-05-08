---
title: Update ID
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create PUT /v2/ids/{id} REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update ID

Updates the description, status, or EDI standard for an existing ECGrid ID.

## Endpoint

```http
PUT /v2/ids/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | The numeric ECGrid ID to update |

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `description` | string | No | — | Updated human-readable label |
| `status` | string | No | See `Status` enum | Lifecycle status of the ID |
| `ediStandard` | string | No | See `EDIStandard` enum | EDI format standard |

```json
{
  "description": "Acme Corp Production (updated)",
  "status": "Active",
  "ediStandard": "X12"
}
```

## Response

Returns the updated `ECGridIDInfo` object.

```json
{
  "success": true,
  "data": {
    "ecGridId": 123456,
    "mailboxId": 1001,
    "networkId": 42,
    "qualifier": "01",
    "id": "PARTNER001",
    "description": "Acme Corp Production (updated)",
    "status": "Active",
    "routingGroup": "ProductionA",
    "ediStandard": "X12"
  }
}
```

## ENUMs

See [Enums reference](../../appendix/enums) for full details on `Status` and `EDIStandard`.

### Status

| Value | Description |
|---|---|
| `Development` | ID is in development/testing phase |
| `Active` | ID is live and routing EDI traffic |
| `Preproduction` | ID is staged but not yet live |
| `Suspended` | ID is temporarily disabled |
| `Terminated` | ID has been permanently deactivated |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X PUT "https://rest.ecgrid.io/v2/ids/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "description": "Acme Corp Production (updated)", "status": "Active", "ediStandard": "X12" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — update description and status for an existing ECGrid ID
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    description = "Acme Corp Production (updated)",
    status = "Active",
    ediStandard = "X12"
};

var response = await client.PutAsJsonAsync(
    $"https://rest.ecgrid.io/v2/ids/{ecGridId}", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ECGridIDInfo>>();
Console.WriteLine($"Updated: {result!.Data.Description}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

String body = "{ \"description\": \"Acme Corp Production (updated)\", \"status\": \"Active\", \"ediStandard\": \"X12\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/ids/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/ids/${id}`;

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "description": "Acme Corp Production (updated)", "status": "Active", "ediStandard": "X12" }),
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
url = f"https://rest.ecgrid.io/v2/ids/{id}"

response = requests.put(
    url,
    json={ "description": "Acme Corp Production (updated)", "status": "Active", "ediStandard": "X12" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Create ID](create-id)
- [Delete ID](delete-id)
- [Update Description](update-description)
