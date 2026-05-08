---
title: TPAddVAN
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of TPAddVAN SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TPAddVAN

Associates a VAN (Value Added Network) qualifier and ID with an existing ECGrid trading partner ID to enable cross-network routing.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/add-van.md).
:::

## Method Signature

```
ECGridIDInfo TPAddVAN(string SessionID, int ECGridID, string VANQualifier, string VANID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `ECGridID` | int | Yes | Numeric ECGrid identifier for the trading partner ID to update |
| `VANQualifier` | string | Yes | ISA qualifier used by the VAN for this trading partner |
| `VANID` | string | Yes | ISA ID value used by the VAN for this trading partner |

## Response Object — ECGridIDInfo

Returns the updated `ECGridIDInfo` object confirming the VAN association.

| Field | Type | Description |
|---|---|---|
| `ECGridID` | int | Unique numeric identifier |
| `MailboxID` | int | Owning mailbox ID |
| `NetworkID` | int | Associated network ID |
| `Qualifier` | string | ECGrid ISA qualifier |
| `ID` | string | ECGrid ISA ID value |
| `Description` | string | Trading partner label |
| `Status` | Status | Lifecycle status |
| `RoutingGroup` | RoutingGroup | Routing group |
| `EDIStandard` | EDIStandard | EDI standard |

```xml
<!-- Example response XML -->
<TPAddVANResult>
  <ECGridID>123456</ECGridID>
  <MailboxID>789</MailboxID>
  <NetworkID>42</NetworkID>
  <Qualifier>01</Qualifier>
  <ID>ACMECORP      </ID>
  <Description>Acme Corporation</Description>
  <Status>Active</Status>
  <RoutingGroup>ProductionA</RoutingGroup>
  <EDIStandard>X12</EDIStandard>
</TPAddVANResult>
```

:::note
VAN cross-referencing allows ECGrid to route inbound EDI that arrives using a VAN's qualifier/ID pair to the correct ECGrid mailbox. This is commonly used when a trading partner is reachable through multiple networks.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Associate VAN identifier "08:VANPARTNER01" with ECGridID 123456
ECGridIDInfo updated = await client.TPAddVANAsync(
    sessionID,
    ecGridID: 123456,
    vanQualifier: "08",
    vanID: "VANPARTNER01");

Console.WriteLine($"VAN association added for ECGridID {updated.ECGridID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.TPAddVAN(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.TPAddVANAsync({
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

result = client.service.TPAddVAN(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Add VAN](../../rest-api/ids/add-van.md) — `POST /v2/ids/tp-add-van`.
