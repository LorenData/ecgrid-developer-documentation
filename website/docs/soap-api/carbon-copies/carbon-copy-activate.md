---
title: CarbonCopyActivate
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CarbonCopyActivate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CarbonCopyActivate

Re-activates a previously suspended carbon copy rule, resuming automatic duplication of EDI traffic for the configured mailbox and direction.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/carbon-copies/update-carbon-copy.md).
:::

## Method Signature

```
bool CarbonCopyActivate(string SessionID, int CarbonCopyID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CarbonCopyID` | int | Yes | Unique identifier of the suspended carbon copy rule to activate |

## Response

Returns a `bool` indicating whether the activation succeeded.

| Value | Meaning |
|---|---|
| `true` | Rule successfully set to `Active` |
| `false` | Activation failed; the rule may already be active or terminated |

```xml
<!-- Example response XML -->
<CarbonCopyActivateResult>true</CarbonCopyActivateResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Re-activate a suspended carbon copy rule after maintenance window
bool success = await client.CarbonCopyActivateAsync(sessionID, carbonCopyID: 301);

if (success)
    Console.WriteLine("Carbon copy rule is now active.");
else
    Console.WriteLine("Activation failed — rule may already be active or terminated.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CarbonCopyActivate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CarbonCopyActivateAsync({
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

result = client.service.CarbonCopyActivate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Carbon Copy](../../rest-api/carbon-copies/update-carbon-copy.md) — `PUT /v2/carboncopies/update` with `status=Active`.
