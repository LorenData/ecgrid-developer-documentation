---
title: CallBackAdd
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CallBackAdd reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CallBackAdd

Registers a new callback endpoint so ECGridOS can POST event notifications to your URL when specified objects change state.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/callbacks/create-callback.md).
:::

## Method Signature

```
CallBackQueueIDInfo CallBackAdd(string SessionID, int NetworkID, int MailboxID, string URL,
    Objects Event, HTTPAuthType AuthType, string Username, string Password)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Network scope for the callback; `0` for all networks |
| `MailboxID` | int | Yes | Mailbox scope for the callback; `0` for all mailboxes under the network |
| `URL` | string | Yes | HTTPS endpoint that will receive the callback POST |
| `Event` | Objects | Yes | Object type that triggers the callback (e.g., `Parcel`, `Interchange`) |
| `AuthType` | HTTPAuthType | Yes | HTTP authentication method ECGridOS uses when calling your endpoint |
| `Username` | string | No | Username for HTTP Basic or Digest authentication; empty string if `AuthType` is `None` |
| `Password` | string | No | Password for HTTP Basic or Digest authentication; empty string if `AuthType` is `None` |

## Response Object — CallBackQueueIDInfo

| Field | Type | Description |
|---|---|---|
| `CallBackQueueID` | long | Unique identifier for the queued callback registration event |
| `CallBackID` | int | Identifier of the newly created callback configuration |
| `NetworkID` | int | Network the callback is scoped to |
| `MailboxID` | int | Mailbox the callback is scoped to |
| `URL` | string | Registered callback endpoint URL |
| `Event` | Objects | Object type that triggers this callback |
| `Status` | string | Current status of the callback queue entry |
| `CreateDate` | datetime | Timestamp when the callback was registered |

```xml
<!-- Example response XML -->
<CallBackQueueIDInfoResult>
  <CallBackQueueID>98765</CallBackQueueID>
  <CallBackID>42</CallBackID>
  <NetworkID>1</NetworkID>
  <MailboxID>100</MailboxID>
  <URL>https://your-app.example.com/ecgrid/callback</URL>
  <Event>Parcel</Event>
  <Status>Active</Status>
  <CreateDate>2026-05-07T12:00:00</CreateDate>
</CallBackQueueIDInfoResult>
```

## ENUMs

### Objects

| Value | Description |
|---|---|
| `System` | System-level events |
| `User` | User account events |
| `Network` | Network configuration events |
| `Mailbox` | Mailbox events |
| `ECGridID` | Trading partner ID events |
| `Interconnect` | Partner interconnect events |
| `Parcel` | Parcel (file) receipt and delivery events |
| `Interchange` | EDI interchange events |
| `CarbonCopy` | Carbon copy rule events |
| `CallBackEvent` | Callback system events |
| `AS2` | AS2 communication events |
| `Comm` | Communication channel events |

See [Appendix — ENUMs](../../appendix/enums.md) for the full `Objects` enumeration.

### HTTPAuthType

| Value | Description |
|---|---|
| `None` | No HTTP authentication |
| `Basic` | HTTP Basic authentication (Base64-encoded credentials) |
| `Digest` | HTTP Digest authentication |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Register a callback for inbound parcel events on a specific mailbox
var result = await client.CallBackAddAsync(
    sessionID,
    networkID: 1,
    mailboxID: 100,
    url: "https://your-app.example.com/ecgrid/callback",
    @event: Objects.Parcel,
    authType: HTTPAuthType.Basic,
    username: config["Callbacks:Username"],
    password: config["Callbacks:Password"]);

Console.WriteLine($"Callback registered. ID: {result.CallBackID}, Queue ID: {result.CallBackQueueID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CallBackAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CallBackAddAsync({
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

result = client.service.CallBackAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create Callback](../../rest-api/callbacks/create-callback.md) — `POST /v2/callbacks/create`.
