---
title: NetworkStatusSummary
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP NetworkStatusSummary reference page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# NetworkStatusSummary

Returns a summary of activity and status statistics for a network, including counts of mailboxes, trading partners, and recent interchange activity.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/reports/mailbox-stats.md).
:::

## Method Signature

```
DataSet NetworkStatusSummary(string SessionID, int NetworkID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from `Login()` |
| `NetworkID` | int | Yes | Numeric identifier of the network to summarize |

## Response Object — DataSet

Returns an ADO.NET `DataSet` containing one or more tables with network-level status counts and statistics. The exact schema varies by network configuration; common fields include:

| Field | Type | Description |
|---|---|---|
| `NetworkID` | int | The queried network identifier |
| `MailboxCount` | int | Total number of mailboxes in the network |
| `ActiveMailboxCount` | int | Number of mailboxes with Active status |
| `InterchangeInCount` | int | Total inbound interchanges in the reporting period |
| `InterchangeOutCount` | int | Total outbound interchanges in the reporting period |
| `PendingParcelCount` | int | Number of parcels awaiting download |
| `LastActivity` | dateTime | UTC timestamp of the most recent interchange activity |

```xml
<!-- Example response XML (DataSet table structure) -->
<DataSet>
  <xs:schema><!-- schema omitted for brevity --></xs:schema>
  <diffgr:diffgram>
    <NetworkSummary>
      <NetworkID>42</NetworkID>
      <MailboxCount>15</MailboxCount>
      <ActiveMailboxCount>14</ActiveMailboxCount>
      <InterchangeInCount>342</InterchangeInCount>
      <InterchangeOutCount>287</InterchangeOutCount>
      <PendingParcelCount>3</PendingParcelCount>
      <LastActivity>2026-05-07T13:45:00</LastActivity>
    </NetworkSummary>
  </diffgr:diffgram>
</DataSet>
```

:::note DataSet Deserialization
The `DataSet` return type requires .NET's built-in XML deserialization. When using the `dotnet-svcutil` generated proxy, the result is strongly typed; if using manual `HttpClient` + raw SOAP, parse the diffgram XML directly.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve network status summary for dashboard display
var summary = await client.NetworkStatusSummaryAsync(sessionID, networkId);

// Access the first table in the dataset
if (summary.Tables.Count > 0)
{
    var row = summary.Tables[0].Rows[0];
    Console.WriteLine($"Mailboxes:         {row["MailboxCount"]}");
    Console.WriteLine($"Active Mailboxes:  {row["ActiveMailboxCount"]}");
    Console.WriteLine($"Inbound Today:     {row["InterchangeInCount"]}");
    Console.WriteLine($"Outbound Today:    {row["InterchangeOutCount"]}");
    Console.WriteLine($"Pending Parcels:   {row["PendingParcelCount"]}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.NetworkStatusSummary(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.NetworkStatusSummaryAsync({
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

result = client.service.NetworkStatusSummary(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Mailbox Stats](../../rest-api/reports/mailbox-stats.md) — `POST /v2/reports/mailbox-stats` provides a partial equivalent for per-mailbox statistics. For full network-level summaries, combine with [Instant Stats](../../rest-api/reports/instant-stats.md).
