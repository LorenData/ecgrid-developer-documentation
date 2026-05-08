---
title: MailboxInBoxTimeout
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxInBoxTimeout reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxInBoxTimeout

Sets the number of hours that undownloaded inbound parcels are retained in a mailbox inbox before expiring.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/update-config.md).
:::

## Method Signature

```
MailboxIDInfo MailboxInBoxTimeout(string SessionID, int MailboxID, short InBoxTimeout)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with MailboxAdmin or higher authority |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to configure |
| `InBoxTimeout` | short | Yes | Retention period in hours (0 = use network default; max typically 240) |

## Response Object — MailboxIDInfo

Returns the updated `MailboxIDInfo` record with the new timeout setting applied.

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | Numeric identifier of the mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier of the mailbox |
| `CompanyName` | string | Display name of the mailbox |
| `Status` | Status | Current status of the mailbox |
| `Created` | dateTime | Original creation timestamp |
| `Modified` | dateTime | UTC timestamp of the configuration change |

```xml
<!-- Example response XML -->
<MailboxIDInfo>
  <MailboxID>100</MailboxID>
  <NetworkID>1</NetworkID>
  <UniqueID>MYMAILBOX</UniqueID>
  <CompanyName>My Mailbox Company</CompanyName>
  <Status>Active</Status>
  <Created>2021-03-20T00:00:00</Created>
  <Modified>2026-05-07T14:00:00</Modified>
</MailboxIDInfo>
```

:::note Timeout Behavior
When `InBoxTimeout` is 0, the network-level default applies. Parcels that exceed the timeout are moved to an expired state and may no longer be downloadable. Contact ECGrid support to recover expired parcels.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Set inbox retention to 72 hours (3 days) for mailbox 100
var updated = await client.MailboxInBoxTimeoutAsync(
    sessionID,
    mailboxId:    100,
    inBoxTimeout: 72);

Console.WriteLine($"Timeout updated for: {updated.CompanyName}");
Console.WriteLine($"Modified: {updated.Modified:yyyy-MM-dd HH:mm}");

// Restore network default — pass 0
// var reset = await client.MailboxInBoxTimeoutAsync(sessionID, 100, 0);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxInBoxTimeout(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxInBoxTimeoutAsync({
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

result = client.service.MailboxInBoxTimeout(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [MailboxConfig](./mailbox-config.md) — set timeout along with other mailbox settings
- [MailboxDeleteOnDownload](./mailbox-delete-on-download.md) — control auto-delete behavior

## REST Equivalent

See [Update Mailbox Config](../../rest-api/mailboxes/update-config.md) — `POST /v2/mailboxes/update-config`.
