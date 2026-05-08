---
title: Update Data Email
sidebar_position: 11
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create POST /v2/ids/tp-update-data-email REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Update Data Email

Sets or updates the data delivery email address and email delivery options for a trading partner ECGrid ID.

## Endpoint

```http
POST /v2/ids/tp-update-data-email
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `ecGridId` | integer | Yes | Must be a valid ECGrid ID | The ECGrid ID to update |
| `email` | string | Yes | Valid email address | Email address for data delivery notifications |
| `emailSystem` | string | No | See `EMailSystem` enum | Email protocol to use |
| `emailPayload` | string | No | See `EMailPayload` enum | How EDI data is delivered in the email |

```json
{
  "ecGridId": 123456,
  "email": "edi@acmecorp.com",
  "emailSystem": "smtp",
  "emailPayload": "Attachment"
}
```

## Response

Returns a success boolean confirming the email configuration update.

```json
{
  "success": true,
  "data": true
}
```

## ENUMs

### EMailSystem

| Value | Description |
|---|---|
| `smtp` | Standard SMTP email delivery |
| `x400` | X.400 messaging system |

### EMailPayload

| Value | Description |
|---|---|
| `Body` | EDI data delivered inline in the email body |
| `Attachment` | EDI data delivered as an email attachment |

See [Enums reference](../../appendix/enums) for complete enum definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/ids/tp-update-data-email" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "ecGridId": 123456, "email": "edi@acmecorp.com", "emailSystem": "smtp", "emailPayload": "Attachment" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — configure data email delivery for a trading partner ID
using var client = httpClientFactory.CreateClient("ECGrid");

var request = new
{
    ecGridId = 123456,
    email = "edi@acmecorp.com",
    emailSystem = "smtp",
    emailPayload = "Attachment"
};

var response = await client.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/ids/tp-update-data-email", request);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();
Console.WriteLine($"Data email updated: {result!.Data}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"ecGridId\": 123456, \"email\": \"edi@acmecorp.com\", \"emailSystem\": \"smtp\", \"emailPayload\": \"Attachment\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/tp-update-data-email"))
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
const url = 'https://rest.ecgrid.io/v2/ids/tp-update-data-email';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "ecGridId": 123456, "email": "edi@acmecorp.com", "emailSystem": "smtp", "emailPayload": "Attachment" }),
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
url = "https://rest.ecgrid.io/v2/ids/tp-update-data-email"

response = requests.post(
    url,
    json={ "ecGridId": 123456, "email": "edi@acmecorp.com", "emailSystem": "smtp", "emailPayload": "Attachment" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get ID](get-id)
- [Update Description](update-description)
- [Update Config](update-config)
