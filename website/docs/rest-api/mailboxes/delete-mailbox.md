---
title: Delete Mailbox
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created DELETE /v2/mailboxes/{id} reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Delete Mailbox

Permanently terminates a mailbox by its numeric ID.

## Endpoint

```http
DELETE /v2/mailboxes/{id}
```

:::danger Irreversible Operation
This permanently terminates the mailbox and all associated data. This cannot be undone. Ensure all trading partner interconnects, callbacks, and pending parcels have been resolved before calling this endpoint.
:::

## Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | Unique numeric identifier of the mailbox to delete |

## Response

Returns a success indicator confirming the mailbox has been terminated.

```json
{
  "success": true,
  "data": null,
  "errorCode": null,
  "message": "Mailbox terminated."
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X DELETE "https://rest.ecgrid.io/v2/mailboxes/$ID" \
  -H "X-API-Key: $ECGRID_API_KEY"
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — permanently delete a mailbox (irreversible — confirm before calling)
var mailboxId = 5002;
var request = new HttpRequestMessage(HttpMethod.Delete, $"https://rest.ecgrid.io/v2/mailboxes/{mailboxId}");
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<object>>();
Console.WriteLine($"Mailbox {mailboxId} deleted: {result?.Success}");
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
    .DELETE()
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
  method: 'DELETE',
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

response = requests.delete(url, headers=headers)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Mailbox](./get-mailbox)
- [Create Mailbox](./create-mailbox)
- [List Mailboxes](./list-mailboxes)
