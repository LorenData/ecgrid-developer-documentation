---
title: MailboxDeleteOnDownload
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxDeleteOnDownload reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxDeleteOnDownload

Sets whether inbound parcels are automatically deleted from the ECGrid inbox after they are downloaded.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/update-config.md).
:::

## Method Signature

```
MailboxIDInfo MailboxDeleteOnDownload(string SessionID, int MailboxID, bool DeleteOnDownload)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with MailboxAdmin or higher authority |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to configure |
| `DeleteOnDownload` | bool | Yes | `true` to auto-delete parcels after download; `false` to retain them |

## Response Object — MailboxIDInfo

Returns the updated `MailboxIDInfo` record with the new setting applied.

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

:::tip When to use DeleteOnDownload
Set `DeleteOnDownload = true` when your integration always processes parcels immediately and confirmed deletion is part of the workflow. Set it to `false` (the default) when you want to retain downloaded parcels for auditing or re-download scenarios. Regardless of this setting, always call `ParcelDownloadConfirm` to mark a parcel as acknowledged.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Enable auto-delete on download for mailbox 100
var updated = await client.MailboxDeleteOnDownloadAsync(
    sessionID,
    mailboxId:        100,
    deleteOnDownload: true);

Console.WriteLine($"DeleteOnDownload set for: {updated.CompanyName}");

// To disable: pass false
// var updated = await client.MailboxDeleteOnDownloadAsync(sessionID, 100, false);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxDeleteOnDownload(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxDeleteOnDownloadAsync({
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

result = client.service.MailboxDeleteOnDownload(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [MailboxConfig](./mailbox-config.md) — configure multiple mailbox settings in a single call
- [ParcelDownloadConfirm](../parcels/parcel-download-confirm.md) — confirm parcel receipt regardless of delete setting

## REST Equivalent

See [Update Mailbox Config](../../rest-api/mailboxes/update-config.md) — `POST /v2/mailboxes/update-config`.
