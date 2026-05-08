---
title: Instant Stats
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Instant Stats REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Instant Stats

Returns real-time parcel activity counts for two configurable trailing time windows.

This endpoint is designed for operational dashboards and health checks — it gives a live count of how many parcels have been processed in the last N minutes across two independently configurable windows (for example, the last 5 minutes versus the last 60 minutes).

## Endpoint

```http
POST /v2/reports/instant-stats
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `minutes1` | int | Yes | Must be a positive integer | Duration (in minutes) for the first time window |
| `minutes2` | int | Yes | Must be a positive integer | Duration (in minutes) for the second time window |

```json
{
  "minutes1": 5,
  "minutes2": 60
}
```

## Response

Returns parcel counts for each of the two requested time windows.

```json
{
  "success": true,
  "data": {
    "window1Minutes": 5,
    "window1Count": 12,
    "window2Minutes": 60,
    "window2Count": 148
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `window1Minutes` | int | The duration of the first time window, as requested |
| `window1Count` | int | Number of parcels processed within the first time window |
| `window2Minutes` | int | The duration of the second time window, as requested |
| `window2Count` | int | Number of parcels processed within the second time window |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/reports/instant-stats" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "minutes1": 5, "minutes2": 60 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Check parcel activity in the last 5 and 60 minutes for a health dashboard
using System.Net.Http.Json;

var request = new
{
    minutes1 = 5,
    minutes2 = 60
};

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/reports/instant-stats",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<InstantStats>>();

Console.WriteLine($"Last {result?.Data?.Window1Minutes} min: {result?.Data?.Window1Count} parcels");
Console.WriteLine($"Last {result?.Data?.Window2Minutes} min: {result?.Data?.Window2Count} parcels");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"minutes1\": 5, \"minutes2\": 60 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/instant-stats"))
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
const url = 'https://rest.ecgrid.io/v2/reports/instant-stats';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "minutes1": 5, "minutes2": 60 }),
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
url = "https://rest.ecgrid.io/v2/reports/instant-stats"

response = requests.post(
    url,
    json={ "minutes1": 5, "minutes2": 60 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Mailbox Interchange Stats](./mailbox-interchange-stats)
- [Traffic Stats](./traffic-stats)
- [Interchange Stats](./interchange-stats)
