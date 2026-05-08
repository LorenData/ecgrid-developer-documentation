---
title: Add Private Certificate
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of Add Private Certificate REST API reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Add Private Certificate

Uploads and associates a private certificate with a communication channel (Comm) for AS2 or encryption use.

## Endpoint

```http
POST /v2/certificates/add-private
```

## Request Body

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `commId` | integer | Yes | Must be a valid Comm ID | Communication channel to associate the certificate with |
| `certType` | CertificateType | Yes | See ENUMs | Type of certificate (X509, PGP, SSH) |
| `keyId` | string | No | — | Key identifier for the certificate |
| `userId` | string | No | — | User identifier associated with this certificate |
| `beginUsage` | datetime | No | ISO 8601 | Date and time when the certificate becomes active |
| `usage` | CertificateUsage | No | See ENUMs | Intended usage (Encryption, Signature, etc.) |
| `cert` | string | No | Base64-encoded | The certificate content encoded as Base64 |
| `password` | string | No | — | Password protecting the private certificate file |

```json
{
  "commId": 5001,
  "certType": "X509",
  "keyId": "my-private-key-2026",
  "userId": "edi-system",
  "beginUsage": "2026-05-07T00:00:00Z",
  "usage": "EncryptionAndSignature",
  "cert": "MIIKxAIBAzCCCn4GCSqGSIb3DQEHAaCC...",
  "password": "p@ssw0rd!"
}
```

## Response

Returns the updated `CommIDInfo` object reflecting the newly associated certificate.

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
curl -X POST "https://rest.ecgrid.io/v2/certificates/add-private" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "commId": 5001, "certType": "X509", "keyId": "my-private-key-2026", "userId": "edi-system", "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "cert": "MIIKxAIBAzCCCn4GCSqGSIb3DQEHAaCC...", "password": "p@ssw0rd!" }'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — Upload a private certificate to a comm channel
// Certificate file is loaded from disk and base64-encoded before submission
var certBytes = await File.ReadAllBytesAsync("path/to/private.pfx");
var certBase64 = Convert.ToBase64String(certBytes);

var request = new
{
    commId = 5001,
    certType = "X509",
    keyId = "my-private-key-2026",
    userId = "edi-system",
    beginUsage = DateTime.UtcNow.ToString("o"),
    usage = "EncryptionAndSignature",
    cert = certBase64,
    password = config["Certificates:PrivateKeyPassword"]
};

using var response = await httpClient.PostAsJsonAsync(
    "https://rest.ecgrid.io/v2/certificates/add-private",
    request);

response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<ApiResponse<CommIdInfo>>();
Console.WriteLine($"Private certificate added to Comm {result.Data.CommId}. WithCerts: {result.Data.WithCerts}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

String apiKey = System.getenv("ECGRID_API_KEY");

String body = "{ \"commId\": 5001, \"certType\": \"X509\", \"keyId\": \"my-private-key-2026\", \"userId\": \"edi-system\", \"beginUsage\": \"2026-05-07T00:00:00Z\", \"usage\": \"EncryptionAndSignature\", \"cert\": \"MIIKxAIBAzCCCn4GCSqGSIb3DQEHAaCC...\", \"password\": \"p@ssw0rd!\" }";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/certificates/add-private"))
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
const url = 'https://rest.ecgrid.io/v2/certificates/add-private';

const response = await fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ "commId": 5001, "certType": "X509", "keyId": "my-private-key-2026", "userId": "edi-system", "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "cert": "MIIKxAIBAzCCCn4GCSqGSIb3DQEHAaCC...", "password": "p@ssw0rd!" }),
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
url = "https://rest.ecgrid.io/v2/certificates/add-private"

response = requests.post(
    url,
    json={ "commId": 5001, "certType": "X509", "keyId": "my-private-key-2026", "userId": "edi-system", "beginUsage": "2026-05-07T00:00:00Z", "usage": "EncryptionAndSignature", "cert": "MIIKxAIBAzCCCn4GCSqGSIb3DQEHAaCC...", "password": "p@ssw0rd!" },
    headers=headers,
)

response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## See Also

- [Add Public Certificate](./add-public)
- [Create Certificate](./create-certificate)
- [Renew Certificate](./renew-certificate)
- [Terminate Certificate](./terminate-certificate)
- [Get Comm](../comms/get-comm)
- [ENUMs Reference](../../appendix/enums)
