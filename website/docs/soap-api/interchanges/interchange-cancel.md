---
title: InterchangeCancel
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP InterchangeCancel method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterchangeCancel

Cancel an outbound interchange that has not yet been delivered to the recipient.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/interchanges/cancel-interchange.md).
:::

:::caution Outbound Only — Cannot Cancel Delivered Interchanges
`InterchangeCancel` applies only to outbound interchanges still in the ECGrid delivery queue. Interchanges that have already been delivered to the recipient cannot be recalled. Verify the interchange status with [`InterchangeInfo`](./interchange-info.md) before attempting cancellation.
:::

## Method Signature

```
bool InterchangeCancel(string SessionID, long InterchangeID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `InterchangeID` | long | Yes | Unique identifier of the interchange to cancel |

## Response Object — bool

Returns `true` if the interchange was successfully cancelled. Returns `false` or a SOAP fault if the interchange has already been delivered, is already cancelled, or the session lacks permission.

```xml
<!-- Example response XML -->
<InterchangeCancelResult>true</InterchangeCancelResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Cancel an outbound interchange before it reaches the trading partner
using var client = new ECGridOSPortTypeClient();

// Confirm the interchange is still queued before cancelling
var info = await client.InterchangeInfoAsync(sessionID, interchangeId: 5551235L);
if (info.Status == "Queued")
{
    bool cancelled = await client.InterchangeCancelAsync(sessionID, interchangeId: 5551235L);

    if (cancelled)
    {
        Console.WriteLine($"Interchange {info.InterchangeID} cancelled successfully.");
    }
    else
    {
        Console.Error.WriteLine("Cancel failed — the interchange may have been delivered.");
    }
}
else
{
    Console.WriteLine($"Cannot cancel — current status is '{info.Status}'.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterchangeCancel(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterchangeCancelAsync({
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

result = client.service.InterchangeCancel(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Cancel Interchange](../../rest-api/interchanges/cancel-interchange.md).
