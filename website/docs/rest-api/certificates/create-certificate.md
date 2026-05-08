---
title: Create Certificate
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Create Certificate REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Create Certificate

Generates a new private certificate for a communication channel, creating the key pair on the ECGrid platform.

## Endpoint

```http
POST /v2/certificates/create
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be a valid Comm ID | Communication channel to associate the new certificate with |
| `beginUsage` | datetime | No | ISO 8601 | Date and time when the certificate becomes active |
| `usage` | CertificateUsage | No | See ENUMs | Intended usage (Encryption, Signature, or EncryptionAndSignature) |
| `secureHashAlgorithm` | CertificateSecureHashAlgorithm | No | See ENUMs | Hashing algorithm for the certificate (SHA1, SHA256, SHA384, SHA512) |
| `partnerAs2Id` | string | No | — | Partner's AS2 identifier to embed in the certificate |
| `expires` | datetime | No | ISO 8601 | Certificate expiration date |

```json
{
  "commId": 5001,
  "beginUsage": "2026-05-07T00:00:00Z",
  "usage": "EncryptionAndSignature",
  "secureHashAlgorithm": "SHA256",
  "partnerAs2Id": "PARTNER-AS2-ID",
  "expires": "2028-05-07T00:00:00Z"
}
```

## Response

Returns the `CommIDInfo` object with the newly generated certificate details.

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

This endpoint uses the `CertificateUsage` and `CertificateSecureHashAlgorithm` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

### CertificateSecureHashAlgorithm

| Value | Description |
|---|---|
| `SHA1` | SHA-1 hashing — established, not recommended for new certificates |
| `SHA256` | SHA-256 hashing — recommended minimum for new certificates |
| `SHA384` | SHA-384 hashing |
| `SHA512` | SHA-512 hashing — strongest available option |

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/certificates/create" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001, "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "secureHashAlgorithm": "SHA256", "partnerAs2Id": "PARTNER-AS2-ID", "expires": "2028-05-07T00:00:00Z" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Generate a new private certificate on the ECGrid platform
// Platform generates the key pair; use SHA256 or higher for new certificates
var request = new
{
    commId = 5001,
    beginUsage = DateTime.UtcNow.ToString("o"),
    usage = "EncryptionAndSignature",
    secureHashAlgorithm = "SHA256",
    partnerAs2Id = "PARTNER-AS2-ID",
    expires = DateTime.UtcNow.AddYears(2).ToString("o")
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/certificates/create",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Certificate created for Comm {result.Data.CommId}.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001, \"beginUsage\": \"2026-05-07T00:00:00Z\", \"usage\": \"EncryptionAndSignature\", \"secureHashAlgorithm\": \"SHA256\", \"partnerAs2Id\": \"PARTNER-AS2-ID\", \"expires\": \"2028-05-07T00:00:00Z\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/certificates/create"))
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
const url = 'https://rest.ecgrid.io/v2/certificates/create';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001, "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "secureHashAlgorithm": "SHA256", "partnerAs2Id": "PARTNER-AS2-ID", "expires": "2028-05-07T00:00:00Z" }),
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
url = "https://rest.ecgrid.io/v2/certificates/create"

response = requests.post(
    url,
    json={ "commId": 5001, "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "secureHashAlgorithm": "SHA256", "partnerAs2Id": "PARTNER-AS2-ID", "expires": "2028-05-07T00:00:00Z" },
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
- [Renew Certificate](./renew-certificate)
- [Terminate Certificate](./terminate-certificate)
- [Get Comm](../comms/get-comm)
- [ENUMs Reference](../../appendix/enums)
