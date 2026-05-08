---
title: CarbonCopyList
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CarbonCopyList reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CarbonCopyList

Returns all carbon copy rules associated with a specific mailbox, optionally filtered by rule status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/carbon-copies/list-carbon-copies.md).
:::

## Method Signature

```
ArrayOfCarbonCopyIDInfo CarbonCopyList(string SessionID, int MailboxID, Status Status)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `MailboxID` | int | Yes | Mailbox to query for carbon copy rules (as either source or destination) |
| `Status` | Status | Yes | Filter by rule status; use `Active` to list only live rules, or the appropriate value to include suspended or terminated rules |

## Response Object — ArrayOfCarbonCopyIDInfo

Returns a collection of `CarbonCopyIDInfo` objects. Each element contains:

| Field | Type | Description |
|---|---|---|
| `CarbonCopyID` | int | Unique identifier for the carbon copy rule |
| `FromMailboxID` | int | Source mailbox whose traffic is being copied |
| `ToMailboxID` | int | Destination mailbox receiving the duplicate traffic |
| `Direction` | Direction | Traffic direction being copied (`InBox` or `OutBox`) |
| `Status` | Status | Current rule status |
| `CreateDate` | datetime | Timestamp when the rule was created |
| `ModDate` | datetime | Timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<ArrayOfCarbonCopyIDInfoResult>
  <CarbonCopyIDInfo>
    <CarbonCopyID>301</CarbonCopyID>
    <FromMailboxID>100</FromMailboxID>
    <ToMailboxID>200</ToMailboxID>
    <Direction>InBox</Direction>
    <Status>Active</Status>
    <CreateDate>2026-05-01T08:00:00</CreateDate>
    <ModDate>2026-05-07T09:00:00</ModDate>
  </CarbonCopyIDInfo>
</ArrayOfCarbonCopyIDInfoResult>
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Active` | Rule is live and duplicating traffic |
| `Suspended` | Rule is temporarily paused |
| `Terminated` | Rule has been permanently removed |
| `Development` | Rule is in a development/testing state |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete `Status` enumeration.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// List all active carbon copy rules for a mailbox
var rules = await client.CarbonCopyListAsync(sessionID, mailboxID: 100, status: Status.Active);

Console.WriteLine($"Active carbon copy rules for mailbox 100: {rules.Length}");

foreach (var rule in rules)
{
    Console.WriteLine(
        $"ID={rule.CarbonCopyID} From={rule.FromMailboxID} To={rule.ToMailboxID} Dir={rule.Direction}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CarbonCopyList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CarbonCopyListAsync({
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

result = client.service.CarbonCopyList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Carbon Copies](../../rest-api/carbon-copies/list-carbon-copies.md) — `POST /v2/carboncopies/list`.
