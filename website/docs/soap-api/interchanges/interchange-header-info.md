---
title: InterchangeHeaderInfo
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP InterchangeHeaderInfo method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterchangeHeaderInfo

Parse a raw ISA header string into a structured `InterchangeIDInfo` object, and optionally extract only the interchange date.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/interchanges/get-header.md).
:::

## Method Signature

```
InterchangeIDInfo InterchangeHeaderInfo(string SessionID, string InterchangeHeader)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `InterchangeHeader` | string | Yes | Raw ISA segment string (106 characters for X12) |

## Response Object — InterchangeIDInfo

| Field | Type | Description |
|---|---|---|
| `InterchangeID` | long | Assigned interchange ID (if already tracked by ECGrid; otherwise 0) |
| `ParcelID` | long | Parent parcel ID (if applicable; otherwise 0) |
| `Sender` | string | ISA06 sender qualifier + ID |
| `Receiver` | string | ISA08 receiver qualifier + ID |
| `Standard` | EDIStandard | EDI standard detected from the header |
| `DocumentType` | string | Functional identifier or transaction set type |
| `Status` | string | Status value if interchange is tracked; otherwise empty |
| `Created` | datetime | ISA09/ISA10 interchange date and time parsed to UTC |

```xml
<!-- Example response XML -->
<InterchangeIDInfo>
  <InterchangeID>0</InterchangeID>
  <ParcelID>0</ParcelID>
  <Sender>ZZ SUPPLIERID</Sender>
  <Receiver>ZZ BUYERID  </Receiver>
  <Standard>X12</Standard>
  <DocumentType></DocumentType>
  <Status></Status>
  <Created>2026-05-07T08:00:00Z</Created>
</InterchangeIDInfo>
```

## Variants

### InterchangeDate

A lightweight utility method that extracts only the interchange datetime from a raw ISA header string. Unlike `InterchangeHeaderInfo`, this method does not require a `SessionID`.

```
datetime InterchangeDate(string InterchangeHeader)
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `InterchangeHeader` | string | Yes | Raw ISA segment string |

Returns a `datetime` value representing the ISA09/ISA10 date and time parsed to UTC.

```xml
<!-- Example response XML -->
<InterchangeDateResult>2026-05-07T08:00:00Z</InterchangeDateResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy

using var client = new ECGridOSPortTypeClient();

// Parse a raw ISA header to extract sender/receiver/date
var rawIsa = "ISA*00*          *00*          *ZZ*SUPPLIERID     *ZZ*BUYERID        *260507*0800*^*00501*000000001*0*P*>";

var info = await client.InterchangeHeaderInfoAsync(sessionID, interchangeHeader: rawIsa);

Console.WriteLine($"Sender:   {info.Sender}");
Console.WriteLine($"Receiver: {info.Receiver}");
Console.WriteLine($"Date:     {info.Created:u}");

// Use InterchangeDate when only the date is needed (no session required)
var ixDate = await client.InterchangeDateAsync(interchangeHeader: rawIsa);
Console.WriteLine($"Interchange date: {ixDate:u}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterchangeHeaderInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterchangeHeaderInfoAsync({
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

result = client.service.InterchangeHeaderInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Interchange Header](../../rest-api/interchanges/get-header.md).
