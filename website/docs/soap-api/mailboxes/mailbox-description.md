---
title: MailboxDescription
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxDescription reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxDescription

Updates the display name (company name) or description for a mailbox.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/update-mailbox.md).
:::

## Method Signature

```
MailboxIDInfo MailboxDescription(string SessionID, int MailboxID, string Description)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with MailboxAdmin or higher authority |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to update |
| `Description` | string | Yes | New display name or description for the mailbox |

## Response Object — MailboxIDInfo

Returns the updated `MailboxIDInfo` record with the new description applied.

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | Numeric identifier of the mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier of the mailbox (unchanged) |
| `CompanyName` | string | Updated display name |
| `Status` | Status | Current status of the mailbox |
| `Created` | dateTime | Original creation timestamp |
| `Modified` | dateTime | UTC timestamp of the update |

```xml
<!-- Example response XML -->
<MailboxIDInfo>
  <MailboxID>100</MailboxID>
  <NetworkID>1</NetworkID>
  <UniqueID>MYMAILBOX</UniqueID>
  <CompanyName>Updated Mailbox Display Name</CompanyName>
  <Status>Active</Status>
  <Created>2021-03-20T00:00:00</Created>
  <Modified>2026-05-07T14:00:00</Modified>
</MailboxIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Rename a mailbox's display name without changing its UniqueID
var updated = await client.MailboxDescriptionAsync(
    sessionID,
    mailboxId:   100,
    description: "Updated Mailbox Display Name");

Console.WriteLine($"New name: {updated.CompanyName}");
Console.WriteLine($"Modified: {updated.Modified:yyyy-MM-dd HH:mm}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxDescription(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxDescriptionAsync({
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

result = client.service.MailboxDescription(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Mailbox](../../rest-api/mailboxes/update-mailbox.md) — `PUT /v2/mailboxes`.
