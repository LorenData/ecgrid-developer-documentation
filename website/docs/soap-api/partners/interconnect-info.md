---
title: InterconnectInfo
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectInfo SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectInfo

Returns detailed information about a single trading partner interconnect by its numeric identifier.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/get-partner.md).
:::

## Method Signature

```
InterconnectIDInfo InterconnectInfo(string SessionID, int InterconnectID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `InterconnectID` | int | Yes | Numeric identifier for the interconnect record |

## Response Object — InterconnectIDInfo

| Field | Type | Description |
|---|---|---|
| `InterconnectID` | int | Unique numeric identifier for this interconnect |
| `ECGridIDFrom` | int | ECGrid ID of the sending trading partner |
| `ECGridIDTo` | int | ECGrid ID of the receiving trading partner |
| `Status` | Status | Current lifecycle status of the interconnect |
| `Created` | datetime | Timestamp when the interconnect was established |
| `Modified` | datetime | Timestamp of the last modification |

```xml
<!-- Example response XML -->
<InterconnectInfoResult>
  <InterconnectID>5001</InterconnectID>
  <ECGridIDFrom>123456</ECGridIDFrom>
  <ECGridIDTo>234567</ECGridIDTo>
  <Status>Active</Status>
  <Created>2024-01-15T10:30:00</Created>
  <Modified>2024-06-01T08:00:00</Modified>
</InterconnectInfoResult>
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | Interconnect is being configured |
| `Active` | Interconnect is live; EDI traffic can flow |
| `Preproduction` | Interconnect is staged for production |
| `Suspended` | Interconnect is temporarily halted |
| `Terminated` | Interconnect has been permanently closed |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

InterconnectIDInfo info = await client.InterconnectInfoAsync(sessionID, 5001);

Console.WriteLine($"Interconnect {info.InterconnectID}: {info.ECGridIDFrom} → {info.ECGridIDTo}");
Console.WriteLine($"Status: {info.Status}  Created: {info.Created:yyyy-MM-dd}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectInfoAsync({
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

result = client.service.InterconnectInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Partner](../../rest-api/partners/get-partner.md) — `GET /v2/partners/{id}`.
