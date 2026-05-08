---
title: Set Mailbag Control ID
sidebar_position: 12
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create REST API parcels/set-mailbag-control-id.md documentation - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Set Mailbag Control ID

Assign a custom mailbag control ID to a parcel for external tracking and reconciliation purposes.

## Endpoint

```http
POST /v2/parcels/set-mailbagcontrolid
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `parcelId` | long | Yes | | Unique identifier of the parcel |
| `mailbagControlId` | string | Yes | Non-empty | Custom control ID string to assign to this parcel |

```json
{
  "parcelId": 987654321,
  "mailbagControlId": "ACME-2026050701"
}
```

## Response

Returns a success boolean indicating the mailbag control ID was assigned.

```json
{
  "success": true,
  "data": true
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/parcels/set-mailbagcontrolid" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "parcelId": 987654321, "mailbagControlId": "ACME-2026050701" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — tag a parcel with a business-defined control ID for reconciliation
using System.Net.Http.Json;

var request = new
{
    parcelId = 987654321L,
    mailbagControlId = "ACME-2026050701"
};

var response = await http.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/parcels/set-mailbagcontrolid",
    request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result!.Data)
{
    Console.WriteLine($"Mailbag control ID assigned to parcel {request.parcelId}.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"parcelId\": 987654321, \"mailbagControlId\": \"ACME-2026050701\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/set-mailbagcontrolid"))
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
const url = 'https://rest.ecgrid.io/v2/parcels/set-mailbagcontrolid';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "parcelId": 987654321, "mailbagControlId": "ACME-2026050701" }),
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
url = "https://rest.ecgrid.io/v2/parcels/set-mailbagcontrolid"

response = requests.post(
    url,
    json={ "parcelId": 987654321, "mailbagControlId": "ACME-2026050701" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Find Mailbag Control ID](./find-mailbag-control-id) — look up parcels by their mailbag control ID
- [Get Parcel](./get-parcel) — retrieve parcel metadata after assignment
