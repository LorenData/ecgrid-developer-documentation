---
title: ParcelNote
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP ParcelNote method documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ParcelNote

Attach a free-text note to a parcel record for audit or acknowledgment purposes.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/parcels/acknowledgment-note.md).
:::

## Method Signature

```
bool ParcelNote(string SessionID, long ParcelID, string Note)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `ParcelID` | long | Yes | Unique identifier of the target parcel |
| `Note` | string | Yes | Free-text note to attach (plain text, no size limit enforced by SOAP layer) |

## Response Object — bool

Returns `true` if the note was saved successfully. Returns `false` or throws a SOAP fault if the parcel ID is invalid or the session lacks write permission.

```xml
<!-- Example response XML -->
<ParcelNoteResult>true</ParcelNoteResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Attach a processing acknowledgment note after business validation
using var client = new ECGridOSPortTypeClient();

bool saved = await client.ParcelNoteAsync(
    sessionID,
    parcelId: 9876543L,
    note:     "Received and posted to ERP order system at 2026-05-07T10:15:00Z by automated integration.");

if (saved)
{
    Console.WriteLine("Note attached to parcel.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ParcelNote(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ParcelNoteAsync({
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

result = client.service.ParcelNote(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Acknowledgment Note](../../rest-api/parcels/acknowledgment-note.md).
