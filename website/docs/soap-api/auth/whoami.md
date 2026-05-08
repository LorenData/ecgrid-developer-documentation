---
title: WhoAmI
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP Auth WhoAmI page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# WhoAmI

Returns identity and authorization details for the user associated with the current session.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/get-me.md).
:::

## Method Signature

```
UserIDInfo WhoAmI(string SessionID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from [Login](./login.md) |

## Response Object — UserIDInfo

| Field | Type | Description |
|---|---|---|
| `UserID` | int | Unique numeric identifier for the authenticated user |
| `Login` | string | Username (login name) of the authenticated user |
| `NetworkID` | int | Network ID associated with the user's account |
| `MailboxID` | int | Default mailbox ID for the user |
| `AuthLevel` | AuthLevel | Authorization level granted to this user |

```xml
<!-- Example response -->
<WhoAmIResponse xmlns="http://www.ecgridos.net/">
  <WhoAmIResult>
    <UserID>12345</UserID>
    <Login>jsmith</Login>
    <NetworkID>100</NetworkID>
    <MailboxID>200</MailboxID>
    <AuthLevel>MailboxAdmin</AuthLevel>
  </WhoAmIResult>
</WhoAmIResponse>
```

## ENUMs

### AuthLevel

See [AuthLevel](../../appendix/enums.md#authlevel) in the Appendix for all valid values.

Common values: `NetworkAdmin`, `MailboxAdmin`, `MailboxUser`, `TPUser`.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSClient(binding, endpoint);

UserIDInfo me = await client.WhoAmIAsync(sessionID);

Console.WriteLine($"Logged in as: {me.Login}");
Console.WriteLine($"Network ID:   {me.NetworkID}");
Console.WriteLine($"Mailbox ID:   {me.MailboxID}");
Console.WriteLine($"Auth Level:   {me.AuthLevel}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.WhoAmI(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.WhoAmIAsync({
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

result = client.service.WhoAmI(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Current User](../../rest-api/users/get-me.md) — `GET /v2/users/me`.
