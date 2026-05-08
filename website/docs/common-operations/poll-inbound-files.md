---
title: Poll for Inbound Files
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create poll-inbound-files common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Poll for Inbound Files

Periodically check your ECGrid mailbox for EDI files that are ready to download. This is the first step of every inbound EDI integration loop.

## Overview

ECGrid queues inbound EDI parcels in your mailbox as they arrive. Your integration polls the inbox list endpoint on a schedule, retrieves the list of parcels in `InBoxReady` status, then downloads and confirms each one. In production, the poll loop typically runs as a `BackgroundService` (Worker Service) or a scheduled job on a 1–15 minute interval.

Sequence:
1. Call the inbox list endpoint with your mailbox credentials and a page size.
2. Receive a list of parcel summary records.
3. For each record — download, process, and confirm.

---

## REST

**Endpoint:** `POST /v2/parcels/pending-inbox-list`

**Auth:** `X-API-Key: <key>` header

### Step 1 — Request the inbox list

```http
POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "mailboxId": 0,
  "pageNo": 1,
  "recordsPerPage": 25
}
```

| Field | Type | Description |
|---|---|---|
| `mailboxId` | integer | Your mailbox ID. Pass `0` to use the default mailbox for the API key. |
| `pageNo` | integer | 1-based page number for pagination. |
| `recordsPerPage` | integer | Maximum records per page. Typical values: 25–100. |

### Step 2 — Inspect the response

```json
{
  "success": true,
  "data": [
    {
      "parcelId": 98765,
      "fileName": "850_order.edi",
      "fromECGridId": 123456,
      "toECGridId": 789012,
      "status": "InBoxReady",
      "receivedDate": "2026-05-07T14:32:00Z",
      "size": 4096
    }
  ],
  "totalRecords": 3,
  "pageNo": 1,
  "recordsPerPage": 25
}
```

Iterate over `data`. For each parcel, proceed to [Download a File](./download-a-file) and then [Confirm Download](./confirm-download).

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -s -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"mailboxId":0,"pageNo":1,"recordsPerPage":25}' | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — poll inbox using IHttpClientFactory (register in DI as "ECGrid")
// Load API key from IConfiguration, not hardcoded

using System.Net.Http.Json;
using System.Text.Json.Serialization;

public record PendingInboxListRequest(
    int MailboxId,
    int PageNo,
    int RecordsPerPage);

public record ParcelSummary(
    long ParcelId,
    string FileName,
    int FromECGridId,
    int ToECGridId,
    string Status,
    DateTimeOffset ReceivedDate,
    long Size);

public record InboxListResponse(
    bool Success,
    List<ParcelSummary> Data,
    int TotalRecords,
    int PageNo,
    int RecordsPerPage);

public class ECGridInboxPoller
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridInboxPoller> _logger;

    public ECGridInboxPoller(IHttpClientFactory httpClientFactory, ILogger<ECGridInboxPoller> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Retrieves all InBoxReady parcels, paging through results until the list is exhausted.
    /// </summary>
    public async Task<List<ParcelSummary>> GetAllReadyParcelsAsync(
        int mailboxId,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");
        var allParcels = new List<ParcelSummary>();
        int pageNo = 1;
        const int pageSize = 25;

        while (true)
        {
            var request = new PendingInboxListRequest(mailboxId, pageNo, pageSize);
            var response = await http.PostAsJsonAsync(
                "/v2/parcels/pending-inbox-list", request, cancellationToken);

            response.EnsureSuccessStatusCode();

            var result = await response.Content
                .ReadFromJsonAsync<InboxListResponse>(cancellationToken: cancellationToken);

            if (result is null || result.Data.Count == 0)
                break;

            allParcels.AddRange(result.Data);
            _logger.LogInformation(
                "Fetched page {Page}: {Count} parcel(s)", pageNo, result.Data.Count);

            // Stop paging when we have received fewer records than the page size
            if (result.Data.Count < pageSize)
                break;

            pageNo++;
        }

        _logger.LogInformation("Total parcels ready: {Total}", allParcels.Count);
        return allParcels;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — poll inbox for ready parcels
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var client = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String body = "{\"mailboxId\":0,\"pageNo\":1,\"recordsPerPage\":25}";

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/pending-inbox-list"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = client.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // parse JSON to get parcel list
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — poll inbox for ready parcels
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/pending-inbox-list', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
});

const result = await response.json();
for (const parcel of result.data ?? []) {
  console.log(`ParcelID: ${parcel.parcelId} — ${parcel.fileName}`);
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

resp = session.post(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25}
)
resp.raise_for_status()

for parcel in resp.json().get("data", []):
    print(f"ParcelID: {parcel['parcelId']} — {parcel['fileName']}")
```

</TabItem>
</Tabs>

**Registration in `Program.cs`:**

```csharp
// Register named HTTP client with base address and auth header
builder.Services.AddHttpClient("ECGrid", client =>
{
    client.BaseAddress = new Uri("https://rest.ecgrid.io");
    client.DefaultRequestHeaders.Add(
        "X-API-Key",
        builder.Configuration["ECGrid:ApiKey"]);
});

