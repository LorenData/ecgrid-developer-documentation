---
title: CertificateAddPublic
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CertificateAddPublic reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CertificateAddPublic

Uploads a trading partner's public certificate to a communication channel (Comm), enabling encrypted or signed EDI exchange with that partner.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/certificates/add-public.md).
:::

## Method Signature

```
CommIDInfo CertificateAddPublic(string SessionID, int CommID, CertificateType CertType,
    string KeyId, string UserId, datetime BeginUsage, CertificateUsage Usage,
    string PartnerCommID, string PartnerURL, base64Binary Cert)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Identifier of the communication channel to associate the certificate with |
| `CertType` | CertificateType | Yes | Type of certificate being added (e.g., `X509`, `PGP`) |
| `KeyId` | string | Yes | Key identifier or thumbprint from the certificate |
| `UserId` | string | Yes | User or entity identifier embedded in the certificate |
| `BeginUsage` | datetime | Yes | Date and time from which the certificate should be considered valid for use |
| `Usage` | CertificateUsage | Yes | Intended cryptographic use of the certificate |
| `PartnerCommID` | string | No | Trading partner's AS2 ID or communication channel identifier |
| `PartnerURL` | string | No | Trading partner's AS2 endpoint URL, if applicable |
| `Cert` | base64Binary | Yes | Raw certificate bytes encoded as Base64 |

## Response Object — CommIDInfo

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Communication channel the certificate was attached to |
| `NetworkID` | int | Network owning the communication channel |
| `MailboxID` | int | Mailbox owning the communication channel |
| `CommType` | string | Protocol type of the channel (e.g., `AS2`, `SFTP`) |
| `Status` | string | Current status of the channel |
| `CertKeyID` | int | Identifier assigned to the newly uploaded certificate key |

```xml
<!-- Example response XML -->
<CommIDInfoResult>
  <CommID>5001</CommID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <CommType>AS2</CommType>
  <Status>Active</Status>
  <CertKeyID>77</CertKeyID>
</CommIDInfoResult>
```

## ENUMs

### CertificateType

| Value | Description |
|---|---|
| `X509` | X.509 standard digital certificate |
| `PGP` | PGP (Pretty Good Privacy) certificate |
| `SSH` | SSH public key certificate |

### CertificateUsage

| Value | Description |
|---|---|
| `SSL` | Used for TLS/SSL transport layer security |
| `Encryption` | Used to encrypt EDI payloads |
| `Signature` | Used to sign EDI payloads |
| `EncryptionAndSignature` | Used for both encryption and signing |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete enumeration definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Upload a trading partner's X.509 public certificate for AS2 encryption
byte[] certBytes = await File.ReadAllBytesAsync("/secure/partner-public.cer");

var commInfo = await client.CertificateAddPublicAsync(
    sessionID,
    commID: 5001,
    certType: CertificateType.X509,
    keyId: "PARTNER-CERT-001",
    userId: "PARTNERID",
    beginUsage: DateTime.UtcNow,
    usage: CertificateUsage.Encryption,
    partnerCommID: "PARTNER-AS2-ID",
    partnerURL: "https://partner.example.com/as2",
    cert: certBytes);

Console.WriteLine($"Certificate uploaded. CertKeyID: {commInfo.CertKeyID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CertificateAddPublic(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CertificateAddPublicAsync({
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

result = client.service.CertificateAddPublic(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Add Public Certificate](../../rest-api/certificates/add-public.md) — `POST /v2/certificates/add-public`.
