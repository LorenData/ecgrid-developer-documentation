---
title: Update Mailbox
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/mailboxes/update reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Mailbox

Updates the profile information for an existing mailbox.

## Endpoint

```http
POST /v2/mailboxes/update
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | Yes | — | ID of the mailbox to update |
| `companyName` | string | No | — | Updated display name for the mailbox |

> Additional optional fields (address, phone, etc.) follow the same shape as the network update. Refer to the live [Swagger UI](https://rest.ecgrid.io/swagger/index.html) for the complete field list.

```json
{
  "mailboxId": 5001,
  "companyName": "Acme Mailbox One — Updated"
}
```

## Response

Returns the updated `MailboxIDInfo` object reflecting the saved values.

```json
{
  "success": true,
  "data": {
    "mailboxId": 5001,
    "networkId": 1001,
    "uniqueId": "ACMEMBOX01",
    "companyName": "Acme Mailbox One — Updated",
    "status": "Active",
    "created": "2021-06-10T09:00:00Z",
    "modified": "2026-05-07T10:45:00Z"
  },
  "errorCode": null,
  "message": null
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/mailboxes/update" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 5001, "companyName": "Acme Mailbox One — Updated" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — update the display name of a mailbox
var payload = new
{
    mailboxId = 5001,
    companyName = "Acme Mailbox One — Updated"
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/mailboxes/update")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxIdInfo>>();
Console.WriteLine($"Updated: {result?.Data?.CompanyName} at {result?.Data?.Modified}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 5001, \"companyName\": \"Acme Mailbox One — Updated\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/update"))
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
const url = 'https://rest.ecgrid.io/v2/mailboxes/update';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 5001, "companyName": "Acme Mailbox One — Updated" }),
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
url = "https://rest.ecgrid.io/v2/mailboxes/update"

response = requests.post(
    url,
    json={ "mailboxId": 5001, "companyName": "Acme Mailbox One — Updated" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Mailbox](./get-mailbox)
- [Update Mailbox Config](./update-config)
- [Delete Mailbox](./delete-mailbox)
