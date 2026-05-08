---
title: NetworkGateway
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkGateway reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkGateway

Sets the default gateway communication channel (Comm) for a network.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/networks/update-config.md).
:::

## Method Signature

```
NetworkIDInfo NetworkGateway(string SessionID, int NetworkID, int CommID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetworkAdmin or higher authority |
| `NetworkID` | int | Yes | Numeric identifier of the network to configure |
| `CommID` | int | Yes | Numeric identifier of the Comm record to set as the default gateway |

## Response Object — NetworkIDInfo

Returns the updated `NetworkIDInfo` record with the new gateway configuration applied.

| Field | Type | Description |
|---|---|---|
| `NetworkID` | int | Numeric identifier of the network |
| `UniqueID` | string | Unique string identifier of the network |
| `CompanyName` | string | Display name of the network |
| `Status` | Status | Current status of the network |
| `Created` | dateTime | UTC creation timestamp |
| `Modified` | dateTime | UTC timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<NetworkIDInfo>
  <NetworkID>42</NetworkID>
  <UniqueID>MYNETWORK</UniqueID>
  <CompanyName>My Network Company</CompanyName>
  <Status>Active</Status>
  <Created>2020-01-15T00:00:00</Created>
  <Modified>2026-05-07T14:00:00</Modified>
</NetworkIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Assign CommID 101 as the default gateway for network 42
// Use CommFind or CommList to look up valid CommID values first
var updated = await client.NetworkGatewayAsync(
    sessionID,
    networkId: 42,
    commId:    101);

Console.WriteLine($"Gateway updated for network: {updated.CompanyName}");
Console.WriteLine($"Modified: {updated.Modified:yyyy-MM-dd HH:mm}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkGateway(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkGatewayAsync({
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

result = client.service.NetworkGateway(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [CommList](../comms/comm-list.md) — retrieve available Comm channel IDs
- [CommFind](../comms/comm-find.md) — search for a Comm by criteria

## REST Equivalent

See [Update Network Config](../../rest-api/networks/update-config.md) — `POST /v2/networks/update-config`.
