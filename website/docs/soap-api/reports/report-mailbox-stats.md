---
title: ReportMailboxStats
sidebar_position: 3
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP API Reports - ReportMailboxStats documentation page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# ReportMailboxStats

Returns an overall mailbox activity summary including parcel and interchange totals.

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use the [REST equivalent](../../rest-api/reports/mailbox-stats.md).
:::

## Method Signature

```
DataSet ReportMailboxStats(string SessionID)
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SessionID` | string | Yes | Active session token from Login() |

## Response Object — DataSet

Returns an ADO.NET `DataSet` summarizing mailbox-level activity. Access results via `DataTable` rows.

| Column | Type | Description |
|---|---|---|
| `MailboxID` | int | Unique identifier of the mailbox |
| `MailboxName` | string | Display name of the mailbox |
| `ParcelsIn` | int | Total inbound parcels received |
| `ParcelsOut` | int | Total outbound parcels sent |
| `InterchangesIn` | int | Total inbound interchanges received |
| `InterchangesOut` | int | Total outbound interchanges sent |
| `LastActivity` | datetime | Timestamp of the most recent activity |

```xml
<!-- Example response XML -->
<DataSet>
  <Table>
    <MailboxID>10001</MailboxID>
    <MailboxName>Acme Corp Production</MailboxName>
    <ParcelsIn>1482</ParcelsIn>
    <ParcelsOut>976</ParcelsOut>
    <InterchangesIn>8640</InterchangesIn>
    <InterchangesOut>5210</InterchangesOut>
    <LastActivity>2026-05-07T09:14:00</LastActivity>
  </Table>
</DataSet>
```

:::note DataSet Access Pattern
The SOAP `DataSet` return type is an ADO.NET dataset. Iterate `Tables[0].Rows` to access each mailbox summary row.
:::

## Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Retrieve the mailbox activity summary for the authenticated session's scope
var result = await client.ReportMailboxStatsAsync(sessionID);

// DataSet returned — iterate rows for each mailbox
var table = result.Tables[0];
foreach (DataRow row in table.Rows)
{
    Console.WriteLine($"Mailbox: {row["MailboxName"]} (ID: {row["MailboxID"]})");
    Console.WriteLine($"  Parcels In/Out:       {row["ParcelsIn"]} / {row["ParcelsOut"]}");
    Console.WriteLine($"  Interchanges In/Out:  {row["InterchangesIn"]} / {row["InterchangesOut"]}");
    Console.WriteLine($"  Last Activity:        {row["LastActivity"]:yyyy-MM-dd HH:mm}");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// JAX-WS generated client
// wsimport -s src https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

ECGridOS service = new ECGridOS();
ECGridOSPortType port = service.getECGridOSPort();

var result = port.ReportMailboxStats(sessionID /*, additional params */);
System.out.println(result);
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// npm install soap
import soap from 'soap';

const WSDL = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL';
const client = await soap.createClientAsync(WSDL);

const [result] = await client.ReportMailboxStatsAsync({
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

result = client.service.ReportMailboxStats(
    SessionID=session_id,
    # additional params
)
print(result)
```

</TabItem>
</Tabs>

## REST Equivalent

See [Mailbox Stats](../../rest-api/reports/mailbox-stats.md) — `GET /v2/reports/mailbox-stats`.
