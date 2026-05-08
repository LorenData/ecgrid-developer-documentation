---
title: CommPair
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommPair documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommPair

Returns the communication channels that are active between two trading partners identified by their ECGrid IDs.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/comm-pair.md).
:::

## Method Signature

```
ArrayOfCommIDInfo CommPair(string SessionID, int ECGridIDFrom, int ECGridIDTo)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ECGridIDFrom` | int | Yes | ECGrid ID of the sending trading partner |
| `ECGridIDTo` | int | Yes | ECGrid ID of the receiving trading partner |

## Response Object — ArrayOfCommIDInfo

Returns an array of `CommIDInfo` objects representing the comm channels connecting the two trading partners.

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Unique identifier of the comm channel |
| `MailboxID` | int | Mailbox associated with this comm channel |
| `CommType` | NetworkGatewayCommChannel | Protocol type |
| `Identifier` | string | Protocol-specific identifier |
| `Status` | Status | Current status of the comm channel |
| `UseType` | UseType | Test, production, or both |
| `PrivateKeyRequired` | bool | Whether a private key is required |
| `WithCerts` | bool | Whether certificate details are included |

```xml
<!-- Example response XML -->
<ArrayOfCommIDInfo>
  <CommIDInfo>
    <CommID>4521</CommID>
    <MailboxID>100</MailboxID>
    <CommType>as2</CommType>
    <Identifier>PARTNER-AS2-ID</Identifier>
    <Status>Active</Status>
    <UseType>Production</UseType>
    <PrivateKeyRequired>true</PrivateKeyRequired>
    <WithCerts>false</WithCerts>
  </CommIDInfo>
</ArrayOfCommIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Find comm channels between two trading partners
CommIDInfo[] pair = await client.CommPairAsync(
    sessionID,
    ECGridIDFrom: 1234567,
    ECGridIDTo: 9876543);

foreach (var ch in pair)
{
    Console.WriteLine($"CommID: {ch.CommID} | Type: {ch.CommType} | Identifier: {ch.Identifier}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommPair(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommPairAsync({
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

result = client.service.CommPair(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Comm Pair](../../rest-api/comms/comm-pair.md) — `POST /v2/comms/pair`.
