---
title: SessionLog
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP Auth SessionLog page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# SessionLog

Returns a list of recent session records for a specified user, useful for auditing login activity.

:::caution Established API
The SOAP API is in maintenance mode. There is no direct REST equivalent for this method.
:::

## Method Signature

```
ArrayOfSessionIDInfo SessionLog(string SessionID, int UserID, short MaxRecords)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from [Login](./login.md) |
| `UserID` | int | Yes | Numeric ID of the user whose session history to retrieve. Pass `0` to retrieve sessions for the currently authenticated user |
| `MaxRecords` | short | Yes | Maximum number of session records to return. Typical values: `10`–`100` |

## Response Object — ArrayOfSessionIDInfo

Returns an array of `SessionIDInfo` objects, each representing one session record.

| Field | Type | Description |
|---|---|---|
| `SessionID` | string | Session token for this historical session |
| `UserID` | int | Numeric ID of the user who owned the session |
| `NetworkID` | int | Network ID associated with the session |
| `MailboxID` | int | Default mailbox ID for the session |
| `Created` | dateTime | UTC timestamp when the session was created |
| `Expires` | dateTime | UTC timestamp when the session expired or was invalidated |

```xml
<!-- Example response -->
<SessionLogResponse xmlns="http://www.ecgridos.net/">
  <SessionLogResult>
    <SessionIDInfo>
      <SessionID>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</SessionID>
      <UserID>12345</UserID>
      <NetworkID>100</NetworkID>
      <MailboxID>200</MailboxID>
      <Created>2026-05-07T08:00:00Z</Created>
      <Expires>2026-05-07T09:00:00Z</Expires>
    </SessionIDInfo>
    <SessionIDInfo>
      <SessionID>B2C3D4E5-F6A7-8901-BCDE-F12345678901</SessionID>
      <UserID>12345</UserID>
      <NetworkID>100</NetworkID>
      <MailboxID>200</MailboxID>
      <Created>2026-05-06T14:30:00Z</Created>
      <Expires>2026-05-06T15:30:00Z</Expires>
    </SessionIDInfo>
  </SessionLogResult>
</SessionLogResponse>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSClient(binding, endpoint);

// Retrieve the last 20 sessions for the current user
SessionIDInfo[] sessions = await client.SessionLogAsync(
    sessionID,
    userID:     0,       // 0 = current authenticated user
    maxRecords: 20);

foreach (var s in sessions)
{
    Console.WriteLine($"{s.Created:O}  →  {s.Expires:O}  [{s.SessionID}]");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.SessionLog(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.SessionLogAsync({
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

result = client.service.SessionLog(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

There is no direct REST equivalent for `SessionLog`. For user activity auditing on the REST API, use the [Reports](../../rest-api/reports/report-list.md) endpoints.
