---
title: Update Comm
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Update Comm REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Comm

Updates the identifier or status of an existing communication channel.

## Endpoint

```http
PUT /v2/comms/update
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be an existing Comm ID | Unique identifier of the communication channel to update |
| `identifier` | string | No | — | New channel-specific identifier (AS2 ID, FTP username, etc.) |
| `status` | Status | No | See ENUMs | New status for the channel (e.g., `Active`, `Suspended`) |

```json
{
  "commId": 5001,
  "identifier": "MYCOMPANY-AS2-NEW",
  "status": "Active"
}
```

## Response

Returns the updated `CommIDInfo` object.

```json
{
  "success": true,
  "data": {
    "commId": 5001,
    "mailboxId": 101,
    "commType": "as2",
    "identifier": "MYCOMPANY-AS2-NEW",
    "status": "Active",
    "useType": "Production",
    "privateKeyRequired": true,
    "withCerts": true
  }
}
```

## ENUMs

This endpoint uses the `Status` ENUM. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X PUT "https://rest.ecgrid.io/v2/comms/update" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001, "identifier": "MYCOMPANY-AS2-NEW", "status": "Active" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Update the AS2 identifier on an existing comm channel
var request = new
{
    commId = 5001,
    identifier = "MYCOMPANY-AS2-NEW"
};

using var response = await httpClient.PutAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/update",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Comm {result.Data.CommId} updated — Identifier: {result.Data.Identifier}, Status: {result.Data.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001, \"identifier\": \"MYCOMPANY-AS2-NEW\", \"status\": \"Active\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/update"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .PUT(HttpRequest.BodyPublishers.ofString(body))
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
const url = 'https://rest.ecgrid.io/v2/comms/update';

const response = await fetch(url, {
  method: 'PUT',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001, "identifier": "MYCOMPANY-AS2-NEW", "status": "Active" }),
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
url = "https://rest.ecgrid.io/v2/comms/update"

response = requests.put(
    url,
    json={ "commId": 5001, "identifier": "MYCOMPANY-AS2-NEW", "status": "Active" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Comm](./get-comm)
- [Create Comm](./create-comm)
- [Update Comm Config](./update-config)
- [ENUMs Reference](../../appendix/enums)
