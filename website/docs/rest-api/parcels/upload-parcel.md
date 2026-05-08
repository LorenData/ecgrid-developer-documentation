---
title: Upload Parcel
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/upload-parcel.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Upload Parcel

Upload an EDI file to ECGrid as an outbound parcel for delivery to a trading partner.

## Endpoint

```http
POST /v2/parcels/upload
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `fileName` | string | Yes | Non-empty | Name of the EDI file being uploaded |
| `content` | string | Yes | Base64-encoded | EDI file content encoded as a Base64 string |
| `bytes` | int | No | | Size of the file in bytes |
| `ecGridIdFrom` | int | No | | Sender ECGrid ID; overrides ISA sender qualifier if provided |
| `ecGridIdTo` | int | No | | Recipient ECGrid ID; overrides ISA receiver qualifier if provided |
| `mailboxId` | int | No | | Mailbox to send from; defaults to the authenticated user's mailbox |

:::info Routing Behavior
When `ecGridIdFrom` and `ecGridIdTo` are omitted, ECGrid automatically routes the parcel based on the ISA segment sender and receiver qualifiers embedded in the EDI content.
:::

```json
{
  "fileName": "po_batch_20260507.edi",
  "content": "SVFU4OiogU2VuZGluZyBFREkgZGF0YSB2aWEgRUNHcmlk...",
  "bytes": 4096,
  "ecGridIdFrom": 112233,
  "ecGridIdTo": 445566,
  "mailboxId": 1001
}
```

## Response

Returns the `parcelId` (long) of the newly created outbound parcel.

```json
{
  "success": true,
  "data": 987654322
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/upload" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "fileName": "po_batch_20260507.edi", "content": "SVFU4OiogU2VuZGluZyBFREkgZGF0YSB2aWEgRUNHcmlk...", "bytes": 4096, "ecGridIdFrom": 112233, "ecGridIdTo": 445566, "mailboxId": 1001 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — read a local EDI file and upload it as a parcel
using System.Net.Http.Json;

var filePath = "po_batch_20260507.edi";
var fileBytes = await File.ReadAllBytesAsync(filePath);

var uploadRequest = new
{
    fileName = Path.GetFileName(filePath),
    content = Convert.ToBase64String(fileBytes),
    bytes = fileBytes.Length,
    ecGridIdFrom = 112233,
    ecGridIdTo = 445566,
    mailboxId = 1001
};

var response = await http.PostAsJsonAsync("https://rest.ecgrid.io/v2/parcels/upload", uploadRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<long>>();
Console.WriteLine($"Parcel uploaded — ID: {result!.Data}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"fileName\": \"po_batch_20260507.edi\", \"content\": \"SVFU4OiogU2VuZGluZyBFREkgZGF0YSB2aWEgRUNHcmlk...\", \"bytes\": 4096, \"ecGridIdFrom\": 112233, \"ecGridIdTo\": 445566, \"mailboxId\": 1001 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/upload"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/upload';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "fileName": "po_batch_20260507.edi", "content": "SVFU4OiogU2VuZGluZyBFREkgZGF0YSB2aWEgRUNHcmlk...", "bytes": 4096, "ecGridIdFrom": 112233, "ecGridIdTo": 445566, "mailboxId": 1001 }),
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
url = "https://rest.ecgrid.io/v2/parcels/upload"

response = requests.post(
    url,
    json={ "fileName": "po_batch_20260507.edi", "content": "SVFU4OiogU2VuZGluZyBFREkgZGF0YSB2aWEgRUNHcmlk...", "bytes": 4096, "ecGridIdFrom": 112233, "ecGridIdTo": 445566, "mailboxId": 1001 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Outbox List](./outbox-list) — verify the parcel appears in the outbound queue
- [Get Parcel](./get-parcel) — check status after upload
- [Send Test File](./send-test-file) — send a synthetic test EDI file to verify routing
