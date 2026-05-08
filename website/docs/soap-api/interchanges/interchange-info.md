---
title: InterchangeInfo
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP InterchangeInfo method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterchangeInfo

Retrieve full metadata for a single interchange by its unique ID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/interchanges/get-interchange.md).
:::

## Method Signature

```
InterchangeIDInfo InterchangeInfo(string SessionID, long InterchangeID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `InterchangeID` | long | Yes | Unique identifier of the interchange |

## Response Object — InterchangeIDInfo

| Field | Type | Description |
|---|---|---|
| `InterchangeID` | long | Unique interchange identifier |
| `ParcelID` | long | Parent parcel that contained this interchange |
| `Sender` | string | ISA06 sender qualifier + ID |
| `Receiver` | string | ISA08 receiver qualifier + ID |
| `Standard` | EDIStandard | EDI standard used |
| `DocumentType` | string | Functional identifier or transaction set type |
| `Status` | string | Current interchange status |
| `Created` | datetime | Timestamp when the interchange was processed (UTC) |

```xml
<!-- Example response XML -->
<InterchangeIDInfo>
  <InterchangeID>5551234</InterchangeID>
  <ParcelID>9876543</ParcelID>
  <Sender>SUPPLIERID</Sender>
  <Receiver>BUYERID</Receiver>
  <Standard>X12</Standard>
  <DocumentType>810</DocumentType>
  <Status>Delivered</Status>
  <Created>2026-05-07T08:05:00Z</Created>
</InterchangeIDInfo>
```

## ENUMs

### EDIStandard

| Value | Description |
|---|---|
| `X12` | ANSI X12 |
| `EDIFACT` | UN/EDIFACT |
| `TRADACOMS` | TRADACOMS |
| `VDA` | VDA |
| `XML` | XML payload |
| `TXT` | Plain text |
| `PDF` | PDF document |
| `Binary` | Binary/proprietary format |

See [Appendix — ENUMs](../../appendix/enums.md) for the full `EDIStandard` list.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve interchange details for audit or troubleshooting
using var client = new ECGridOSPortTypeClient();

var info = await client.InterchangeInfoAsync(sessionID, interchangeId: 5551234L);

Console.WriteLine($"InterchangeID: {info.InterchangeID}");
Console.WriteLine($"Standard:      {info.Standard}");
Console.WriteLine($"DocumentType:  {info.DocumentType}");
Console.WriteLine($"Sender:        {info.Sender}");
Console.WriteLine($"Receiver:      {info.Receiver}");
Console.WriteLine($"Status:        {info.Status}");
Console.WriteLine($"Created:       {info.Created:u}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterchangeInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterchangeInfoAsync({
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

result = client.service.InterchangeInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Interchange](../../rest-api/interchanges/get-interchange.md).
