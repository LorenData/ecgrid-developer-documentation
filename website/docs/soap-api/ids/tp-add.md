---
title: TPAdd
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of TPAdd SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TPAdd

Creates a new ECGrid trading partner ID within the specified network and mailbox.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/create-id.md).
:::

## Method Signature

```
ECGridIDInfo TPAdd(string SessionID, int NetworkID, int MailboxID, string Qualifier, string ID, string Description, RoutingGroup RoutingGroup, EDIStandard EDIStandard)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `NetworkID` | int | Yes | Network to create the trading partner ID under |
| `MailboxID` | int | Yes | Mailbox to own this trading partner ID |
| `Qualifier` | string | Yes | ISA qualifier (e.g., `01`, `08`, `12`, `ZZ`) — 2 characters |
| `ID` | string | Yes | ISA sender/receiver ID value — up to 15 characters |
| `Description` | string | Yes | Human-readable label for the trading partner |
| `RoutingGroup` | RoutingGroup | Yes | Routing group for message delivery |
| `EDIStandard` | EDIStandard | Yes | EDI standard used by this trading partner |

## Response Object — ECGridIDInfo

Returns the newly created `ECGridIDInfo` object.

| Field | Type | Description |
|---|---|---|
| `ECGridID` | int | System-assigned numeric identifier for the new ECGrid ID |
| `MailboxID` | int | Owning mailbox ID |
| `NetworkID` | int | Associated network ID |
| `Qualifier` | string | ISA qualifier as provided |
| `ID` | string | ISA ID value as provided |
| `Description` | string | Trading partner label as provided |
| `Status` | Status | Initial status — typically `Active` |
| `RoutingGroup` | RoutingGroup | Routing group as provided |
| `EDIStandard` | EDIStandard | EDI standard as provided |

```xml
<!-- Example response XML -->
<TPAddResult>
  <ECGridID>123458</ECGridID>
  <MailboxID>789</MailboxID>
  <NetworkID>42</NetworkID>
  <Qualifier>ZZ</Qualifier>
  <ID>NEWPARTNER01</ID>
  <Description>New Partner One</Description>
  <Status>Active</Status>
  <RoutingGroup>ProductionA</RoutingGroup>
  <EDIStandard>X12</EDIStandard>
</TPAddResult>
```

## ENUMs

### RoutingGroup

| Value | Description |
|---|---|
| `ProductionA` | Primary production routing group |
| `ProductionB` | Secondary production routing group |
| `Migration1` | Migration routing group 1 |
| `Migration2` | Migration routing group 2 |
| `ManagedFileTransfer` | Managed file transfer group |
| `Test` | Test routing group |
| `SuperHub` | Super hub routing group |

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

ECGridIDInfo newId = await client.TPAddAsync(
    sessionID,
    networkID: 42,
    mailboxID: 789,
    qualifier: "ZZ",
    id: "NEWPARTNER01",
    description: "New Partner One",
    routingGroup: RoutingGroup.ProductionA,
    ediStandard: EDIStandard.X12);

Console.WriteLine($"Created ECGridID: {newId.ECGridID}");
Console.WriteLine($"Qualifier/ID: {newId.Qualifier}:{newId.ID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.TPAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.TPAddAsync({
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

result = client.service.TPAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create ID](../../rest-api/ids/create-id.md) — `POST /v2/ids`.
