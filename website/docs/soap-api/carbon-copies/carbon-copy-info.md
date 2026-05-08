---
title: CarbonCopyInfo
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CarbonCopyInfo reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CarbonCopyInfo

Returns the full configuration details for a specific carbon copy rule, including its direction, linked mailboxes, and current status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/carbon-copies/get-carbon-copy.md).
:::

## Method Signature

```
CarbonCopyIDInfo CarbonCopyInfo(string SessionID, int CarbonCopyID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CarbonCopyID` | int | Yes | Unique identifier of the carbon copy rule to retrieve |

## Response Object — CarbonCopyIDInfo

| Field | Type | Description |
|---|---|---|
| `CarbonCopyID` | int | Unique identifier for this carbon copy rule |
| `FromMailboxID` | int | Source mailbox whose traffic is being copied |
| `ToMailboxID` | int | Destination mailbox receiving the duplicate traffic |
| `Direction` | Direction | Traffic direction being copied (`InBox` or `OutBox`) |
| `Status` | Status | Current rule status (`Active`, `Suspended`, `Terminated`) |
| `CreateDate` | datetime | Timestamp when the rule was created |
| `ModDate` | datetime | Timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<CarbonCopyIDInfoResult>
  <CarbonCopyID>301</CarbonCopyID>
  <FromMailboxID>100</FromMailboxID>
  <ToMailboxID>200</ToMailboxID>
  <Direction>InBox</Direction>
  <Status>Active</Status>
  <CreateDate>2026-05-01T08:00:00</CreateDate>
  <ModDate>2026-05-07T09:00:00</ModDate>
</CarbonCopyIDInfoResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve current configuration for a carbon copy rule
var ccInfo = await client.CarbonCopyInfoAsync(sessionID, carbonCopyID: 301);

Console.WriteLine($"CarbonCopyID: {ccInfo.CarbonCopyID}");
Console.WriteLine($"From Mailbox: {ccInfo.FromMailboxID}");
Console.WriteLine($"To Mailbox:   {ccInfo.ToMailboxID}");
Console.WriteLine($"Direction:    {ccInfo.Direction}");
Console.WriteLine($"Status:       {ccInfo.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CarbonCopyInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CarbonCopyInfoAsync({
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

result = client.service.CarbonCopyInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Carbon Copy](../../rest-api/carbon-copies/get-carbon-copy.md) — `GET /v2/carboncopies/{id}`.
