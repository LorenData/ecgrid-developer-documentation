---
title: NetworkInfo
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkInfo reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkInfo

Retrieves detailed information about a single network by its NetworkID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/networks/get-network.md).
:::

## Method Signature

```
NetworkIDInfo NetworkInfo(string SessionID, int NetworkID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Numeric identifier of the network to retrieve |

## Response Object — NetworkIDInfo

| Field | Type | Description |
|---|---|---|
| `NetworkID` | int | Unique numeric identifier for the network |
| `UniqueID` | string | Unique string identifier (slug) for the network |
| `CompanyName` | string | Display name of the network company |
| `Status` | Status | Current status of the network (see ENUMs) |
| `Created` | dateTime | UTC timestamp when the network record was created |
| `Modified` | dateTime | UTC timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<NetworkIDInfo>
  <NetworkID>1</NetworkID>
  <UniqueID>MYNETWORK</UniqueID>
  <CompanyName>My Network Company</CompanyName>
  <Status>Active</Status>
  <Created>2020-01-15T00:00:00</Created>
  <Modified>2024-03-10T12:34:56</Modified>
</NetworkIDInfo>
```

## ENUMs

### Status

See [Status enum](../../appendix/enums.md#status) for all possible values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve network details for a known NetworkID
var result = await client.NetworkInfoAsync(sessionID, networkId);

Console.WriteLine($"Network: {result.CompanyName} ({result.Status})");
Console.WriteLine($"Created: {result.Created:yyyy-MM-dd}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkInfoAsync({
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

result = client.service.NetworkInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Network](../../rest-api/networks/get-network.md) — `GET /v2/networks/{id}`.
