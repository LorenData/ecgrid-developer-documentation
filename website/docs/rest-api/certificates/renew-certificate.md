---
title: Renew Certificate
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Renew Certificate REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Renew Certificate

Renews an existing private certificate for a communication channel, generating a new key pair while preserving an overlap period for a graceful transition.

## Endpoint

```http
POST /v2/certificates/renew
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be a valid Comm ID | Communication channel whose certificate will be renewed |
| `certKeyId` | integer | Yes | Must match an existing cert | Unique identifier of the certificate to renew |
| `overlapDays` | integer | No | >= 0, default varies | Number of days the old certificate remains valid alongside the new one |
| `years` | integer | No | >= 1, default 2 | Validity period of the new certificate in years |
| `secureHashAlgorithm` | CertificateSecureHashAlgorithm | No | See ENUMs | Hashing algorithm for the renewed certificate |

```json
{
  "commId": 5001,
  "certKeyId": 88,
  "overlapDays": 30,
  "years": 2,
  "secureHashAlgorithm": "SHA256"
}
```

## Response

Returns the `CommIDInfo` object reflecting the renewed certificate.

```json
{
  "success": true,
  "data": {
    "commId": 5001,
    "mailboxId": 101,
    "commType": "as2",
    "identifier": "MYCOMPANY-AS2",
    "status": "Active",
    "useType": "Production",
    "privateKeyRequired": true,
    "withCerts": true
  }
}
```

## ENUMs

This endpoint uses the `CertificateSecureHashAlgorithm` ENUM. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/certificates/renew" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001, "certKeyId": 88, "overlapDays": 30, "years": 2, "secureHashAlgorithm": "SHA256" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Renew an expiring certificate with a 30-day overlap window
// The overlap window allows trading partners time to accept the new certificate
var request = new
{
    commId = 5001,
    certKeyId = 88,
    overlapDays = 30,
    years = 2,
    secureHashAlgorithm = "SHA256"
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/certificates/renew",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Certificate renewed for Comm {result.Data.CommId}.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001, \"certKeyId\": 88, \"overlapDays\": 30, \"years\": 2, \"secureHashAlgorithm\": \"SHA256\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/certificates/renew"))
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
const url = 'https://rest.ecgrid.io/v2/certificates/renew';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001, "certKeyId": 88, "overlapDays": 30, "years": 2, "secureHashAlgorithm": "SHA256" }),
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
url = "https://rest.ecgrid.io/v2/certificates/renew"

response = requests.post(
    url,
    json={ "commId": 5001, "certKeyId": 88, "overlapDays": 30, "years": 2, "secureHashAlgorithm": "SHA256" },
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
- [Terminate Certificate](./terminate-certificate)
- [Get Comm](../comms/get-comm)
- [ENUMs Reference](../../appendix/enums)
