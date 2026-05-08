---
title: CertAddPrivate
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CertAddPrivate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CertAddPrivate

Uploads your organization's private certificate (with its private key) to a communication channel, enabling your mailbox to decrypt inbound EDI and sign outbound EDI.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/certificates/add-private.md).
:::

## Method Signature

```
as2CommInfo CertAddPrivate(string SessionID, int CommID, CertificateType CertType,
    string KeyId, string UserId, datetime BeginUsage, CertificateUsage Usage,
    string PartnerAS2ID, base64Binary Cert, string Password)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Identifier of the communication channel to associate the certificate with |
| `CertType` | CertificateType | Yes | Type of certificate being uploaded (typically `X509` for AS2) |
| `KeyId` | string | Yes | Key identifier or thumbprint of the certificate |
| `UserId` | string | Yes | User or entity identifier embedded in the certificate |
| `BeginUsage` | datetime | Yes | Date and time from which the certificate becomes valid for use |
| `Usage` | CertificateUsage | Yes | Intended cryptographic use (`Encryption`, `Signature`, `EncryptionAndSignature`) |
| `PartnerAS2ID` | string | No | AS2 ID of the trading partner this private certificate will communicate with |
| `Cert` | base64Binary | Yes | Raw certificate bytes (including the private key, typically PKCS#12 / `.pfx`) encoded as Base64 |
| `Password` | string | No | Password protecting the private key within the certificate file; empty string if none |

## Response Object — as2CommInfo

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Communication channel the certificate was attached to |
| `NetworkID` | int | Network owning the channel |
| `MailboxID` | int | Mailbox owning the channel |
| `AS2ID` | string | AS2 ID configured for the channel |
| `PartnerAS2ID` | string | Trading partner AS2 ID |
| `Status` | string | Current status of the channel |
| `CertKeyID` | int | Identifier assigned to the newly uploaded private certificate key |
| `CertExpiration` | datetime | Expiration date of the uploaded certificate |

```xml
<!-- Example response XML -->
<as2CommInfoResult>
  <CommID>5001</CommID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <AS2ID>MY-AS2-ID</AS2ID>
  <PartnerAS2ID>PARTNER-AS2-ID</PartnerAS2ID>
  <Status>Active</Status>
  <CertKeyID>78</CertKeyID>
  <CertExpiration>2027-05-07T00:00:00</CertExpiration>
</as2CommInfoResult>
```

## ENUMs

### CertificateType

| Value | Description |
|---|---|
| `X509` | X.509 standard digital certificate (PKCS#12 for private keys) |
| `PGP` | PGP certificate |
| `SSH` | SSH key certificate |

### CertificateUsage

| Value | Description |
|---|---|
| `SSL` | TLS/SSL transport layer |
| `Encryption` | Encrypt inbound EDI payloads |
| `Signature` | Sign outbound EDI payloads |
| `EncryptionAndSignature` | Both encryption and signing |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete enumeration definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Upload a PKCS#12 private certificate for AS2 encryption and signing
byte[] pfxBytes = await File.ReadAllBytesAsync("/secure/my-private.pfx");

// Certificate password loaded from secure configuration — never hardcode
string certPassword = config["Certificates:PfxPassword"];

var as2Info = await client.CertAddPrivateAsync(
    sessionID,
    commID: 5001,
    certType: CertificateType.X509,
    keyId: "MY-CERT-001",
    userId: "MY-AS2-ID",
    beginUsage: DateTime.UtcNow,
    usage: CertificateUsage.EncryptionAndSignature,
    partnerAS2ID: "PARTNER-AS2-ID",
    cert: pfxBytes,
    password: certPassword);

Console.WriteLine($"Private certificate uploaded. CertKeyID: {as2Info.CertKeyID}");
Console.WriteLine($"Expires: {as2Info.CertExpiration:yyyy-MM-dd}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CertAddPrivate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CertAddPrivateAsync({
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

result = client.service.CertAddPrivate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Add Private Certificate](../../rest-api/certificates/add-private.md) — `POST /v2/certificates/add-private`.
