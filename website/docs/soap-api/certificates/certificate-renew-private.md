---
title: CertificateRenewPrivate
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CertificateRenewPrivate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CertificateRenewPrivate

Renews an existing platform-generated private certificate, creating a new certificate with an overlapping validity period to ensure uninterrupted EDI communication during the transition.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/certificates/renew-certificate.md).
:::

## Method Signature

```
CommIDInfo CertificateRenewPrivate(string SessionID, int CommID, int CertKeyID,
    short OverlapDays, short Years, CertificateSecureHashAlgorithm SecureHashAlgorithm)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Identifier of the communication channel whose certificate is being renewed |
| `CertKeyID` | int | Yes | Key ID of the existing certificate to renew |
| `OverlapDays` | short | Yes | Number of days before the existing certificate expires that the new certificate should become active; allows partners time to update their trust stores |
| `Years` | short | Yes | Validity duration for the renewed certificate in years |
| `SecureHashAlgorithm` | CertificateSecureHashAlgorithm | Yes | Hashing algorithm to use for the new certificate |

## Response Object — CommIDInfo

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Communication channel the renewed certificate is attached to |
| `NetworkID` | int | Network owning the channel |
| `MailboxID` | int | Mailbox owning the channel |
| `CommType` | string | Protocol type of the channel |
| `Status` | string | Current channel status |
| `CertKeyID` | int | Identifier of the newly generated renewal certificate key |

```xml
<!-- Example response XML -->
<CommIDInfoResult>
  <CommID>5001</CommID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <CommType>AS2</CommType>
  <Status>Active</Status>
  <CertKeyID>80</CertKeyID>
</CommIDInfoResult>
```

## ENUMs

### CertificateSecureHashAlgorithm

| Value | Description |
|---|---|
| `SHA1` | SHA-1 (established — avoid for renewed certificates) |
| `SHA256` | SHA-256 (recommended minimum) |
| `SHA384` | SHA-384 |
| `SHA512` | SHA-512 |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete enumeration definitions.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Renew an expiring certificate with a 30-day overlap period and 2-year validity
var commInfo = await client.CertificateRenewPrivateAsync(
    sessionID,
    commID: 5001,
    certKeyID: 79,
    overlapDays: 30,
    years: 2,
    secureHashAlgorithm: CertificateSecureHashAlgorithm.SHA256);

Console.WriteLine($"Certificate renewed. New CertKeyID: {commInfo.CertKeyID}");
Console.WriteLine("Share the new public certificate with trading partners during the overlap period.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CertificateRenewPrivate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CertificateRenewPrivateAsync({
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

result = client.service.CertificateRenewPrivate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Renew Certificate](../../rest-api/certificates/renew-certificate.md) — `POST /v2/certificates/renew`.
