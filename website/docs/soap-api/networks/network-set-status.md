---
title: NetworkSetStatus
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkSetStatus reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkSetStatus

Sets the operational status of a network (e.g., Active, Suspended, Terminated).

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/networks/update-network.md).
:::

## Method Signature

```
bool NetworkSetStatus(string SessionID, int NetworkID, Status Status)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetOps or higher authority |
| `NetworkID` | int | Yes | Numeric identifier of the network to update |
| `Status` | Status | Yes | The new status to apply to the network |

## Response

Returns `true` if the status was successfully updated, or `false` if the operation failed.

```xml
<!-- Example response XML -->
<NetworkSetStatusResult>true</NetworkSetStatusResult>
```

## ENUMs

### Status

See [Status enum](../../appendix/enums.md#status) for all possible values.

| Value | Description |
|---|---|
| `Development` | Network is in setup/development mode |
| `Active` | Network is live and processing EDI |
| `Preproduction` | Network is in testing/staging mode |
| `Suspended` | Network is temporarily disabled |
| `Terminated` | Network is permanently closed |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Suspend a network temporarily — requires elevated authority
bool success = await client.NetworkSetStatusAsync(
    sessionID,
    networkId: 42,
    status:    Status.Suspended);

if (success)
    Console.WriteLine("Network status updated to Suspended.");
else
    Console.WriteLine("Status update failed — check authority level.");

// Reactivate later
success = await client.NetworkSetStatusAsync(sessionID, networkId: 42, status: Status.Active);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkSetStatus(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkSetStatusAsync({
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

result = client.service.NetworkSetStatus(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Network](../../rest-api/networks/update-network.md) — `PUT /v2/networks` (include a `status` field in the request body).
