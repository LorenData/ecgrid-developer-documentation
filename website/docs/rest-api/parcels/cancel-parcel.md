---
title: Cancel Parcel
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/cancel-parcel.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Cancel Parcel

Cancel an outbound parcel before it has been delivered to the recipient.

## Endpoint

```http
POST /v2/parcels/cancel/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | Unique identifier of the outbound parcel to cancel |

:::caution Outbound Parcels Only
Cancellation is only available for outbound parcels that have not yet been delivered. Attempting to cancel an already-delivered parcel or an inbound parcel will return an error.
:::

## Response

Returns a success boolean indicating whether the parcel was successfully cancelled.

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
curl -X POST "https://rest.ecgrid.io/v2/parcels/cancel/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — cancel an outbound parcel that has not yet been delivered
using System.Net.Http.Json;

var parcelId = 987654322L;

var response = await http.PostAsync(
    $"https://rest.ecgrid.io/v2/parcels/cancel/{parcelId}",
    null);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result!.Data)
{
    Console.WriteLine($"Parcel {parcelId} successfully cancelled.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/parcels/cancel/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/parcels/cancel/${id}`;

const response = await fetch(url, {
  method: 'POST',
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
url = f"https://rest.ecgrid.io/v2/parcels/cancel/{id}"

response = requests.post(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Upload Parcel](./upload-parcel) — send a replacement parcel after cancellation
- [Outbox List](./outbox-list) — verify parcel status before attempting cancellation
- [Get Parcel](./get-parcel) — check current delivery status
