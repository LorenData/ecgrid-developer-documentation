---
title: Create Portal
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Portals / Create Portal REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Portal

Creates a new customer-facing web portal configuration and links it to the specified ECGrid mailbox.

## Endpoint

```http
POST /v2/portals/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | int | Yes | Must be a valid mailbox ID | The mailbox to associate with the new portal |

```json
{
  "mailboxId": 7890
}
```

## Response

Returns the newly created portal record including its assigned ID and URL.

```json
{
  "success": true,
  "data": {
    "portalId": 502,
    "mailboxId": 7890,
    "url": "https://portal.ecgrid.io/new-portal-slug",
    "status": "Active",
    "created": "2026-05-07T09:00:00Z"
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `portalId` | int | Unique identifier for the newly created portal |
| `mailboxId` | int | The mailbox this portal is linked to |
| `url` | string | The public-facing URL for the customer portal |
| `status` | string | Initial status of the portal upon creation |
| `created` | datetime | UTC timestamp when the portal was created |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/portals/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 7890 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Create a new portal for a given mailbox
using System.Net.Http.Json;

var request = new { mailboxId = 7890 };

var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/portals/create",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<PortalInfo>>();
Console.WriteLine($"Portal created — ID: {result?.Data?.PortalId}");
Console.WriteLine($"Portal URL: {result?.Data?.Url}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 7890 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/portals/create"))
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
const url = 'https://rest.ecgrid.io/v2/portals/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 7890 }),
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
url = "https://rest.ecgrid.io/v2/portals/create"

response = requests.post(
    url,
    json={ "mailboxId": 7890 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Portal by Mailbox](./get-portal-by-mailbox)
- [Create Mailbox](../mailboxes/create-mailbox)
- [Get Mailbox](../mailboxes/get-mailbox)
