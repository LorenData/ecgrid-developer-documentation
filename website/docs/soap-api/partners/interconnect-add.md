---
title: InterconnectAdd
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectAdd SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectAdd

Creates a new trading partner interconnect that permits EDI traffic to flow between two ECGrid IDs.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/create-partner.md).
:::

## Method Signature

```
InterconnectIDInfo InterconnectAdd(string SessionID, int ECGridIDFrom, int ECGridIDTo)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `ECGridIDFrom` | int | Yes | ECGrid ID of the initiating (sending) trading partner |
| `ECGridIDTo` | int | Yes | ECGrid ID of the receiving trading partner |

## Response Object — InterconnectIDInfo

Returns the newly created `InterconnectIDInfo` object.

| Field | Type | Description |
|---|---|---|
| `InterconnectID` | int | System-assigned numeric identifier for the new interconnect |
| `ECGridIDFrom` | int | ECGrid ID of the sending trading partner |
| `ECGridIDTo` | int | ECGrid ID of the receiving trading partner |
| `Status` | Status | Initial status — typically `Active` |
| `Created` | datetime | Timestamp when the interconnect was created |
| `Modified` | datetime | Timestamp of last modification (same as Created on creation) |

```xml
<!-- Example response XML -->
<InterconnectAddResult>
  <InterconnectID>5002</InterconnectID>
  <ECGridIDFrom>123456</ECGridIDFrom>
  <ECGridIDTo>345678</ECGridIDTo>
  <Status>Active</Status>
  <Created>2026-05-07T12:00:00</Created>
  <Modified>2026-05-07T12:00:00</Modified>
</InterconnectAddResult>
```

:::note
An interconnect represents a bilateral permission: traffic is permitted from `ECGridIDFrom` to `ECGridIDTo`. To allow traffic in both directions, create two interconnects — one for each direction.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

InterconnectIDInfo newInterconnect = await client.InterconnectAddAsync(
    sessionID,
    ecGridIDFrom: 123456,
    ecGridIDTo: 345678);

Console.WriteLine($"Created InterconnectID: {newInterconnect.InterconnectID}");
Console.WriteLine($"Status: {newInterconnect.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectAddAsync({
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

result = client.service.InterconnectAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create Partner](../../rest-api/partners/create-partner.md) — `POST /v2/partners`.
