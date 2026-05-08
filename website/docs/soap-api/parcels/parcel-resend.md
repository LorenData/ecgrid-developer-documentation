---
title: ParcelResend
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelResend method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelResend

Requeue a previously sent parcel for outbound re-delivery.

:::caution Established API
The SOAP API is in maintenance mode. For inbound re-processing in the REST API, see [Reset to Inbox](../../rest-api/parcels/reset-to-inbox.md). There is no direct REST equivalent for outbound resend.
:::

## Method Signature

```
bool ParcelResend(string SessionID, long ParcelID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ParcelID` | long | Yes | Unique identifier of the parcel to resend |

## Response Object — bool

Returns `true` if the parcel was successfully requeued for delivery. Returns `false` or a SOAP fault if the parcel is not in a resendable state, has already been confirmed by the recipient, or the session lacks permission.

```xml
<!-- Example response XML -->
<ParcelResendResult>true</ParcelResendResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Resend an outbound parcel that failed to deliver
using var client = new ECGridOSPortTypeClient();

bool requeued = await client.ParcelResendAsync(sessionID, parcelId: 9876545L);

if (requeued)
{
    Console.WriteLine($"Parcel {parcelId} requeued for delivery.");
}
else
{
    Console.Error.WriteLine($"Resend failed — check parcel status with ParcelInfo before retrying.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelResend(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelResendAsync({
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

result = client.service.ParcelResend(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

There is no direct REST equivalent for outbound parcel resend. For inbound parcels, see [Reset to Inbox](../../rest-api/parcels/reset-to-inbox.md).
