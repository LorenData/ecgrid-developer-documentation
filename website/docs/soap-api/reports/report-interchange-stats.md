---
title: ReportInterchangeStats
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Reports - ReportInterchangeStats documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ReportInterchangeStats

Returns interchange volume statistics for a specified date range and direction.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/reports/interchange-stats.md).
:::

## Method Signature

```
DataSet ReportInterchangeStats(string SessionID, DateTime StartTime, DateTime EndTime, Direction Direction)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `StartTime` | datetime | Yes | Start of the reporting period (inclusive) |
| `EndTime` | datetime | Yes | End of the reporting period (inclusive) |
| `Direction` | Direction | Yes | Filter by inbound, outbound, or both |

## Response Object — DataSet

Returns an ADO.NET `DataSet` with interchange volume rows for the requested period. Access results via `DataTable` rows.

| Column | Type | Description |
|---|---|---|
| `InterchangeDate` | datetime | Date of the interchange activity |
| `Direction` | string | Direction of interchange flow (InBox / OutBox) |
| `Count` | int | Number of interchanges for this date and direction |
| `ISAs` | int | Number of ISA envelopes processed |
| `GSSTs` | int | Number of GS/ST groups/transactions processed |

```xml
<!-- Example response XML -->
<DataSet>
  <Table>
    <InterchangeDate>2026-05-01T00:00:00</InterchangeDate>
    <Direction>InBox</Direction>
    <Count>142</Count>
    <ISAs>142</ISAs>
    <GSSTs>874</GSSTs>
  </Table>
  <Table>
    <InterchangeDate>2026-05-01T00:00:00</InterchangeDate>
    <Direction>OutBox</Direction>
    <Count>98</Count>
    <ISAs>98</ISAs>
    <GSSTs>521</GSSTs>
  </Table>
</DataSet>
```

:::note DataSet Access Pattern
The SOAP `DataSet` return type is an ADO.NET dataset. Iterate `Tables[0].Rows` to access each data row.
:::

## ENUMs

### Direction

| Value | Description |
|---|---|
| `NoDir` | No direction filter — returns both inbound and outbound |
| `OutBox` | Outbound interchanges only |
| `InBox` | Inbound interchanges only |

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Get interchange statistics for a specific date range
var startTime = new DateTime(2026, 5, 1, 0, 0, 0);
var endTime   = new DateTime(2026, 5, 7, 23, 59, 59);

var result = await client.ReportInterchangeStatsAsync(
    sessionID,
    startTime,
    endTime,
    Direction.NoDir);

// DataSet returned — iterate rows for each date/direction combination
var table = result.Tables[0];
foreach (DataRow row in table.Rows)
{
    Console.WriteLine(
        $"{row["InterchangeDate"]:yyyy-MM-dd} | {row["Direction"],6} | " +
        $"Count: {row["Count"],5} | ISAs: {row["ISAs"],5} | GSSTs: {row["GSSTs"],6}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ReportInterchangeStats(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ReportInterchangeStatsAsync({
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

result = client.service.ReportInterchangeStats(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Interchange Stats](../../rest-api/reports/interchange-stats.md) — `POST /v2/reports/interchange-stats`.
