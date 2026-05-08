---
title: CarbonCopySuspend
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CarbonCopySuspend reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CarbonCopySuspend

Temporarily pauses an active carbon copy rule without permanently removing it, allowing you to resume duplication later with `CarbonCopyActivate`.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/carbon-copies/update-carbon-copy.md).
:::

## Method Signature

```
bool CarbonCopySuspend(string SessionID, int CarbonCopyID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CarbonCopyID` | int | Yes | Unique identifier of the active carbon copy rule to suspend |

## Response

Returns a `bool` indicating whether the suspension succeeded.

| Value | Meaning |
|---|---|
| `true` | Rule successfully set to `Suspended`; traffic duplication has stopped |
| `false` | Suspension failed; the rule may already be suspended or terminated |

```xml
<!-- Example response XML -->
<CarbonCopySuspendResult>true</CarbonCopySuspendResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Suspend a carbon copy rule during a planned maintenance window
bool success = await client.CarbonCopySuspendAsync(sessionID, carbonCopyID: 301);

if (success)
    Console.WriteLine("Carbon copy rule suspended. Call CarbonCopyActivate to resume.");
else
    Console.WriteLine("Suspension failed — rule may already be suspended or terminated.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CarbonCopySuspend(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CarbonCopySuspendAsync({
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

result = client.service.CarbonCopySuspend(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [CarbonCopyActivate](./carbon-copy-activate.md) — Resume a suspended rule
- [CarbonCopyTerminate](./carbon-copy-terminate.md) — Permanently remove a rule

## REST Equivalent

See [Update Carbon Copy](../../rest-api/carbon-copies/update-carbon-copy.md) — `PUT /v2/carboncopies/update` with `status=Suspended`.
