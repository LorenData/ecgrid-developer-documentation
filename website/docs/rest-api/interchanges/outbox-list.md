---
title: Interchange Outbox List
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of interchanges outbox-list REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Interchange Outbox List

Retrieve a paginated list of outbound interchanges for a mailbox within a specified date range.

## Endpoint

```http
POST /v2/interchanges/outbox-list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | int | No | — | Filter results to a specific mailbox. |
| `ecGridIdFrom` | int | No | — | Filter by the sending ECGrid ID. |
| `ecGridIdTo` | int | No | — | Filter by the receiving ECGrid ID. |
| `beginDate` | datetime | No | ISO 8601 | Start of the date range to query. |
| `endDate` | datetime | No | ISO 8601 | End of the date range to query. |
| `pageNo` | int | No | Minimum: 1 | Page number for paginated results. Defaults to 1. |
| `recordsPerPage` | int | No | Maximum: 500 | Number of records per page. Defaults to 100. |

```json
{
  "mailboxId": 12345,
  "ecGridIdFrom": 0,
  "ecGridIdTo": 0,
  "beginDate": "2026-05-01T00:00:00Z",
  "endDate": "2026-05-07T23:59:59Z",
  "pageNo": 1,
  "recordsPerPage": 100
}
```

## Response

Returns a paginated array of `InterchangeIDInfo` objects representing outbound interchanges matching the query criteria.

```json
{
  "success": true,
  "data": {
    "totalRecords": 18,
    "pageNo": 1,
    "recordsPerPage": 100,
    "interchanges": [
      {
        "interchangeId": 9870099,
        "parcelId": 5550010,
        "sender": "BUYER_INC",
        "receiver": "ACME_CORP",
        "standard": "X12",
        "documentType": "810",
        "status": "Active",
        "created": "2026-05-03T14:15:00Z"
      }
    ]
  }
}
```

## ENUMs

### EDIStandard

See [Enums Reference](../../appendix/enums) for the full `EDIStandard` and `Status` ENUM definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/interchanges/outbox-list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 12345, "ecGridIdFrom": 0, "ecGridIdTo": 0, "beginDate": "2026-05-01T00:00:00Z", "endDate": "2026-05-07T23:59:59Z", "pageNo": 1, "recordsPerPage": 100 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — query outbound interchanges with date range and pagination
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new
{
    mailboxId = 12345,
    beginDate = DateTime.UtcNow.AddDays(-7),
    endDate = DateTime.UtcNow,
    pageNo = 1,
    recordsPerPage = 100
};

var response = await client.PostAsJsonAsync("/v2/interchanges/outbox-list", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<PagedResult<InterchangeIdInfo>>>();
Console.WriteLine($"Found {result.Data.TotalRecords} outbound interchanges.");
foreach (var interchange in result.Data.Interchanges)
{
    Console.WriteLine($"  [{interchange.InterchangeId}] {interchange.Sender} → {interchange.Receiver} | {interchange.DocumentType}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 12345, \"ecGridIdFrom\": 0, \"ecGridIdTo\": 0, \"beginDate\": \"2026-05-01T00:00:00Z\", \"endDate\": \"2026-05-07T23:59:59Z\", \"pageNo\": 1, \"recordsPerPage\": 100 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/interchanges/outbox-list"))
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
const url = 'https://rest.ecgrid.io/v2/interchanges/outbox-list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 12345, "ecGridIdFrom": 0, "ecGridIdTo": 0, "beginDate": "2026-05-01T00:00:00Z", "endDate": "2026-05-07T23:59:59Z", "pageNo": 1, "recordsPerPage": 100 }),
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
url = "https://rest.ecgrid.io/v2/interchanges/outbox-list"

response = requests.post(
    url,
    json={ "mailboxId": 12345, "ecGridIdFrom": 0, "ecGridIdTo": 0, "beginDate": "2026-05-01T00:00:00Z", "endDate": "2026-05-07T23:59:59Z", "pageNo": 1, "recordsPerPage": 100 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Interchange Inbox List](./inbox-list)
- [Get Interchange](./get-interchange)
- [Cancel Interchange](./cancel-interchange)
- [Resend Interchange](./resend-interchange)
- [Parcel Outbox List](../parcels/outbox-list)
