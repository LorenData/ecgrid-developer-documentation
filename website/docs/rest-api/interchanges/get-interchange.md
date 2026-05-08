---
title: Get Interchange
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of get-interchange REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Interchange

Retrieve the details of a single interchange by its unique ECGrid Interchange ID.

## Endpoint

```http
GET /v2/interchanges/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | The unique ECGrid Interchange ID. |

## Response

Returns an `InterchangeIDInfo` object containing the full details of the requested interchange.

```json
{
  "success": true,
  "data": {
    "interchangeId": 9870001,
    "parcelId": 5550001,
    "sender": "ACME_CORP",
    "receiver": "BUYER_INC",
    "standard": "X12",
    "documentType": "850",
    "status": "Active",
    "created": "2026-05-01T10:30:00Z"
  }
}
```

## ENUMs

### EDIStandard

| Value | Description |
|---|---|
| `X12` | ASC X12 (North American standard) |
| `EDIFACT` | UN/EDIFACT (international standard) |
| `TRADACOMS` | TRADACOMS (UK retail standard) |
| `VDA` | VDA (German automotive standard) |
| `XML` | XML-based EDI |
| `TXT` | Plain text |
| `PDF` | PDF document |
| `Binary` | Binary file |

### Status

| Value | Description |
|---|---|
| `Development` | In development / testing |
| `Active` | Actively in use |
| `Preproduction` | Pre-production stage |
| `Suspended` | Temporarily suspended |
| `Terminated` | Permanently terminated |

See [Enums Reference](../../appendix/enums) for full ENUM definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/interchanges/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve a single interchange record by ID
using var client = httpClientFactory.CreateClient("ECGrid");

var response = await client.GetAsync($"/v2/interchanges/{interchangeId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<InterchangeIdInfo>>();
Console.WriteLine($"Interchange {result.Data.InterchangeId}: {result.Data.DocumentType} — {result.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/interchanges/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/interchanges/${id}`;

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
url = f"https://rest.ecgrid.io/v2/interchanges/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Cancel Interchange](./cancel-interchange)
- [Get Interchange Manifest](./get-manifest)
- [Resend Interchange](./resend-interchange)
- [Inbox List](./inbox-list)
- [Outbox List](./outbox-list)
