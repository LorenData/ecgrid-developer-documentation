---
title: Report List
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Report List REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Report List

Returns a list of available reports, with an option to include inactive reports.

## Endpoint

```http
GET /v2/reports/{ShowInactive}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ShowInactive` | bool | Yes | Pass `true` to include inactive reports; `false` to return only active reports |

## Response

Returns an array of report descriptors available for the authenticated account.

```json
{
  "success": true,
  "data": [
    {
      "reportId": 1,
      "name": "Monthly Interchange Summary",
      "description": "Summarizes interchange activity for a calendar month.",
      "active": true
    },
    {
      "reportId": 2,
      "name": "Traffic Volume Report",
      "description": "Shows byte volume and parcel counts across configurable time periods.",
      "active": true
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `reportId` | int | Unique identifier for the report, used with other report endpoints |
| `name` | string | Human-readable name of the report |
| `description` | string | Brief description of the report's content and purpose |
| `active` | bool | Whether this report is currently active and available to run |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/reports/$SHOW_INACTIVE" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve only active reports available to the authenticated account
using System.Net.Http.Json;

bool showInactive = false;

var response = await httpClient.GetAsync(
    $"https://rest.ecgrid.io/v2/reports/{showInactive}");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ReportDescriptor>>>();

foreach (var report in result?.Data ?? [])
{
    Console.WriteLine($"[{report.ReportId}] {report.Name} — Active: {report.Active}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String ShowInactive = "0"; // replace with actual ShowInactive

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/reports/%s", ShowInactive)))
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
const url = `https://rest.ecgrid.io/v2/reports/${ShowInactive}`;

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
show_inactive = 0  # replace with actual show_inactive
url = f"https://rest.ecgrid.io/v2/reports/{show_inactive}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Report by Date](./report-by-date)
- [Monthly Report](./monthly-report)
- [Traffic Stats](./traffic-stats)
- [Interchange Stats](./interchange-stats)
