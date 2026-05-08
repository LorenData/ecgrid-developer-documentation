---
title: UserUpdate
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserUpdate documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserUpdate

Updates the contact details (name and email) of an existing user account.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/update-user.md).
:::

## Method Signature

```
UserIDInfo UserUpdate(string SessionID, int UserID, string FirstName, string LastName, string Email)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user to update |
| `FirstName` | string | Yes | Updated first name |
| `LastName` | string | Yes | Updated last name |
| `Email` | string | Yes | Updated email address |

## Response Object — UserIDInfo

Returns the updated `UserIDInfo` object reflecting the changes.

| Field | Type | Description |
|---|---|---|
| `UserID` | int | Unique identifier of the user |
| `Login` | string | Login name (unchanged) |
| `Email` | string | Updated email address |
| `FirstName` | string | Updated first name |
| `LastName` | string | Updated last name |
| `NetworkID` | int | Network the user belongs to |
| `MailboxID` | int | Mailbox the user belongs to |
| `AuthLevel` | AuthLevel | Authorization level (unchanged) |
| `Status` | Status | Account status (unchanged) |
| `Created` | dateTime | Account creation timestamp (unchanged) |

```xml
<!-- Example response XML -->
<UserIDInfo>
  <UserID>5001</UserID>
  <Login>jsmith</Login>
  <Email>john.smith@newdomain.com</Email>
  <FirstName>John</FirstName>
  <LastName>Smith</LastName>
  <NetworkID>10</NetworkID>
  <MailboxID>100</MailboxID>
  <AuthLevel>MailboxAdmin</AuthLevel>
  <Status>Active</Status>
  <Created>2024-01-15T09:30:00</Created>
</UserIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Update user 5001's name and email address
UserIDInfo updated = await client.UserUpdateAsync(
    sessionID,
    UserID: 5001,
    FirstName: "John",
    LastName: "Smith",
    Email: "john.smith@newdomain.com");

Console.WriteLine($"UserID: {updated.UserID}");
Console.WriteLine($"Email:  {updated.Email}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserUpdate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserUpdateAsync({
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

result = client.service.UserUpdate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update User](../../rest-api/users/update-user.md) — `PUT /v2/users`.
