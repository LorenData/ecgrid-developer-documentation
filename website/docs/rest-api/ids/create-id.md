---
title: Create ID
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create ID

Creates a new ECGrid ID (Trading Partner ID) and assigns it to a mailbox.

## Endpoint

```http
POST /v2/ids
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | Yes | Must be a valid mailbox | Mailbox to assign this ECGrid ID to |
| `qualifier` | string | Yes | ISA qualifier code (e.g. `"01"`, `"ZZ"`) | EDI ISA-05/ISA-07 qualifier |
| `id` | string | Yes | ISA ID value (e.g. `"PARTNER001"`) | EDI ISA-06/ISA-08 identifier |
| `description` | string | No | — | Human-readable label for this trading partner |
| `ediStandard` | string | No | See `EDIStandard` enum | EDI format standard; defaults to `X12` |
| `routingGroup` | string | No | See `RoutingGroup` enum | Routing tier; defaults to `ProductionA` |

```json
{
  "mailboxId": 1001,
  "qualifier": "01",
  "id": "PARTNER001",
  "description": "Acme Corp Production",
  "ediStandard": "X12",
  "routingGroup": "ProductionA"
}
```

## Response

Returns the newly created `ECGridIDInfo` object.

```json
{
  "success": true,
  "data": {
    "ecGridId": 123456,
    "mailboxId": 1001,
    "networkId": 42,
    "qualifier": "01",
    "id": "PARTNER001",
    "description": "Acme Corp Production",
    "status": "Active",
    "routingGroup": "ProductionA",
    "ediStandard": "X12"
  }
}
```

## ENUMs

See [Enums reference](../../appendix/enums) for full details on `EDIStandard` and `RoutingGroup`.

### EDIStandard (common values)

| Value | Description |
|---|---|
| `X12` | ANSI X12 (most common in North America) |
| `EDIFACT` | UN/EDIFACT |
| `XML` | XML payload |
| `Binary` | Binary/unstructured file |

### RoutingGroup (common values)

| Value | Description |
|---|---|
| `ProductionA` | Primary production routing tier |
| `ProductionB` | Secondary production routing tier |
| `Test` | Test/development routing |
| `ManagedFileTransfer` | MFT routing group |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/ids" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 1001, "qualifier": "01", "id": "PARTNER001", "description": "Acme Corp Production", "ediStandard": "X12", "routingGroup": "ProductionA" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — create a new ECGrid ID and assign it to a mailbox
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    mailboxId = 1001,
    qualifier = "01",
    id = "PARTNER001",
    description = "Acme Corp Production",
    ediStandard = "X12",
    routingGroup = "ProductionA"
};

var response = await client.PostAsJsonAsync("https://rest.ecgrid.io/v2/ids", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ECGridIDInfo>>();
Console.WriteLine($"Created ECGrid ID: {result!.Data.EcGridId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 1001, \"qualifier\": \"01\", \"id\": \"PARTNER001\", \"description\": \"Acme Corp Production\", \"ediStandard\": \"X12\", \"routingGroup\": \"ProductionA\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids"))
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
const url = 'https://rest.ecgrid.io/v2/ids';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 1001, "qualifier": "01", "id": "PARTNER001", "description": "Acme Corp Production", "ediStandard": "X12", "routingGroup": "ProductionA" }),
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
url = "https://rest.ecgrid.io/v2/ids"

response = requests.post(
    url,
    json={ "mailboxId": 1001, "qualifier": "01", "id": "PARTNER001", "description": "Acme Corp Production", "ediStandard": "X12", "routingGroup": "ProductionA" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Update ID](update-id)
- [Delete ID](delete-id)
- [Create Partner (Interconnect)](../partners/create-partner)
