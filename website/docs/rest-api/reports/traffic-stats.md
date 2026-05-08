---
title: Traffic Stats
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Traffic Stats REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Traffic Stats

Returns traffic volume statistics across multiple time periods, centered on a target timestamp.

## Endpoint

```http
POST /v2/reports/traffic-stats
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `targetTime` | datetime | Yes | ISO 8601 UTC format | The reference point from which periods are calculated (typically now or a past timestamp) |
| `numPeriods` | int | Yes | Must be a positive integer | Number of periods to return going back from `targetTime` |
| `period` | string | Yes | Must be a valid `StatisticsPeriod` value | The granularity of each period (hour, day, week, or month) |

```json
{
  "targetTime": "2026-05-07T00:00:00Z",
  "numPeriods": 7,
  "period": "Day"
}
```

## Response

Returns an ordered array of traffic statistics records, one per period, from oldest to most recent.

```json
{
  "success": true,
  "data": [
    {
      "periodStart": "2026-05-01T00:00:00Z",
      "periodEnd": "2026-05-01T23:59:59Z",
      "sentCount": 340,
      "receivedCount": 280,
      "totalBytes": 3145728
    },
    {
      "periodStart": "2026-05-02T00:00:00Z",
      "periodEnd": "2026-05-02T23:59:59Z",
      "sentCount": 398,
      "receivedCount": 315,
      "totalBytes": 3670016
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `periodStart` | datetime | UTC start of this traffic period |
| `periodEnd` | datetime | UTC end of this traffic period |
| `sentCount` | int | Number of items sent during this period |
| `receivedCount` | int | Number of items received during this period |
| `totalBytes` | long | Combined byte volume for this period |

## ENUMs

### StatisticsPeriod

See [StatisticsPeriod in the Appendix](../../appendix/enums#statisticsperiod) for the full list of values.

| Value | Description |
|---|---|
| `Hour` | Each period spans one hour |
| `Day` | Each period spans one day |
| `Week` | Each period spans one week |
| `Month` | Each period spans one calendar month |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/reports/traffic-stats" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "targetTime": "2026-05-07T00:00:00Z", "numPeriods": 7, "period": "Day" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve daily traffic stats for the past 7 days
using System.Net.Http.Json;

var request = new
{
    targetTime = DateTime.UtcNow,
    numPeriods = 7,
    period = "Day"
};

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/reports/traffic-stats",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<TrafficStatsPeriod>>>();

foreach (var p in result?.Data ?? [])
{
    Console.WriteLine(
        $"{p.PeriodStart:d}: Sent={p.SentCount}, Received={p.ReceivedCount}, Bytes={p.TotalBytes:N0}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"targetTime\": \"2026-05-07T00:00:00Z\", \"numPeriods\": 7, \"period\": \"Day\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/traffic-stats"))
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
const url = 'https://rest.ecgrid.io/v2/reports/traffic-stats';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "targetTime": "2026-05-07T00:00:00Z", "numPeriods": 7, "period": "Day" }),
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
url = "https://rest.ecgrid.io/v2/reports/traffic-stats"

response = requests.post(
    url,
    json={ "targetTime": "2026-05-07T00:00:00Z", "numPeriods": 7, "period": "Day" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Interchange Stats](./interchange-stats)
- [Instant Stats](./instant-stats)
- [Mailbox Interchange Stats](./mailbox-interchange-stats)
- [Monthly Report](./monthly-report)
- [StatisticsPeriod Enum](../../appendix/enums#statisticsperiod)
