---
title: CallBackFailedList
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackFailedList reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackFailedList

Returns all callback queue entries that failed delivery within the past N days, allowing you to identify and investigate endpoints that are not receiving notifications.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/queue-list.md).
:::

## Method Signature

```
ArrayOfCallBackQueueIDInfo CallBackFailedList(string SessionID, short MaxDays)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `MaxDays` | short | Yes | Number of past days to search for failed callbacks (e.g., `7` returns failures from the last week) |

## Response Object — ArrayOfCallBackQueueIDInfo

Returns a collection of `CallBackQueueIDInfo` objects for entries that exhausted all retry attempts. Each element contains:

| Field | Type | Description |
|---|---|---|
| `CallBackQueueID` | long | Unique identifier for the queued delivery attempt |
| `CallBackID` | int | Identifier of the parent callback configuration |
| `NetworkID` | int | Network associated with this queue entry |
| `MailboxID` | int | Mailbox associated with this queue entry |
| `URL` | string | Callback endpoint that failed to receive the notification |
| `Event` | Objects | Object type that triggered this queue entry |
| `Status` | string | Queue status (always `Failed` in this list) |
| `CreateDate` | datetime | Timestamp when the event was first enqueued |
| `LastAttemptDate` | datetime | Timestamp of the final delivery attempt |
| `AttemptCount` | int | Total number of delivery attempts made |
| `HTTPResponse` | int | Last HTTP status code returned (or `0` for connection errors) |

```xml
<!-- Example response XML -->
<ArrayOfCallBackQueueIDInfoResult>
  <CallBackQueueIDInfo>
    <CallBackQueueID>98755</CallBackQueueID>
    <CallBackID>42</CallBackID>
    <NetworkID>1</NetworkID>
    <MailboxID>100</MailboxID>
    <URL>https://your-app.example.com/ecgrid/callback</URL>
    <Event>Parcel</Event>
    <Status>Failed</Status>
    <CreateDate>2026-05-06T14:00:00</CreateDate>
    <LastAttemptDate>2026-05-06T14:30:00</LastAttemptDate>
    <AttemptCount>5</AttemptCount>
    <HTTPResponse>503</HTTPResponse>
  </CallBackQueueIDInfo>
</ArrayOfCallBackQueueIDInfoResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Check for failed callbacks in the last 7 days
var failedItems = await client.CallBackFailedListAsync(sessionID, maxDays: 7);

if (failedItems.Length == 0)
{
    Console.WriteLine("No failed callbacks in the past 7 days.");
    return;
}

Console.WriteLine($"Failed callback deliveries (last 7 days): {failedItems.Length}");

foreach (var item in failedItems)
{
    Console.WriteLine(
        $"QueueID={item.CallBackQueueID} URL={item.URL} " +
        $"Attempts={item.AttemptCount} HTTP={item.HTTPResponse} " +
        $"LastAttempt={item.LastAttemptDate:O}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackFailedList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackFailedListAsync({
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

result = client.service.CallBackFailedList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Queue List](../../rest-api/callbacks/queue-list.md) — `POST /v2/callbacks/queue-list` with `status=Failed`.
