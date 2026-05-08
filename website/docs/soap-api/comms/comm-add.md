---
title: CommAdd
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommAdd documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommAdd

Creates a new communication channel for the specified mailbox with the given protocol type and identifier.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/create-comm.md).
:::

## Method Signature

```
CommIDInfo CommAdd(string SessionID, int MailboxID, NetworkGatewayCommChannel CommType, string Identifier, UseType UseType, bool PrivateKeyRequired)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `MailboxID` | int | Yes | Mailbox to associate with the new comm channel |
| `CommType` | NetworkGatewayCommChannel | Yes | Protocol type for the new channel (SFTP, AS2, FTP, etc.) |
| `Identifier` | string | Yes | Protocol-specific identifier (hostname, AS2 ID, URL, etc.) |
| `UseType` | UseType | Yes | Whether the channel handles test, production, or both |
| `PrivateKeyRequired` | bool | Yes | Set to `true` if a private key is required for authentication |

## Response Object — CommIDInfo

Returns the newly created `CommIDInfo` object.

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Unique identifier assigned to the new comm channel |
| `MailboxID` | int | Mailbox associated with this comm channel |
| `CommType` | NetworkGatewayCommChannel | Protocol type |
| `Identifier` | string | Protocol-specific identifier |
| `Status` | Status | Initial status (typically `Active`) |
| `UseType` | UseType | Test, production, or both |
| `PrivateKeyRequired` | bool | Whether a private key is required |
| `WithCerts` | bool | Whether certificate details are included |

```xml
<!-- Example response XML -->
<CommIDInfo>
  <CommID>4530</CommID>
  <MailboxID>100</MailboxID>
  <CommType>sftp</CommType>
  <Identifier>sftp.newpartner.com</Identifier>
  <Status>Active</Status>
  <UseType>Production</UseType>
  <PrivateKeyRequired>false</PrivateKeyRequired>
  <WithCerts>false</WithCerts>
</CommIDInfo>
```

## ENUMs

### NetworkGatewayCommChannel

| Value | Description |
|---|---|
| `none` | No channel configured |
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

// Add a new SFTP production comm channel for mailbox 100
CommIDInfo newComm = await client.CommAddAsync(
    sessionID,
    MailboxID: 100,
    CommType: NetworkGatewayCommChannel.sftp,
    Identifier: "sftp.newpartner.com",
    UseType: UseType.Production,
    PrivateKeyRequired: false);

Console.WriteLine($"Created CommID: {newComm.CommID}");
Console.WriteLine($"Status: {newComm.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommAdd(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommAddAsync({
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

result = client.service.CommAdd(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create Comm](../../rest-api/comms/create-comm.md) — `POST /v2/comms/create`.
