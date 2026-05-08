---
title: Work with Carbon Copies
sidebar_position: 12
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create work-with-carbon-copies common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Work with Carbon Copies

Automatically duplicate EDI traffic to a secondary mailbox for compliance archiving, secondary processing, or IT-team visibility without modifying the primary EDI flow.

## Overview

A carbon copy rule tells ECGrid to deliver a copy of every parcel that matches a defined scope (by ECGrid ID, direction, or document type) to an additional mailbox. The original delivery path is unaffected — the copy is made transparently in the routing layer. Common use cases include:

- **Compliance archiving:** Route a copy of all inbound and outbound EDI to a dedicated archive mailbox.
- **Secondary processing:** Send a copy of inbound 850 Purchase Orders to a separate fulfillment system.
- **IT visibility:** Give a monitoring team read access to EDI traffic without granting access to the production mailbox.

Sequence:
1. Create the carbon copy rule with `POST /v2/carboncopies/create`.
2. Verify the rule with `GET /v2/carboncopies/{id}`.
3. List all active rules with `POST /v2/carboncopies/list`.

---

## REST

**Auth:** `X-API-Key: <key>` header

### Step 1 — Create a carbon copy rule

```http
POST https://rest.ecgrid.io/v2/carboncopies/create
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "networkId": 0,
  "mailboxId": 54321,
  "ecGridIdFrom": 0,
  "ecGridIdTo": 0,
  "copyToMailboxId": 99001,
  "direction": "InBox",
  "status": "Active"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `networkId` | integer | No | Network scope. Pass `0` for the API key's default network. |
| `mailboxId` | integer | Yes | Source mailbox — parcels flowing through this mailbox will be copied. |
| `ecGridIdFrom` | integer | No | Filter by sender ECGrid ID. Pass `0` to copy from any sender. |
| `ecGridIdTo` | integer | No | Filter by recipient ECGrid ID. Pass `0` to copy to any recipient. |
| `copyToMailboxId` | integer | Yes | Destination mailbox that receives the copy. |
| `direction` | string | No | `"InBox"`, `"OutBox"`, or `"NoDir"` (both directions). Default: `"NoDir"`. |
| `status` | string | No | `"Active"` to enable immediately. Default: `"Active"`. |

**Response:**

```json
{
  "success": true,
  "data": {
    "carbonCopyId": 5500,
    "mailboxId": 54321,
    "copyToMailboxId": 99001,
    "direction": "InBox",
    "status": "Active",
    "createdDate": "2026-05-07T12:00:00Z"
  }
}
```

### Step 2 — Verify the rule

```http
GET https://rest.ecgrid.io/v2/carboncopies/5500
X-API-Key: YOUR_API_KEY
```

Confirm the rule shows `status: "Active"` and the correct source and destination mailbox IDs.

### Step 3 — List all active rules

```http
POST https://rest.ecgrid.io/v2/carboncopies/list
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "networkId": 0,
  "mailboxId": 54321,
  "pageNo": 1,
  "recordsPerPage": 25
}
```

Pass `mailboxId: 0` to list all carbon copy rules across the network.

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "carbonCopyId": 5500,
      "mailboxId": 54321,
      "copyToMailboxId": 99001,
      "direction": "InBox",
      "status": "Active"
    }
  ],
  "totalRecords": 1
}
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -s -X POST https://rest.ecgrid.io/v2/carboncopies/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":54321,"ecGridIdFrom":0,"ecGridIdTo":0,"copyToMailboxId":99001,"direction":"InBox","status":"Active"}' | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — create, verify, and list carbon copy rules using IHttpClientFactory (registered as "ECGrid")
// API key loaded from IConfiguration — never hardcoded

using System.Net.Http.Json;

public record CreateCarbonCopyRequest(
    int NetworkId,
    int MailboxId,
    int ECGridIdFrom,
    int ECGridIdTo,
    int CopyToMailboxId,
    string Direction,
    string Status);

public record CarbonCopyInfo(
    int CarbonCopyId,
    int MailboxId,
    int CopyToMailboxId,
    string Direction,
    string Status,
    DateTimeOffset CreatedDate);

public record ListCarbonCopiesRequest(
    int NetworkId,
    int MailboxId,
    int PageNo,
    int RecordsPerPage);

public record ListResponse<T>(bool Success, List<T> Data, int TotalRecords);
public record ApiResponse<T>(bool Success, T Data);

public class ECGridCarbonCopyService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridCarbonCopyService> _logger;

    public ECGridCarbonCopyService(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridCarbonCopyService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger            = logger;
    }

    /// <summary>
    /// Creates a carbon copy rule that duplicates EDI parcels to a secondary mailbox.
    /// </summary>
    /// <param name="sourceMailboxId">Mailbox whose traffic will be copied.</param>
    /// <param name="destinationMailboxId">Mailbox that receives the copied parcels.</param>
    /// <param name="direction">"InBox", "OutBox", or "NoDir" for both directions.</param>
    public async Task<CarbonCopyInfo> CreateCarbonCopyAsync(
        int sourceMailboxId,
        int destinationMailboxId,
        string direction = "NoDir",
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        var request = new CreateCarbonCopyRequest(
            NetworkId:       0,
            MailboxId:       sourceMailboxId,
            ECGridIdFrom:    0,
            ECGridIdTo:      0,
            CopyToMailboxId: destinationMailboxId,
            Direction:       direction,
            Status:          "Active");

        var response = await http.PostAsJsonAsync(
            "/v2/carboncopies/create", request, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<CarbonCopyInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from carbon copy create.");

        _logger.LogInformation(
            "Carbon copy created: ID={Id} Source={Source} Destination={Dest} Direction={Dir}",
            result.Data.CarbonCopyId,
            result.Data.MailboxId,
            result.Data.CopyToMailboxId,
            result.Data.Direction);

        return result.Data;
    }

    /// <summary>
    /// Lists all carbon copy rules for a mailbox, paging through all results.
    /// </summary>
    /// <param name="mailboxId">Source mailbox ID. Pass 0 for all mailboxes in the network.</param>
    public async Task<List<CarbonCopyInfo>> ListCarbonCopiesAsync(
        int mailboxId = 0,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");
        var all = new List<CarbonCopyInfo>();
        int pageNo = 1;
        const int pageSize = 25;

        while (true)
        {
            var request = new ListCarbonCopiesRequest(
                NetworkId:       0,
                MailboxId:       mailboxId,
                PageNo:          pageNo,
                RecordsPerPage:  pageSize);

            var response = await http.PostAsJsonAsync(
                "/v2/carboncopies/list", request, cancellationToken);
            response.EnsureSuccessStatusCode();

            var result = await response.Content
                .ReadFromJsonAsync<ListResponse<CarbonCopyInfo>>(cancellationToken: cancellationToken);

            if (result is null || result.Data.Count == 0)
                break;

            all.AddRange(result.Data);

            if (result.Data.Count < pageSize)
                break;

            pageNo++;
        }

        _logger.LogInformation("Total carbon copy rules: {Count}", all.Count);
        return all;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — create a carbon copy rule
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String body = "{\"networkId\":0,\"mailboxId\":54321,\"ecGridIdFrom\":0,\"ecGridIdTo\":0,"
    + "\"copyToMailboxId\":99001,\"direction\":\"InBox\",\"status\":\"Active\"}";

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/carboncopies/create"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // carbonCopyId
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — create a carbon copy rule
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/carboncopies/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({
    networkId: 0, mailboxId: 54321,
    ecGridIdFrom: 0, ecGridIdTo: 0,
    copyToMailboxId: 99001, direction: 'InBox', status: 'Active'
  })
});

const { data } = await response.json();
console.log(`Carbon copy created: ID=${data.carbonCopyId}`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]

resp = requests.post(
    "https://rest.ecgrid.io/v2/carboncopies/create",
    headers={"X-API-Key": api_key},
    json={
        "networkId": 0, "mailboxId": 54321,
        "ecGridIdFrom": 0, "ecGridIdTo": 0,
        "copyToMailboxId": 99001, "direction": "InBox", "status": "Active"
    }
)
resp.raise_for_status()
print(f"Carbon copy created: ID={resp.json()['data']['carbonCopyId']}")
```

