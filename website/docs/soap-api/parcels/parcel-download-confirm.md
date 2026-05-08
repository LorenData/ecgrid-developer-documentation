---
title: ParcelDownloadConfirm
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelDownloadConfirm method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelDownloadConfirm

Confirm that an inbound parcel has been successfully downloaded and saved.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/parcels/confirm-download.md).
:::

:::caution Confirmation Is Mandatory
This method **must** be called after every successful [`ParcelDownload`](./parcel-download.md). Without confirmation, ECGrid marks the parcel as undelivered and will re-deliver it on the next polling cycle, causing duplicate file processing.
:::

## Method Signature

```
bool ParcelDownloadConfirm(string SessionID, long ParcelID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ParcelID` | long | Yes | Unique identifier of the parcel to confirm |

## Response Object — bool

Returns `true` if the confirmation was accepted. Returns `false` or throws a SOAP fault if the parcel ID is invalid, already confirmed, or the session lacks permission.

```xml
<!-- Example response XML -->
<ParcelDownloadConfirmResult>true</ParcelDownloadConfirmResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Confirm receipt only after the file has been durably saved
using var client = new ECGridOSPortTypeClient();

bool confirmed = await client.ParcelDownloadConfirmAsync(sessionID, parcelId: 9876543L);

if (confirmed)
{
    Console.WriteLine($"Parcel {parcelId} confirmed — removed from delivery queue.");
}
else
{
    // Surface this as an operational alert; the parcel will be re-delivered
    Console.Error.WriteLine($"Confirm failed for parcel {parcelId}.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelDownloadConfirm(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelDownloadConfirmAsync({
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

result = client.service.ParcelDownloadConfirm(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Confirm Download](../../rest-api/parcels/confirm-download.md).
