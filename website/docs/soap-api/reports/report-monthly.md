---
title: ReportMonthly
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Reports - ReportMonthly documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ReportMonthly

Returns a monthly activity report for a specified report type and month.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/reports/monthly-report.md).
:::

## Method Signature

```
DataSet ReportMonthly(string SessionID, short Report, DateTime Month)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |
| `Report` | short | Yes | Report type identifier specifying which monthly report to generate |
| `Month` | datetime | Yes | The target month; only the year and month components are used — the day and time values are ignored |

## Response Object — DataSet

Returns an ADO.NET `DataSet` with rows representing the monthly report data for the requested report type. The exact columns returned depend on the `Report` type identifier supplied.

| Column | Type | Description |
|---|---|---|
| `ReportDate` | datetime | First day of the reported month |
| `MailboxID` | int | Mailbox the data applies to |
| `MailboxName` | string | Display name of the mailbox |
| `ParcelsIn` | int | Inbound parcels for the month |
| `ParcelsOut` | int | Outbound parcels for the month |
| `InterchangesIn` | int | Inbound interchanges for the month |
| `InterchangesOut` | int | Outbound interchanges for the month |
| `BytesIn` | long | Total bytes received during the month |
| `BytesOut` | long | Total bytes sent during the month |

```xml
<!-- Example response XML -->
<DataSet>
  <Table>
    <ReportDate>2026-05-01T00:00:00</ReportDate>
    <MailboxID>10001</MailboxID>
    <MailboxName>Acme Corp Production</MailboxName>
    <ParcelsIn>820</ParcelsIn>
    <ParcelsOut>541</ParcelsOut>
    <InterchangesIn>4820</InterchangesIn>
    <InterchangesOut>3105</InterchangesOut>
    <BytesIn>52428800</BytesIn>
    <BytesOut>26214400</BytesOut>
  </Table>
</DataSet>
```

:::note Month Parameter
Only the year and month portions of the `Month` datetime are evaluated. Pass any day value (e.g., the first of the month) to avoid ambiguity.
:::

:::note DataSet Access Pattern
The SOAP `DataSet` return type is an ADO.NET dataset. Iterate `Tables[0].Rows` to access each row in the monthly report.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Get monthly report type 1 for May 2026
// Only the year and month of the datetime are used — pass the first of the month for clarity
var targetMonth = new DateTime(2026, 5, 1);

var result = await client.ReportMonthlyAsync(sessionID, report: 1, targetMonth);

// DataSet returned — iterate rows for monthly summary data
var table = result.Tables[0];
foreach (DataRow row in table.Rows)
{
    Console.WriteLine($"Report Month: {row["ReportDate"]:yyyy-MM}");
    Console.WriteLine($"  Mailbox:              {row["MailboxName"]} (ID: {row["MailboxID"]})");
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

var result = port.ReportMonthly(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ReportMonthlyAsync({
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

result = client.service.ReportMonthly(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Monthly Report](../../rest-api/reports/monthly-report.md) — `POST /v2/reports/monthly`.
