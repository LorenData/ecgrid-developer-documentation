---
title: Add Public Certificate
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Add Public Certificate REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Add Public Certificate

Uploads and associates a trading partner's public certificate with a communication channel for AS2 signature verification or encryption.

## Endpoint

```http
POST /v2/certificates/add-public
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be a valid Comm ID | Communication channel to associate the public certificate with |
| `certType` | CertificateType | Yes | See ENUMs | Type of certificate (X509, PGP, SSH) |
| `keyId` | string | No | — | Key identifier for the partner's certificate |
| `userId` | string | No | — | User identifier associated with this certificate |
| `beginUsage` | datetime | No | ISO 8601 | Date and time when the certificate becomes active |
| `usage` | CertificateUsage | No | See ENUMs | Intended usage (Encryption, Signature, etc.) |
| `partnerCommId` | string | No | — | Partner's AS2 communication identifier |
| `partnerUrl` | string | No | Valid URL | Partner's AS2 endpoint URL |
| `cert` | string | No | Base64-encoded | The partner's public certificate encoded as Base64 |

```json
{
  "commId": 5001,
  "certType": "X509",
  "keyId": "partner-public-cert-2026",
  "userId": "partner-edi",
  "beginUsage": "2026-05-07T00:00:00Z",
  "usage": "EncryptionAndSignature",
  "partnerCommId": "PARTNER-AS2-ID",
  "partnerUrl": "https://as2.tradingpartner.com/receive",
  "cert": "MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3Df..."
}
```

## Response

Returns the updated `CommIDInfo` object reflecting the newly associated public certificate.

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

This endpoint uses the `CertificateType` and `CertificateUsage` ENUMs. See [ENUMs Reference](../../appendix/enums) for all valid values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -X POST "https://rest.ecgrid.io/v2/certificates/add-public" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001, "certType": "X509", "keyId": "partner-public-cert-2026", "userId": "partner-edi", "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "partnerCommId": "PARTNER-AS2-ID", "partnerUrl": "https://as2.tradingpartner.com/receive", "cert": "MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3Df..." }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Upload a trading partner's public certificate to a comm channel
// Public certificate is typically received from the partner as a .cer or .pem file
var certBytes = await File.ReadAllBytesAsync("path/to/partner-public.cer");
var certBase64 = Convert.ToBase64String(certBytes);

var request = new
{
    commId = 5001,
    certType = "X509",
    keyId = "partner-public-cert-2026",
    userId = "partner-edi",
    beginUsage = DateTime.UtcNow.ToString("o"),
    usage = "EncryptionAndSignature",
    partnerCommId = "PARTNER-AS2-ID",
    partnerUrl = "https://as2.tradingpartner.com/receive",
    cert = certBase64
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/certificates/add-public",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Public certificate added to Comm {result.Data.CommId}. WithCerts: {result.Data.WithCerts}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001, \"certType\": \"X509\", \"keyId\": \"partner-public-cert-2026\", \"userId\": \"partner-edi\", \"beginUsage\": \"2026-05-07T00:00:00Z\", \"usage\": \"EncryptionAndSignature\", \"partnerCommId\": \"PARTNER-AS2-ID\", \"partnerUrl\": \"https://as2.tradingpartner.com/receive\", \"cert\": \"MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3Df...\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/certificates/add-public"))
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
const url = 'https://rest.ecgrid.io/v2/certificates/add-public';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001, "certType": "X509", "keyId": "partner-public-cert-2026", "userId": "partner-edi", "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "partnerCommId": "PARTNER-AS2-ID", "partnerUrl": "https://as2.tradingpartner.com/receive", "cert": "MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3Df..." }),
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
url = "https://rest.ecgrid.io/v2/certificates/add-public"

response = requests.post(
    url,
    json={ "commId": 5001, "certType": "X509", "keyId": "partner-public-cert-2026", "userId": "partner-edi", "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "partnerCommId": "PARTNER-AS2-ID", "partnerUrl": "https://as2.tradingpartner.com/receive", "cert": "MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3Df..." },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Add Private Certificate](./add-private)
- [Create Certificate](./create-certificate)
- [Renew Certificate](./renew-certificate)
- [Terminate Certificate](./terminate-certificate)
- [Get Comm](../comms/get-comm)
- [ENUMs Reference](../../appendix/enums)
