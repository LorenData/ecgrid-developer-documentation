---
title: SessionInfo
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP Auth SessionInfo page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# SessionInfo

Returns details about the current session, including when it was created and when it expires.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/auth/session.md).
:::

## Method Signature

```
SessionIDInfo SessionInfo(string SessionID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from [Login](./login.md) |

## Response Object — SessionIDInfo

| Field | Type | Description |
|---|---|---|
| `SessionID` | string | The session token (mirrors the input) |
| `UserID` | int | Numeric ID of the user who owns the session |
| `NetworkID` | int | Network ID associated with the session |
| `MailboxID` | int | Default mailbox ID for the session |
| `Created` | dateTime | UTC timestamp when the session was created |
| `Expires` | dateTime | UTC timestamp when the session will expire |

```xml
<!-- Example response -->
<SessionInfoResponse xmlns="http://www.ecgridos.net/">
  <SessionInfoResult>
    <SessionID>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</SessionID>
    <UserID>12345</UserID>
    <NetworkID>100</NetworkID>
    <MailboxID>200</MailboxID>
    <Created>2026-05-07T10:00:00Z</Created>
    <Expires>2026-05-07T11:00:00Z</Expires>
  </SessionInfoResult>
</SessionInfoResponse>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSClient(binding, endpoint);

SessionIDInfo session = await client.SessionInfoAsync(sessionID);

Console.WriteLine($"Session created: {session.Created:O}");
Console.WriteLine($"Session expires: {session.Expires:O}");

// Check if the session is close to expiring and re-authenticate if needed
if (session.Expires - DateTimeOffset.UtcNow < TimeSpan.FromMinutes(5))
{
    // Re-authenticate before the session lapses
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.SessionInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.SessionInfoAsync({
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

result = client.service.SessionInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Session](../../rest-api/auth/session.md) — `POST /v2/auth/session`.
