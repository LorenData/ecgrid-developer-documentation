---
title: Mailbox Stats
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Mailbox Stats REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Mailbox Stats

Returns an overall activity summary for the mailbox associated with the authenticated session.

## Endpoint

```http
GET /v2/reports/mailbox-stats
```

## Response

Returns a high-level statistics summary for the current mailbox, including parcel and interchange counts.

```json
{
  "success": true,
  "data": {
    "mailboxId": 7890,
    "totalParcels": 3245,
    "totalInterchanges": 18900,
    "totalBytes": 52428800,
    "activePartners": 42,
    "reportGeneratedAt": "2026-05-07T08:00:00Z"
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `mailboxId` | int | The mailbox these statistics apply to |
| `totalParcels` | int | Total number of parcels processed |
| `totalInterchanges` | int | Total number of interchanges processed |
| `totalBytes` | long | Total byte volume across all activity |
| `activePartners` | int | Number of active trading partner connections |
| `reportGeneratedAt` | datetime | UTC timestamp when the statistics were compiled |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/reports/mailbox-stats" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve overall mailbox statistics for the authenticated session
using System.Net.Http.Json;

var response = await httpClient.GetAsync(
    "https://rest.ecgrid.io/v2/reports/mailbox-stats");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxStats>>();
Console.WriteLine($"Total Interchanges: {result?.Data?.TotalInterchanges:N0}");
Console.WriteLine($"Active Partners: {result?.Data?.ActivePartners}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/mailbox-stats"))
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
const url = 'https://rest.ecgrid.io/v2/reports/mailbox-stats';

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
url = "https://rest.ecgrid.io/v2/reports/mailbox-stats"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Mailbox Interchange Stats](./mailbox-interchange-stats)
- [Interchange Stats](./interchange-stats)
- [Monthly Report](./monthly-report)
- [Traffic Stats](./traffic-stats)
