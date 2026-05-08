---
title: NetworkVPN
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkVPN reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkVPN

Configures the VPN IP address and port for a network's secure tunnel connection.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/networks/update-config.md).
:::

## Method Signature

```
bool NetworkVPN(string SessionID, int NetworkID, string VPNIP, int VPNPort)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetworkAdmin or higher authority |
| `NetworkID` | int | Yes | Numeric identifier of the network to configure |
| `VPNIP` | string | Yes | IP address of the VPN endpoint (IPv4, e.g., `192.168.1.1`) |
| `VPNPort` | int | Yes | TCP port number for the VPN tunnel |

## Response

Returns `true` if the VPN configuration was saved successfully, or `false` if the update failed.

```xml
<!-- Example response XML -->
<NetworkVPNResult>true</NetworkVPNResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Set VPN endpoint for network 42 — requires NetworkAdmin authority or higher
bool success = await client.NetworkVPNAsync(
    sessionID,
    networkId: 42,
    vpnIP:     "10.0.0.50",
    vpnPort:   1194);

if (success)
    Console.WriteLine("VPN configuration saved.");
else
    Console.WriteLine("VPN configuration failed — verify IP, port, and authority.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkVPN(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkVPNAsync({
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

result = client.service.NetworkVPN(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Network Config](../../rest-api/networks/update-config.md) — `POST /v2/networks/update-config`.
