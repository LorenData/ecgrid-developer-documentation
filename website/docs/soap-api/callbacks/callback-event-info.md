---
title: CallBackEventInfo
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackEventInfo reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackEventInfo

Returns full details for a single callback event record, including its type, trigger conditions, and associated object identifiers.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/get-event-by-id.md).
:::

## Method Signature

```
CallBackEvent CallBackEventInfo(string SessionID, int CallBackEventID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CallBackEventID` | int | Yes | Unique identifier of the callback event to retrieve |

## Response Object — CallBackEvent

| Field | Type | Description |
|---|---|---|
| `CallBackEventID` | int | Unique identifier for this callback event definition |
| `CallBackID` | int | Identifier of the parent callback configuration |
| `NetworkID` | int | Network associated with this event |
| `MailboxID` | int | Mailbox associated with this event |
| `Event` | Objects | Object type that triggered the event |
| `EventDate` | datetime | Timestamp when the event was raised |
| `ParcelID` | long | Parcel identifier if the event was parcel-related; `0` otherwise |
| `InterchangeID` | long | Interchange identifier if the event was interchange-related; `0` otherwise |
| `UserID` | int | User identifier if the event was user-related; `0` otherwise |
| `Status` | string | Current status of the event (e.g., `Pending`, `Delivered`, `Failed`) |
| `URL` | string | Callback endpoint URL that was notified |
| `HTTPResponse` | int | HTTP status code returned by your endpoint |

```xml
<!-- Example response XML -->
<CallBackEventResult>
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
</CallBackEventResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve details for a specific callback event
var callBackEvent = await client.CallBackEventInfoAsync(sessionID, callBackEventID: 55001);

Console.WriteLine($"Event ID:    {callBackEvent.CallBackEventID}");
Console.WriteLine($"Object Type: {callBackEvent.Event}");
Console.WriteLine($"Status:      {callBackEvent.Status}");
Console.WriteLine($"HTTP Code:   {callBackEvent.HTTPResponse}");
Console.WriteLine($"Event Date:  {callBackEvent.EventDate:O}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackEventInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackEventInfoAsync({
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

result = client.service.CallBackEventInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Event by ID](../../rest-api/callbacks/get-event-by-id.md) — `POST /v2/callbacks/get-event-by-id`.
