---
title: Interchange Stats
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Interchange Stats REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Interchange Stats

Returns interchange statistics grouped by time period for a specified date range and direction.

## Endpoint

```http
POST /v2/reports/interchange-stats
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `startTime` | datetime | Yes | ISO 8601 UTC format | Start of the reporting window (inclusive) |
| `endTime` | datetime | Yes | ISO 8601 UTC format; must be after `startTime` | End of the reporting window (inclusive) |
| `direction` | string | Yes | Must be a valid `Direction` value | Filter by inbound, outbound, or both directions |

```json
{
  "startTime": "2026-04-01T00:00:00Z",
  "endTime": "2026-04-30T23:59:59Z",
  "direction": "InBox"
}
```

## Response

Returns an array of interchange statistics records, one per period within the specified range.

```json
{
  "success": true,
  "data": [
    {
      "periodStart": "2026-04-01T00:00:00Z",
      "periodEnd": "2026-04-01T23:59:59Z",
      "count": 215,
      "totalBytes": 1048576,
      "direction": "InBox"
    },
    {
      "periodStart": "2026-04-02T00:00:00Z",
      "periodEnd": "2026-04-02T23:59:59Z",
      "count": 198,
      "totalBytes": 983040,
      "direction": "InBox"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `periodStart` | datetime | UTC start of the statistics period |
| `periodEnd` | datetime | UTC end of the statistics period |
| `count` | int | Number of interchanges in this period |
| `totalBytes` | long | Total byte volume for this period |
| `direction` | string | Direction filter applied — see `Direction` enum |

## ENUMs

### Direction

See [Direction in the Appendix](../../appendix/enums#direction) for the full list of values.

| Value | Description |
|---|---|
| `NoDir` | No direction filter applied |
| `OutBox` | Outbound interchanges only |
| `InBox` | Inbound interchanges only |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/reports/interchange-stats" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "startTime": "2026-04-01T00:00:00Z", "endTime": "2026-04-30T23:59:59Z", "direction": "InBox" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve inbound interchange statistics for April 2026
using System.Net.Http.Json;

var request = new
{
    startTime = new DateTime(2026, 4, 1, 0, 0, 0, DateTimeKind.Utc),
    endTime = new DateTime(2026, 4, 30, 23, 59, 59, DateTimeKind.Utc),
    direction = "InBox"
};

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/reports/interchange-stats",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<InterchangeStatsPeriod>>>();

foreach (var period in result?.Data ?? [])
{
    Console.WriteLine($"{period.PeriodStart:d}: {period.Count} interchanges ({period.TotalBytes:N0} bytes)");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"startTime\": \"2026-04-01T00:00:00Z\", \"endTime\": \"2026-04-30T23:59:59Z\", \"direction\": \"InBox\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/interchange-stats"))
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
const url = 'https://rest.ecgrid.io/v2/reports/interchange-stats';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "startTime": "2026-04-01T00:00:00Z", "endTime": "2026-04-30T23:59:59Z", "direction": "InBox" }),
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
url = "https://rest.ecgrid.io/v2/reports/interchange-stats"

response = requests.post(
    url,
    json={ "startTime": "2026-04-01T00:00:00Z", "endTime": "2026-04-30T23:59:59Z", "direction": "InBox" },
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
- [Report by Date](./report-by-date)
- [Direction Enum](../../appendix/enums#direction)
