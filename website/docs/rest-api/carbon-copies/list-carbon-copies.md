---
title: List Carbon Copies
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of List Carbon Copies REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Carbon Copies

Returns a paginated list of carbon copy rules for a given mailbox, optionally filtered by status.

## Endpoint

```http
POST /v2/carboncopies/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | No | Must be a valid mailbox | Filter results to rules associated with this mailbox |
| `status` | Status | No | See ENUMs | Filter by rule status (e.g., `Active`, `Suspended`) |
| `pageNo` | integer | No | >= 1, default 1 | Page number for paginated results |
| `recordsPerPage` | integer | No | 1–1000, default 100 | Number of records returned per page |

```json
{
  "mailboxId": 101,
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 50
}
```

## Response

Returns a paginated array of carbon copy rule objects.

```json
{
  "success": true,
  "data": [
    {
      "ccId": 1042,
      "fromMailboxId": 101,
      "toMailboxId": 202,
      "status": "Active",
      "direction": "InBox",
      "created": "2025-01-15T10:30:00Z"
    },
    {
      "ccId": 1043,
      "fromMailboxId": 101,
      "toMailboxId": 303,
      "status": "Active",
      "direction": "OutBox",
      "created": "2025-03-22T08:15:00Z"
    }
  ],
  "pageNo": 1,
  "recordsPerPage": 50,
  "totalRecords": 2
}
```

## ENUMs

This endpoint uses the `Status` ENUM. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/carboncopies/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 101, "status": "Active", "pageNo": 1, "recordsPerPage": 50 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — List all active carbon copy rules for a mailbox
var request = new
{
    mailboxId = 101,
    status = "Active",
    pageNo = 1,
    recordsPerPage = 100
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/carboncopies/list",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<CarbonCopyInfo>>>();
Console.WriteLine($"Found {result.TotalRecords} carbon copy rule(s).");

foreach (var cc in result.Data)
{
    Console.WriteLine($"CC {cc.CcId}: {cc.Direction} from {cc.FromMailboxId} to {cc.ToMailboxId} [{cc.Status}]");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 101, \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 50 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/carboncopies/list"))
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
const url = 'https://rest.ecgrid.io/v2/carboncopies/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 101, "status": "Active", "pageNo": 1, "recordsPerPage": 50 }),
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
url = "https://rest.ecgrid.io/v2/carboncopies/list"

response = requests.post(
    url,
    json={ "mailboxId": 101, "status": "Active", "pageNo": 1, "recordsPerPage": 50 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Carbon Copy](./get-carbon-copy)
- [Create Carbon Copy](./create-carbon-copy)
- [Update Carbon Copy](./update-carbon-copy)
- [Delete Carbon Copy](./delete-carbon-copy)
- [ENUMs Reference](../../appendix/enums)
