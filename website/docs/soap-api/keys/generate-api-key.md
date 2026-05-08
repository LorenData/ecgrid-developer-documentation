---
title: GenerateAPIKey
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Keys - GenerateAPIKey documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# GenerateAPIKey

Generates a new API key for a user, replacing any existing key.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/generate-api-key.md).
:::

:::caution Key Replacement
Generating a new key immediately invalidates the previous key for this user. Update any integrations that use the old key before or immediately after calling this method.
:::

## Method Signature

```
string GenerateAPIKey(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `UserID` | int | Yes | ID of the user for whom to generate a new API key |

## Response Object — string

Returns the newly generated API key string.

```xml
<!-- Example response XML -->
<GenerateAPIKeyResult>mnp456qrs789tuv012wxy345zab678cd</GenerateAPIKeyResult>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Generate a new API key — the previous key is immediately invalidated
string newKey = await client.GenerateAPIKeyAsync(sessionID, userId);

Console.WriteLine($"New API key generated for user {userId}:");
Console.WriteLine(newKey);
Console.WriteLine("Update all integrations using this user's previous key.");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.GenerateAPIKey(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.GenerateAPIKeyAsync({
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

result = client.service.GenerateAPIKey(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Generate API Key](../../rest-api/users/generate-api-key.md) — `POST /v2/users/key-generate/{id}`.
