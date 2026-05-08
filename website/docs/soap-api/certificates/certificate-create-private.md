---
title: CertificateCreatePrivate
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CertificateCreatePrivate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CertificateCreatePrivate

Generates a new private certificate directly on the ECGridOS platform for a communication channel, eliminating the need to provision and upload a certificate externally.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/certificates/create-certificate.md).
:::

## Method Signature

```
CommIDInfo CertificateCreatePrivate(string SessionID, int CommID, datetime BeginUsage,
    CertificateUsage Usage, CertificateSecureHashAlgorithm SecureHashAlgorithm,
    string PartnerAS2ID, datetime Expires)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Identifier of the communication channel to generate the certificate for |
| `BeginUsage` | datetime | Yes | Date and time from which the certificate should be considered valid |
| `Usage` | CertificateUsage | Yes | Intended cryptographic purpose of the generated certificate |
| `SecureHashAlgorithm` | CertificateSecureHashAlgorithm | Yes | Hashing algorithm to use when generating the certificate |
| `PartnerAS2ID` | string | No | AS2 ID of the trading partner that will use this certificate |
| `Expires` | datetime | Yes | Expiration date for the generated certificate |

## Response Object — CommIDInfo

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Communication channel the certificate was generated for |
| `NetworkID` | int | Network owning the channel |
| `MailboxID` | int | Mailbox owning the channel |
| `CommType` | string | Protocol type of the channel |
| `Status` | string | Current channel status |
| `CertKeyID` | int | Identifier of the newly generated certificate key |

```xml
<!-- Example response XML -->
<CommIDInfoResult>
  <CommID>5001</CommID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <CommType>AS2</CommType>
  <Status>Active</Status>
  <CertKeyID>79</CertKeyID>
</CommIDInfoResult>
```

## ENUMs

### CertificateUsage

| Value | Description |
|---|---|
| `SSL` | TLS/SSL transport layer security |
| `Encryption` | Encrypt EDI payloads |
| `Signature` | Sign EDI payloads |
| `EncryptionAndSignature` | Both encryption and signing |

### CertificateSecureHashAlgorithm

| Value | Description |
|---|---|
| `SHA1` | SHA-1 (established — avoid for new certificates) |
| `SHA256` | SHA-256 (recommended minimum) |
| `SHA384` | SHA-384 |
| `SHA512` | SHA-512 |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete enumeration definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Generate a new SHA-256 certificate for AS2 encryption and signing, valid for 2 years
var commInfo = await client.CertificateCreatePrivateAsync(
    sessionID,
    commID: 5001,
    beginUsage: DateTime.UtcNow,
    usage: CertificateUsage.EncryptionAndSignature,
    secureHashAlgorithm: CertificateSecureHashAlgorithm.SHA256,
    partnerAS2ID: "PARTNER-AS2-ID",
    expires: DateTime.UtcNow.AddYears(2));

Console.WriteLine($"Certificate generated. CertKeyID: {commInfo.CertKeyID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CertificateCreatePrivate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CertificateCreatePrivateAsync({
  SessionID: sessionId,
  // additional params
});
console.log(result);
```

</TabItem>
<TabItem value="python" label="Python">

```python
# pip install zeep
from zeep import Client

WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL'
client = Client(WSDL)

result = client.service.CertificateCreatePrivate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create Certificate](../../rest-api/certificates/create-certificate.md) — `POST /v2/certificates/create`.