</TabItem>
</Tabs>

**Registration in `Program.cs`:**

```csharp
builder.Services.AddHttpClient("ECGrid", client =>
{
    client.BaseAddress = new Uri("https://rest.ecgrid.io");
    client.DefaultRequestHeaders.Add(
        "X-API-Key",
        builder.Configuration["ECGrid:ApiKey"]);
});

builder.Services.AddScoped<ECGridCarbonCopyService>();
```

:::tip Archiving Pattern
For a compliance archive, create two carbon copy rules on each production mailbox — one for `"InBox"` and one for `"OutBox"` — both pointing to a dedicated archive mailbox. Set the archive mailbox to never delete on download so every parcel is retained.
:::

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Methods:**
- `CarbonCopyAdd(SessionID, NetworkID, MailboxID, ECGridIDFrom, ECGridIDTo, CopyToMailboxID, ...)` — create the rule
- `CarbonCopyInfo(SessionID, CarbonCopyID)` — verify the rule
- `CarbonCopyList(SessionID, NetworkID, MailboxID, ...)` — list all rules

### Step 1 — Log in and get a session ID

```csharp
var loginResult = await client.LoginAsync(username, password);
string sessionId = loginResult.LoginResult;
```

### Step 2 — Create the rule with CarbonCopyAdd

```csharp
var result = await client.CarbonCopyAddAsync(
    sessionId,
    networkId:       0,
    mailboxId:       54321,
    ecgridIdFrom:    0,
    ecgridIdTo:      0,
    copyToMailboxId: 99001,
    direction:       ECGridDirection.NoDir);

int carbonCopyId = result.CarbonCopyAddResult;
Console.WriteLine($"Carbon copy created: ID={carbonCopyId}");
```

### Step 3 — Verify with CarbonCopyInfo

