---
title: ParcelUpload
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelUpload method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelUpload

Upload an EDI file to ECGrid as a parcel for outbound delivery to trading partners.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/parcels/upload-parcel.md).
:::

## Method Signature

```
long ParcelUpload(string SessionID, string FileName, int Bytes, base64Binary Content)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `FileName` | string | Yes | Original file name (used for logging and identification) |
| `Bytes` | int | Yes | File size in bytes |
| `Content` | base64Binary | Yes | Base64-encoded EDI file content |

## Response Object — long

Returns the newly assigned `ParcelID` (long integer) on success.

```xml
<!-- Example response XML -->
<ParcelUploadResult>9876545</ParcelUploadResult>
```

## Variants

### ParcelUploadEx

Uploads a parcel with an explicit mailbox context, bypassing the session default. Use this when the authenticated session has access to multiple mailboxes and you need to send on behalf of a specific one.

```
long ParcelUploadEx(string SessionID, int NetworkID, int MailboxID,
    string FileName, int Bytes, base64Binary Content)
```

| Additional Parameter | Type | Description |
|---|---|---|
| `NetworkID` | int | Network ID of the sending mailbox |
| `MailboxID` | int | Mailbox ID to send from |

### ParcelUploadMft

Uploads a parcel with explicit sender and recipient ECGrid IDs for direct routing. Use when the routing cannot be inferred from the EDI envelope or when overriding the default routing.

```
long ParcelUploadMft(string SessionID, string FileName, int Bytes,
    base64Binary Content, int ECGridIDFrom, int ECGridIDTo)
```

| Additional Parameter | Type | Description |
|---|---|---|
| `ECGridIDFrom` | int | Sender ECGrid ID |
| `ECGridIDTo` | int | Recipient ECGrid ID |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Read a local EDI file and upload it as a parcel
using var client = new ECGridOSPortTypeClient();

var filePath = "/data/edi/outbound/invoice.edi";
var fileBytes = await File.ReadAllBytesAsync(filePath);
var fileName  = Path.GetFileName(filePath);

long parcelId = await client.ParcelUploadAsync(
    sessionID,
    fileName: fileName,
    bytes:    fileBytes.Length,
    content:  fileBytes);

Console.WriteLine($"Uploaded parcel ID: {parcelId}");

// Use ParcelUploadEx to send from a specific mailbox
long parcelIdEx = await client.ParcelUploadExAsync(
    sessionID,
    networkID: 1,
    mailboxID: 101,
    fileName:  fileName,
    bytes:     fileBytes.Length,
    content:   fileBytes);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelUpload(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelUploadAsync({
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

result = client.service.ParcelUpload(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Upload Parcel](../../rest-api/parcels/upload-parcel.md).
