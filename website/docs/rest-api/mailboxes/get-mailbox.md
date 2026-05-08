---
title: Get Mailbox
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created GET /v2/mailboxes/{id} reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Mailbox

Retrieves detailed information for a single ECGrid mailbox by its numeric ID.

## Endpoint

```http
GET /v2/mailboxes/{id}
```

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | Unique numeric identifier of the mailbox |

## Response

Returns a `MailboxIDInfo` object for the requested mailbox.

```json
{
  "success": true,
  "data": {
    "mailboxId": 5001,
    "networkId": 1001,
    "uniqueId": "ACMEMBOX01",
    "companyName": "Acme Mailbox One",
    "status": "Active",
    "created": "2021-06-10T09:00:00Z",
    "modified": "2025-02-14T11:30:00Z"
  },
  "errorCode": null,
  "message": null
}
```

## ENUMs

### Status

The `status` field uses the `Status` enum. See the full value table in [Appendix: ENUMs](../../appendix/enums#status).

| Value | Description |
|---|---|
| `Development` | Mailbox is in development/testing |
| `Active` | Mailbox is live and operational |
| `Preproduction` | Staging state before go-live |
| `Suspended` | Temporarily disabled |
| `Terminated` | Permanently closed |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X GET "https://rest.ecgrid.io/v2/mailboxes/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — retrieve a mailbox by ID
var mailboxId = 5001;
var request = new HttpRequestMessage(HttpMethod.Get, $"https://rest.ecgrid.io/v2/mailboxes/{mailboxId}");
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<MailboxIdInfo>>();
Console.WriteLine($"Mailbox: {result?.Data?.CompanyName} — Status: {result?.Data?.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");
String id = "0"; // replace with actual id

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(String.format("https://rest.ecgrid.io/v2/mailboxes/%s", id)))
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
const url = `https://rest.ecgrid.io/v2/mailboxes/${id}`;

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
id = 0  # replace with actual id
url = f"https://rest.ecgrid.io/v2/mailboxes/{id}"

response = requests.get(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [List Mailboxes](./list-mailboxes)
- [Create Mailbox](./create-mailbox)
- [Update Mailbox](./update-mailbox)
- [Delete Mailbox](./delete-mailbox)
- [Appendix: ENUMs](../../appendix/enums)
