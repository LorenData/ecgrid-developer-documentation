---
title: TPList
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of TPList SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TPList

Returns a paginated list of ECGrid trading partner IDs scoped to the specified network and mailbox.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/list-ids.md).
:::

## Method Signature

```
ArrayOfECGridIDInfo TPList(string SessionID, int NetworkID, int MailboxID, Status Status, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `NetworkID` | int | Yes | Network scope; use `0` to include all accessible networks |
| `MailboxID` | int | Yes | Mailbox scope; use `0` to include all mailboxes within the network |
| `Status` | Status | Yes | Filter by lifecycle status; use `Active` for live IDs |
| `PageNo` | short | Yes | 1-based page number for paginated results |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfECGridIDInfo

Returns an array of `ECGridIDInfo` objects. See [ECGridIDInfo](./ecgrid-id-info.md) for field definitions.

| Field | Type | Description |
|---|---|---|
| `ECGridID` | int | Unique numeric identifier |
| `MailboxID` | int | Owning mailbox ID |
| `NetworkID` | int | Associated network ID |
| `Qualifier` | string | ISA qualifier |
| `ID` | string | ISA ID value |
| `Description` | string | Trading partner label |
| `Status` | Status | Lifecycle status |
| `RoutingGroup` | RoutingGroup | Routing group |
| `EDIStandard` | EDIStandard | EDI standard |

```xml
<!-- Example response XML -->
<TPListResult>
  <ECGridIDInfo>
    <ECGridID>123456</ECGridID>
    <MailboxID>789</MailboxID>
    <NetworkID>42</NetworkID>
    <Qualifier>01</Qualifier>
    <ID>ACMECORP      </ID>
    <Description>Acme Corporation</Description>
    <Status>Active</Status>
    <RoutingGroup>ProductionA</RoutingGroup>
    <EDIStandard>X12</EDIStandard>
  </ECGridIDInfo>
  <ECGridIDInfo>
    <ECGridID>123457</ECGridID>
    <MailboxID>789</MailboxID>
    <NetworkID>42</NetworkID>
    <Qualifier>ZZ</Qualifier>
    <ID>PARTNER002</ID>
    <Description>Partner Two</Description>
    <Status>Active</Status>
    <RoutingGroup>ProductionA</RoutingGroup>
    <EDIStandard>X12</EDIStandard>
  </ECGridIDInfo>
</TPListResult>
```

## Variants

### TPListEx

Extends `TPList` with an additional `RoutingGroup` filter parameter, allowing results to be scoped to a specific routing group.

| Additional Parameter | Type | Description |
|---|---|---|
| `RoutingGroup` | RoutingGroup | Filter results to a specific routing group |

```
ArrayOfECGridIDInfo TPListEx(string SessionID, int NetworkID, int MailboxID, Status Status, RoutingGroup RoutingGroup, short PageNo, short RecordsPerPage)
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | ID is in development/testing |
| `Active` | ID is live and routing traffic |
| `Preproduction` | ID is staged for production |
| `Suspended` | ID is temporarily inactive |
| `Terminated` | ID has been permanently disabled |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Retrieve the first page of active IDs for a specific mailbox
ECGridIDInfo[] idList = await client.TPListAsync(
    sessionID,
    networkID: 42,
    mailboxID: 789,
    status: Status.Active,
    pageNo: 1,
    recordsPerPage: 100);

foreach (var id in idList)
{
    Console.WriteLine($"{id.Qualifier}:{id.ID} — {id.Description}");
}

// Using the Ex variant to filter by routing group
ECGridIDInfo[] filteredList = await client.TPListExAsync(
    sessionID,
    networkID: 42,
    mailboxID: 789,
    status: Status.Active,
    routingGroup: RoutingGroup.ProductionA,
    pageNo: 1,
    recordsPerPage: 100);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.TPList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.TPListAsync({
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

result = client.service.TPList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List IDs](../../rest-api/ids/list-ids.md) — `POST /v2/ids/list`.
