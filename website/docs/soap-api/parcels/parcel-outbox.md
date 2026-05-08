---
title: ParcelOutBox
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelOutBox method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelOutBox

List parcels in the outbound queue for a mailbox, with optional filtering by trading partner, status, and date range.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/parcels/outbox-list.md).
:::

## Method Signature

```
ArrayOfParcelIDInfo ParcelOutBox(string SessionID, int NetworkID, int MailboxID,
    int ECGridIDFrom, int ECGridIDTo, ParcelStatus Status,
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
| `Status` | ParcelStatus | Yes | Parcel status filter (see ENUMs below) |
| `BeginDate` | datetime | Yes | Start of the date range (UTC) |
| `EndDate` | datetime | Yes | End of the date range (UTC) |
| `PageNo` | short | Yes | 1-based page number for paginated results |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfParcelIDInfo

Returns an array of `ParcelIDInfo` objects.

| Field | Type | Description |
|---|---|---|
| `ParcelID` | long | Unique parcel identifier |
| `NetworkID` | int | Network that owns the parcel |
| `MailboxID` | int | Mailbox that sent the parcel |
| `FileName` | string | Original file name of the parcel |
| `Bytes` | int | File size in bytes |
| `Status` | ParcelStatus | Current parcel status |
| `ECGridIDFrom` | int | Sender ECGrid ID |
| `ECGridIDTo` | int | Recipient ECGrid ID |
| `Created` | datetime | Timestamp when the parcel was created (UTC) |

```xml
<!-- Example response XML -->
<ArrayOfParcelIDInfo>
  <ParcelIDInfo>
    <ParcelID>9876544</ParcelID>
    <NetworkID>1</NetworkID>
    <MailboxID>101</MailboxID>
    <FileName>po_20260507.edi</FileName>
    <Bytes>2048</Bytes>
    <Status>ftpSent</Status>
    <ECGridIDFrom>654321</ECGridIDFrom>
    <ECGridIDTo>123456</ECGridIDTo>
    <Created>2026-05-07T09:30:00Z</Created>
  </ParcelIDInfo>
</ArrayOfParcelIDInfo>
```

## ENUMs

### ParcelStatus

| Value | Description |
|---|---|
| `InBoxReady` | Parcel is available for download |
| `InBoxTransferred` | Parcel has been downloaded and confirmed |
| `as2Receive` | Parcel received via AS2 |
| `as2Sent` | Parcel sent via AS2 |
| `ftpReceived` | Parcel received via FTP |
| `ftpSent` | Parcel delivered via FTP |
| `outboxDeliveryError` | Outbound delivery failed |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete `ParcelStatus` value list.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve the first page of outbound parcels sent today
using var client = new ECGridOSPortTypeClient();

var begin = DateTime.UtcNow.Date;
var end   = begin.AddDays(1).AddSeconds(-1);

var parcels = await client.ParcelOutBoxAsync(
    sessionID,
    networkID:       0,
    mailboxID:       0,
    eCGridIDFrom:    0,
    eCGridIDTo:      0,
    status:          ParcelStatus.ftpSent,
    beginDate:       begin,
    endDate:         end,
    pageNo:          1,
    recordsPerPage:  100);

foreach (var parcel in parcels)
{
    Console.WriteLine($"ParcelID={parcel.ParcelID}  File={parcel.FileName}  Status={parcel.Status}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelOutBox(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelOutBoxAsync({
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

result = client.service.ParcelOutBox(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Parcel Outbox List](../../rest-api/parcels/outbox-list.md).
