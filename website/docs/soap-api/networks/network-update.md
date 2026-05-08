---
title: NetworkUpdate
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkUpdate reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkUpdate

Updates the contact and address information for an existing network.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/networks/update-network.md).
:::

## Method Signature

```
NetworkIDInfo NetworkUpdate(string SessionID, int NetworkID, string CompanyName, string Address1, string City, string State, string Zip, string Phone)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetworkAdmin or higher authority |
| `NetworkID` | int | Yes | Numeric identifier of the network to update |
| `CompanyName` | string | Yes | Updated display name for the network |
| `Address1` | string | Yes | Primary street address |
| `City` | string | Yes | City |
| `State` | string | Yes | State or province code |
| `Zip` | string | Yes | Postal code |
| `Phone` | string | Yes | Primary contact phone number |

## Response Object — NetworkIDInfo

Returns the updated `NetworkIDInfo` record reflecting the changes.

| Field | Type | Description |
|---|---|---|
| `NetworkID` | int | Numeric identifier of the updated network |
| `UniqueID` | string | Unique string identifier (unchanged) |
| `CompanyName` | string | Updated display name |
| `Status` | Status | Current status of the network |
| `Created` | dateTime | Original creation timestamp (unchanged) |
| `Modified` | dateTime | UTC timestamp of the update |

```xml
<!-- Example response XML -->
<NetworkIDInfo>
  <NetworkID>42</NetworkID>
  <UniqueID>MYNETWORK</UniqueID>
  <CompanyName>My Updated Network Name</CompanyName>
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
// Update network contact details — all fields are required
var updated = await client.NetworkUpdateAsync(
    sessionID,
    networkId:   42,
    companyName: "My Updated Network Name",
    address1:    "456 Corporate Blvd",
    city:        "Springfield",
    state:       "IL",
    zip:         "62701",
    phone:       "555-123-4567");

Console.WriteLine($"Updated: {updated.CompanyName} at {updated.Modified:yyyy-MM-dd HH:mm}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkUpdate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkUpdateAsync({
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

result = client.service.NetworkUpdate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Network](../../rest-api/networks/update-network.md) — `PUT /v2/networks`.
