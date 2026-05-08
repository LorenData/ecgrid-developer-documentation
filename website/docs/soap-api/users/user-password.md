---
title: UserPassword
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserPassword documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserPassword

Resets a user's password to the specified value. This is an administrative operation — the caller must hold sufficient authorization to modify the target user's account.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/update-password.md).
:::

## Method Signature

```
bool UserPassword(string SessionID, int UserID, string NewPassword)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user whose password is being reset |
| `NewPassword` | string | Yes | New password — must satisfy complexity requirements |

:::note Password Requirements
Passwords must match: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

At least one lowercase letter, one uppercase letter, one digit, and one special character are required.
:::

## Response

Returns `true` if the password was successfully updated; throws a SOAP fault on failure (e.g., insufficient auth level or password complexity violation).

```xml
<!-- Example response XML -->
<UserPasswordResult>true</UserPasswordResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder().AddEnvironmentVariables().Build();
var newPassword = config["RESET_PASSWORD"]
    ?? throw new InvalidOperationException("RESET_PASSWORD is not set.");

var client = new ECGridOSPortTypeClient();

// Reset password for user 5001 — requires admin-level session
bool success = await client.UserPasswordAsync(
    sessionID,
    UserID: 5001,
    NewPassword: newPassword);

if (success)
{
    Console.WriteLine("Password reset successfully.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserPassword(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserPasswordAsync({
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

result = client.service.UserPassword(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Password](../../rest-api/users/update-password.md) — `POST /v2/users/password`.
