---
title: List Mailboxes
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/mailboxes/list reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Mailboxes

Returns a paginated list of mailboxes accessible to the caller, with optional filtering by network or status.

## Endpoint

```http
POST /v2/mailboxes/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `networkId` | integer | No | — | Filter to mailboxes belonging to this network; `0` returns all accessible mailboxes |
| `status` | string | No | See [`Status`](../../appendix/enums#status) | Limit results to mailboxes in this status |
| `pageNo` | integer | No | ≥ 1 | Page number for pagination (default: `1`) |
| `recordsPerPage` | integer | No | 1–500 | Number of records per page (default: `25`) |

```json
{
  "networkId": 1001,
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 25
}
```

## Response

Returns an array of `MailboxIDInfo` objects with pagination metadata.

```json
{
  "success": true,
  "data": {
    "totalRecords": 14,
    "pageNo": 1,
    "recordsPerPage": 25,
    "mailboxes": [
      {
        "mailboxId": 5001,
        "networkId": 1001,
        "uniqueId": "ACMEMBOX01",
        "companyName": "Acme Mailbox One",
        "status": "Active",
        "created": "2021-06-10T09:00:00Z",
        "modified": "2025-02-14T11:30:00Z"
      }
    ]
  },
  "errorCode": null,
  "message": null
}
```

## ENUMs

### Status

The `status` filter uses the `Status` enum. See the full value table in [Appendix: ENUMs](../../appendix/enums#status).

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/mailboxes/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "networkId": 1001, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — list all active mailboxes for a network
var payload = new
{
    networkId = 1001,
    status = "Active",
    pageNo = 1,
    recordsPerPage = 25
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/mailboxes/list")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxListResponse>>();
Console.WriteLine($"Total mailboxes: {result?.Data?.TotalRecords}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"networkId\": 1001, \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 25 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/list"))
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
const url = 'https://rest.ecgrid.io/v2/mailboxes/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "networkId": 1001, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }),
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
url = "https://rest.ecgrid.io/v2/mailboxes/list"

response = requests.post(
    url,
    json={ "networkId": 1001, "status": "Active", "pageNo": 1, "recordsPerPage": 25 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Mailbox](./get-mailbox)
- [Create Mailbox](./create-mailbox)
- [Appendix: ENUMs](../../appendix/enums)
