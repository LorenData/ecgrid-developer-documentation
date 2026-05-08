---
title: CallBackQueueInfo
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackQueueInfo reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackQueueInfo

Returns the status and delivery details for a specific callback queue entry, identified by its queue ID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/get-queue-by-id.md).
:::

## Method Signature

```
CallBackQueueIDInfo CallBackQueueInfo(string SessionID, long CallBackQueueID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CallBackQueueID` | long | Yes | Unique identifier of the callback queue entry to retrieve |

## Response Object — CallBackQueueIDInfo

| Field | Type | Description |
|---|---|---|
| `CallBackQueueID` | long | Unique identifier for this queue entry |
| `CallBackID` | int | Identifier of the parent callback configuration |
| `NetworkID` | int | Network associated with this queue entry |
| `MailboxID` | int | Mailbox associated with this queue entry |
| `URL` | string | Callback endpoint targeted for delivery |
| `Event` | Objects | Object type that triggered the callback |
| `Status` | string | Current queue status (`Pending`, `Delivered`, `Failed`) |
| `CreateDate` | datetime | Timestamp when the event was first enqueued |
| `LastAttemptDate` | datetime | Timestamp of the most recent delivery attempt |
| `AttemptCount` | int | Number of delivery attempts made |
| `HTTPResponse` | int | HTTP status code from the most recent delivery attempt; `0` for connection errors |
| `ParcelID` | long | Related parcel ID if event type is `Parcel`; `0` otherwise |
| `InterchangeID` | long | Related interchange ID if event type is `Interchange`; `0` otherwise |

```xml
<!-- Example response XML -->
<CallBackQueueIDInfoResult>
  <CallBackQueueID>98770</CallBackQueueID>
  <CallBackID>42</CallBackID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <URL>https://your-app.example.com/ecgrid/callback</URL>
  <Event>Parcel</Event>
  <Status>Delivered</Status>
  <CreateDate>2026-05-07T10:15:00</CreateDate>
  <LastAttemptDate>2026-05-07T10:15:03</LastAttemptDate>
  <AttemptCount>1</AttemptCount>
  <HTTPResponse>200</HTTPResponse>
  <ParcelID>7890123</ParcelID>
  <InterchangeID>0</InterchangeID>
</CallBackQueueIDInfoResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Look up the status of a specific queued callback delivery
var queueEntry = await client.CallBackQueueInfoAsync(sessionID, callBackQueueID: 98770L);

Console.WriteLine($"Queue ID:    {queueEntry.CallBackQueueID}");
Console.WriteLine($"Status:      {queueEntry.Status}");
Console.WriteLine($"Attempts:    {queueEntry.AttemptCount}");
Console.WriteLine($"HTTP Code:   {queueEntry.HTTPResponse}");
Console.WriteLine($"Last Try:    {queueEntry.LastAttemptDate:O}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackQueueInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackQueueInfoAsync({
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

result = client.service.CallBackQueueInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Queue by ID](../../rest-api/callbacks/get-queue-by-id.md) — `GET /v2/callbacks/get-queue-by-id`.
