---
title: UserGetAPIKey
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP UserGetAPIKey documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# UserGetAPIKey

Retrieves the API key for the specified user account, which can be used for REST API authentication via the `X-API-Key` header.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/users/get-api-key.md).
:::

## Method Signature

```
string UserGetAPIKey(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `UserID` | int | Yes | Unique identifier of the user whose API key is being retrieved |

## Response

Returns the user's API key as a plain string. This key is used as the value of the `X-API-Key` header when calling the ECGrid REST API.

```xml
<!-- Example response XML -->
<UserGetAPIKeyResult>abc123def456ghi789jkl012mno345pqr</UserGetAPIKeyResult>
```

:::warning Keep API Keys Secure
Never log, display in UI, or store API keys in source code. Load them from environment variables or a secrets manager.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using ECGridOSClient;

var client = new ECGridOSPortTypeClient();

// Retrieve the API key for user 5001
string apiKey = await client.UserGetAPIKeyAsync(sessionID, UserID: 5001);

// Use the key — store securely, never log it
Console.WriteLine("API key retrieved successfully.");

// Example: pass to REST client configuration
httpClient.DefaultRequestHeaders.Add("X-API-Key", apiKey);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.UserGetAPIKey(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.UserGetAPIKeyAsync({
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

result = client.service.UserGetAPIKey(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get API Key](../../rest-api/users/get-api-key.md) — `GET /v2/users/key/{id}`.
