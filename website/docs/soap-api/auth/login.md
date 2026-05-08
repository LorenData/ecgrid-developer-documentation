---
title: Login
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP Auth Login page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Login

Authenticates a user and returns a `SessionID` string that must be passed as the first parameter to every subsequent SOAP API call.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/auth/login.md).
:::

## Method Signature

```
string Login(string UserName, string Password, string SenderSolution,
             string SenderVersion, string SenderCompanyName,
             string SenderContact, string SenderContactEmail)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `UserName` | string | Yes | ECGridOS account username |
| `Password` | string | Yes | Account password. Must satisfy the complexity rule: at least one uppercase letter, one lowercase letter, one digit, and one special character |
| `SenderSolution` | string | Yes | Name of the calling application or integration |
| `SenderVersion` | string | Yes | Version string of the calling application (e.g., `"1.0"`) |
| `SenderCompanyName` | string | Yes | Company name of the integration developer |
| `SenderContact` | string | Yes | Name of the technical contact responsible for the integration |
| `SenderContactEmail` | string | Yes | Email address of the technical contact |

:::note No SessionID parameter
`Login` is the only method that does **not** take a `SessionID`. It creates the session and returns the `SessionID`.
:::

## Response

Returns a `string` containing the `SessionID` token. Store this value and pass it as the first argument to every subsequent SOAP API call.

Sessions expire after a period of inactivity. For long-running server applications, consider refreshing the session periodically or catching authentication faults and re-authenticating.

```xml
<!-- Example response -->
<LoginResponse xmlns="http://www.ecgridos.net/">
  <LoginResult>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</LoginResult>
</LoginResponse>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSClient(binding, endpoint);

string sessionID = await client.LoginAsync(
    userName:           config["ECGrid:UserName"],
    password:           config["ECGrid:Password"],
    senderSolution:     "MyIntegration",
    senderVersion:      "1.0",
    senderCompanyName:  "My Company LLC",
    senderContact:      "Developer Name",
    senderContactEmail: "dev@example.com");

try
{
    // Use sessionID for subsequent calls...
}
finally
{
    // Always release the session, even on error
    await client.LogoutAsync(sessionID);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.Login(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.LoginAsync({
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

result = client.service.Login(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

:::tip Server applications
For daemon processes and background services, session-based auth requires periodic re-authentication when sessions expire. The REST API's API Key (`X-API-Key` header) is stateless and better suited for server-to-server workloads.
:::

## REST Equivalent

See [Login](../../rest-api/auth/login.md) — `POST /v2/auth/login`.
