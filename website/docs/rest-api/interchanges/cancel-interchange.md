---
title: Cancel Interchange
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of cancel-interchange REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Cancel Interchange

Cancel an outbound interchange that has not yet been delivered to the recipient.

## Endpoint

```http
POST /v2/interchanges/cancel/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | long | Yes | The unique ECGrid Interchange ID to cancel. |

:::caution
Only outbound interchanges that have **not yet been delivered** can be cancelled. Attempting to cancel an already-delivered or inbound interchange will return an error.
:::

## Response

Returns a boolean indicating whether the cancellation was successful.

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
curl -X POST "https://rest.ecgrid.io/v2/interchanges/cancel/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — cancel an outbound interchange before delivery
using var client = httpClientFactory.CreateClient("ECGrid");

var response = await client.PostAsync($"/v2/interchanges/cancel/{interchangeId}", null);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
if (result.Data)
{
    Console.WriteLine($"Interchange {interchangeId} successfully cancelled.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/interchanges/cancel/%s", id)))
    .header("X-API-Key", apiKey)
    .GET()
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
const url = `https://rest.ecgrid.io/v2/interchanges/cancel/${id}`;

const response = await fetch(url, {
  method: 'POST',
  headers: { 'X-API-Key': apiKey },
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
id = 0  # replace with actual id
url = f"https://rest.ecgrid.io/v2/interchanges/cancel/{id}"

response = requests.post(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Interchange](./get-interchange)
- [Resend Interchange](./resend-interchange)
- [Outbox List](./outbox-list)
