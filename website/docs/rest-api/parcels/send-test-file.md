---
title: Send Test File
sidebar_position: 15
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/send-test-file.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Send Test File

Send a synthetic test EDI file to verify routing configuration between two ECGrid trading partners.

## Endpoint

```http
POST /v2/parcels/send-test-file
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridIdFrom` | int | Yes | | Sender ECGrid ID for the test transmission |
| `ecGridIdTo` | int | Yes | | Recipient ECGrid ID for the test transmission |
| `documentType` | string | No | | EDI document type to use in the test file (e.g., `"850"`) |

:::info Routing Verification
This endpoint generates a valid synthetic EDI payload and injects it into the routing engine exactly as a real parcel would be processed. Use it to confirm that a new trading partner interconnect is correctly configured before going live with production data.
:::

```json
{
  "ecGridIdFrom": 112233,
  "ecGridIdTo": 445566,
  "documentType": "850"
}
```

## Response

Returns the `parcelId` (long) of the test parcel that was created and submitted.

```json
{
  "success": true,
  "data": 987654399
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/send-test-file" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridIdFrom": 112233, "ecGridIdTo": 445566, "documentType": "850" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — send a synthetic test EDI file to validate a new interconnect
using System.Net.Http.Json;

var testRequest = new
{
    ecGridIdFrom = 112233,
    ecGridIdTo = 445566,
    documentType = "850"
};

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/send-test-file",
    testRequest);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<long>>();
Console.WriteLine($"Test parcel submitted — ID: {result!.Data}");

// Poll Get Parcel to observe delivery status
var statusResponse = await http.GetAsync(
    $"https://rest.ecgrid.io/v2/parcels/{result.Data}");
statusResponse.EnsureSuccessStatusCode();

var statusResult = await statusResponse.Content
    .ReadFromJsonAsync<ApiResponse<ParcelIdInfo>>();
Console.WriteLine($"Test parcel status: {statusResult!.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridIdFrom\": 112233, \"ecGridIdTo\": 445566, \"documentType\": \"850\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/send-test-file"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/send-test-file';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridIdFrom": 112233, "ecGridIdTo": 445566, "documentType": "850" }),
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
url = "https://rest.ecgrid.io/v2/parcels/send-test-file"

response = requests.post(
    url,
    json={ "ecGridIdFrom": 112233, "ecGridIdTo": 445566, "documentType": "850" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Upload Parcel](./upload-parcel) — upload a real EDI file for production delivery
- [Get Parcel](./get-parcel) — track the status of the submitted test parcel
- [Partners — Get Partner](../partners/get-partner) — verify the interconnect exists before sending a test file
