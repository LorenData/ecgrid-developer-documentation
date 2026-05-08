---
title: Set X12 Delimiters
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created POST /v2/mailboxes/x12-delimiters reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Set X12 Delimiters

Configures the X12 EDI delimiter characters used by a mailbox for element, sub-element, and segment separation, overriding the parent network defaults.

## Endpoint

```http
POST /v2/mailboxes/x12-delimiters
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `mailboxId` | integer | Yes | — | ID of the mailbox to configure |
| `elementDelimiter` | string | Yes | Single character | Character used to separate data elements (typically `*`) |
| `subElementDelimiter` | string | Yes | Single character | Character used to separate composite sub-elements (typically `:` or `>`) |
| `segmentTerminator` | string | Yes | Single character | Character used to end each segment (typically `~`) |

```json
{
  "mailboxId": 5001,
  "elementDelimiter": "*",
  "subElementDelimiter": ">",
  "segmentTerminator": "~"
}
```

## Response

Returns a success indicator confirming the delimiter settings were saved.

```json
{
  "success": true,
  "data": null,
  "errorCode": null,
  "message": "X12 delimiters updated."
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/mailboxes/x12-delimiters" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "mailboxId": 5001, "elementDelimiter": "*", "subElementDelimiter": ">", "segmentTerminator": "~" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — set mailbox-level X12 delimiters (overrides network defaults)
var payload = new
{
    mailboxId = 5001,
    elementDelimiter = "*",
    subElementDelimiter = ">",
    segmentTerminator = "~"
};

var request = new HttpRequestMessage(HttpMethod.Post, "https://rest.ecgrid.io/v2/mailboxes/x12-delimiters")
{
    Content = JsonContent.Create(payload)
};
request.Headers.Add("X-API-Key", configuration["ECGrid:ApiKey"]);

var response = await httpClient.SendAsync(request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<object>>();
Console.WriteLine($"Delimiter update succeeded: {result?.Success}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"mailboxId\": 5001, \"elementDelimiter\": \"*\", \"subElementDelimiter\": \">\", \"segmentTerminator\": \"~\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/x12-delimiters"))
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
const url = 'https://rest.ecgrid.io/v2/mailboxes/x12-delimiters';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "mailboxId": 5001, "elementDelimiter": "*", "subElementDelimiter": ">", "segmentTerminator": "~" }),
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
url = "https://rest.ecgrid.io/v2/mailboxes/x12-delimiters"

response = requests.post(
    url,
    json={ "mailboxId": 5001, "elementDelimiter": "*", "subElementDelimiter": ">", "segmentTerminator": "~" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Update Mailbox Config](./update-config)
- [Network X12 Delimiters](../networks/x12-delimiters)
- [Get Mailbox](./get-mailbox)
