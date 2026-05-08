---
title: InterconnectCount
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectCount SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectCount

Returns the total count of interconnects associated with a given ECGrid ID, filtered by lifecycle status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/count-partners.md).
:::

## Method Signature

```
int InterconnectCount(string SessionID, int ECGridID, Status Status)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `ECGridID` | int | Yes | The ECGrid ID to count interconnects for |
| `Status` | Status | Yes | Filter count by lifecycle status |

## Response

Returns an `int` representing the total number of interconnects matching the criteria.

```xml
<!-- Example response XML -->
<InterconnectCountResult>47</InterconnectCountResult>
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | Count interconnects in development |
| `Active` | Count active interconnects |
| `Preproduction` | Count preproduction interconnects |
| `Suspended` | Count suspended interconnects |
| `Terminated` | Count terminated interconnects |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Count all active interconnects for ECGridID 123456
int activeCount = await client.InterconnectCountAsync(
    sessionID,
    ecGridID: 123456,
    status: Status.Active);

Console.WriteLine($"Active interconnects for ECGridID 123456: {activeCount}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectCount(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectCountAsync({
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

result = client.service.InterconnectCount(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Count Partners](../../rest-api/partners/count-partners.md) — `POST /v2/partners/count`.
