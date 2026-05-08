---
title: UserSetAuthLevel
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserSetAuthLevel documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserSetAuthLevel

Changes the authorization level of a user account, optionally scoping the permission to a specific network and mailbox.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/set-role.md).
:::

:::warning Elevated Access Risk
`Root` and `TechOps` authorization levels grant broad system-wide access. Assign these levels only to trusted administrators and review assignments regularly.
:::

## Method Signature

```
UserIDInfo UserSetAuthLevel(string SessionID, int UserID, int NetworkID, int MailboxID, AuthLevel AuthLevel)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user whose auth level is being changed |
| `NetworkID` | int | Yes | Network scope for the auth level; use `0` to apply at the system level |
| `MailboxID` | int | Yes | Mailbox scope for the auth level; use `0` to apply at the network level |
| `AuthLevel` | AuthLevel | Yes | New authorization level to assign |

## Response Object — UserIDInfo

Returns the updated `UserIDInfo` object reflecting the new authorization level.

| Field | Type | Description |
|---|---|---|
| `UserID` | int | Unique identifier of the user |
| `Login` | string | Login name |
| `Email` | string | Email address |
| `FirstName` | string | First name |
| `LastName` | string | Last name |
| `NetworkID` | int | Network scope |
| `MailboxID` | int | Mailbox scope |
| `AuthLevel` | AuthLevel | Updated authorization level |
| `Status` | Status | Account status (unchanged) |
| `Created` | dateTime | Account creation timestamp |

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
| `Root` | Full system access — assign sparingly |
| `TechOps` | Technical operations access — assign sparingly |
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

var client = new ECGridOSPortTypeClient();

// Promote user 5001 to MailboxAdmin scoped to network 10, mailbox 100
UserIDInfo updated = await client.UserSetAuthLevelAsync(
    sessionID,
    UserID: 5001,
    NetworkID: 10,
    MailboxID: 100,
    AuthLevel: AuthLevel.MailboxAdmin);

Console.WriteLine($"UserID:    {updated.UserID}");
Console.WriteLine($"AuthLevel: {updated.AuthLevel}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserSetAuthLevel(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserSetAuthLevelAsync({
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

result = client.service.UserSetAuthLevel(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Set Role](../../rest-api/users/set-role.md) — `POST /v2/users/role`.
