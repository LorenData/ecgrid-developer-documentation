---
title: ParcelDownload
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelDownload method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelDownload

Download the raw EDI content of an inbound parcel by its ID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/parcels/download-parcel.md).
:::

:::tip Confirm After Every Download
Always call [`ParcelDownloadConfirm`](./parcel-download-confirm.md) after successfully saving the file. Without confirmation, ECGrid treats the parcel as undelivered and will re-deliver it on the next poll cycle.
:::

## Method Signature

```
base64Binary ParcelDownload(string SessionID, long ParcelID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ParcelID` | long | Yes | Unique identifier of the parcel to download |

## Response Object — base64Binary

Returns the raw EDI file content encoded as a Base64 binary string. Decode the bytes and write them to disk before calling confirm.

```xml
<!-- Example response XML (content truncated) -->
<ParcelDownloadResult>SVNBKjAwKjAwMDAwMDAwMDAq...</ParcelDownloadResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Download a parcel, save to disk, then confirm receipt
using var client = new ECGridOSPortTypeClient();

// Fetch the file bytes (returned as base64Binary / byte[])
byte[] content = await client.ParcelDownloadAsync(sessionID, parcelId: 9876543L);

// Persist to the local outbound staging directory
var outputPath = Path.Combine("/data/edi/inbound", $"{parcelId}.edi");
await File.WriteAllBytesAsync(outputPath, content);

Console.WriteLine($"Saved {content.Length} bytes to {outputPath}");

// Always confirm immediately after a successful save
bool confirmed = await client.ParcelDownloadConfirmAsync(sessionID, parcelId: 9876543L);
if (!confirmed)
{
    // Log warning — the parcel will be re-delivered on the next poll
    Console.Error.WriteLine("Warning: confirmation failed for parcel {parcelId}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelDownload(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelDownloadAsync({
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

result = client.service.ParcelDownload(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Download Parcel](../../rest-api/parcels/download-parcel.md).
