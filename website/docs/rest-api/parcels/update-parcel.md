---
title: Update Parcel
sidebar_position: 11
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/update-parcel.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Parcel

Update the status or metadata of an existing parcel record.

## Endpoint

```http
POST /v2/parcels/update
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `parcelId` | long | Yes | | Unique identifier of the parcel to update |
| `status` | ParcelStatus | No | | New status to assign to the parcel |

```json
{
  "parcelId": 987654321,
  "status": "InBoxReady"
}
```

## Response

Returns the updated `ParcelIDInfo` object reflecting the new state.

```json
{
  "success": true,
  "data": {
    "parcelId": 987654321,
    "mailboxId": 1001,
    "networkId": 42,
    "fileName": "invoice_batch_20260507.edi",
    "bytes": 14872,
    "status": "InBoxReady",
    "ecGridIdFrom": 112233,
    "ecGridIdTo": 445566,
    "created": "2026-05-07T08:00:00Z",
    "modified": "2026-05-07T10:30:00Z"
  }
}
```

## ENUMs

### ParcelStatus

See [ParcelStatus in Appendix — ENUMs](../../appendix/enums) for the full list of parcel status values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/update" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "parcelId": 987654321, "status": "InBoxReady" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — update the status of a parcel
using System.Net.Http.Json;

var updateRequest = new
{
    parcelId = 987654321L,
    status = "InBoxReady"
};

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/update",
    updateRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ParcelIdInfo>>();
Console.WriteLine($"Parcel {result!.Data.ParcelId} updated — Status: {result.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"parcelId\": 987654321, \"status\": \"InBoxReady\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/update"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/update';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "parcelId": 987654321, "status": "InBoxReady" }),
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
url = "https://rest.ecgrid.io/v2/parcels/update"

response = requests.post(
    url,
    json={ "parcelId": 987654321, "status": "InBoxReady" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Parcel](./get-parcel) — retrieve current parcel metadata before updating
- [Reset to Inbox](./reset-to-inbox) — dedicated endpoint to reset a confirmed parcel to InBoxReady
- [Cancel Parcel](./cancel-parcel) — cancel an outbound parcel before delivery
