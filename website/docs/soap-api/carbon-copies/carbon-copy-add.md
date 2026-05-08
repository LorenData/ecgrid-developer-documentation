---
title: CarbonCopyAdd
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CarbonCopyAdd reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CarbonCopyAdd

Creates a new carbon copy rule that automatically duplicates EDI traffic flowing in the specified direction from one mailbox to another.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/carbon-copies/create-carbon-copy.md).
:::

## Method Signature

```
int CarbonCopyAdd(string SessionID, int FromMailboxID, int ToMailboxID, Direction Direction)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `FromMailboxID` | int | Yes | Mailbox whose inbound or outbound traffic will be copied |
| `ToMailboxID` | int | Yes | Mailbox that will receive the duplicate traffic |
| `Direction` | Direction | Yes | Which traffic direction to copy (`InBox`, `OutBox`) |

## Response

Returns an `int` representing the newly created `CarbonCopyID`. Store this value to manage or terminate the rule later.

```xml
<!-- Example response XML -->
<CarbonCopyAddResult>301</CarbonCopyAddResult>
```

## ENUMs

### Direction

| Value | Description |
|---|---|
| `NoDir` | No direction specified (not valid for this call) |
| `OutBox` | Copy outbound traffic from `FromMailboxID` to `ToMailboxID` |
| `InBox` | Copy inbound traffic arriving at `FromMailboxID` to `ToMailboxID` |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete `Direction` enumeration.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Mirror all inbound parcels from mailbox 100 to mailbox 200 for archival
int carbonCopyId = await client.CarbonCopyAddAsync(
    sessionID,
    fromMailboxID: 100,
    toMailboxID: 200,
    direction: Direction.InBox);

Console.WriteLine($"Carbon copy rule created. CarbonCopyID: {carbonCopyId}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CarbonCopyAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CarbonCopyAddAsync({
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

result = client.service.CarbonCopyAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create Carbon Copy](../../rest-api/carbon-copies/create-carbon-copy.md) — `POST /v2/carboncopies/create`.
