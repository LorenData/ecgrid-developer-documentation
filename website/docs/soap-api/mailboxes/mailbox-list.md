---
title: MailboxList
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxList reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxList

Returns a paginated list of mailboxes within a network, optionally filtered by status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/list-mailboxes.md).
:::

## Method Signature

```
ArrayOfMailboxIDInfo MailboxList(string SessionID, int NetworkID, Status Status, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Scope the list to this network |
| `Status` | Status | Yes | Filter by mailbox status; use `Active` for live mailboxes |
| `PageNo` | short | Yes | 1-based page number for pagination |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfMailboxIDInfo

Returns an array of `MailboxIDInfo` objects.

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | Unique numeric identifier for the mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier (slug) for the mailbox |
| `CompanyName` | string | Display name of the mailbox company |
| `Status` | Status | Current status of the mailbox |
| `Created` | dateTime | UTC timestamp when the mailbox record was created |
| `Modified` | dateTime | UTC timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<ArrayOfMailboxIDInfo>
  <MailboxIDInfo>
    <MailboxID>100</MailboxID>
    <NetworkID>1</NetworkID>
    <UniqueID>MYMAILBOX</UniqueID>
    <CompanyName>My Mailbox Company</CompanyName>
    <Status>Active</Status>
    <Created>2021-03-20T00:00:00</Created>
    <Modified>2024-11-15T09:22:00</Modified>
  </MailboxIDInfo>
  <MailboxIDInfo>
    <MailboxID>101</MailboxID>
    <NetworkID>1</NetworkID>
    <UniqueID>SECONDMAILBOX</UniqueID>
    <CompanyName>Second Mailbox Inc.</CompanyName>
    <Status>Active</Status>
    <Created>2022-07-01T00:00:00</Created>
    <Modified>2025-01-10T11:00:00</Modified>
  </MailboxIDInfo>
</ArrayOfMailboxIDInfo>
```

## ENUMs

### Status

See [Status enum](../../appendix/enums.md#status) for all possible values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Page through all active mailboxes in a network
short pageNo = 1;
const short pageSize = 100;

MailboxIDInfo[] page;
do
{
    page = await client.MailboxListAsync(sessionID, networkId, Status.Active, pageNo, pageSize);
    foreach (var mailbox in page)
    {
        Console.WriteLine($"{mailbox.MailboxID}: {mailbox.CompanyName} ({mailbox.Status})");
    }
    pageNo++;
} while (page.Length == pageSize);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxListAsync({
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

result = client.service.MailboxList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Mailboxes](../../rest-api/mailboxes/list-mailboxes.md) — `POST /v2/mailboxes/list`.
