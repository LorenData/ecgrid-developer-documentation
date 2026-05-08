---
title: CommUpdate
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommUpdate documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommUpdate

Updates the identifier and/or status of an existing communication channel.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/update-comm.md).
:::

## Method Signature

```
CommIDInfo CommUpdate(string SessionID, int CommID, string Identifier, Status Status)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Unique identifier of the comm channel to update |
| `Identifier` | string | Yes | New protocol-specific identifier (hostname, AS2 ID, URL, etc.) |
| `Status` | Status | Yes | New status for the comm channel |

## Response Object — CommIDInfo

Returns the updated `CommIDInfo` object reflecting the changes.

| Field | Type | Description |
|---|---|---|
| `CommID` | int | Unique identifier of the comm channel |
| `MailboxID` | int | Mailbox associated with this comm channel |
| `CommType` | NetworkGatewayCommChannel | Protocol type (unchanged) |
| `Identifier` | string | Updated protocol-specific identifier |
| `Status` | Status | Updated status |
| `UseType` | UseType | Use type (unchanged) |
| `PrivateKeyRequired` | bool | Whether a private key is required (unchanged) |
| `WithCerts` | bool | Whether certificate details are included |

```xml
<!-- Example response XML -->
<CommIDInfo>
  <CommID>4521</CommID>
  <MailboxID>100</MailboxID>
  <CommType>sftp</CommType>
  <Identifier>sftp.updatedhost.com</Identifier>
  <Status>Active</Status>
  <UseType>Production</UseType>
  <PrivateKeyRequired>false</PrivateKeyRequired>
  <WithCerts>false</WithCerts>
</CommIDInfo>
```

## ENUMs

### Status

| Value | Description |
|---|---|
| `Development` | In development |
| `Active` | Active and operational |
| `Preproduction` | Staging / pre-production |
| `Suspended` | Temporarily suspended |
| `Terminated` | Permanently terminated |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Update comm channel 4521 with a new hostname and keep it active
CommIDInfo updated = await client.CommUpdateAsync(
    sessionID,
    CommID: 4521,
    Identifier: "sftp.updatedhost.com",
    Status: Status.Active);

Console.WriteLine($"CommID:     {updated.CommID}");
Console.WriteLine($"Identifier: {updated.Identifier}");
Console.WriteLine($"Status:     {updated.Status}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommUpdate(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommUpdateAsync({
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

result = client.service.CommUpdate(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Comm](../../rest-api/comms/update-comm.md) — `PUT /v2/comms/update`.
