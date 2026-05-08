---
title: NetworkList
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkList reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkList

Returns a paginated list of networks, optionally filtered by status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/networks/list-networks.md).
:::

## Method Signature

```
ArrayOfNetworkIDInfo NetworkList(string SessionID, int NetworkID, Status Status, short PageNo, short RecordsPerPage)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Scope the list to this network (0 for all accessible networks) |
| `Status` | Status | Yes | Filter by network status; use `Active` for live networks |
| `PageNo` | short | Yes | 1-based page number for pagination |
| `RecordsPerPage` | short | Yes | Number of records per page (max 500) |

## Response Object — ArrayOfNetworkIDInfo

Returns an array of `NetworkIDInfo` objects.

| Field | Type | Description |
|---|---|---|
| `NetworkID` | int | Unique numeric identifier for the network |
| `UniqueID` | string | Unique string identifier (slug) for the network |
| `CompanyName` | string | Display name of the network company |
| `Status` | Status | Current status of the network |
| `Created` | dateTime | UTC timestamp when the network record was created |
| `Modified` | dateTime | UTC timestamp of the most recent modification |

```xml
<!-- Example response XML -->
<ArrayOfNetworkIDInfo>
  <NetworkIDInfo>
    <NetworkID>1</NetworkID>
    <UniqueID>MYNETWORK</UniqueID>
    <CompanyName>My Network Company</CompanyName>
    <Status>Active</Status>
    <Created>2020-01-15T00:00:00</Created>
    <Modified>2024-03-10T12:34:56</Modified>
  </NetworkIDInfo>
  <NetworkIDInfo>
    <NetworkID>2</NetworkID>
    <UniqueID>PARTNERNETWORK</UniqueID>
    <CompanyName>Partner Network Inc.</CompanyName>
    <Status>Active</Status>
    <Created>2021-06-01T00:00:00</Created>
    <Modified>2024-01-20T08:00:00</Modified>
  </NetworkIDInfo>
</ArrayOfNetworkIDInfo>
```

## Variants

### NetworkListEx

Returns the same list but scoped to a specific mailbox within the network, enabling finer-grained filtering.

```
ArrayOfNetworkIDInfo NetworkListEx(string SessionID, int NetworkID, int MailboxID, Status Status, short PageNo, short RecordsPerPage)
```

| Additional Parameter | Type | Description |
|---|---|---|
| `MailboxID` | int | Scope results to networks visible from this mailbox |

## ENUMs

### Status

See [Status enum](../../appendix/enums.md#status) for all possible values.

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Page through all active networks
short pageNo = 1;
const short pageSize = 100;

NetworkIDInfo[] page;
do
{
    page = await client.NetworkListAsync(sessionID, networkId, Status.Active, pageNo, pageSize);
    foreach (var network in page)
    {
        Console.WriteLine($"{network.NetworkID}: {network.CompanyName}");
    }
    pageNo++;
} while (page.Length == pageSize);

// Extended variant — scope to a specific mailbox
var mailboxNetworks = await client.NetworkListExAsync(
    sessionID, networkId, mailboxId, Status.Active, 1, 100);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkListAsync({
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

result = client.service.NetworkList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Networks](../../rest-api/networks/list-networks.md) — `POST /v2/networks/list`.
