---
title: InterconnectUpdate
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectUpdate SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectUpdate

Updates the lifecycle status of an existing trading partner interconnect.

:::caution Established API
The SOAP API is in maintenance mode. There is no direct REST equivalent for this operation; use the [REST Partners](../../rest-api/partners/get-partner.md) section for related management.
:::

## Method Signature

```
InterconnectIDInfo InterconnectUpdate(string SessionID, int InterconnectID, Status Status)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `InterconnectID` | int | Yes | Numeric identifier for the interconnect to update |
| `Status` | Status | Yes | New lifecycle status to assign to this interconnect |

## Response Object — InterconnectIDInfo

Returns the updated `InterconnectIDInfo` object reflecting the new status.

| Field | Type | Description |
|---|---|---|
| `InterconnectID` | int | Unique numeric identifier (unchanged) |
| `ECGridIDFrom` | int | ECGrid ID of the sending trading partner (unchanged) |
| `ECGridIDTo` | int | ECGrid ID of the receiving trading partner (unchanged) |
| `Status` | Status | Updated lifecycle status |
| `Created` | datetime | Original creation timestamp (unchanged) |
| `Modified` | datetime | Updated to reflect when the status change was made |

```xml
<!-- Example response XML after status update -->
<InterconnectUpdateResult>
  <InterconnectID>5001</InterconnectID>
  <ECGridIDFrom>123456</ECGridIDFrom>
  <ECGridIDTo>234567</ECGridIDTo>
  <Status>Suspended</Status>
  <Created>2024-01-15T10:30:00</Created>
  <Modified>2026-05-07T12:00:00</Modified>
</InterconnectUpdateResult>
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | Set interconnect back to development/configuration state |
| `Active` | Reactivate — allows EDI traffic to flow |
| `Preproduction` | Stage for production testing |
| `Suspended` | Temporarily halt EDI traffic on this interconnect |
| `Terminated` | Permanently close the interconnect |

:::caution
Setting status to `Terminated` is irreversible. Use `Suspended` if you need to temporarily stop traffic with the option to resume later. To permanently close an interconnect, consider using [InterconnectCancel](./interconnect-cancel.md) instead.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Suspend an interconnect temporarily
InterconnectIDInfo updated = await client.InterconnectUpdateAsync(
    sessionID,
    interconnectID: 5001,
    status: Status.Suspended);

Console.WriteLine($"InterconnectID {updated.InterconnectID} status: {updated.Status}");

// Reactivate it later
InterconnectIDInfo reactivated = await client.InterconnectUpdateAsync(
    sessionID,
    interconnectID: 5001,
    status: Status.Active);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectUpdate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectUpdateAsync({
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

result = client.service.InterconnectUpdate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

There is no direct REST equivalent for status-only updates. See [Get Partner](../../rest-api/partners/get-partner.md) for partner management options in the REST API.
