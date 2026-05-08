---
title: TPSearch
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of TPSearch SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# TPSearch

Searches the ECGrid network directory for trading partner IDs matching the given ISA qualifier and ID value.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/ids/find-id.md).
:::

## Method Signature

```
ArrayOfECGridIDInfo TPSearch(string SessionID, string Qualifier, string ID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `Qualifier` | string | Yes | ISA qualifier to search for (e.g., `01`, `08`, `ZZ`) |
| `ID` | string | Yes | ISA ID value to search for; supports partial/wildcard matching |

## Response Object — ArrayOfECGridIDInfo

Returns an array of matching `ECGridIDInfo` objects. See [ECGridIDInfo](./ecgrid-id-info.md) for field definitions.

| Field | Type | Description |
|---|---|---|
| `ECGridID` | int | Unique numeric identifier |
| `MailboxID` | int | Owning mailbox ID |
| `NetworkID` | int | Associated network ID |
| `Qualifier` | string | ISA qualifier |
| `ID` | string | ISA ID value |
| `Description` | string | Trading partner label |
| `Status` | Status | Lifecycle status |
| `RoutingGroup` | RoutingGroup | Routing group |
| `EDIStandard` | EDIStandard | EDI standard |

```xml
<!-- Example response XML -->
<TPSearchResult>
  <ECGridIDInfo>
    <ECGridID>123456</ECGridID>
    <MailboxID>789</MailboxID>
    <NetworkID>42</NetworkID>
    <Qualifier>01</Qualifier>
    <ID>ACMECORP      </ID>
    <Description>Acme Corporation</Description>
    <Status>Active</Status>
    <RoutingGroup>ProductionA</RoutingGroup>
    <EDIStandard>X12</EDIStandard>
  </ECGridIDInfo>
</TPSearchResult>
```

## Variants

### TPSearchEx

Extends `TPSearch` by scoping the search to a specific network and mailbox, allowing operators to find IDs within their own managed environment.

```
ArrayOfECGridIDInfo TPSearchEx(string SessionID, int NetworkID, int MailboxID, string Qualifier, string ID)
```

| Additional Parameter | Type | Description |
|---|---|---|
| `NetworkID` | int | Scope search to this network; use `0` for all accessible networks |
| `MailboxID` | int | Scope search to this mailbox; use `0` for all mailboxes |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

// Search across all accessible networks
ECGridIDInfo[] results = await client.TPSearchAsync(
    sessionID,
    qualifier: "01",
    id: "ACMECORP");

foreach (var match in results)
{
    Console.WriteLine($"ECGridID: {match.ECGridID}  {match.Qualifier}:{match.ID}  {match.Description}");
}

// Scoped search using TPSearchEx
ECGridIDInfo[] scopedResults = await client.TPSearchExAsync(
    sessionID,
    networkID: 42,
    mailboxID: 0,    // all mailboxes in network 42
    qualifier: "ZZ",
    id: "PARTNER");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.TPSearch(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.TPSearchAsync({
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

result = client.service.TPSearch(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Find ID](../../rest-api/ids/find-id.md) — `POST /v2/ids/find`.
