---
title: CommDefaultMailbox
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP CommDefaultMailbox documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# CommDefaultMailbox

Sets the default mailbox for a communication channel, determining which mailbox receives inbound EDI when no more-specific routing rule applies.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/comms/update-config.md).
:::

## Method Signature

```
bool CommDefaultMailbox(string SessionID, int CommID, int MailboxID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `CommID` | int | Yes | Unique identifier of the communication channel |
| `MailboxID` | int | Yes | Mailbox ID to set as the default for this comm channel |

## Response

Returns `true` if the default mailbox was successfully updated; throws a SOAP fault on failure.

```xml
<!-- Example response XML -->
<CommDefaultMailboxResult>true</CommDefaultMailboxResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Set mailbox 200 as the default for comm channel 4521
bool success = await client.CommDefaultMailboxAsync(
    sessionID,
    CommID: 4521,
    MailboxID: 200);

if (success)
{
    Console.WriteLine("Default mailbox updated successfully.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.CommDefaultMailbox(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.CommDefaultMailboxAsync({
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

result = client.service.CommDefaultMailbox(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Update Comm Config](../../rest-api/comms/update-config.md) — `PUT /v2/comms/update-config`.
