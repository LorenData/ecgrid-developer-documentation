---
title: ParcelInfo
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelInfo method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelInfo

Retrieve full metadata for a single parcel by its unique ID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/parcels/get-parcel.md).
:::

## Method Signature

```
ParcelIDInfo ParcelInfo(string SessionID, long ParcelID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ParcelID` | long | Yes | Unique identifier of the parcel |

## Response Object — ParcelIDInfo

| Field | Type | Description |
|---|---|---|
| `ParcelID` | long | Unique parcel identifier |
| `NetworkID` | int | Network that owns the parcel |
| `MailboxID` | int | Mailbox associated with the parcel |
| `FileName` | string | Original file name |
| `Bytes` | int | File size in bytes |
| `Status` | ParcelStatus | Current lifecycle status of the parcel |
| `ECGridIDFrom` | int | Sender ECGrid ID |
| `ECGridIDTo` | int | Recipient ECGrid ID |
| `Created` | datetime | Timestamp when the parcel entered ECGrid (UTC) |

```xml
<!-- Example response XML -->
<ParcelIDInfo>
  <ParcelID>9876543</ParcelID>
  <NetworkID>1</NetworkID>
  <MailboxID>101</MailboxID>
  <FileName>invoice_20260507.edi</FileName>
  <Bytes>4096</Bytes>
  <Status>InBoxReady</Status>
  <ECGridIDFrom>123456</ECGridIDFrom>
  <ECGridIDTo>654321</ECGridIDTo>
  <Created>2026-05-07T08:00:00Z</Created>
</ParcelIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Look up parcel details before deciding whether to download
using var client = new ECGridOSPortTypeClient();

var info = await client.ParcelInfoAsync(sessionID, parcelId: 9876543L);

Console.WriteLine($"File:    {info.FileName}");
Console.WriteLine($"Bytes:   {info.Bytes}");
Console.WriteLine($"Status:  {info.Status}");
Console.WriteLine($"Created: {info.Created:u}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelInfoAsync({
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

result = client.service.ParcelInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Parcel](../../rest-api/parcels/get-parcel.md).
