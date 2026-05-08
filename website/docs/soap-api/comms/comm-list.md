---
title: CommList
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommList documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommList

Returns a filtered list of communication channels based on type, key requirements, use type, and active status.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/list-comms.md).
:::

## Method Signature

```
ArrayOfCommIDInfo CommList(string SessionID, NetworkGatewayCommChannel CommType, bool PrivateKeyRequired, UseType UseType, bool ShowInactive, bool WithCerts)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommType` | NetworkGatewayCommChannel | Yes | Filter by protocol type; use `none` to return all types |
| `PrivateKeyRequired` | bool | Yes | Filter to channels that require a private key |
| `UseType` | UseType | Yes | Filter by use type (Test, Production, or both) |
| `ShowInactive` | bool | Yes | When `true`, includes suspended and terminated channels in results |
| `WithCerts` | bool | Yes | When `true`, includes certificate details in each result |

## Response Object — ArrayOfCommIDInfo

Returns an array of `CommIDInfo` objects. Each element contains:

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
    <CommID>4521</CommID>
    <MailboxID>100</MailboxID>
    <CommType>sftp</CommType>
    <Identifier>sftp.tradingpartner.com</Identifier>
    <Status>Active</Status>
    <UseType>Production</UseType>
    <PrivateKeyRequired>false</PrivateKeyRequired>
    <WithCerts>false</WithCerts>
  </CommIDInfo>
  <CommIDInfo>
    <CommID>4522</CommID>
    <MailboxID>101</MailboxID>
    <CommType>as2</CommType>
    <Identifier>MYPARTNER-AS2-ID</Identifier>
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
| `none` | No filter — return all types |
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

### UseType

| Value | Description |
|---|---|
| `Undefined` | Not specified |
| `Test` | Test traffic only |
| `Production` | Production traffic only |
| `TestAndProduction` | Both test and production traffic |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// List all active SFTP production channels (no private key filter, no certs)
CommIDInfo[] channels = await client.CommListAsync(
    sessionID,
    CommType: NetworkGatewayCommChannel.sftp,
    PrivateKeyRequired: false,
    UseType: UseType.Production,
    ShowInactive: false,
    WithCerts: false);

foreach (var ch in channels)
{
    Console.WriteLine($"CommID: {ch.CommID} | Mailbox: {ch.MailboxID} | Host: {ch.Identifier}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommListAsync({
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

result = client.service.CommList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Comms](../../rest-api/comms/list-comms.md) — `POST /v2/comms/list`.
