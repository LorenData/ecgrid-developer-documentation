---
title: UserList
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserList documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserList

Returns a paginated list of user accounts filtered by network, mailbox, authorization level, and status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/list-users.md).
:::

## Method Signature

```
ArrayOfUserIDInfo UserList(string SessionID, int NetworkID, int MailboxID, AuthLevel AuthLevel, Status Status, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Filter by network; use `0` to search across all networks accessible to the session |
| `MailboxID` | int | Yes | Filter by mailbox; use `0` to return users across all mailboxes in the network |
| `AuthLevel` | AuthLevel | Yes | Filter by authorization level; use `NoChange` to return all levels |
| `Status` | Status | Yes | Filter by account status |
| `PageNo` | short | Yes | 1-based page number for pagination |
| `RecordsPerPage` | short | Yes | Number of records per page (maximum varies by server config) |

## Response Object — ArrayOfUserIDInfo

Returns an array of `UserIDInfo` objects matching the filter criteria.

| Field | Type | Description |
|---|---|---|
| `UserID` | int | Unique identifier of the user |
| `Login` | string | Username / login name |
| `Email` | string | Email address |
| `FirstName` | string | User's first name |
| `LastName` | string | User's last name |
| `NetworkID` | int | Network the user belongs to |
| `MailboxID` | int | Mailbox the user belongs to |
| `AuthLevel` | AuthLevel | Authorization level |
| `Status` | Status | Current account status |
| `Created` | dateTime | Account creation date and time |

```xml
<!-- Example response XML -->
<ArrayOfUserIDInfo>
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
</ArrayOfUserIDInfo>
```

## ENUMs

### AuthLevel

| Value | Description |
|---|---|
| `NoChange` | No filter — return all levels |
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

// List all active mailbox-level users in mailbox 100, page 1
UserIDInfo[] users = await client.UserListAsync(
    sessionID,
    NetworkID: 10,
    MailboxID: 100,
    AuthLevel: AuthLevel.NoChange,
    Status: Status.Active,
    PageNo: 1,
    RecordsPerPage: 25);

foreach (var u in users)
{
    Console.WriteLine($"UserID: {u.UserID} | {u.FirstName} {u.LastName} | {u.AuthLevel}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserListAsync({
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

result = client.service.UserList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Users](../../rest-api/users/list-users.md) — `POST /v2/users/list`.
