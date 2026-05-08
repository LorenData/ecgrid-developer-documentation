---
title: Terminate Certificate
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Terminate Certificate REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Terminate Certificate

Permanently terminates a certificate associated with a communication channel, revoking its use for AS2 or encryption operations.

:::danger Irreversible Action
Terminating a certificate used for active AS2 connections will immediately break EDI delivery for that channel. Ensure the trading partner has accepted a replacement certificate before terminating the existing one, or use the overlap period provided by [Renew Certificate](./renew-certificate).
:::

## Endpoint

```http
POST /v2/certificates/terminate
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be a valid Comm ID | Communication channel whose certificate will be terminated |
| `certKeyId` | integer | Yes | Must match an existing cert | Unique identifier of the certificate to terminate |

```json
{
  "commId": 5001,
  "certKeyId": 88
}
```

## Response

Returns a success boolean confirming the certificate has been terminated.

```json
{
  "success": true,
  "data": true
}
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/certificates/terminate" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001, "certKeyId": 88 }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Terminate a certificate after confirming a replacement is active
// Verify the replacement certificate is accepted by all trading partners before calling this
var request = new
{
    commId = 5001,
    certKeyId = 88
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/certificates/terminate",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<bool>>();

if (result.Data)
{
    Console.WriteLine($"Certificate {88} on Comm {5001} has been terminated.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001, \"certKeyId\": 88 }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/certificates/terminate"))
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
const url = 'https://rest.ecgrid.io/v2/certificates/terminate';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001, "certKeyId": 88 }),
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
url = "https://rest.ecgrid.io/v2/certificates/terminate"

response = requests.post(
    url,
    json={ "commId": 5001, "certKeyId": 88 },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Add Private Certificate](./add-private)
- [Add Public Certificate](./add-public)
- [Create Certificate](./create-certificate)
- [Renew Certificate](./renew-certificate)
- [Get Comm](../comms/get-comm)
