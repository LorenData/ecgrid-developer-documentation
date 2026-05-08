---
title: CommSetPair
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommSetPair documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommSetPair

Assigns a specific communication channel to a trading partner pair, establishing the preferred channel for EDI exchange between two ECGrid IDs.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/set-pair.md).
:::

## Method Signature

```
ArrayOfCommIDInfo CommSetPair(string SessionID, int ECGridIDFrom, int ECGridIDTo, int CommID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ECGridIDFrom` | int | Yes | ECGrid ID of the sending trading partner |
| `ECGridIDTo` | int | Yes | ECGrid ID of the receiving trading partner |
| `CommID` | int | Yes | CommID of the channel to assign to this trading partner pair |

## Response Object — ArrayOfCommIDInfo

Returns an array of `CommIDInfo` objects reflecting the updated comm channel pairing.

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
    <CommType>sftp</CommType>
    <Identifier>sftp.tradingpartner.com</Identifier>
    <Status>Active</Status>
    <UseType>Production</UseType>
    <PrivateKeyRequired>false</PrivateKeyRequired>
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

// Assign comm channel 4521 to the pair (ECGridIDFrom → ECGridIDTo)
CommIDInfo[] result = await client.CommSetPairAsync(
    sessionID,
    ECGridIDFrom: 1234567,
    ECGridIDTo: 9876543,
    CommID: 4521);

foreach (var ch in result)
{
    Console.WriteLine($"CommID: {ch.CommID} | Type: {ch.CommType} | Status: {ch.Status}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommSetPair(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommSetPairAsync({
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

result = client.service.CommSetPair(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Set Pair](../../rest-api/comms/set-pair.md) — `POST /v2/comms/set-pair`.
