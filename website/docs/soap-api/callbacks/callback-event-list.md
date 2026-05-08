---
title: CallBackEventList
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackEventList reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackEventList

Returns a paged list of callback events filtered by network, mailbox, object type, and date range.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/event-list.md).
:::

## Method Signature

```
ArrayOfCallBackEvent CallBackEventList(string SessionID, int NetworkID, int MailboxID,
    Objects Event, datetime BeginDate, datetime EndDate, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Filter by network; `0` for all accessible networks |
| `MailboxID` | int | Yes | Filter by mailbox; `0` for all mailboxes under the specified network |
| `Event` | Objects | Yes | Filter by object type (e.g., `Parcel`, `Interchange`); use the integer value `0` for all event types |
| `BeginDate` | datetime | Yes | Start of the date range (inclusive) for event lookup |
| `EndDate` | datetime | Yes | End of the date range (inclusive) for event lookup |
| `PageNo` | short | Yes | 1-based page number for paginated results |
| `RecordsPerPage` | short | Yes | Number of records to return per page (maximum typically 100) |

## Response Object — ArrayOfCallBackEvent

Returns a collection of `CallBackEvent` objects. Each element contains:

| Field | Type | Description |
|---|---|---|
| `CallBackEventID` | int | Unique identifier for the callback event |
| `CallBackID` | int | Identifier of the parent callback configuration |
| `NetworkID` | int | Network associated with the event |
| `MailboxID` | int | Mailbox associated with the event |
| `Event` | Objects | Object type that triggered the event |
| `EventDate` | datetime | Timestamp when the event occurred |
| `ParcelID` | long | Parcel ID if parcel-related; `0` otherwise |
| `InterchangeID` | long | Interchange ID if interchange-related; `0` otherwise |
| `UserID` | int | User ID if user-related; `0` otherwise |
| `Status` | string | Delivery status (`Pending`, `Delivered`, `Failed`) |
| `URL` | string | Callback endpoint that was notified |
| `HTTPResponse` | int | HTTP status code returned by the endpoint |

```xml
<!-- Example response XML -->
<ArrayOfCallBackEventResult>
  <CallBackEvent>
    <CallBackEventID>55001</CallBackEventID>
    <CallBackID>42</CallBackID>
    <NetworkID>1</NetworkID>
    <MailboxID>100</MailboxID>
    <Event>Parcel</Event>
    <EventDate>2026-05-07T09:30:00</EventDate>
    <ParcelID>7890123</ParcelID>
    <InterchangeID>0</InterchangeID>
    <UserID>0</UserID>
    <Status>Delivered</Status>
    <URL>https://your-app.example.com/ecgrid/callback</URL>
    <HTTPResponse>200</HTTPResponse>
  </CallBackEvent>
</ArrayOfCallBackEventResult>
```

## ENUMs

### Objects

| Value | Description |
|---|---|
| `Parcel` | Parcel (file) receipt and delivery events |
| `Interchange` | EDI interchange events |
| `Mailbox` | Mailbox events |
| `ECGridID` | Trading partner ID events |
| `Interconnect` | Partner interconnect events |
| `CarbonCopy` | Carbon copy rule events |
| `User` | User account events |
| `Network` | Network configuration events |

See [Appendix — ENUMs](../../appendix/enums.md) for the complete `Objects` enumeration.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve all Parcel callback events for today, page 1
var events = await client.CallBackEventListAsync(
    sessionID,
    networkID: 1,
    mailboxID: 0,
    @event: Objects.Parcel,
    beginDate: DateTime.UtcNow.Date,
    endDate: DateTime.UtcNow,
    pageNo: 1,
    recordsPerPage: 50);

foreach (var ev in events)
{
    Console.WriteLine($"[{ev.EventDate:O}] EventID={ev.CallBackEventID} Status={ev.Status} HTTP={ev.HTTPResponse}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackEventList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackEventListAsync({
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

result = client.service.CallBackEventList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Event List](../../rest-api/callbacks/event-list.md) — `POST /v2/callbacks/event-list`.
