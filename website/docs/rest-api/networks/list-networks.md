---
title: List Networks
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/networks/list reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Networks

Returns a paginated list of networks visible to the authenticated caller, with optional filters by network ID, mailbox ID, or status.

## Endpoint

```http
POST /v2/networks/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `networkId` | integer | No | — | Filter to a specific network ID; `0` returns all accessible networks |
| `mailboxId` | integer | No | — | Filter networks that own the given mailbox |
| `status` | string | No | See [`Status`](../../appendix/enums#status) | Limit results to networks in this status |
| `pageNo` | integer | No | ≥ 1 | Page number for pagination (default: `1`) |
| `recordsPerPage` | integer | No | 1–500 | Number of records per page (default: `25`) |

```json
{
  "networkId": 0,
  "mailboxId": 0,
  "status": "Active",
  "pageNo": 1,
  "recordsPerPage": 25
}
```

## Response

Returns an array of `NetworkIDInfo` objects along with pagination metadata.

```json
{
  "success": true,
  "data": {
    "totalRecords": 42,
    "pageNo": 1,
    "recordsPerPage": 25,
    "networks": [
      {
        "networkId": 1001,
        "uniqueId": "MYNETWORK",
        "companyName": "Acme Corporation",
        "status": "Active",
        "created": "2020-03-15T08:00:00Z",
        "modified": "2024-11-01T14:22:10Z"
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
curl -X POST "https://rest.ecgrid.io/v2/networks/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "networkId": 0, "mailboxId": 0, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — list all active networks, first page
var payload = new
{
    networkId = 0,
    mailboxId = 0,
    status = "Active",
    pageNo = 1,
    recordsPerPage = 25
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/networks/list")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<NetworkListResponse>>();
Console.WriteLine($"Total networks: {result?.Data?.TotalRecords}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"networkId\": 0, \"mailboxId\": 0, \"status\": \"Active\", \"pageNo\": 1, \"recordsPerPage\": 25 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/networks/list"))
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
const url = 'https://rest.ecgrid.io/v2/networks/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "networkId": 0, "mailboxId": 0, "status": "Active", "pageNo": 1, "recordsPerPage": 25 }),
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
url = "https://rest.ecgrid.io/v2/networks/list"

response = requests.post(
    url,
    json={ "networkId": 0, "mailboxId": 0, "status": "Active", "pageNo": 1, "recordsPerPage": 25 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Network](./get-network)
- [Update Network](./update-network)
- [Appendix: ENUMs](../../appendix/enums)
