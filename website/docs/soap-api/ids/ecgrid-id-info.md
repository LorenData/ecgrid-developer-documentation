---
title: ECGridIDInfo
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of ECGridIDInfo SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ECGridIDInfo

Returns detailed information about a single ECGrid trading partner ID by its numeric identifier.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/get-id.md).
:::

## Method Signature

```
ECGridIDInfo ECGridIDInfo(string SessionID, int ECGridID)
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
| `EDIStandard` | EDIStandard | EDI standard used by this trading partner (e.g., X12, EDIFACT) |

```xml
<!-- Example response XML -->
<ECGridIDInfoResult>
  <ECGridID>123456</ECGridID>
  <MailboxID>789</MailboxID>
  <NetworkID>42</NetworkID>
  <Qualifier>01</Qualifier>
  <ID>ACMECORP      </ID>
  <Description>Acme Corporation</Description>
  <Status>Active</Status>
  <RoutingGroup>ProductionA</RoutingGroup>
  <EDIStandard>X12</EDIStandard>
</ECGridIDInfoResult>
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | ID is in development/testing |
| `Active` | ID is live and routing traffic |
| `Preproduction` | ID is staged for production |
| `Suspended` | ID is temporarily inactive |
| `Terminated` | ID has been permanently disabled |

### RoutingGroup

| Value | Description |
|---|---|
| `ProductionA` | Primary production routing group |
| `ProductionB` | Secondary production routing group |
| `Migration1` | Migration routing group 1 |
| `Migration2` | Migration routing group 2 |
| `ManagedFileTransfer` | Managed file transfer group |
| `Test` | Test routing group |

### EDIStandard

| Value | Description |
|---|---|
| `X12` | ANSI X12 EDI standard |
| `EDIFACT` | UN/EDIFACT standard |
| `TRADACOMS` | TRADACOMS standard |
| `VDA` | VDA automotive standard |
| `XML` | XML-based documents |
| `TXT` | Plain text |
| `PDF` | PDF documents |
| `Binary` | Binary/proprietary format |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

ECGridIDInfo idInfo = await client.ECGridIDInfoAsync(sessionID, 123456);

Console.WriteLine($"Qualifier: {idInfo.Qualifier}  ID: {idInfo.ID}");
Console.WriteLine($"Description: {idInfo.Description}");
Console.WriteLine($"Status: {idInfo.Status}  Routing: {idInfo.RoutingGroup}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ECGridIDInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ECGridIDInfoAsync({
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

result = client.service.ECGridIDInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get ID](../../rest-api/ids/get-id.md) — `GET /v2/ids/{id}`.
