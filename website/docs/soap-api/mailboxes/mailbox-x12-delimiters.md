---
title: MailboxX12Delimiters
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxX12Delimiters reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxX12Delimiters

Sets the X12 EDI delimiters (element, sub-element, and segment) used for outbound EDI from a mailbox.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/x12-delimiters.md).
:::

## Method Signature

```
MailboxIDInfo MailboxX12Delimiters(string SessionID, int MailboxID, string ElementDelimiter, string SubElementDelimiter, string SegmentTerminator)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with MailboxAdmin or higher authority |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to configure |
| `ElementDelimiter` | string | Yes | Single character used to separate data elements (typically `*`) |
| `SubElementDelimiter` | string | Yes | Single character used to separate sub-elements (typically `:` or `>`) |
| `SegmentTerminator` | string | Yes | Single character used to end segments (typically `~`) |

## Response Object — MailboxIDInfo

Returns the updated `MailboxIDInfo` record with the new delimiter configuration applied.

| Field | Type | Description |
|---|---|---|
| `MailboxID` | int | Numeric identifier of the mailbox |
| `NetworkID` | int | Numeric identifier of the parent network |
| `UniqueID` | string | Unique string identifier of the mailbox |
| `CompanyName` | string | Display name of the mailbox |
| `Status` | Status | Current status of the mailbox |
| `Created` | dateTime | Original creation timestamp |
| `Modified` | dateTime | UTC timestamp of the delimiter configuration change |

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

:::note X12 Standard Defaults
Standard X12 delimiters are: Element=`*`, SubElement=`>`, Segment=`~`. These defaults work with most trading partners. Only change delimiters when a specific trading partner requires non-standard characters.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Apply standard X12 delimiters to mailbox 100
var updated = await client.MailboxX12DelimitersAsync(
    sessionID,
    mailboxId:           100,
    elementDelimiter:    "*",
    subElementDelimiter: ">",
    segmentTerminator:   "~");

Console.WriteLine($"X12 delimiters set for: {updated.CompanyName}");

// Non-standard example for a partner that requires pipe-delimited elements
// var updated = await client.MailboxX12DelimitersAsync(sessionID, 100, "|", ":", "~");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxX12Delimiters(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxX12DelimitersAsync({
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

result = client.service.MailboxX12Delimiters(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [X12 Delimiters](../../rest-api/mailboxes/x12-delimiters.md) — `POST /v2/mailboxes/x12-delimiters`.
