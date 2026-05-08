---
title: Monthly Report
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Monthly Report REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Monthly Report

Generates and returns a monthly dataset for the specified report type and calendar month.

## Endpoint

```http
POST /v2/reports/monthly
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `report` | int | Yes | Must be a valid report ID from the report list | The ID of the report to generate |
| `month` | datetime | Yes | ISO 8601 UTC format; day and time components are ignored | The target month for the report (e.g., `2026-04-01T00:00:00Z` for April 2026) |

```json
{
  "report": 1,
  "month": "2026-04-01T00:00:00Z"
}
```

## Response

Returns the monthly report dataset. The structure of each row in `data` varies by report type.

```json
{
  "success": true,
  "data": [
    {
      "week": 1,
      "sent": 540,
      "received": 423,
      "totalBytes": 5242880
    },
    {
      "week": 2,
      "sent": 612,
      "received": 498,
      "totalBytes": 6291456
    },
    {
      "week": 3,
      "sent": 589,
      "received": 467,
      "totalBytes": 5767168
    },
    {
      "week": 4,
      "sent": 511,
      "received": 401,
      "totalBytes": 4718592
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `week` | int | Week number within the month |
| `sent` | int | Number of items sent during this week |
| `received` | int | Number of items received during this week |
| `totalBytes` | long | Total byte volume for this week |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/reports/monthly" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "report": 1, "month": "2026-04-01T00:00:00Z" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Generate a monthly report for report ID 1, targeting April 2026
using System.Net.Http.Json;

var request = new
{
    report = 1,
    // Only the year and month matter — use the first of the month at midnight UTC
    month = new DateTime(2026, 4, 1, 0, 0, 0, DateTimeKind.Utc)
};

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/reports/monthly",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<MonthlyReportRow>>>();
Console.WriteLine($"Weeks in report: {result?.Data?.Count}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"report\": 1, \"month\": \"2026-04-01T00:00:00Z\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/monthly"))
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
const url = 'https://rest.ecgrid.io/v2/reports/monthly';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "report": 1, "month": "2026-04-01T00:00:00Z" }),
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
url = "https://rest.ecgrid.io/v2/reports/monthly"

response = requests.post(
    url,
    json={ "report": 1, "month": "2026-04-01T00:00:00Z" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Report List](./report-list)
- [Report by Date](./report-by-date)
- [Traffic Stats](./traffic-stats)
- [Mailbox Stats](./mailbox-stats)
