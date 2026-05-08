---
title: Create Mailbox
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/mailboxes/create reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Mailbox

Creates a new mailbox under the specified network.

## Endpoint

```http
POST /v2/mailboxes/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `networkId` | integer | Yes | — | ID of the parent network that will own this mailbox |
| `uniqueId` | string | Yes | Max 12 characters, alphanumeric | Short unique identifier for this mailbox within the network |
| `companyName` | string | Yes | — | Display name for the mailbox / company |

```json
{
  "networkId": 1001,
  "uniqueId": "ACMEMBOX02",
  "companyName": "Acme Mailbox Two"
}
```

## Response

Returns the newly created `MailboxIDInfo` object, including the system-assigned `mailboxId`.

```json
{
  "success": true,
  "data": {
    "mailboxId": 5002,
    "networkId": 1001,
    "uniqueId": "ACMEMBOX02",
    "companyName": "Acme Mailbox Two",
    "status": "Active",
    "created": "2026-05-07T10:00:00Z",
    "modified": "2026-05-07T10:00:00Z"
  },
  "errorCode": null,
  "message": null
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/mailboxes/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "networkId": 1001, "uniqueId": "ACMEMBOX02", "companyName": "Acme Mailbox Two" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — create a new mailbox under an existing network
var payload = new
{
    networkId = 1001,
    uniqueId = "ACMEMBOX02",
    companyName = "Acme Mailbox Two"
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/mailboxes/create")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxIdInfo>>();
Console.WriteLine($"Created mailbox ID: {result?.Data?.MailboxId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"networkId\": 1001, \"uniqueId\": \"ACMEMBOX02\", \"companyName\": \"Acme Mailbox Two\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/create"))
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
const url = 'https://rest.ecgrid.io/v2/mailboxes/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "networkId": 1001, "uniqueId": "ACMEMBOX02", "companyName": "Acme Mailbox Two" }),
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
url = "https://rest.ecgrid.io/v2/mailboxes/create"

response = requests.post(
    url,
    json={ "networkId": 1001, "uniqueId": "ACMEMBOX02", "companyName": "Acme Mailbox Two" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Mailbox](./get-mailbox)
- [Update Mailbox](./update-mailbox)
- [Delete Mailbox](./delete-mailbox)
- [Common Operations: Create a Mailbox](../../common-operations/create-a-mailbox)
