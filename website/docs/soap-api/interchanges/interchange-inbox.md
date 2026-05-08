---
title: InterchangeInBox
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP InterchangeInBox method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterchangeInBox

List inbound interchanges for a mailbox, with optional filtering by trading partner and date range.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/interchanges/inbox-list.md).
:::

## Method Signature

```
ArrayOfInterchangeIDInfo InterchangeInBox(string SessionID, int NetworkID, int MailboxID,
    int ECGridIDFrom, int ECGridIDTo,
    datetime BeginDate, datetime EndDate, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Network ID; use `0` for the session default |
| `MailboxID` | int | Yes | Mailbox ID; use `0` for the session default |
| `ECGridIDFrom` | int | No | Filter by sender ECGrid ID; use `0` for all |
| `ECGridIDTo` | int | No | Filter by recipient ECGrid ID; use `0` for all |
| `BeginDate` | datetime | Yes | Start of the date range (UTC) |
| `EndDate` | datetime | Yes | End of the date range (UTC) |
| `PageNo` | short | Yes | 1-based page number for paginated results |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfInterchangeIDInfo

Returns an array of `InterchangeIDInfo` objects.

| Field | Type | Description |
|---|---|---|
| `InterchangeID` | long | Unique interchange identifier |
| `ParcelID` | long | Parent parcel that contained this interchange |
| `Sender` | string | ISA06 sender ID |
| `Receiver` | string | ISA08 receiver ID |
| `Standard` | EDIStandard | EDI standard used (e.g., X12, EDIFACT) |
| `DocumentType` | string | Functional identifier / transaction set type |
| `Status` | string | Current interchange status |
| `Created` | datetime | Timestamp when the interchange was received (UTC) |

```xml
<!-- Example response XML -->
<ArrayOfInterchangeIDInfo>
  <InterchangeIDInfo>
    <InterchangeID>5551234</InterchangeID>
    <ParcelID>9876543</ParcelID>
    <Sender>SUPPLIERID</Sender>
    <Receiver>BUYERID</Receiver>
    <Standard>X12</Standard>
    <DocumentType>810</DocumentType>
    <Status>Delivered</Status>
    <Created>2026-05-07T08:05:00Z</Created>
  </InterchangeIDInfo>
</ArrayOfInterchangeIDInfo>
```

## ENUMs

### EDIStandard

| Value | Description |
|---|---|
| `X12` | ANSI X12 |
| `EDIFACT` | UN/EDIFACT |
| `TRADACOMS` | TRADACOMS |
| `VDA` | VDA |
| `XML` | XML payload |
| `TXT` | Plain text |
| `PDF` | PDF document |
| `Binary` | Binary/proprietary format |

See [Appendix — ENUMs](../../appendix/enums.md) for the full `EDIStandard` list.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve today's inbound interchanges
using var client = new ECGridOSPortTypeClient();

var begin = DateTime.UtcNow.Date;
var end   = begin.AddDays(1).AddSeconds(-1);

var interchanges = await client.InterchangeInBoxAsync(
    sessionID,
    networkID:       0,
    mailboxID:       0,
    eCGridIDFrom:    0,
    eCGridIDTo:      0,
    beginDate:       begin,
    endDate:         end,
    pageNo:          1,
    recordsPerPage:  100);

foreach (var ix in interchanges)
{
    Console.WriteLine($"InterchangeID={ix.InterchangeID}  Type={ix.DocumentType}  From={ix.Sender}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterchangeInBox(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterchangeInBoxAsync({
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

result = client.service.InterchangeInBox(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Interchange Inbox List](../../rest-api/interchanges/inbox-list.md).
