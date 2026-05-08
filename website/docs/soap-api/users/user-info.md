---
title: UserInfo
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserInfo documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserInfo

Retrieves detailed information about a single user account by its unique UserID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/get-user.md).
:::

## Method Signature

```
UserIDInfo UserInfo(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user to retrieve |

## Response Object — UserIDInfo

| Field | Type | Description |
|---|---|---|
| `UserID` | int | Unique identifier of the user |
| `Login` | string | Username / login name |
| `Email` | string | Email address for the user |
| `FirstName` | string | User's first name |
| `LastName` | string | User's last name |
| `NetworkID` | int | Network the user belongs to |
| `MailboxID` | int | Mailbox the user belongs to (0 = network-level user) |
| `AuthLevel` | AuthLevel | Authorization level of the user |
| `Status` | Status | Current account status |
| `Created` | dateTime | Date and time the account was created |

```xml
<!-- Example response XML -->
<UserIDInfo>
  <UserID>5001</UserID>
  <Login>jsmith</Login>
  <Email>jsmith@example.com</Email>
  <FirstName>John</FirstName>
  <LastName>Smith</LastName>
  <NetworkID>10</NetworkID>
  <MailboxID>100</MailboxID>
  <AuthLevel>MailboxAdmin</AuthLevel>
  <Status>Active</Status>
  <Created>2024-01-15T09:30:00</Created>
</UserIDInfo>
```

## ENUMs

### AuthLevel

| Value | Description |
|---|---|
| `NoChange` | No change to current level |
| `Root` | Full system access |
| `TechOps` | Technical operations access |
| `NetOps` | Network operations access |
| `NetworkAdmin` | Network administrator |
| `NetworkUser` | Network-level user |
| `MailboxAdmin` | Mailbox administrator |
| `MailboxUser` | Mailbox-level user |
| `TPUser` | Trading partner user |
| `General` | General / limited access |

### Status

| Value | Description |
|---|---|
| `Development` | In development |
| `Active` | Active and operational |
| `Preproduction` | Staging / pre-production |
| `Suspended` | Temporarily suspended |
| `Terminated` | Permanently terminated |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Retrieve user account details by UserID
UserIDInfo user = await client.UserInfoAsync(sessionID, UserID: 5001);

Console.WriteLine($"UserID:    {user.UserID}");
Console.WriteLine($"Login:     {user.Login}");
Console.WriteLine($"Name:      {user.FirstName} {user.LastName}");
Console.WriteLine($"Email:     {user.Email}");
Console.WriteLine($"AuthLevel: {user.AuthLevel}");
Console.WriteLine($"Status:    {user.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserInfoAsync({
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

result = client.service.UserInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get User](../../rest-api/users/get-user.md) — `GET /v2/users/{id}`.
