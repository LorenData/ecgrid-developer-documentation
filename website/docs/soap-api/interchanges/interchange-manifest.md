---
title: InterchangeManifest
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP InterchangeManifest method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterchangeManifest

Retrieve the manifest of functional groups and transaction sets contained within an interchange.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/interchanges/get-manifest.md).
:::

## Method Signature

```
ArrayOfManifestInfo InterchangeManifest(string SessionID, long InterchangeID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `InterchangeID` | long | Yes | Unique identifier of the interchange to inspect |

## Response Object — ArrayOfManifestInfo

Returns an array of `ManifestInfo` objects, one per functional group or transaction set found in the interchange envelope.

| Field | Type | Description |
|---|---|---|
| `GroupID` | string | GS functional group identifier |
| `TransactionSetID` | string | ST transaction set identifier |
| `TransactionCount` | int | Number of transaction sets in the group |
| `SenderID` | string | GS02 application sender code |
| `ReceiverID` | string | GS03 application receiver code |
| `GroupDate` | datetime | GS04/GS05 group date and time (UTC) |

```xml
<!-- Example response XML -->
<ArrayOfManifestInfo>
  <ManifestInfo>
    <GroupID>IN</GroupID>
    <TransactionSetID>810</TransactionSetID>
    <TransactionCount>3</TransactionCount>
    <SenderID>SUPPLIER_APP</SenderID>
    <ReceiverID>BUYER_APP</ReceiverID>
    <GroupDate>2026-05-07T08:00:00Z</GroupDate>
  </ManifestInfo>
</ArrayOfManifestInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Inspect the functional groups within an interchange before processing
using var client = new ECGridOSPortTypeClient();

var manifest = await client.InterchangeManifestAsync(sessionID, interchangeId: 5551234L);

foreach (var entry in manifest)
{
    Console.WriteLine(
        $"Group={entry.GroupID}  TxSet={entry.TransactionSetID}  Count={entry.TransactionCount}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterchangeManifest(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterchangeManifestAsync({
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

result = client.service.InterchangeManifest(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Interchange Manifest](../../rest-api/interchanges/get-manifest.md).
