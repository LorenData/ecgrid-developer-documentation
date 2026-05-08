---
title: CommInfo
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommInfo documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommInfo

Retrieves detailed information about a single communication channel by its unique CommID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/get-comm.md).
:::

## Method Signature

```
CommIDInfo CommInfo(string SessionID, int CommID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Unique identifier of the communication channel to retrieve |

## Response Object — CommIDInfo

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Unique identifier of the comm channel |
| `MailboxID` | int | Mailbox associated with this comm channel |
| `CommType` | NetworkGatewayCommChannel | Protocol type (FTP, SFTP, AS2, etc.) |
| `Identifier` | string | Protocol-specific identifier (URL, hostname, AS2 ID, etc.) |
| `Status` | Status | Current status of the comm channel |
| `UseType` | UseType | Whether the channel is used for test, production, or both |
| `PrivateKeyRequired` | bool | Whether a private key is required for authentication |
| `WithCerts` | bool | Whether certificate information is included in the response |

```xml
<!-- Example response XML -->
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

### Status

| Value | Description |
|---|---|
| `Development` | In development |
| `Active` | Active and operational |
| `Preproduction` | Staging / pre-production |
| `Suspended` | Temporarily suspended |
| `Terminated` | Permanently terminated |

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

// Retrieve comm channel details by CommID
CommIDInfo commInfo = await client.CommInfoAsync(sessionID, commID: 4521);

Console.WriteLine($"CommID:     {commInfo.CommID}");
Console.WriteLine($"MailboxID:  {commInfo.MailboxID}");
Console.WriteLine($"Type:       {commInfo.CommType}");
Console.WriteLine($"Identifier: {commInfo.Identifier}");
Console.WriteLine($"Status:     {commInfo.Status}");
Console.WriteLine($"UseType:    {commInfo.UseType}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommInfo(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommInfoAsync({
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

result = client.service.CommInfo(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Comm](../../rest-api/comms/get-comm.md) — `GET /v2/comms/{id}`.
