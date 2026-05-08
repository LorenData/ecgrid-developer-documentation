---
title: MailboxAdd
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxAdd reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxAdd

Creates a new mailbox within the specified network and returns the newly created mailbox record.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/create-mailbox.md).
:::

## Method Signature

```
MailboxIDInfo MailboxAdd(string SessionID, int NetworkID, string UniqueID, string CompanyName, string Address1, string Address2, string City, string State, string Zip, string Phone, string AdminEmail)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetworkAdmin or higher authority |
| `NetworkID` | int | Yes | Numeric identifier of the parent network |
| `UniqueID` | string | Yes | Unique string identifier (slug) for the new mailbox; must be unique within the network |
| `CompanyName` | string | Yes | Display name of the mailbox company |
| `Address1` | string | Yes | Primary street address |
| `Address2` | string | No | Secondary address line (suite, floor, etc.) |
| `City` | string | Yes | City |
| `State` | string | Yes | State or province code |
| `Zip` | string | Yes | Postal code |
| `Phone` | string | Yes | Primary contact phone number |
| `AdminEmail` | string | Yes | Email address for the mailbox administrator |

## Response Object — MailboxIDInfo

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | System-assigned numeric identifier for the new mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier as provided |
| `CompanyName` | string | Display name as provided |
| `Status` | Status | Initial status of the mailbox (typically `Active`) |
| `Created` | dateTime | UTC timestamp of mailbox creation |
| `Modified` | dateTime | UTC timestamp of the record (same as Created on initial add) |

```xml
<!-- Example response XML -->
<MailboxIDInfo>
  <MailboxID>200</MailboxID>
  <NetworkID>1</NetworkID>
  <UniqueID>NEWMAILBOX</UniqueID>
  <CompanyName>New Mailbox Corp</CompanyName>
  <Status>Active</Status>
  <Created>2026-05-07T14:00:00</Created>
  <Modified>2026-05-07T14:00:00</Modified>
</MailboxIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Create a new mailbox under network 1 — requires NetworkAdmin authority
var newMailbox = await client.MailboxAddAsync(
    sessionID,
    networkId:   1,
    uniqueID:    "NEWMAILBOX",
    companyName: "New Mailbox Corp",
    address1:    "789 Commerce Dr",
    address2:    "Suite 400",
    city:        "Chicago",
    state:       "IL",
    zip:         "60601",
    phone:       "312-555-9000",
    adminEmail:  "admin@newmailbox.com");

Console.WriteLine($"Created MailboxID: {newMailbox.MailboxID}");
Console.WriteLine($"Status: {newMailbox.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxAddAsync({
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

result = client.service.MailboxAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [MailboxInfo](./mailbox-info.md) — retrieve the mailbox after creation
- [Create a Mailbox](../../common-operations/create-a-mailbox.md) — step-by-step guide covering both REST and SOAP

## REST Equivalent

See [Create Mailbox](../../rest-api/mailboxes/create-mailbox.md) — `POST /v2/mailboxes/create`.
