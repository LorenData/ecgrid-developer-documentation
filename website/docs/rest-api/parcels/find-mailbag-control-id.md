---
title: Find Mailbag Control ID
sidebar_position: 13
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/find-mailbag-control-id.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Find Mailbag Control ID

Search for parcels that match a given mailbag control ID string.

## Endpoint

```http
POST /v2/parcels/find-mailbagcontrolid
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | int | No | | Narrow the search to a specific mailbox |
| `mailbagControlId` | string | Yes | Non-empty | The mailbag control ID string to search for |

```json
{
  "mailboxId": 1001,
  "mailbagControlId": "ACME-2026050701"
}
```

## Response

Returns an array of `ParcelIDInfo` objects whose mailbag control ID matches the search value.

```json
{
  "success": true,
  "data": [
    {
      "parcelId": 987654321,
      "mailboxId": 1001,
      "networkId": 42,
      "fileName": "invoice_batch_20260507.edi",
      "bytes": 14872,
      "status": "InBoxTransferred",
      "ecGridIdFrom": 112233,
      "ecGridIdTo": 445566,
      "created": "2026-05-07T08:00:00Z",
      "modified": "2026-05-07T08:10:00Z"
    }
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/find-mailbagcontrolid" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 1001, "mailbagControlId": "ACME-2026050701" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — look up parcels by a previously assigned mailbag control ID
using System.Net.Http.Json;

var searchRequest = new
{
    mailboxId = 1001,
    mailbagControlId = "ACME-2026050701"
};

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/find-mailbagcontrolid",
    searchRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ParcelIdInfo>>>();
Console.WriteLine($"Found {result!.Data.Count} parcel(s) matching control ID.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 1001, \"mailbagControlId\": \"ACME-2026050701\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/find-mailbagcontrolid"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/find-mailbagcontrolid';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 1001, "mailbagControlId": "ACME-2026050701" }),
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
url = "https://rest.ecgrid.io/v2/parcels/find-mailbagcontrolid"

response = requests.post(
    url,
    json={ "mailboxId": 1001, "mailbagControlId": "ACME-2026050701" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Set Mailbag Control ID](./set-mailbag-control-id) — assign a mailbag control ID to a parcel
- [Get Parcel](./get-parcel) — retrieve full parcel details for a matched result
- [Inbox List](./inbox-list) — broad parcel search with date and status filters
