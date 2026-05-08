---
title: InterconnectListByStatus
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectListByStatus SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectListByStatus

Returns a paginated list of interconnects scoped to the specified network and mailbox, filtered by lifecycle status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/list-partners.md).
:::

## Method Signature

```
ArrayOfInterconnectIDInfo InterconnectListByStatus(string SessionID, int NetworkID, int MailboxID, Status Status, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `NetworkID` | int | Yes | Network scope; use `0` to include all accessible networks |
| `MailboxID` | int | Yes | Mailbox scope; use `0` to include all mailboxes within the network |
| `Status` | Status | Yes | Filter results by this lifecycle status |
| `PageNo` | short | Yes | 1-based page number for paginated results |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfInterconnectIDInfo

Returns an array of `InterconnectIDInfo` objects. See [InterconnectInfo](./interconnect-info.md) for full field definitions.

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
<InterconnectListByStatusResult>
  <InterconnectIDInfo>
    <InterconnectID>5001</InterconnectID>
    <ECGridIDFrom>123456</ECGridIDFrom>
    <ECGridIDTo>234567</ECGridIDTo>
    <Status>Active</Status>
    <Created>2024-01-15T10:30:00</Created>
    <Modified>2024-06-01T08:00:00</Modified>
  </InterconnectIDInfo>
  <InterconnectIDInfo>
    <InterconnectID>5002</InterconnectID>
    <ECGridIDFrom>123456</ECGridIDFrom>
    <ECGridIDTo>345678</ECGridIDTo>
    <Status>Active</Status>
    <Created>2026-05-07T12:00:00</Created>
    <Modified>2026-05-07T12:00:00</Modified>
  </InterconnectIDInfo>
</InterconnectListByStatusResult>
```

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

// List all active interconnects for a specific mailbox
InterconnectIDInfo[] list = await client.InterconnectListByStatusAsync(
    sessionID,
    networkID: 42,
    mailboxID: 789,
    status: Status.Active,
    pageNo: 1,
    recordsPerPage: 100);

foreach (var interconnect in list)
{
    Console.WriteLine($"ID {interconnect.InterconnectID}: {interconnect.ECGridIDFrom} → {interconnect.ECGridIDTo}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectListByStatus(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectListByStatusAsync({
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

result = client.service.InterconnectListByStatus(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Partners](../../rest-api/partners/list-partners.md) — `POST /v2/partners/list`.
