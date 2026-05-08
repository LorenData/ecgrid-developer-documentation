---
title: Create Carbon Copy
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Create Carbon Copy REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Carbon Copy

Creates a new carbon copy rule that automatically duplicates EDI traffic from one mailbox to another.

## Endpoint

```http
POST /v2/carboncopies/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `fromMailboxId` | integer | Yes | Must be a valid mailbox | Source mailbox whose traffic will be duplicated |
| `toMailboxId` | integer | Yes | Must be a valid mailbox | Destination mailbox that receives the duplicated traffic |
| `direction` | Direction | Yes | See ENUMs | Traffic direction to duplicate — InBox, OutBox, or NoDir (both) |

```json
{
  "fromMailboxId": 101,
  "toMailboxId": 202,
  "direction": "InBox"
}
```

## Response

Returns the newly created carbon copy rule.

```json
{
  "success": true,
  "data": {
    "ccId": 1043,
    "fromMailboxId": 101,
    "toMailboxId": 202,
    "status": "Active",
    "direction": "InBox",
    "created": "2026-05-07T14:00:00Z"
  }
}
```

## ENUMs

This endpoint uses the `Direction` ENUM. See [ENUMs Reference](../../appendix/enums) for all valid values.

### Direction (summary)

| Value | Description |
|---|---|
| `InBox` | Copies inbound traffic received by the source mailbox |
| `OutBox` | Copies outbound traffic sent from the source mailbox |
| `NoDir` | Copies both inbound and outbound traffic |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/carboncopies/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "fromMailboxId": 101, "toMailboxId": 202, "direction": "InBox" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Create a new carbon copy rule
var request = new
{
    fromMailboxId = 101,
    toMailboxId = 202,
    direction = "InBox"
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/carboncopies/create",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CarbonCopyInfo>>();
Console.WriteLine($"Created CC Rule ID: {result.Data.CcId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"fromMailboxId\": 101, \"toMailboxId\": 202, \"direction\": \"InBox\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/carboncopies/create"))
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
const url = 'https://rest.ecgrid.io/v2/carboncopies/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "fromMailboxId": 101, "toMailboxId": 202, "direction": "InBox" }),
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
url = "https://rest.ecgrid.io/v2/carboncopies/create"

response = requests.post(
    url,
    json={ "fromMailboxId": 101, "toMailboxId": 202, "direction": "InBox" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Carbon Copy](./get-carbon-copy)
- [List Carbon Copies](./list-carbon-copies)
- [Update Carbon Copy](./update-carbon-copy)
- [Delete Carbon Copy](./delete-carbon-copy)
- [ENUMs Reference](../../appendix/enums)
