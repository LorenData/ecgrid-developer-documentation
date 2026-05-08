---
title: Queue List
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of queue-list REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Queue List

Retrieve a paginated list of callback queue entries for a mailbox, optionally filtered by delivery status.

## Endpoint

```http
POST /v2/callbacks/queue-list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | int | No | — | Filter queue entries to a specific mailbox. |
| `status` | Status | No | See ENUMs | Filter by delivery status. Omit to return all statuses. |
| `pageNo` | int | No | Minimum: 1 | Page number for paginated results. Defaults to 1. |
| `recordsPerPage` | int | No | Maximum: 500 | Number of records per page. Defaults to 100. |

```json
{
  "mailboxId": 12345,
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 100
}
```

## Response

Returns a paginated array of callback queue entries showing the delivery state for each registered callback.

```json
{
  "success": true,
  "data": {
    "totalRecords": 3,
    "pageNo": 1,
    "recordsPerPage": 100,
    "queueEntries": [
      {
        "callbackId": 7001,
        "url": "https://app.example.com/webhooks/ecgrid",
        "event": "Parcel",
        "mailboxId": 12345,
        "queuedAt": "2026-05-07T09:00:00Z",
        "lastAttempt": "2026-05-07T09:01:00Z",
        "attempts": 1,
        "status": "Active",
        "lastHttpStatus": 200
      }
    ]
  }
}
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Active` | Callback is active and pending or delivered |
| `Suspended` | Callback delivery is paused |
| `Terminated` | Callback is permanently disabled |

See [Enums Reference](../../appendix/enums) for the complete `Status` ENUM.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/callbacks/queue-list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 12345, "status": "Active", "pageNo": 1, "recordsPerPage": 100 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — list all active callback queue entries for a mailbox
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new
{
    mailboxId = 12345,
    status = "Active",
    pageNo = 1,
    recordsPerPage = 100
};

var response = await client.PostAsJsonAsync("/v2/callbacks/queue-list", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<PagedResult<CallbackQueueEntry>>>();
Console.WriteLine($"Found {result.Data.TotalRecords} queue entries.");
foreach (var entry in result.Data.QueueEntries)
{
    Console.WriteLine($"  Callback {entry.CallbackId}: {entry.Event} | Attempts: {entry.Attempts} | HTTP: {entry.LastHttpStatus}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 12345, \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 100 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/queue-list"))
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
const url = 'https://rest.ecgrid.io/v2/callbacks/queue-list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 12345, "status": "Active", "pageNo": 1, "recordsPerPage": 100 }),
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
url = "https://rest.ecgrid.io/v2/callbacks/queue-list"

response = requests.post(
    url,
    json={ "mailboxId": 12345, "status": "Active", "pageNo": 1, "recordsPerPage": 100 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Queue by ID](./get-queue-by-id)
- [Event List](./event-list)
- [Create Callback](./create-callback)
- [Update Callback](./update-callback)
