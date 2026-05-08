---
title: UserTerminate
sidebar_position: 10
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserTerminate documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserTerminate

Permanently terminates a user account, revoking all access and invalidating all sessions. This action is irreversible.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/terminate-user.md).
:::

:::danger Irreversible Action
`UserTerminate` permanently terminates the user account. The user's login, sessions, and API keys are immediately invalidated and cannot be restored. Use [UserSuspend](./user-suspend.md) if you need a reversible option.
:::

## Method Signature

```
bool UserTerminate(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user account to permanently terminate |

## Response

Returns `true` if the account was successfully terminated; throws a SOAP fault on failure.

```xml
<!-- Example response XML -->
<UserTerminateResult>true</UserTerminateResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Permanently terminate user 5001 — this action cannot be undone
bool success = await client.UserTerminateAsync(sessionID, UserID: 5001);

if (success)
{
    Console.WriteLine("User 5001 has been permanently terminated.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserTerminate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserTerminateAsync({
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

result = client.service.UserTerminate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Terminate User](../../rest-api/users/terminate-user.md) — `DELETE /v2/users/{id}`.
