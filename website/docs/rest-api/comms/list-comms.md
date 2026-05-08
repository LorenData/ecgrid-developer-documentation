---
title: List Comms
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of List Comms REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# List Comms

Returns a list of communication channels, optionally filtered by type, use type, and other criteria.

## Endpoint

```http
POST /v2/comms/list
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commType` | NetworkGatewayCommChannel | No | See ENUMs | Filter by channel type (e.g., `as2`, `sftp`, `ftp`) |
| `privateKeyRequired` | boolean | No | — | When `true`, returns only channels that require a private key |
| `useType` | UseType | No | See ENUMs | Filter by intended use (Test, Production, TestAndProduction) |
| `showInactive` | boolean | No | Default `false` | When `true`, includes suspended and terminated channels |
| `withCerts` | boolean | No | — | When `true`, returns only channels that have certificates attached |

```json
{
  "commType": "as2",
  "useType": "Production",
  "showInactive": false,
  "withCerts": true
}
```

## Response

Returns an array of `CommIDInfo` objects matching the specified filters.

```json
{
  "success": true,
  "data": [
    {
      "commId": 5001,
      "mailboxId": 101,
      "commType": "as2",
      "identifier": "MYCOMPANY-AS2",
      "status": "Active",
      "useType": "Production",
      "privateKeyRequired": true,
      "withCerts": true
    },
    {
      "commId": 5002,
      "mailboxId": 102,
      "commType": "as2",
      "identifier": "DIVISION-AS2",
      "status": "Active",
      "useType": "Production",
      "privateKeyRequired": true,
      "withCerts": true
    }
  ]
}
```

## ENUMs

This endpoint uses the `NetworkGatewayCommChannel` and `UseType` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/comms/list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commType": "as2", "useType": "Production", "showInactive": false, "withCerts": true }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — List all active AS2 production comm channels
var request = new
{
    commType = "as2",
    useType = "Production",
    showInactive = false
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/list",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<CommIdInfo>>>();
Console.WriteLine($"Found {result.Data.Count} AS2 production comm channel(s).");

foreach (var comm in result.Data)
{
    Console.WriteLine($"  Comm {comm.CommId}: {comm.Identifier} on Mailbox {comm.MailboxId}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commType\": \"as2\", \"useType\": \"Production\", \"showInactive\": false, \"withCerts\": true }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/list"))
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
const url = 'https://rest.ecgrid.io/v2/comms/list';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commType": "as2", "useType": "Production", "showInactive": false, "withCerts": true }),
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
url = "https://rest.ecgrid.io/v2/comms/list"

response = requests.post(
    url,
    json={ "commType": "as2", "useType": "Production", "showInactive": false, "withCerts": true },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Comm](./get-comm)
- [Find Comm](./find-comm)
- [Create Comm](./create-comm)
- [Update Comm](./update-comm)
- [ENUMs Reference](../../appendix/enums)
