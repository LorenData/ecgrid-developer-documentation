---
title: ReportTrafficStats
sidebar_position: 4
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Reports - ReportTrafficStats documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ReportTrafficStats

Returns traffic volume statistics across a specified number of time periods ending at a target date and time.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/reports/traffic-stats.md).
:::

## Method Signature

```
DataSet ReportTrafficStats(string SessionID, DateTime TargetTime, short NumPeriods, StatisticsPeriod Period)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `TargetTime` | datetime | Yes | End point of the reporting range; the report works backwards from this time |
| `NumPeriods` | short | Yes | Number of time periods to include in the report (e.g., 7 for seven days) |
| `Period` | StatisticsPeriod | Yes | Granularity of each period: Hour, Day, Week, or Month |

## Response Object — DataSet

Returns an ADO.NET `DataSet` with one row per time period. Access results via `DataTable` rows.

| Column | Type | Description |
|---|---|---|
| `PeriodStart` | datetime | Start of this time period |
| `PeriodEnd` | datetime | End of this time period |
| `ParcelsIn` | int | Inbound parcels received in this period |
| `ParcelsOut` | int | Outbound parcels sent in this period |
| `InterchangesIn` | int | Inbound interchanges in this period |
| `InterchangesOut` | int | Outbound interchanges in this period |
| `BytesIn` | long | Total bytes received in this period |
| `BytesOut` | long | Total bytes sent in this period |

```xml
<!-- Example response XML -->
<DataSet>
  <Table>
    <PeriodStart>2026-05-06T00:00:00</PeriodStart>
    <PeriodEnd>2026-05-06T23:59:59</PeriodEnd>
    <ParcelsIn>38</ParcelsIn>
    <ParcelsOut>22</ParcelsOut>
    <InterchangesIn>210</InterchangesIn>
    <InterchangesOut>145</InterchangesOut>
    <BytesIn>1048576</BytesIn>
    <BytesOut>524288</BytesOut>
  </Table>
  <Table>
    <PeriodStart>2026-05-07T00:00:00</PeriodStart>
    <PeriodEnd>2026-05-07T23:59:59</PeriodEnd>
    <ParcelsIn>21</ParcelsIn>
    <ParcelsOut>14</ParcelsOut>
    <InterchangesIn>118</InterchangesIn>
    <InterchangesOut>87</InterchangesOut>
    <BytesIn>614400</BytesIn>
    <BytesOut>307200</BytesOut>
  </Table>
</DataSet>
```

:::note DataSet Access Pattern
The SOAP `DataSet` return type is an ADO.NET dataset. Iterate `Tables[0].Rows` to access each period row; rows are ordered from oldest to newest period.
:::

## ENUMs

### StatisticsPeriod

| Value | Description |
|---|---|
| `Hour` | Each period represents one hour |
| `Day` | Each period represents one calendar day |
| `Week` | Each period represents one week |
| `Month` | Each period represents one calendar month |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Get daily traffic stats for the last 7 days ending now
var targetTime = DateTime.UtcNow;

var result = await client.ReportTrafficStatsAsync(
    sessionID,
    targetTime,
    numPeriods: 7,
    StatisticsPeriod.Day);

// DataSet returned — iterate rows oldest to newest
var table = result.Tables[0];
foreach (DataRow row in table.Rows)
{
    Console.WriteLine($"Period: {row["PeriodStart"]:yyyy-MM-dd}");
    Console.WriteLine($"  Parcels In/Out:       {row["ParcelsIn"]} / {row["ParcelsOut"]}");
    Console.WriteLine($"  Interchanges In/Out:  {row["InterchangesIn"]} / {row["InterchangesOut"]}");
    Console.WriteLine($"  Bytes In/Out:         {row["BytesIn"]:N0} / {row["BytesOut"]:N0}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ReportTrafficStats(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ReportTrafficStatsAsync({
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

result = client.service.ReportTrafficStats(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Traffic Stats](../../rest-api/reports/traffic-stats.md) — `POST /v2/reports/traffic-stats`.
