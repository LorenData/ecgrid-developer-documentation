---
title: Get Status Lists
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Status Lists / Get Status Lists REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Status Lists

Returns the authoritative list of all valid status codes supported by the current API version, covering parcels, interchanges, and other tracked objects.

:::tip Cache This Response
Status code values are stable and rarely change between API versions. This response is safe to cache in your application for extended periods. Re-fetch it when upgrading to a new API version to detect any additions or changes.
:::

## Endpoint

```http
GET /v2/status-lists
```

## Response

Returns an object containing named arrays, each holding the valid status codes for a specific object type.

```json
{
  "success": true,
  "data": {
    "parcelStatuses": [
      { "code": "InBoxReady", "description": "Parcel is in the inbox and ready for download" },
      { "code": "InBoxTransferred", "description": "Parcel has been transferred to the recipient" },
      { "code": "as2Receive", "description": "Parcel received via AS2" },
      { "code": "as2Sent", "description": "Parcel sent via AS2" },
      { "code": "ftpReceived", "description": "Parcel received via FTP" },
      { "code": "ftpSent", "description": "Parcel sent via FTP" },
      { "code": "outboxDeliveryError", "description": "Delivery error occurred in the outbox" }
    ],
    "interchangeStatuses": [
      { "code": "Received", "description": "Interchange has been received" },
      { "code": "Delivered", "description": "Interchange has been delivered to the recipient" },
      { "code": "Cancelled", "description": "Interchange was cancelled before delivery" }
    ]
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `parcelStatuses` | array | All valid status codes for parcel objects |
| `interchangeStatuses` | array | All valid status codes for interchange objects |
| `parcelStatuses[].code` | string | The status code string used in API requests and responses |
| `parcelStatuses[].description` | string | Human-readable explanation of the status |
| `interchangeStatuses[].code` | string | The status code string used in API requests and responses |
| `interchangeStatuses[].description` | string | Human-readable explanation of the status |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/status-lists" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Fetch the status lists and build a lookup dictionary for parcel statuses
using System.Net.Http.Json;

var response = await httpClient.GetAsync(
    "https://rest.ecgrid.io/v2/status-lists");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<StatusLists>>();

// Build a lookup for fast status code validation or display
var parcelStatusMap = result?.Data?.ParcelStatuses
    .ToDictionary(s => s.Code, s => s.Description)
    ?? [];

Console.WriteLine($"Parcel statuses available: {parcelStatusMap.Count}");

if (parcelStatusMap.TryGetValue("InBoxReady", out var desc))
{
    Console.WriteLine($"InBoxReady: {desc}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/status-lists"))
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
const url = 'https://rest.ecgrid.io/v2/status-lists';

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
url = "https://rest.ecgrid.io/v2/status-lists"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Parcel Status Codes](../../appendix/parcel-status-codes)
- [Interchange Status Codes](../../appendix/interchange-status-codes)
- [Inbox List (Parcels)](../parcels/inbox-list)
- [Outbox List (Parcels)](../parcels/outbox-list)
