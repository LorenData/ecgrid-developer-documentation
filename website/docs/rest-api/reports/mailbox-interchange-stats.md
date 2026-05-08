---
title: Mailbox Interchange Stats
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Reports / Mailbox Interchange Stats REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Mailbox Interchange Stats

Returns interchange-level statistics for the mailbox associated with the authenticated session.

## Endpoint

```http
GET /v2/reports/mailbox-interchange-stats
```

## Response

Returns interchange count and byte totals for the current mailbox, segmented by sent and received activity.

```json
{
  "success": true,
  "data": {
    "sent": 1452,
    "received": 873,
    "totalBytes": 10485760,
    "period": "2026-04"
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `sent` | int | Number of interchanges sent during the reporting period |
| `received` | int | Number of interchanges received during the reporting period |
| `totalBytes` | long | Total byte volume of all interchanges for the period |
| `period` | string | The reporting period covered by these statistics |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/reports/mailbox-interchange-stats" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve interchange statistics for the authenticated mailbox
using System.Net.Http.Json;

var response = await httpClient.GetAsync(
    "https://rest.ecgrid.io/v2/reports/mailbox-interchange-stats");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxInterchangeStats>>();
Console.WriteLine($"Sent: {result?.Data?.Sent} | Received: {result?.Data?.Received}");
Console.WriteLine($"Total bytes: {result?.Data?.TotalBytes:N0}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/reports/mailbox-interchange-stats"))
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
const url = 'https://rest.ecgrid.io/v2/reports/mailbox-interchange-stats';

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
url = "https://rest.ecgrid.io/v2/reports/mailbox-interchange-stats"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Mailbox Stats](./mailbox-stats)
- [Interchange Stats](./interchange-stats)
- [Instant Stats](./instant-stats)
- [Traffic Stats](./traffic-stats)
