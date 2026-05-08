---
title: Get Interchange Header
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of get-header REST API doc - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Get Interchange Header

Parse a raw ISA header string into its individual component fields.

## Endpoint

```http
POST /v2/interchanges/get-header
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `interchangeHeader` | string | Yes | Must be a valid ISA segment string | The raw ISA interchange header string to parse. |

```json
{
  "interchangeHeader": "ISA*00*          *00*          *ZZ*ACMECORP       *ZZ*BUYERINC       *260501*1030*^*00501*000000001*0*P*>"
}
```

## Response

Returns a structured object containing the parsed fields from the ISA header, including sender and receiver qualifiers and IDs, interchange date and time, control number, and acknowledgment/usage flags.

```json
{
  "success": true,
  "data": {
    "authorizationInfoQualifier": "00",
    "authorizationInfo": "          ",
    "securityInfoQualifier": "00",
    "securityInfo": "          ",
    "senderIdQualifier": "ZZ",
    "senderId": "ACMECORP       ",
    "receiverIdQualifier": "ZZ",
    "receiverId": "BUYERINC       ",
    "interchangeDate": "260501",
    "interchangeTime": "1030",
    "repetitionSeparator": "^",
    "controlVersionNumber": "00501",
    "controlNumber": "000000001",
    "acknowledgmentRequested": "0",
    "usageIndicator": "P",
    "componentElementSeparator": ">"
  }
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/interchanges/get-header" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "interchangeHeader": "ISA*00* *00* *ZZ*ACMECORP *ZZ*BUYERINC *260501*1030*^*00501*000000001*0*P*>" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — parse an ISA header string into its component fields
using var client = httpClientFactory.CreateClient("ECGrid");

var requestBody = new { interchangeHeader = isaHeaderString };

var response = await client.PostAsJsonAsync("/v2/interchanges/get-header", requestBody);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<InterchangeHeaderInfo>>();
Console.WriteLine($"Sender: {result.Data.SenderIdQualifier}:{result.Data.SenderId.Trim()}");
Console.WriteLine($"Receiver: {result.Data.ReceiverIdQualifier}:{result.Data.ReceiverId.Trim()}");
Console.WriteLine($"Control Number: {result.Data.ControlNumber}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"interchangeHeader\": \"ISA*00* *00* *ZZ*ACMECORP *ZZ*BUYERINC *260501*1030*^*00501*000000001*0*P*>\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/interchanges/get-header"))
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
const url = 'https://rest.ecgrid.io/v2/interchanges/get-header';

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
url = "https://rest.ecgrid.io/v2/interchanges/get-header"

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

- [Get Interchange Date](./get-date)
- [Get Interchange](./get-interchange)
- [Inbox List](./inbox-list)
