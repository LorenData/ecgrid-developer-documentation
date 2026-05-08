---
title: Logout
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP Auth Logout page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Logout

Invalidates the current session, releasing server-side resources associated with the `SessionID`.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/auth/logout.md).
:::

## Method Signature

```
bool Logout(string SessionID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from [Login](./login.md) |

## Response

Returns `true` if the session was successfully invalidated, `false` if the session was already expired or not found.

```xml
<!-- Example response -->
<LogoutResponse xmlns="http://www.ecgridos.net/">
  <LogoutResult>true</LogoutResult>
</LogoutResponse>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Always call Logout in a finally block to guarantee cleanup
using var client = new ECGridOSClient(binding, endpoint);

string sessionID = await client.LoginAsync(/* credentials */);

try
{
    // Perform API operations...
    var info = await client.WhoAmIAsync(sessionID);
}
finally
{
    // Releases the session on the server regardless of success or failure
    bool loggedOut = await client.LogoutAsync(sessionID);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.Logout(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.LogoutAsync({
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

result = client.service.Logout(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

:::tip Best practice
Always call `Logout` in a `finally` block. Orphaned sessions consume server-side resources and may count against concurrent session limits on your account.
:::

## REST Equivalent

See [Logout](../../rest-api/auth/logout.md) — `POST /v2/auth/logout`.
