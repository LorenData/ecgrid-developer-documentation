---
title: MailboxInfo
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxInfo reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxInfo

Retrieves detailed information about a single mailbox by its MailboxID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/get-mailbox.md).
:::

## Method Signature

```
MailboxIDInfo MailboxInfo(string SessionID, int MailboxID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to retrieve |

## Response Object — MailboxIDInfo

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | Unique numeric identifier for the mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier (slug) for the mailbox |
| `CompanyName` | string | Display name of the mailbox company |
| `Status` | Status | Current status of the mailbox (see ENUMs) |
| `Created` | dateTime | UTC timestamp when the mailbox record was created |
| `Modified` | dateTime | UTC timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<MailboxIDInfo>
  <MailboxID>100</MailboxID>
  <NetworkID>1</NetworkID>
  <UniqueID>MYMAILBOX</UniqueID>
  <CompanyName>My Mailbox Company</CompanyName>
  <Status>Active</Status>
  <Created>2021-03-20T00:00:00</Created>
  <Modified>2024-11-15T09:22:00</Modified>
</MailboxIDInfo>
```

## ENUMs

### Status

See [Status enum](../../appendix/enums.md#status) for all possible values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve mailbox details for a known MailboxID
var result = await client.MailboxInfoAsync(sessionID, mailboxId);

Console.WriteLine($"Mailbox: {result.CompanyName} (ID: {result.MailboxID})");
Console.WriteLine($"Network: {result.NetworkID} | Status: {result.Status}");
Console.WriteLine($"Created: {result.Created:yyyy-MM-dd}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxInfoAsync({
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

result = client.service.MailboxInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Mailbox](../../rest-api/mailboxes/get-mailbox.md) — `GET /v2/mailboxes/{id}`.