builder.Services.AddScoped<ECGridInboxPoller>();
```

:::tip Production Polling Pattern
In production, run the polling loop inside an `IHostedService` / `BackgroundService` with a configurable interval. Use `PeriodicTimer` (.NET 6+) rather than `Task.Delay` to avoid drift.

```csharp
// Inside ExecuteAsync() of your BackgroundService
using var timer = new PeriodicTimer(TimeSpan.FromMinutes(5));
while (await timer.WaitForNextTickAsync(stoppingToken))
{
    var parcels = await _poller.GetAllReadyParcelsAsync(mailboxId, stoppingToken);
    foreach (var parcel in parcels)
        await ProcessParcelAsync(parcel, stoppingToken);
}
```
:::

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Method:** `ParcelInBox(SessionID, NetworkID, MailboxID, ECGridIDFrom, ECGridIDTo, Status, BeginDate, EndDate, PageNo, RecordsPerPage)`

### Step 1 — Log in and get a session ID

```csharp
var session = await client.LoginAsync("username", "password");
string sessionId = session.LoginResult;
```

### Step 2 — Call ParcelInBox

```csharp
var result = await client.ParcelInBoxAsync(
    sessionId,
    networkId:       0,          // 0 = default for session
    mailboxId:       0,          // 0 = default for session
    ecgridIdFrom:    0,          // 0 = any sender
    ecgridIdTo:      0,          // 0 = any recipient
    status:          ParcelStatus.InBoxReady,
    beginDate:       DateTime.MinValue,
    endDate:         DateTime.MaxValue,
    pageNo:          1,
    recordsPerPage:  25);

foreach (var parcel in result.ParcelInBoxResult ?? [])
{
    Console.WriteLine($"ParcelID={parcel.ParcelID}  File={parcel.FileName}  Size={parcel.Size}");
}
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Reference: https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

using ECGridOS; // namespace from generated proxy

var binding  = new BasicHttpBinding(BasicHttpSecurityMode.Transport);
var endpoint = new EndpointAddress("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx");
var client   = new ECGridOSAPIClient(binding, endpoint);

string sessionId = string.Empty;

try
{
    // Obtain session — store and reuse; do not call Login() on every poll
    var loginResult = await client.LoginAsync(
        Environment.GetEnvironmentVariable("ECGRID_USER")!,
        Environment.GetEnvironmentVariable("ECGRID_PASS")!);
    sessionId = loginResult.LoginResult;

    int pageNo   = 1;
    const int pageSize = 25;

    while (true)
    {
        var inbox = await client.ParcelInBoxAsync(
            sessionId,
            networkId:       0,
            mailboxId:       0,
            ecgridIdFrom:    0,
            ecgridIdTo:      0,
            status:          ParcelStatus.InBoxReady,
            beginDate:       DateTime.MinValue,
            endDate:         DateTime.MaxValue,
            pageNo:          pageNo,
            recordsPerPage:  pageSize);

        var parcels = inbox.ParcelInBoxResult;
        if (parcels is null || parcels.Length == 0)
            break;

        foreach (var p in parcels)
            Console.WriteLine($"Ready: ParcelID={p.ParcelID}  File={p.FileName}");

        if (parcels.Length < pageSize)
            break;

        pageNo++;
    }
}
finally
{
    // Always log out to release the session slot
    if (!string.IsNullOrEmpty(sessionId))
        await client.LogoutAsync(sessionId);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP ParcelInBox via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID"; // obtain from Login

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:ParcelInBox>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>"
    + "<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>"
    + "<ecg:Status>InBoxReady</ecg:Status>"
    + "<ecg:BeginDate>0001-01-01T00:00:00</ecg:BeginDate>"
    + "<ecg:EndDate>9999-12-31T00:00:00</ecg:EndDate>"
    + "<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>25</ecg:RecordsPerPage>"
    + "</ecg:ParcelInBox></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/ParcelInBox\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, BodyHandlers.ofString());
System.out.println(response.body()); // parse ParcelIDInfo elements from XML
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP ParcelInBox via raw HTTP
const sessionId = 'YOUR_SESSION_ID'; // obtain from Login

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:ParcelInBox>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>
    <ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>
    <ecg:Status>InBoxReady</ecg:Status>
    <ecg:BeginDate>0001-01-01T00:00:00</ecg:BeginDate>
    <ecg:EndDate>9999-12-31T00:00:00</ecg:EndDate>
    <ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>25</ecg:RecordsPerPage>
  </ecg:ParcelInBox></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://www.ecgridos.net/ParcelInBox"'
  },
  body: envelope
});
const xml = await response.text();
console.log(xml); // parse ParcelIDInfo elements from XML
```

</TabItem>
<TabItem value="python" label="Python">

```python
import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:ParcelInBox>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>'
    '<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>'
    '<ecg:Status>InBoxReady</ecg:Status>'
    '<ecg:BeginDate>0001-01-01T00:00:00</ecg:BeginDate>'
    '<ecg:EndDate>9999-12-31T00:00:00</ecg:EndDate>'
    '<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>25</ecg:RecordsPerPage>'
    '</ecg:ParcelInBox></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/ParcelInBox"'}
)
resp.raise_for_status()
print(resp.text)  # parse ParcelIDInfo elements from XML
```

</TabItem>
</Tabs>

:::tip Reuse the Session
The SOAP `SessionID` is valid for the duration of a session. Do not call `Login()` on every poll iteration — obtain the session once at startup and renew it only when it expires.
:::

---

## Related

- [Download a File](./download-a-file)
- [Confirm a Download](./confirm-download)
- [REST — Parcels: Pending Inbox List](../rest-api/parcels/pending-inbox-list)
- [SOAP — ParcelInBox](../soap-api/parcels/parcel-inbox)
