---
title: UserSuspend
sidebar_position: 9
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserSuspend documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserSuspend

Suspends a user account, preventing login while preserving the account for future reactivation.

:::caution Established API
The SOAP API is in maintenance mode. There is no direct REST equivalent — use [Update User](../../rest-api/users/update-user.md) (`PUT /v2/users`) to update the user's status field.
:::

## Method Signature

```
bool UserSuspend(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user account to suspend |

## Response

Returns `true` if the account was successfully suspended; throws a SOAP fault on failure.

```xml
<!-- Example response XML -->
<UserSuspendResult>true</UserSuspendResult>
```

:::tip Reversible Action
Suspension is reversible. The account retains all configuration and history. To permanently remove access, use [UserTerminate](./user-terminate.md) instead.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Suspend user 5001 — account is disabled but not deleted
bool success = await client.UserSuspendAsync(sessionID, UserID: 5001);

if (success)
{
    Console.WriteLine("User 5001 has been suspended.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserSuspend(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserSuspendAsync({
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

result = client.service.UserSuspend(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

There is no direct REST equivalent for this operation. To achieve the same result via REST, call [Update User](../../rest-api/users/update-user.md) (`PUT /v2/users`) and set the user's status to `Suspended`.
