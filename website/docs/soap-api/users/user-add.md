---
title: UserAdd
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserAdd documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserAdd

Creates a new user account under the specified network and mailbox with the given credentials and authorization level.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/create-user.md).
:::

## Method Signature

```
UserIDInfo UserAdd(string SessionID, int NetworkID, int MailboxID, string Login, string Password, string FirstName, string LastName, string Email, AuthLevel AuthLevel)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Network to create the user under |
| `MailboxID` | int | Yes | Mailbox to associate the user with; use `0` for a network-level user |
| `Login` | string | Yes | Unique login name for the new user |
| `Password` | string | Yes | Initial password — must satisfy complexity requirements |
| `FirstName` | string | Yes | User's first name |
| `LastName` | string | Yes | User's last name |
| `Email` | string | Yes | User's email address |
| `AuthLevel` | AuthLevel | Yes | Authorization level to assign to the new user |

:::note Password Requirements
Passwords must match: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$`

At least one lowercase letter, one uppercase letter, one digit, and one special character are required.
:::

## Response Object — UserIDInfo

Returns the newly created `UserIDInfo` object.

| Field | Type | Description |
|---|---|---|
| `UserID` | int | Unique identifier assigned to the new user |
| `Login` | string | Login name |
| `Email` | string | Email address |
| `FirstName` | string | First name |
| `LastName` | string | Last name |
| `NetworkID` | int | Network the user belongs to |
| `MailboxID` | int | Mailbox the user belongs to |
| `AuthLevel` | AuthLevel | Authorization level |
| `Status` | Status | Initial status (typically `Active`) |
| `Created` | dateTime | Account creation timestamp |

```xml
<!-- Example response XML -->
<UserIDInfo>
  <UserID>5050</UserID>
  <Login>newuser</Login>
  <Email>newuser@example.com</Email>
  <FirstName>Jane</FirstName>
  <LastName>Doe</LastName>
  <NetworkID>10</NetworkID>
  <MailboxID>100</MailboxID>
  <AuthLevel>MailboxUser</AuthLevel>
  <Status>Active</Status>
  <Created>2026-05-07T10:00:00</Created>
</UserIDInfo>
```

## ENUMs

### AuthLevel

| Value | Description |
|---|---|
| `NoChange` | No change (not valid for UserAdd) |
| `Root` | Full system access |
| `TechOps` | Technical operations access |
| `NetOps` | Network operations access |
| `NetworkAdmin` | Network administrator |
| `NetworkUser` | Network-level user |
| `MailboxAdmin` | Mailbox administrator |
| `MailboxUser` | Mailbox-level user |
| `TPUser` | Trading partner user |
| `General` | General / limited access |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder().AddEnvironmentVariables().Build();
var initialPassword = config["NEW_USER_PASSWORD"]
    ?? throw new InvalidOperationException("NEW_USER_PASSWORD is not set.");

var client = new ECGridOSPortTypeClient();

// Create a new mailbox-level user
UserIDInfo newUser = await client.UserAddAsync(
    sessionID,
    NetworkID: 10,
    MailboxID: 100,
    Login: "newuser",
    Password: initialPassword,
    FirstName: "Jane",
    LastName: "Doe",
    Email: "newuser@example.com",
    AuthLevel: AuthLevel.MailboxUser);

Console.WriteLine($"Created UserID: {newUser.UserID}");
Console.WriteLine($"Login:          {newUser.Login}");
Console.WriteLine($"AuthLevel:      {newUser.AuthLevel}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserAddAsync({
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

result = client.service.UserAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create User](../../rest-api/users/create-user.md) — `POST /v2/users`.
