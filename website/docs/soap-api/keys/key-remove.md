---
title: KeyRemove
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Keys - KeyRemove documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# KeyRemove

Permanently removes an API key by its key ID.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/keys/delete-key.md).
:::

:::caution Irreversible Action
Removing a key immediately invalidates it. Any integrations or systems authenticating with this key will stop working instantly. Verify no active integrations depend on this key before removing it.
:::

## Method Signature

```
bool KeyRemove(string SessionID, int KeyID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `KeyID` | int | Yes | ID of the API key to remove |

## Response Object — bool

Returns `true` if the key was successfully removed; `false` otherwise.

```xml
<!-- Example response XML -->
<KeyRemoveResult>true</KeyRemoveResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Remove an API key — this action is immediate and irreversible
bool removed = await client.KeyRemoveAsync(sessionID, keyId);

if (removed)
{
    Console.WriteLine($"Key {keyId} has been removed. Any integrations using this key are now invalidated.");
}
else
{
    Console.WriteLine($"Key {keyId} could not be removed. Verify the key ID and your permissions.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.KeyRemove(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.KeyRemoveAsync({
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

result = client.service.KeyRemove(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Delete Key](../../rest-api/keys/delete-key.md) — `DELETE /v2/keys`.
