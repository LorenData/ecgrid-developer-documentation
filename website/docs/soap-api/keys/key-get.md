---
title: KeyGet
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Keys - KeyGet documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# KeyGet

Returns the API key information for a specified user.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/keys/get-key.md).
:::

## Method Signature

```
KeyIDInfo KeyGet(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `UserID` | int | Yes | ID of the user whose API key to retrieve |

## Response Object — KeyIDInfo

| Field | Type | Description |
|---|---|---|
| `KeyID` | int | Unique identifier for this API key record |
| `UserID` | int | ID of the user that owns this key |
| `Key` | string | The API key string value |
| `Visibility` | KeyVisibility | Scope of visibility for this key |
| `Created` | datetime | Date and time the key was created |

```xml
<!-- Example response XML -->
<KeyIDInfo>
  <KeyID>1042</KeyID>
  <UserID>5001</UserID>
  <Key>abc123def456ghi789jkl012mno345pq</Key>
  <Visibility>Private</Visibility>
  <Created>2025-01-15T08:30:00</Created>
</KeyIDInfo>
```

## ENUMs

### KeyVisibility

| Value | Description |
|---|---|
| `Private` | Key is accessible only to the owning user |
| `Shared` | Key is shared within the mailbox or network |
| `Public` | Key is publicly visible |
| `Session` | Key is valid only for the current session |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve the API key record for a specific user
var keyInfo = await client.KeyGetAsync(sessionID, userId);

Console.WriteLine($"Key ID:      {keyInfo.KeyID}");
Console.WriteLine($"Key:         {keyInfo.Key}");
Console.WriteLine($"Visibility:  {keyInfo.Visibility}");
Console.WriteLine($"Created:     {keyInfo.Created:yyyy-MM-dd}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.KeyGet(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.KeyGetAsync({
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

result = client.service.KeyGet(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Get Key](../../rest-api/keys/get-key.md) — `POST /v2/keys/get-key`.
