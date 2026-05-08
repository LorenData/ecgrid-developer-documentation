---
title: CallBackTest
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackTest reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackTest

Sends a synthetic test event to the registered callback endpoint to verify that it is reachable and responding correctly.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/test-callback.md).
:::

## Method Signature

```
CallBackQueueIDInfo CallBackTest(string SessionID, int CallBackEventID, long ParcelID,
    long InterchangeID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CallBackEventID` | int | Yes | ID of the callback event definition to test; identifies which endpoint configuration to target |
| `ParcelID` | long | No | Parcel ID to include in the test payload; use `0` if the callback is not parcel-scoped |
| `InterchangeID` | long | No | Interchange ID to include in the test payload; use `0` if not interchange-scoped |
| `UserID` | int | No | User ID to include in the test payload; use `0` if not user-scoped |

## Response Object — CallBackQueueIDInfo

| Field | Type | Description |
|---|---|---|
| `CallBackQueueID` | long | Unique identifier for the queued test delivery |
| `CallBackID` | int | Identifier of the callback configuration being tested |
| `NetworkID` | int | Network associated with the test event |
| `MailboxID` | int | Mailbox associated with the test event |
| `URL` | string | Callback endpoint that received the test POST |
| `Event` | Objects | Object type used for the test event |
| `Status` | string | Delivery status of the test (`Pending`, `Delivered`, `Failed`) |
| `CreateDate` | datetime | Timestamp when the test was dispatched |
| `HTTPResponse` | int | HTTP status code returned by your endpoint |

```xml
<!-- Example response XML -->
<CallBackQueueIDInfoResult>
  <CallBackQueueID>99001</CallBackQueueID>
  <CallBackID>42</CallBackID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <URL>https://your-app.example.com/ecgrid/callback</URL>
  <Event>Parcel</Event>
  <Status>Delivered</Status>
  <CreateDate>2026-05-07T13:00:00</CreateDate>
  <HTTPResponse>200</HTTPResponse>
</CallBackQueueIDInfoResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Fire a test event against a specific callback event configuration
var testResult = await client.CallBackTestAsync(
    sessionID,
    callBackEventID: 55001,
    parcelID: 0L,
    interchangeID: 0L,
    userID: 0);

Console.WriteLine($"Test dispatched. Queue ID: {testResult.CallBackQueueID}");
Console.WriteLine($"Status:    {testResult.Status}");
Console.WriteLine($"HTTP Code: {testResult.HTTPResponse}");

if (testResult.HTTPResponse == 200)
    Console.WriteLine("Endpoint is healthy and accepting callbacks.");
else
    Console.WriteLine($"Warning: endpoint returned HTTP {testResult.HTTPResponse}.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackTest(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackTestAsync({
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

result = client.service.CallBackTest(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Test Callback](../../rest-api/callbacks/test-callback.md) — `POST /v2/callbacks/test`.
