---
title: InterchangeResend
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP InterchangeResend method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterchangeResend

Requeue a previously delivered interchange for re-transmission to its recipient.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/interchanges/resend-interchange.md).
:::

## Method Signature

```
bool InterchangeResend(string SessionID, long InterchangeID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `InterchangeID` | long | Yes | Unique identifier of the interchange to resend |

## Response Object — bool

Returns `true` if the interchange was successfully requeued. Returns `false` or a SOAP fault if the interchange cannot be resent (e.g., it is in a cancelled state or the session lacks permission).

```xml
<!-- Example response XML -->
<InterchangeResendResult>true</InterchangeResendResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Resend an interchange that was reported as missing by the trading partner
using var client = new ECGridOSPortTypeClient();

bool requeued = await client.InterchangeResendAsync(sessionID, interchangeId: 5551234L);

if (requeued)
{
    Console.WriteLine($"Interchange {interchangeId} requeued for delivery.");
}
else
{
    Console.Error.WriteLine("Resend failed — verify interchange status with InterchangeInfo.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterchangeResend(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterchangeResendAsync({
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

result = client.service.InterchangeResend(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Resend Interchange](../../rest-api/interchanges/resend-interchange.md).
