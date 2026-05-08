---
title: KeySet
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Keys - KeySet documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# KeySet

Creates or updates an API key for a user with a specified visibility level.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/keys/create-key.md).
:::

## Method Signature

```
KeyIDInfo KeySet(string SessionID, int UserID, KeyVisibility Visibility)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `UserID` | int | Yes | ID of the user for whom to create or update the API key |
| `Visibility` | KeyVisibility | Yes | Visibility scope to assign to the key |

## Response Object — KeyIDInfo

| Field | Type | Description |
|---|---|---|
| `KeyID` | int | Unique identifier for this API key record |
| `UserID` | int | ID of the user that owns this key |
| `Key` | string | The API key string value |
| `Visibility` | KeyVisibility | Visibility scope assigned to this key |
| `Created` | datetime | Date and time the key was created |

```xml
<!-- Example response XML -->
<KeyIDInfo>
  <KeyID>1043</KeyID>
  <UserID>5001</UserID>
  <Key>xyz987uvw654rst321opq098nml765kj</Key>
  <Visibility>Shared</Visibility>
  <Created>2026-05-07T10:00:00</Created>
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
// Create or update an API key with Shared visibility
var keyInfo = await client.KeySetAsync(sessionID, userId, KeyVisibility.Shared);

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

var result = port.KeySet(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.KeySetAsync({
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

result = client.service.KeySet(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Create Key](../../rest-api/keys/create-key.md) — `POST /v2/keys/create`.