```csharp
var info = await client.CarbonCopyInfoAsync(sessionId, carbonCopyId);
Console.WriteLine($"Status: {info.CarbonCopyInfoResult.Status}");
Console.WriteLine($"Source:      {info.CarbonCopyInfoResult.MailboxID}");
Console.WriteLine($"Destination: {info.CarbonCopyInfoResult.CopyToMailboxID}");
```

### Step 4 — List rules with CarbonCopyList

```csharp
var list = await client.CarbonCopyListAsync(
    sessionId,
    networkId:      0,
    mailboxId:      54321,
    pageNo:         1,
    recordsPerPage: 25);

foreach (var cc in list.CarbonCopyListResult ?? [])
    Console.WriteLine($"  ID={cc.CarbonCopyID}  Dir={cc.Direction}  Dest={cc.CopyToMailboxID}");
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy
// Reference: https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx?WSDL

using ECGridOS;

var binding  = new BasicHttpBinding(BasicHttpSecurityMode.Transport);
var endpoint = new EndpointAddress("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx");
var client   = new ECGridOSAPIClient(binding, endpoint);

string sessionId = string.Empty;

try
{
    var loginResult = await client.LoginAsync(
        Environment.GetEnvironmentVariable("ECGRID_USER")!,
        Environment.GetEnvironmentVariable("ECGRID_PASS")!);
    sessionId = loginResult.LoginResult;

    // Create the carbon copy rule — copy all inbound parcels to archive mailbox
    var addResult = await client.CarbonCopyAddAsync(
        sessionId,
        networkId:       0,
        mailboxId:       54321,     // source mailbox
        ecgridIdFrom:    0,         // any sender
        ecgridIdTo:      0,         // any recipient
        copyToMailboxId: 99001,     // archive mailbox
        direction:       ECGridDirection.InBox);

    int ccId = addResult.CarbonCopyAddResult;
    Console.WriteLine($"Carbon copy created: ID={ccId}");

    // Verify the rule
    var info = await client.CarbonCopyInfoAsync(sessionId, ccId);
    Console.WriteLine($"Status:      {info.CarbonCopyInfoResult.Status}");
    Console.WriteLine($"Source:      Mailbox {info.CarbonCopyInfoResult.MailboxID}");
    Console.WriteLine($"Destination: Mailbox {info.CarbonCopyInfoResult.CopyToMailboxID}");

    // List all rules for the source mailbox
    var listResult = await client.CarbonCopyListAsync(
        sessionId,
        networkId:      0,
        mailboxId:      54321,
        pageNo:         1,
        recordsPerPage: 25);

    Console.WriteLine($"\nActive carbon copy rules for mailbox 54321:");
    foreach (var cc in listResult.CarbonCopyListResult ?? [])
        Console.WriteLine($"  ID={cc.CarbonCopyID}  Direction={cc.Direction}  Dest={cc.CopyToMailboxID}  Status={cc.Status}");
}
finally
{
    if (!string.IsNullOrEmpty(sessionId))
        await client.LogoutAsync(sessionId);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP CarbonCopyAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:CarbonCopyAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>"
    + "<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>"
    + "<ecg:CopyToMailboxID>99001</ecg:CopyToMailboxID>"
    + "<ecg:Direction>InBox</ecg:Direction>"
    + "</ecg:CarbonCopyAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/CarbonCopyAdd\"")
    .POST(BodyPublishers.ofString(envelope)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // carbon copy ID
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP CarbonCopyAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:CarbonCopyAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>
    <ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>
    <ecg:CopyToMailboxID>99001</ecg:CopyToMailboxID>
    <ecg:Direction>InBox</ecg:Direction>
  </ecg:CarbonCopyAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/CarbonCopyAdd"' },
  body: envelope
});
console.log(await response.text()); // carbon copy ID
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
    '<soap:Body><ecg:CarbonCopyAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>'
    '<ecg:ECGridIDFrom>0</ecg:ECGridIDFrom><ecg:ECGridIDTo>0</ecg:ECGridIDTo>'
    '<ecg:CopyToMailboxID>99001</ecg:CopyToMailboxID>'
    '<ecg:Direction>InBox</ecg:Direction>'
    '</ecg:CarbonCopyAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/CarbonCopyAdd"'}
)
resp.raise_for_status()
print(resp.text)  # carbon copy ID
```

</TabItem>
</Tabs>

---

## Related

- [REST — Carbon Copies: Create](../rest-api/carbon-copies/create-carbon-copy)
- [REST — Carbon Copies: Get](../rest-api/carbon-copies/get-carbon-copy)
- [REST — Carbon Copies: List](../rest-api/carbon-copies/list-carbon-copies)
- [REST — Carbon Copies: Update](../rest-api/carbon-copies/update-carbon-copy)
- [REST — Carbon Copies: Delete](../rest-api/carbon-copies/delete-carbon-copy)
- [SOAP — CarbonCopyAdd](../soap-api/carbon-copies/carbon-copy-add)
- [SOAP — CarbonCopyInfo](../soap-api/carbon-copies/carbon-copy-info)
- [SOAP — CarbonCopyList](../soap-api/carbon-copies/carbon-copy-list)
- [Appendix: ENUMs — Direction](../appendix/enums)
