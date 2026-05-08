---
title: ReportInstantStats
sidebar_position: 1
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Reports - ReportInstantStats documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ReportInstantStats

Returns parcel and interchange counts for two configurable trailing time windows, providing a real-time activity snapshot.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/reports/instant-stats.md).
:::

## Method Signature

```
DataSet ReportInstantStats(string SessionID, short Minutes1, short Minutes2)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `Minutes1` | short | Yes | First time window in minutes (e.g., 15 for the last 15 minutes) |
| `Minutes2` | short | Yes | Second time window in minutes (e.g., 60 for the last hour) |

## Response Object — DataSet

Returns an ADO.NET `DataSet` containing activity counts across both time windows. Access results via `DataTable` rows.

| Column | Type | Description |
|---|---|---|
| `ParcelsIn1` | int | Inbound parcels received within Minutes1 |
| `ParcelsOut1` | int | Outbound parcels sent within Minutes1 |
| `InterchangesIn1` | int | Inbound interchanges within Minutes1 |
| `InterchangesOut1` | int | Outbound interchanges within Minutes1 |
| `ParcelsIn2` | int | Inbound parcels received within Minutes2 |
| `ParcelsOut2` | int | Outbound parcels sent within Minutes2 |
| `InterchangesIn2` | int | Inbound interchanges within Minutes2 |
| `InterchangesOut2` | int | Outbound interchanges within Minutes2 |

```xml
<!-- Example response XML -->
<DataSet>
  <Table>
    <ParcelsIn1>4</ParcelsIn1>
    <ParcelsOut1>2</ParcelsOut1>
    <InterchangesIn1>12</InterchangesIn1>
    <InterchangesOut1>8</InterchangesOut1>
    <ParcelsIn2>18</ParcelsIn2>
    <ParcelsOut2>9</ParcelsOut2>
    <InterchangesIn2>47</InterchangesIn2>
    <InterchangesOut2>31</InterchangesOut2>
  </Table>
</DataSet>
```

:::note DataSet Access Pattern
The SOAP `DataSet` return type is an ADO.NET dataset. Access the first `DataTable` in `Tables[0]` and read column values from `Rows[0]`.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Get activity counts for the last 15 and 60 minutes
var result = await client.ReportInstantStatsAsync(sessionID, minutes1: 15, minutes2: 60);

// DataSet returned — access via the first DataTable
var table = result.Tables[0];
if (table.Rows.Count > 0)
{
    var row = table.Rows[0];
    Console.WriteLine("=== Last 15 minutes ===");
    Console.WriteLine($"  Parcels In:       {row["ParcelsIn1"]}");
    Console.WriteLine($"  Parcels Out:      {row["ParcelsOut1"]}");
    Console.WriteLine($"  Interchanges In:  {row["InterchangesIn1"]}");
    Console.WriteLine($"  Interchanges Out: {row["InterchangesOut1"]}");

    Console.WriteLine("=== Last 60 minutes ===");
    Console.WriteLine($"  Parcels In:       {row["ParcelsIn2"]}");
    Console.WriteLine($"  Parcels Out:      {row["ParcelsOut2"]}");
    Console.WriteLine($"  Interchanges In:  {row["InterchangesIn2"]}");
    Console.WriteLine($"  Interchanges Out: {row["InterchangesOut2"]}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ReportInstantStats(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ReportInstantStatsAsync({
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

result = client.service.ReportInstantStats(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Instant Stats](../../rest-api/reports/instant-stats.md) — `POST /v2/reports/instant-stats`.
