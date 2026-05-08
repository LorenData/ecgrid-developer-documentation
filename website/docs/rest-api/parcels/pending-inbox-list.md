---
title: Pending Inbox List
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/pending-inbox-list.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Pending Inbox List

Return all inbound parcels with `InBoxReady` status that have not yet been downloaded.

## Endpoint

```http
POST /v2/parcels/pending-inbox-list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | int | No | | Mailbox to check for pending parcels; defaults to authenticated user's mailbox |

:::info Efficient Polling
This endpoint is optimized for polling loops. It returns only unread parcels (`InBoxReady`) without requiring date range filters or pagination parameters, making it more efficient than [Inbox List](./inbox-list) for routine file pickup checks.
:::

```json
{
  "mailboxId": 1001
}
```

## Response

Returns an array of `ParcelIDInfo` objects where each parcel has `InBoxReady` status.

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
      "ecGridIdFrom": 112233,
      "ecGridIdTo": 445566,
      "created": "2026-05-07T08:00:00Z",
      "modified": "2026-05-07T08:00:00Z"
    }
  ]
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/pending-inbox-list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 1001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — poll for pending inbound parcels and download each one
using System.Net.Http.Json;

var listRequest = new { mailboxId = 1001 };

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    listRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<ParcelIdInfo>>>();

foreach (var parcel in result!.Data)
{
    // Download each pending parcel
    var downloadResponse = await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/parcels/download",
        new { parcelId = parcel.ParcelId });
    downloadResponse.EnsureSuccessStatusCode();

    var download = await downloadResponse.Content
        .ReadFromJsonAsync<ApiResponse<ParcelDownload>>();
    var ediBytes = Convert.FromBase64String(download!.Data.Content);
    await File.WriteAllBytesAsync(download.Data.FileName, ediBytes);

    // Confirm after saving so ECGrid marks the parcel as transferred
    await http.PostAsJsonAsync(
        "https://rest.ecgrid.io/v2/parcels/confirm",
        new { parcelId = parcel.ParcelId });

    Console.WriteLine($"Processed parcel {parcel.ParcelId} — {parcel.FileName}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 1001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/pending-inbox-list"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/pending-inbox-list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 1001 }),
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
url = "https://rest.ecgrid.io/v2/parcels/pending-inbox-list"

response = requests.post(
    url,
    json={ "mailboxId": 1001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Download Parcel](./download-parcel) — download a parcel's EDI content
- [Confirm Download](./confirm-download) — acknowledge delivery after saving
- [Inbox List](./inbox-list) — full paginated inbox search with date and status filters
