---
title: Outbox List
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/outbox-list.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Outbox List

Search and paginate outbound parcels sent from a mailbox.

## Endpoint

```http
POST /v2/parcels/outbox-list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | int | No | | Filter by mailbox ID; defaults to authenticated user's mailbox |
| `ecGridIdFrom` | int | No | | Filter by sender ECGrid ID |
| `ecGridIdTo` | int | No | | Filter by recipient ECGrid ID |
| `status` | ParcelStatus | No | | Filter by parcel status |
| `beginDate` | datetime | No | ISO 8601 | Return parcels created on or after this date |
| `endDate` | datetime | No | ISO 8601 | Return parcels created on or before this date |
| `pageNo` | int | No | Default: 1 | Page number for paginated results |
| `recordsPerPage` | int | No | Default: 25 | Number of records per page |

```json
{
  "mailboxId": 1001,
  "ecGridIdFrom": 112233,
  "beginDate": "2026-05-01T00:00:00Z",
  "endDate": "2026-05-07T23:59:59Z",
  "pageNo": 1,
  "recordsPerPage": 25
}
```

## Response

Returns a paginated array of outbound `ParcelIDInfo` objects matching the filter criteria.

```json
{
  "success": true,
  "data": [
    {
      "parcelId": 987654322,
      "mailboxId": 1001,
      "networkId": 42,
      "fileName": "po_batch_20260507.edi",
      "bytes": 4096,
      "status": "OutBoxDelivered",
      "ecGridIdFrom": 112233,
      "ecGridIdTo": 445566,
      "created": "2026-05-07T09:00:00Z",
      "modified": "2026-05-07T09:02:00Z"
    }
  ]
}
```

## ENUMs

### ParcelStatus

See [ParcelStatus in Appendix — ENUMs](../../appendix/enums) for the full list of parcel status values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/outbox-list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 1001, "ecGridIdFrom": 112233, "beginDate": "2026-05-01T00:00:00Z", "endDate": "2026-05-07T23:59:59Z", "pageNo": 1, "recordsPerPage": 25 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve outbound parcels for a date range to verify delivery
using System.Net.Http.Json;

var listRequest = new
{
    mailboxId = 1001,
    beginDate = DateTime.UtcNow.AddDays(-7),
    endDate = DateTime.UtcNow,
    pageNo = 1,
    recordsPerPage = 50
};

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/outbox-list",
    listRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ParcelIdInfo>>>();
Console.WriteLine($"Found {result!.Data.Count} outbound parcel(s).");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 1001, \"ecGridIdFrom\": 112233, \"beginDate\": \"2026-05-01T00:00:00Z\", \"endDate\": \"2026-05-07T23:59:59Z\", \"pageNo\": 1, \"recordsPerPage\": 25 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/outbox-list"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/outbox-list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 1001, "ecGridIdFrom": 112233, "beginDate": "2026-05-01T00:00:00Z", "endDate": "2026-05-07T23:59:59Z", "pageNo": 1, "recordsPerPage": 25 }),
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
url = "https://rest.ecgrid.io/v2/parcels/outbox-list"

response = requests.post(
    url,
    json={ "mailboxId": 1001, "ecGridIdFrom": 112233, "beginDate": "2026-05-01T00:00:00Z", "endDate": "2026-05-07T23:59:59Z", "pageNo": 1, "recordsPerPage": 25 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Upload Parcel](./upload-parcel) — send an outbound parcel
- [Cancel Parcel](./cancel-parcel) — cancel an outbound parcel before delivery
- [Inbox List](./inbox-list) — search inbound parcels
