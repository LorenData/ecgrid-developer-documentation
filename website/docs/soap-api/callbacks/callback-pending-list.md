---
title: CallBackPendingList
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackPendingList reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackPendingList

Returns all callback queue entries currently in a pending state — events that have been raised but not yet successfully delivered to the registered endpoint.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/queue-list.md).
:::

## Method Signature

```
ArrayOfCallBackQueueIDInfo CallBackPendingList(string SessionID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |

## Response Object — ArrayOfCallBackQueueIDInfo

Returns a collection of `CallBackQueueIDInfo` objects. Each element contains:

| Field | Type | Description |
|---|---|---|
| `CallBackQueueID` | long | Unique identifier for the queued delivery attempt |
| `CallBackID` | int | Identifier of the parent callback configuration |
| `NetworkID` | int | Network associated with this queue entry |
| `MailboxID` | int | Mailbox associated with this queue entry |
| `URL` | string | Callback endpoint targeted for delivery |
| `Event` | Objects | Object type that triggered this queue entry |
| `Status` | string | Current queue status (always `Pending` in this list) |
| `CreateDate` | datetime | Timestamp when the event was enqueued |
| `LastAttemptDate` | datetime | Timestamp of the most recent delivery attempt |
| `AttemptCount` | int | Number of delivery attempts made so far |

```xml
<!-- Example response XML -->
<ArrayOfCallBackQueueIDInfoResult>
  <CallBackQueueIDInfo>
    <CallBackQueueID>98770</CallBackQueueID>
    <CallBackID>42</CallBackID>
    <NetworkID>1</NetworkID>
    <MailboxID>100</MailboxID>
    <URL>https://your-app.example.com/ecgrid/callback</URL>
    <Event>Parcel</Event>
    <Status>Pending</Status>
    <CreateDate>2026-05-07T10:15:00</CreateDate>
    <LastAttemptDate>2026-05-07T10:16:00</LastAttemptDate>
    <AttemptCount>1</AttemptCount>
  </CallBackQueueIDInfo>
</ArrayOfCallBackQueueIDInfoResult>
```

## Variants

### CallBackPendingListEx

Returns pending callbacks scoped to a specific network and mailbox.

```
ArrayOfCallBackQueueIDInfo CallBackPendingListEx(string SessionID, int NetworkID, int MailboxID)
```

| Additional Parameter | Type | Description |
|---|---|---|
| `NetworkID` | int | Filter results to a specific network; `0` for all accessible networks |
| `MailboxID` | int | Filter results to a specific mailbox; `0` for all mailboxes under the network |

```csharp
// Scoped variant — filter to a specific mailbox
var pending = await client.CallBackPendingListExAsync(sessionID, networkID: 1, mailboxID: 100);
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve all pending callbacks across all networks and mailboxes
var pendingItems = await client.CallBackPendingListAsync(sessionID);

Console.WriteLine($"Pending callback deliveries: {pendingItems.Length}");

foreach (var item in pendingItems)
{
    Console.WriteLine(
        $"QueueID={item.CallBackQueueID} Event={item.Event} " +
        $"Attempts={item.AttemptCount} Last={item.LastAttemptDate:O}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackPendingList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackPendingListAsync({
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

result = client.service.CallBackPendingList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Queue List](../../rest-api/callbacks/queue-list.md) — `POST /v2/callbacks/queue-list` with `status=Pending`.
