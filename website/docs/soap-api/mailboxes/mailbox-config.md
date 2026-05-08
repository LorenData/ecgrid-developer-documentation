---
title: MailboxConfig
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxConfig reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxConfig

Configures operational settings for a mailbox, including inbound/outbound processing options and notification preferences.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/update-config.md).
:::

## Method Signature

```
MailboxIDInfo MailboxConfig(string SessionID, int MailboxID, bool DeleteOnDownload, short InBoxTimeout, bool Managed, string NotifyEmail, bool NotifyOnInBox)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with MailboxAdmin or higher authority |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to configure |
| `DeleteOnDownload` | bool | Yes | Whether to automatically delete parcels after they are downloaded |
| `InBoxTimeout` | short | Yes | Hours to retain undownloaded inbound parcels (0 = network default) |
| `Managed` | bool | Yes | Whether the mailbox operates in managed mode |
| `NotifyEmail` | string | No | Email address for inbound parcel notifications; empty string to disable |
| `NotifyOnInBox` | bool | Yes | Whether to send notification emails when parcels arrive |

## Response Object — MailboxIDInfo

Returns the updated `MailboxIDInfo` record reflecting all configuration changes.

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | Numeric identifier of the configured mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier of the mailbox |
| `CompanyName` | string | Display name of the mailbox |
| `Status` | Status | Current status of the mailbox |
| `Created` | dateTime | Original creation timestamp |
| `Modified` | dateTime | UTC timestamp of the configuration update |

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

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Configure mailbox: retain parcels 48 hours, notify on receipt, do not auto-delete
var updated = await client.MailboxConfigAsync(
    sessionID,
    mailboxId:        100,
    deleteOnDownload: false,
    inBoxTimeout:     48,
    managed:          false,
    notifyEmail:      "ops@mycompany.com",
    notifyOnInBox:    true);

Console.WriteLine($"Config applied to: {updated.CompanyName} (Modified: {updated.Modified:yyyy-MM-dd HH:mm})");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxConfig(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxConfigAsync({
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

result = client.service.MailboxConfig(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [MailboxDeleteOnDownload](./mailbox-delete-on-download.md) — set auto-delete alone
- [MailboxInBoxTimeout](./mailbox-inbox-timeout.md) — set retention timeout alone
- [MailboxManaged](./mailbox-managed.md) — set managed mode alone

## REST Equivalent

See [Update Mailbox Config](../../rest-api/mailboxes/update-config.md) — `POST /v2/mailboxes/update-config`.
