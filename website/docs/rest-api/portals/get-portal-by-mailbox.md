---
title: Get Portal by Mailbox
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Portals / Get Portal by Mailbox REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Portal by Mailbox

Retrieves the portal configuration associated with a specific ECGrid mailbox.

## Endpoint

```http
GET /v2/portals/by-mailbox/{mailboxId}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `mailboxId` | int | Yes | The ID of the mailbox whose portal configuration should be retrieved |

## Response

Returns the portal record linked to the specified mailbox, including the portal URL and current status.

```json
{
  "success": true,
  "data": {
    "portalId": 501,
    "mailboxId": 7890,
    "url": "https://portal.ecgrid.io/company-name",
    "status": "Active",
    "created": "2024-09-01T12:00:00Z"
  }
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `portalId` | int | Unique identifier for the portal record |
| `mailboxId` | int | The mailbox this portal is associated with |
| `url` | string | The public-facing URL for the customer portal |
| `status` | string | Current status of the portal (e.g., `Active`, `Suspended`) |
| `created` | datetime | UTC timestamp when the portal was created |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/portals/by-mailbox/$MAILBOX_ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Retrieve the portal configuration for a given mailbox
using System.Net.Http.Json;

int mailboxId = 7890;

var response = await httpClient.GetAsync(
    $"https://rest.ecgrid.io/v2/portals/by-mailbox/{mailboxId}");

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<PortalInfo>>();
Console.WriteLine($"Portal URL: {result?.Data?.Url}");
Console.WriteLine($"Status: {result?.Data?.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String mailboxId = "0"; // replace with actual mailboxId

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/portals/by-mailbox/%s", mailboxId)))
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
const url = `https://rest.ecgrid.io/v2/portals/by-mailbox/${mailboxId}`;

const response = await fetch(url, {
  method: 'GET',
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
mailbox_id = 0  # replace with actual mailbox_id
url = f"https://rest.ecgrid.io/v2/portals/by-mailbox/{mailbox_id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Create Portal](./create-portal)
- [Get Mailbox](../mailboxes/get-mailbox)
