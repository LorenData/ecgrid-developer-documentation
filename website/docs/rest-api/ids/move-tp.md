---
title: Move Trading Partner
sidebar_position: 10
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids/tp-move REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Move Trading Partner

Moves a trading partner ECGrid ID from its current mailbox to a different mailbox.

## Endpoint

```http
POST /v2/ids/tp-move
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridId` | integer | Yes | Must be a valid ECGrid ID | The ECGrid ID to move |
| `newMailboxId` | integer | Yes | Must be a valid mailbox within the same network | The destination mailbox |

```json
{
  "ecGridId": 123456,
  "newMailboxId": 1002
}
```

## Response

Returns the updated `ECGridIDInfo` object reflecting the new mailbox assignment.

```json
{
  "success": true,
  "data": {
    "ecGridId": 123456,
    "mailboxId": 1002,
    "networkId": 42,
    "qualifier": "01",
    "id": "PARTNER001",
    "description": "Acme Corp Production",
    "status": "Active",
    "routingGroup": "ProductionA",
    "ediStandard": "X12"
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/ids/tp-move" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridId": 123456, "newMailboxId": 1002 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — move a trading partner ID to a different mailbox
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridId = 123456,
    newMailboxId = 1002
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/ids/tp-move", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<ECGridIDInfo>>();
Console.WriteLine($"Moved to mailbox: {result!.Data.MailboxId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridId\": 123456, \"newMailboxId\": 1002 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/tp-move"))
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
const url = 'https://rest.ecgrid.io/v2/ids/tp-move';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridId": 123456, "newMailboxId": 1002 }),
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
url = "https://rest.ecgrid.io/v2/ids/tp-move"

response = requests.post(
    url,
    json={ "ecGridId": 123456, "newMailboxId": 1002 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Get Mailbox Default](get-mailbox-default)
- [List IDs](list-ids)
