---
title: Report by Date
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Report by Date REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Report by Date

Runs a specific report for a given date range and returns the resulting data rows.

## Endpoint

```http
POST /v2/reports/bydate
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `reportId` | int | Yes | Must be a valid report ID from the report list | The ID of the report to run |
| `startDate` | datetime | Yes | ISO 8601 UTC format | Start of the date range (inclusive) |
| `endDate` | datetime | Yes | ISO 8601 UTC format; must be after `startDate` | End of the date range (inclusive) |

```json
{
  "reportId": 1,
  "startDate": "2026-04-01T00:00:00Z",
  "endDate": "2026-04-30T23:59:59Z"
}
```

## Response

Returns the report dataset for the specified period. The structure of the `data` array varies by report type.

```json
{
  "success": true,
  "data": [
    {
      "date": "2026-04-01",
      "sent": 120,
      "received": 95,
      "totalBytes": 524288
    },
    {
      "date": "2026-04-02",
      "sent": 134,
      "received": 110,
      "totalBytes": 614400
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `date` | string | The date this row covers |
| `sent` | int | Number of items sent on this date |
| `received` | int | Number of items received on this date |
| `totalBytes` | long | Byte volume for this date |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/reports/bydate" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "reportId": 1, "startDate": "2026-04-01T00:00:00Z", "endDate": "2026-04-30T23:59:59Z" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Run report ID 1 for the month of April 2026
using System.Net.Http.Json;

var request = new
{
    reportId = 1,
    startDate = new DateTime(2026, 4, 1, 0, 0, 0, DateTimeKind.Utc),
    endDate = new DateTime(2026, 4, 30, 23, 59, 59, DateTimeKind.Utc)
};

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/reports/bydate",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ReportRow>>>();
Console.WriteLine($"Rows returned: {result?.Data?.Count}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"reportId\": 1, \"startDate\": \"2026-04-01T00:00:00Z\", \"endDate\": \"2026-04-30T23:59:59Z\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/bydate"))
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
const url = 'https://rest.ecgrid.io/v2/reports/bydate';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "reportId": 1, "startDate": "2026-04-01T00:00:00Z", "endDate": "2026-04-30T23:59:59Z" }),
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
url = "https://rest.ecgrid.io/v2/reports/bydate"

response = requests.post(
    url,
    json={ "reportId": 1, "startDate": "2026-04-01T00:00:00Z", "endDate": "2026-04-30T23:59:59Z" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Report List](./report-list)
- [Monthly Report](./monthly-report)
- [Interchange Stats](./interchange-stats)
- [Traffic Stats](./traffic-stats)
