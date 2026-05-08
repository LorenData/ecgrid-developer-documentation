---
title: InterconnectListByECGridID
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectListByECGridID SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectListByECGridID

Returns a paginated list of all interconnects for a specific ECGrid ID, filtered by lifecycle status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/list-partners.md).
:::

## Method Signature

```
ArrayOfInterconnectIDInfo InterconnectListByECGridID(string SessionID, int ECGridID, Status Status, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `ECGridID` | int | Yes | The ECGrid ID whose interconnects to retrieve (as sender or receiver) |
| `Status` | Status | Yes | Filter results by this lifecycle status |
| `PageNo` | short | Yes | 1-based page number for paginated results |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfInterconnectIDInfo

Returns an array of `InterconnectIDInfo` objects where `ECGridID` appears as either `ECGridIDFrom` or `ECGridIDTo`. See [InterconnectInfo](./interconnect-info.md) for full field definitions.

| Field | Type | Description |
|---|---|---|
| `InterconnectID` | int | Unique numeric identifier |
| `ECGridIDFrom` | int | ECGrid ID of the sending trading partner |
| `ECGridIDTo` | int | ECGrid ID of the receiving trading partner |
| `Status` | Status | Lifecycle status |
| `Created` | datetime | Creation timestamp |
| `Modified` | datetime | Last modification timestamp |

```xml
<!-- Example response XML -->
<InterconnectListByECGridIDResult>
  <InterconnectIDInfo>
    <InterconnectID>5001</InterconnectID>
    <ECGridIDFrom>123456</ECGridIDFrom>
    <ECGridIDTo>234567</ECGridIDTo>
    <Status>Active</Status>
    <Created>2024-01-15T10:30:00</Created>
    <Modified>2024-06-01T08:00:00</Modified>
  </InterconnectIDInfo>
  <InterconnectIDInfo>
    <InterconnectID>4900</InterconnectID>
    <ECGridIDFrom>111111</ECGridIDFrom>
    <ECGridIDTo>123456</ECGridIDTo>
    <Status>Active</Status>
    <Created>2023-08-20T09:00:00</Created>
    <Modified>2023-08-20T09:00:00</Modified>
  </InterconnectIDInfo>
</InterconnectListByECGridIDResult>
```

:::note
This method returns all interconnects where the specified ECGrid ID appears in either the `ECGridIDFrom` or `ECGridIDTo` position. Use this to get a complete picture of all trading relationships for a single ID.
:::

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | Interconnect is being configured |
| `Active` | Interconnect is live |
| `Preproduction` | Staged for production |
| `Suspended` | Temporarily halted |
| `Terminated` | Permanently closed |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Retrieve all active interconnects involving ECGridID 123456
InterconnectIDInfo[] list = await client.InterconnectListByECGridIDAsync(
    sessionID,
    ecGridID: 123456,
    status: Status.Active,
    pageNo: 1,
    recordsPerPage: 100);

foreach (var interconnect in list)
{
    string direction = interconnect.ECGridIDFrom == 123456 ? "→" : "←";
    int partner = interconnect.ECGridIDFrom == 123456
        ? interconnect.ECGridIDTo
        : interconnect.ECGridIDFrom;

    Console.WriteLine($"InterconnectID {interconnect.InterconnectID}: 123456 {direction} {partner}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectListByECGridID(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectListByECGridIDAsync({
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

result = client.service.InterconnectListByECGridID(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Partners](../../rest-api/partners/list-partners.md) — `POST /v2/partners/list` (filter by `ecGridId`).
