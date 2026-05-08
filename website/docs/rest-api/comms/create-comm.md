---
title: Create Comm
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Create Comm REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Comm

Creates a new communication channel for a mailbox, defining the technical connection details for EDI delivery via AS2, FTP, SFTP, or another supported protocol.

## Endpoint

```http
POST /v2/comms/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | Yes | Must be a valid mailbox | Mailbox to associate the new communication channel with |
| `commType` | NetworkGatewayCommChannel | Yes | See ENUMs | Protocol type for the channel (e.g., `as2`, `sftp`, `ftp`) |
| `identifier` | string | Yes | — | Channel-specific identifier (AS2 ID, FTP username, SFTP host, etc.) |
| `useType` | UseType | No | See ENUMs | Intended use — Test, Production, or TestAndProduction |

```json
{
  "mailboxId": 101,
  "commType": "as2",
  "identifier": "MYCOMPANY-AS2",
  "useType": "Production"
}
```

## Response

Returns the newly created `CommIDInfo` object.

```json
{
  "success": true,
  "data": {
    "commId": 5010,
    "mailboxId": 101,
    "commType": "as2",
    "identifier": "MYCOMPANY-AS2",
    "status": "Active",
    "useType": "Production",
    "privateKeyRequired": false,
    "withCerts": false
  }
}
```

## ENUMs

This endpoint uses the `NetworkGatewayCommChannel` and `UseType` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/comms/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 101, "commType": "as2", "identifier": "MYCOMPANY-AS2", "useType": "Production" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Create a new AS2 communication channel for a mailbox
var request = new
{
    mailboxId = 101,
    commType = "as2",
    identifier = "MYCOMPANY-AS2",
    useType = "Production"
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/comms/create",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Created Comm ID: {result.Data.CommId} — Type: {result.Data.CommType}, Identifier: {result.Data.Identifier}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 101, \"commType\": \"as2\", \"identifier\": \"MYCOMPANY-AS2\", \"useType\": \"Production\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/comms/create"))
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
const url = 'https://rest.ecgrid.io/v2/comms/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 101, "commType": "as2", "identifier": "MYCOMPANY-AS2", "useType": "Production" }),
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
url = "https://rest.ecgrid.io/v2/comms/create"

response = requests.post(
    url,
    json={ "mailboxId": 101, "commType": "as2", "identifier": "MYCOMPANY-AS2", "useType": "Production" },
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
- [List Comms](./list-comms)
- [Update Comm](./update-comm)
- [Update Comm Config](./update-config)
- [Add Private Certificate](../certificates/add-private)
- [ENUMs Reference](../../appendix/enums)
