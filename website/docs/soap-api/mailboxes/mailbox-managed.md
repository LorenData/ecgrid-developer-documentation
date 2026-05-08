---
title: MailboxManaged
sidebar_position: 9
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP MailboxManaged reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MailboxManaged

Sets a mailbox to managed or unmanaged mode, which controls whether ECGrid handles certain processing operations on behalf of the mailbox owner.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/mailboxes/update-config.md).
:::

## Method Signature

```
bool MailboxManaged(string SessionID, int MailboxID, bool Managed)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` with NetworkAdmin or higher authority |
| `MailboxID` | int | Yes | Numeric identifier of the mailbox to configure |
| `Managed` | bool | Yes | `true` to enable managed mode; `false` to set unmanaged (self-service) mode |

## Response

Returns `true` if the managed mode was successfully updated, or `false` if the operation failed.

```xml
<!-- Example response XML -->
<MailboxManagedResult>true</MailboxManagedResult>
```

:::note Managed Mode
In managed mode, the network operator takes responsibility for certain EDI processing tasks on behalf of the mailbox. This is typically used for customers who outsource EDI operations to their VAN or network provider. Changing this setting requires NetworkAdmin authority.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Enable managed mode for a mailbox — requires NetworkAdmin authority
bool success = await client.MailboxManagedAsync(
    sessionID,
    mailboxId: 100,
    managed:   true);

if (success)
    Console.WriteLine("Mailbox 100 is now in managed mode.");
else
    Console.WriteLine("Failed to update managed mode — check authority level.");

// Disable managed mode
// bool reset = await client.MailboxManagedAsync(sessionID, 100, false);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.MailboxManaged(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.MailboxManagedAsync({
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

result = client.service.MailboxManaged(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## See Also

- [MailboxConfig](./mailbox-config.md) — configure managed mode alongside other settings in a single call

## REST Equivalent

See [Update Mailbox Config](../../rest-api/mailboxes/update-config.md) — `POST /v2/mailboxes/update-config`.
