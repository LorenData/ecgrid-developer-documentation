---
title: Confirm Download
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/confirm-download.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Confirm Download

Acknowledge that an inbound parcel has been successfully received and saved.

## Endpoint

```http
POST /v2/parcels/confirm
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `parcelId` | long | Yes | | Unique identifier of the parcel to confirm |

:::caution Required After Every Download
This call must be made after every successful [Download Parcel](./download-parcel) operation. Without confirmation, ECGrid considers the parcel undelivered and will re-deliver it on the next polling cycle, resulting in duplicate processing.
:::

```json
{
  "parcelId": 987654321
}
```

## Response

Returns a success boolean indicating the parcel has been marked as transferred.

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
curl -X POST "https://rest.ecgrid.io/v2/parcels/confirm" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "parcelId": 987654321 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — confirm delivery after saving the downloaded EDI file
using System.Net.Http.Json;

var confirmRequest = new { parcelId = 987654321L };

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/confirm",
    confirmRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result!.Data)
{
    Console.WriteLine("Parcel confirmed — marked as InBoxTransferred.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"parcelId\": 987654321 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/confirm"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/confirm';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "parcelId": 987654321 }),
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
url = "https://rest.ecgrid.io/v2/parcels/confirm"

response = requests.post(
    url,
    json={ "parcelId": 987654321 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Download Parcel](./download-parcel) — download the EDI content before confirming
- [Reset to Inbox](./reset-to-inbox) — revert a confirmed parcel back to InBoxReady if needed
- [Pending Inbox List](./pending-inbox-list) — list parcels awaiting download and confirmation
