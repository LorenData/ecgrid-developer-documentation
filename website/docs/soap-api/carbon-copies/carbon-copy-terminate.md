---
title: CarbonCopyTerminate
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CarbonCopyTerminate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CarbonCopyTerminate

Permanently terminates a carbon copy rule, ending all traffic duplication for the associated mailboxes.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/carbon-copies/delete-carbon-copy.md).
:::

:::danger Irreversible Action
Termination is permanent. The carbon copy rule cannot be restored after this call. Use [CarbonCopySuspend](./carbon-copy-suspend.md) if you need temporary deactivation.
:::

## Method Signature

```
bool CarbonCopyTerminate(string SessionID, int CarbonCopyID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CarbonCopyID` | int | Yes | Unique identifier of the carbon copy rule to permanently terminate |

## Response

Returns a `bool` indicating whether the termination succeeded.

| Value | Meaning |
|---|---|
| `true` | Rule permanently set to `Terminated`; traffic duplication has stopped |
| `false` | Termination failed; the rule may already be terminated or the ID is invalid |

```xml
<!-- Example response XML -->
<CarbonCopyTerminateResult>true</CarbonCopyTerminateResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Permanently remove a carbon copy rule that is no longer needed
// Warning: this action cannot be undone
bool success = await client.CarbonCopyTerminateAsync(sessionID, carbonCopyID: 301);

if (success)
    Console.WriteLine("Carbon copy rule permanently terminated.");
else
    Console.WriteLine("Termination failed — rule may already be terminated.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CarbonCopyTerminate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CarbonCopyTerminateAsync({
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

result = client.service.CarbonCopyTerminate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [CarbonCopySuspend](./carbon-copy-suspend.md) — Reversible alternative to termination
- [CarbonCopyInfo](./carbon-copy-info.md) — Verify rule status before terminating

## REST Equivalent

See [Delete Carbon Copy](../../rest-api/carbon-copies/delete-carbon-copy.md) — `DELETE /v2/carboncopies/{id}`.
