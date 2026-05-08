---
title: NetworkAdd
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkAdd reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkAdd

Creates a new network and returns the newly created network record.

:::caution Established API
The SOAP API is in maintenance mode. Network creation via API is an administrative operation — contact ECGrid support for provisioning assistance.
:::

## Method Signature

```
NetworkIDInfo NetworkAdd(string SessionID, string UniqueID, string CompanyName, string Address1, string Address2, string City, string State, string Zip, string Phone, string AdminEmail)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetOps or higher authority |
| `UniqueID` | string | Yes | Unique string identifier (slug) for the new network; must be unique across ECGrid |
| `CompanyName` | string | Yes | Display name of the network company |
| `Address1` | string | Yes | Primary street address |
| `Address2` | string | No | Secondary address line (suite, floor, etc.) |
| `City` | string | Yes | City |
| `State` | string | Yes | State or province code |
| `Zip` | string | Yes | Postal code |
| `Phone` | string | Yes | Primary contact phone number |
| `AdminEmail` | string | Yes | Email address for the network administrator |

## Response Object — NetworkIDInfo

| Field | Type | Description |
|---|---|---|
| `NetworkID` | int | System-assigned numeric identifier for the new network |
| `UniqueID` | string | Unique string identifier as provided |
| `CompanyName` | string | Display name as provided |
| `Status` | Status | Initial status of the network (typically `Active`) |
| `Created` | dateTime | UTC timestamp of network creation |
| `Modified` | dateTime | UTC timestamp of the record (same as Created on initial add) |

```xml
<!-- Example response XML -->
<NetworkIDInfo>
  <NetworkID>42</NetworkID>
  <UniqueID>NEWNETWORK</UniqueID>
  <CompanyName>New Network LLC</CompanyName>
  <Status>Active</Status>
  <Created>2026-05-07T14:00:00</Created>
  <Modified>2026-05-07T14:00:00</Modified>
</NetworkIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Network creation requires NetOps-level or higher session authority
var newNetwork = await client.NetworkAddAsync(
    sessionID,
    uniqueID:    "NEWNETWORK",
    companyName: "New Network LLC",
    address1:    "123 Main St",
    address2:    "",
    city:        "Anytown",
    state:       "CA",
    zip:         "90210",
    phone:       "555-555-5555",
    adminEmail:  "admin@newnetwork.com");

Console.WriteLine($"Created NetworkID: {newNetwork.NetworkID}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkAddAsync({
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

result = client.service.NetworkAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

There is no direct REST equivalent for network creation — this is an administrative operation handled through ECGrid provisioning. Contact [ECGrid support](https://www.ecgrid.com) for new network requests.
