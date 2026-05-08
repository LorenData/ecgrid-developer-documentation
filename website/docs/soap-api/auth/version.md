---
title: Version
sidebar_position: 6
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP Auth Version page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Version

Returns the current version string of the ECGridOS SOAP API service.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/auth/version.md).
:::

## Method Signature

```
string Version()
```

## Parameters

This method takes no parameters. No `SessionID` is required — it can be called without authenticating first.

## Response

Returns a `string` containing the API version (e.g., `"4.1"`).

```xml
<!-- Example response -->
<VersionResponse xmlns="http://www.ecgridos.net/">
  <VersionResult>4.1</VersionResult>
</VersionResponse>
```

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// No session required — safe to call before Login()
using var client = new ECGridOSClient(binding, endpoint);

string apiVersion = await client.VersionAsync();

Console.WriteLine($"ECGridOS SOAP API version: {apiVersion}");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.Version(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.VersionAsync({
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

result = client.service.Version(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

:::tip Health check
`Version()` is useful as a lightweight connectivity check. If it returns successfully, the service endpoint is reachable and responding. No credentials are required, so it can be called during application startup diagnostics.
:::

## REST Equivalent

See [Version](../../rest-api/auth/version.md) — `GET /v2/auth/version`.
