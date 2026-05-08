---
title: KeyList
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Keys - KeyList documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# KeyList

Returns all API keys associated with a specified user.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/keys/list-keys.md).
:::

## Method Signature

```
ArrayOfKeyIDInfo KeyList(string SessionID, int UserID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `UserID` | int | Yes | ID of the user whose API keys to list |

## Response Object — ArrayOfKeyIDInfo

Returns an array of `KeyIDInfo` objects.

| Field | Type | Description |
|---|---|---|
| `KeyID` | int | Unique identifier for this API key record |
| `UserID` | int | ID of the user that owns this key |
| `Key` | string | The API key string value |
| `Visibility` | KeyVisibility | Visibility scope of this key |
| `Created` | datetime | Date and time the key was created |

```xml
<!-- Example response XML -->
<ArrayOfKeyIDInfo>
  <KeyIDInfo>
    <KeyID>1042</KeyID>
    <UserID>5001</UserID>
    <Key>abc123def456ghi789jkl012mno345pq</Key>
    <Visibility>Private</Visibility>
    <Created>2025-01-15T08:30:00</Created>
  </KeyIDInfo>
  <KeyIDInfo>
    <KeyID>1043</KeyID>
    <UserID>5001</UserID>
    <Key>xyz987uvw654rst321opq098nml765kj</Key>
    <Visibility>Shared</Visibility>
    <Created>2026-05-07T10:00:00</Created>
  </KeyIDInfo>
</ArrayOfKeyIDInfo>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// List all API keys for a user
var keys = await client.KeyListAsync(sessionID, userId);

foreach (var key in keys)
{
    Console.WriteLine($"Key ID: {key.KeyID} | Visibility: {key.Visibility} | Created: {key.Created:yyyy-MM-dd}");
    Console.WriteLine($"  Key: {key.Key}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.KeyList(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.KeyListAsync({
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

result = client.service.KeyList(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [List Keys](../../rest-api/keys/list-keys.md) — `POST /v2/keys/list`.
