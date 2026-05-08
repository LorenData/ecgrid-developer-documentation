---
title: CertificateTerminate
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CertificateTerminate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CertificateTerminate

Permanently terminates a certificate on a communication channel, revoking its use for encryption or signing.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/certificates/terminate-certificate.md).
:::

:::danger Active AS2 Connections Will Break
Terminating a certificate that is currently in use by an AS2 or other communication channel will immediately disrupt EDI exchanges with trading partners that rely on it. Ensure a replacement certificate is in place and partners have been notified before terminating.
:::

## Method Signature

```
bool CertificateTerminate(string SessionID, int CommID, int CertKeyID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Identifier of the communication channel holding the certificate |
| `CertKeyID` | int | Yes | Key ID of the specific certificate to terminate |

## Response

Returns a `bool` indicating whether the termination succeeded.

| Value | Meaning |
|---|---|
| `true` | Certificate successfully terminated; it will no longer be used for encryption or signing |
| `false` | Termination failed; the certificate may already be terminated or the ID is invalid |

```xml
<!-- Example response XML -->
<CertificateTerminateResult>true</CertificateTerminateResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Terminate an old certificate after a renewal has been fully deployed
// Confirm that the replacement certificate (CertKeyID 80) is active before calling this
bool success = await client.CertificateTerminateAsync(
    sessionID,
    commID: 5001,
    certKeyID: 79);

if (success)
    Console.WriteLine("Certificate terminated successfully.");
else
    Console.WriteLine("Termination failed — verify CommID and CertKeyID are correct.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CertificateTerminate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CertificateTerminateAsync({
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

result = client.service.CertificateTerminate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [CertificateCreatePrivate](./certificate-create-private.md) — Generate a replacement certificate
- [CertificateRenewPrivate](./certificate-renew-private.md) — Renew with an overlap period before terminating the old key

## REST Equivalent

See [Terminate Certificate](../../rest-api/certificates/terminate-certificate.md) — `POST /v2/certificates/terminate`.
