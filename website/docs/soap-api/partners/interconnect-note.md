---
title: InterconnectNote
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Initial creation of InterconnectNote SOAP method page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# InterconnectNote

Adds an audit note to an existing interconnect record for tracking changes, approvals, or communications.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/partners/add-note.md).
:::

## Method Signature

```
bool InterconnectNote(string SessionID, int InterconnectID, string Note)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token obtained from `Login()` |
| `InterconnectID` | int | Yes | Numeric identifier for the interconnect to annotate |
| `Note` | string | Yes | Free-text note to attach to the interconnect record |

## Response

Returns `true` if the note was successfully added; `false` otherwise.

```xml
<!-- Example response XML -->
<InterconnectNoteResult>true</InterconnectNoteResult>
```

:::note
Notes are appended to the interconnect's audit trail and are not editable or deletable after creation. Each note is timestamped and associated with the session's user. Use notes to record approval decisions, issue resolutions, or onboarding milestones.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
using var client = new ECGridOSPortTypeClient();

bool added = await client.InterconnectNoteAsync(
    sessionID,
    interconnectID: 5001,
    note: "Approved by trading partner contact — Jane Smith (jane@example.com) on 2026-05-07.");

if (added)
{
    Console.WriteLine("Note added to interconnect 5001.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.InterconnectNote(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.InterconnectNoteAsync({
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

result = client.service.InterconnectNote(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Add Note](../../rest-api/partners/add-note.md) — `POST /v2/partners/note`.
