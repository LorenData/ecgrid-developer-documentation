---
title: Get Interchange Date
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of get-date REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Interchange Date

Parse and return the date from a raw ISA interchange header string.

## Endpoint

```http
POST /v2/interchanges/get-date
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `interchangeHeader` | string | Yes | Must be a valid ISA segment string | Raw ISA header string to parse the interchange date from. |

```json
{
  "interchangeHeader": "ISA*00*          *00*          *ZZ*ACMECORP       *ZZ*BUYERINC       *260501*1030*^*00501*000000001*0*P*>"
}
```

## Response

Returns the interchange date extracted from the ISA header as a datetime value.

```json
{
  "success": true,
  "data": "2026-05-01T10:30:00Z"
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/interchanges/get-date" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "interchangeHeader": "ISA*00* *00* *ZZ*ACMECORP *ZZ*BUYERINC *260501*1030*^*00501*000000001*0*P*>" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — extract the date from a raw ISA header string
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new { interchangeHeader = isaHeaderString };

var response = await client.PostAsJsonAsync("/v2/interchanges/get-date", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<DateTime>>();
Console.WriteLine($"Interchange date: {result.Data:O}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"interchangeHeader\": \"ISA*00* *00* *ZZ*ACMECORP *ZZ*BUYERINC *260501*1030*^*00501*000000001*0*P*>\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/interchanges/get-date"))
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
const url = 'https://rest.ecgrid.io/v2/interchanges/get-date';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "interchangeHeader": "ISA*00* *00* *ZZ*ACMECORP *ZZ*BUYERINC *260501*1030*^*00501*000000001*0*P*>" }),
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
url = "https://rest.ecgrid.io/v2/interchanges/get-date"

response = requests.post(
    url,
    json={ "interchangeHeader": "ISA*00* *00* *ZZ*ACMECORP *ZZ*BUYERINC *260501*1030*^*00501*000000001*0*P*>" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Get Interchange Header](./get-header)
- [Get Interchange](./get-interchange)
- [Inbox List](./inbox-list)
