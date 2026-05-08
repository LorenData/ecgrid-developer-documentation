---
title: CommFind
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommFind documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommFind

Searches for communication channels matching a given identifier string and optional protocol type.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/find-comm.md).
:::

## Method Signature

```
ArrayOfCommIDInfo CommFind(string SessionID, string Identifier, NetworkGatewayCommChannel CommType)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `Identifier` | string | Yes | Protocol-specific identifier to search for (hostname, AS2 ID, URL, etc.) |
| `CommType` | NetworkGatewayCommChannel | Yes | Protocol type to filter by; use `none` to search across all types |

## Response Object — ArrayOfCommIDInfo

Returns an array of `CommIDInfo` objects that match the search criteria. Each element contains:

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Unique identifier of the comm channel |
| `MailboxID` | int | Mailbox associated with this comm channel |
| `CommType` | NetworkGatewayCommChannel | Protocol type |
| `Identifier` | string | Protocol-specific identifier |
| `Status` | Status | Current status of the comm channel |
| `UseType` | UseType | Test, production, or both |
| `PrivateKeyRequired` | bool | Whether a private key is required |
| `WithCerts` | bool | Whether certificate details are included |

```xml
<!-- Example response XML -->
<ArrayOfCommIDInfo>
  <CommIDInfo>
    <CommID>4523</CommID>
    <MailboxID>102</MailboxID>
    <CommType>as2</CommType>
    <Identifier>PARTNER-AS2-ID</Identifier>
    <Status>Active</Status>
    <UseType>Production</UseType>
    <PrivateKeyRequired>true</PrivateKeyRequired>
    <WithCerts>false</WithCerts>
  </CommIDInfo>
</ArrayOfCommIDInfo>
```

## ENUMs

### NetworkGatewayCommChannel

| Value | Description |
|---|---|
| `none` | No filter — search all types |
| `ftp` | FTP |
| `sftp` | SFTP |
| `as2` | AS2 |
| `http` | HTTP |
| `oftp` | OFTP |
| `x400` | X.400 |
| `gisb` | GISB |
| `rnif` | RosettaNet |
| `cxml` | cXML |
| `ftpsslimplicit` | FTP over SSL (implicit) |
| `peppol` | PEPPOL |
| `as4` | AS4 |
| `undefined` | Undefined |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Search for AS2 channels using a known AS2 identifier
CommIDInfo[] results = await client.CommFindAsync(
    sessionID,
    Identifier: "PARTNER-AS2-ID",
    CommType: NetworkGatewayCommChannel.as2);

foreach (var ch in results)
{
    Console.WriteLine($"CommID: {ch.CommID} | Mailbox: {ch.MailboxID} | Status: {ch.Status}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommFind(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommFindAsync({
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

result = client.service.CommFind(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Find Comm](../../rest-api/comms/find-comm.md) — `POST /v2/comms/find`.
