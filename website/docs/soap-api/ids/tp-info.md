---
title: TPInfo
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of TPInfo SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TPInfo

Returns trading partner ID details — an alias for `ECGridIDInfo` that returns the same `ECGridIDInfo` object.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/get-id.md).
:::

## Method Signature

```
ECGridIDInfo TPInfo(string SessionID, int ECGridID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `ECGridID` | int | Yes | Numeric ECGrid identifier for the trading partner ID |

## Response Object — ECGridIDInfo

| Field | Type | Description |
|---|---|---|
| `ECGridID` | int | Unique numeric identifier for this ECGrid ID record |
| `MailboxID` | int | ID of the mailbox that owns this ECGrid ID |
| `NetworkID` | int | ID of the network associated with this ECGrid ID |
| `Qualifier` | string | ISA qualifier (e.g., `01`, `08`, `ZZ`) |
| `ID` | string | ISA sender/receiver ID value |
| `Description` | string | Human-readable label for the trading partner |
| `Status` | Status | Current lifecycle status of the ECGrid ID |
| `RoutingGroup` | RoutingGroup | Routing group assignment for message delivery |
| `EDIStandard` | EDIStandard | EDI standard used by this trading partner |

```xml
<!-- Example response XML -->
<TPInfoResult>
  <ECGridID>123456</ECGridID>
  <MailboxID>789</MailboxID>
  <NetworkID>42</NetworkID>
  <Qualifier>ZZ</Qualifier>
  <ID>TRADEPARTNER01</ID>
  <Description>Trade Partner One</Description>
  <Status>Active</Status>
  <RoutingGroup>ProductionA</RoutingGroup>
  <EDIStandard>X12</EDIStandard>
</TPInfoResult>
```

:::note
`TPInfo` and `ECGridIDInfo` accept identical parameters and return the same `ECGridIDInfo` object. They are interchangeable; `TPInfo` exists for historical naming consistency with other `TP*` methods in the SOAP API.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// TPInfo and ECGridIDInfo return the same type
ECGridIDInfo idInfo = await client.TPInfoAsync(sessionID, 123456);

Console.WriteLine($"Qualifier: {idInfo.Qualifier}  ID: {idInfo.ID}");
Console.WriteLine($"Status: {idInfo.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.TPInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.TPInfoAsync({
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

result = client.service.TPInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get ID](../../rest-api/ids/get-id.md) — `GET /v2/ids/{id}`.
