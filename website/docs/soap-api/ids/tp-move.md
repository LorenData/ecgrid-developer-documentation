---
title: TPMove
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of TPMove SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TPMove

Moves a trading partner ID from its current mailbox to a different target mailbox within the same network.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/move-tp.md).
:::

## Method Signature

```
ECGridIDInfo TPMove(string SessionID, int ECGridID, int NewMailboxID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `ECGridID` | int | Yes | Numeric ECGrid identifier for the trading partner ID to move |
| `NewMailboxID` | int | Yes | Target mailbox ID to move the trading partner ID into |

## Response Object — ECGridIDInfo

Returns the updated `ECGridIDInfo` object reflecting the new mailbox assignment.

| Field | Type | Description |
|---|---|---|
| `ECGridID` | int | Unique numeric identifier (unchanged) |
| `MailboxID` | int | Updated mailbox ID — reflects the new mailbox |
| `NetworkID` | int | Associated network ID (unchanged) |
| `Qualifier` | string | ISA qualifier (unchanged) |
| `ID` | string | ISA ID value (unchanged) |
| `Description` | string | Trading partner label (unchanged) |
| `Status` | Status | Lifecycle status (unchanged) |
| `RoutingGroup` | RoutingGroup | Routing group (unchanged) |
| `EDIStandard` | EDIStandard | EDI standard (unchanged) |

```xml
<!-- Example response XML after move -->
<TPMoveResult>
  <ECGridID>123456</ECGridID>
  <MailboxID>999</MailboxID>
  <NetworkID>42</NetworkID>
  <Qualifier>01</Qualifier>
  <ID>ACMECORP      </ID>
  <Description>Acme Corporation</Description>
  <Status>Active</Status>
  <RoutingGroup>ProductionA</RoutingGroup>
  <EDIStandard>X12</EDIStandard>
</TPMoveResult>
```

:::note
Both the source and target mailboxes must belong to the same network. The calling session must have sufficient authorization (NetworkAdmin or higher) to perform the move.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Move ECGridID 123456 from its current mailbox to mailbox 999
ECGridIDInfo moved = await client.TPMoveAsync(
    sessionID,
    ecGridID: 123456,
    newMailboxID: 999);

Console.WriteLine($"ECGridID {moved.ECGridID} now in MailboxID {moved.MailboxID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.TPMove(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.TPMoveAsync({
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

result = client.service.TPMove(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Move TP](../../rest-api/ids/move-tp.md) — `POST /v2/ids/tp-move`.
