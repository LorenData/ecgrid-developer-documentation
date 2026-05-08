---
title: InterconnectCancel
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectCancel SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectCancel

Permanently terminates a trading partner interconnect, preventing further EDI traffic between the two parties.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/delete-partner.md).
:::

## Method Signature

```
bool InterconnectCancel(string SessionID, int InterconnectID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `InterconnectID` | int | Yes | Numeric identifier for the interconnect to cancel |

## Response

Returns `true` if the interconnect was successfully terminated; `false` otherwise.

```xml
<!-- Example response XML -->
<InterconnectCancelResult>true</InterconnectCancelResult>
```

:::caution
Cancelling an interconnect is a permanent action. Once cancelled, EDI traffic can no longer flow between the two ECGrid IDs on this interconnect. A new interconnect must be created with [InterconnectAdd](./interconnect-add.md) to restore routing.

To temporarily halt traffic, use [InterconnectUpdate](./interconnect-update.md) with `Status.Suspended` instead.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

bool cancelled = await client.InterconnectCancelAsync(sessionID, 5001);

if (cancelled)
{
    Console.WriteLine("Interconnect 5001 has been permanently terminated.");
}
else
{
    Console.WriteLine("Cancellation failed — verify InterconnectID and permissions.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectCancel(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectCancelAsync({
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

result = client.service.InterconnectCancel(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Delete Partner](../../rest-api/partners/delete-partner.md) — `DELETE /v2/partners/{id}`.
