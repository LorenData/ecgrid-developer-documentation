---
title: Reset to Inbox
sidebar_position: 9
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/reset-to-inbox.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Reset to Inbox

Reset a previously confirmed inbound parcel back to `InBoxReady` so it can be downloaded again.

## Endpoint

```http
POST /v2/parcels/reset-to-inbox/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | Unique identifier of the inbound parcel to reset |

:::info When to Use This
Use this endpoint when a parcel was confirmed but the local file was lost or corrupted and needs to be re-downloaded. After reset, the parcel will reappear in [Pending Inbox List](./pending-inbox-list) and [Inbox List](./inbox-list) with `InBoxReady` status.
:::

## Response

Returns a success boolean indicating whether the parcel was successfully reset.

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
curl -X POST "https://rest.ecgrid.io/v2/parcels/reset-to-inbox/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — restore a previously confirmed parcel to InBoxReady for re-download
using System.Net.Http.Json;

var parcelId = 987654321L;

var response = await http.PostAsync(
    $"https://rest.ecgrid.io/v2/parcels/reset-to-inbox/{parcelId}",
    null);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result!.Data)
{
    Console.WriteLine($"Parcel {parcelId} reset to InBoxReady — ready for re-download.");
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
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/parcels/reset-to-inbox/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/parcels/reset-to-inbox/${id}`;

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
url = f"https://rest.ecgrid.io/v2/parcels/reset-to-inbox/{id}"

response = requests.post(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Download Parcel](./download-parcel) — re-download the parcel after resetting
- [Confirm Download](./confirm-download) — confirm delivery again after re-downloading
- [Get Parcel](./get-parcel) — verify parcel status before and after reset
