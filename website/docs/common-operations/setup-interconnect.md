---
title: Set Up an Interconnect
sidebar_position: 9
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create setup-interconnect common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Set Up an Interconnect

Define the authorized EDI routing relationship between two ECGrid IDs so that EDI documents can flow between your mailbox and a trading partner's mailbox.

## Overview

An interconnect is the record in ECGrid that permits EDI routing between two ECGrid IDs. Without an active interconnect, parcels addressed between those IDs will be rejected. Interconnects are directional by configuration but typically set up bidirectionally — one interconnect record covers both inbound and outbound flows between the two IDs.

When your trading partner's ECGrid ID is already registered in the ECGrid network (e.g., they use a different VAN or are an existing ECGrid subscriber), you search for their ID first, then create the interconnect. If the partner is brand new to ECGrid, follow [Onboard a Trading Partner](./onboard-trading-partner) instead, which covers creating the ECGrid ID as well.

Sequence:
1. Search for the trading partner's ECGrid ID with `GET /v2/ids/find`.
2. Create the interconnect with `POST /v2/partners`.

---

## REST

**Auth:** `X-API-Key: <key>` header

### Step 1 — Find the trading partner's ECGrid ID

Search by ISA qualifier and ISA ID to locate the partner's registered ECGrid ID.

```http
GET https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO
X-API-Key: YOUR_API_KEY
```

| Query Parameter | Type | Required | Description |
|---|---|---|---|
| `isaQualifier` | string | Yes | Two-character ISA qualifier (e.g., `"01"`, `"ZZ"`). |
| `isaId` | string | Yes | The ISA ID to search for. Partial matches may be supported. |

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "ecGridId": 334455,
      "isaQualifier": "01",
      "isaId": "PARTNERCO     ",
      "companyName": "Partner Company Inc.",
      "status": "Active"
    }
  ]
}
```

If no results are returned, the partner may not yet have an ECGrid ID. In that case, create one first — see [Onboard a Trading Partner](./onboard-trading-partner).

### Step 2 — Create the interconnect

Use your ECGrid ID and the partner's `ecGridId` from Step 1 to create the interconnect.

```http
POST https://rest.ecgrid.io/v2/partners
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "ecGridIdFrom": 111111,
  "ecGridIdTo": 334455,
  "status": "Active"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `ecGridIdFrom` | integer | Yes | Your ECGrid ID — the initiating side of the relationship. |
| `ecGridIdTo` | integer | Yes | The trading partner's ECGrid ID from Step 1. |
| `status` | string | No | Initial status. Use `"Active"` to enable routing immediately. Defaults to `"Active"`. |

**Response:**

```json
{
  "success": true,
  "data": {
    "interconnectId": 88200,
    "ecGridIdFrom": 111111,
    "ecGridIdTo": 334455,
    "status": "Active",
    "createdDate": "2026-05-07T11:00:00Z"
  }
}
```

Once `status` is `"Active"`, ECGrid begins routing EDI parcels addressed between the two IDs in both directions.

:::tip Verify routing
After creating the interconnect, use [Send a Test File](./send-edi-to-trading-partner) to confirm that EDI flows end-to-end between the two parties.
:::

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — find the trading partner's ECGrid ID
curl -s "https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO" \
  -H "X-API-Key: $ECGRID_API_KEY" | jq '.data[0].ecGridId'

# Step 2 — create the interconnect (replace PARTNER_ID with result above)
curl -s -X POST https://rest.ecgrid.io/v2/partners \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"ecGridIdFrom\":111111,\"ecGridIdTo\":$PARTNER_ID,\"status\":\"Active\"}" | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — find a partner's ECGrid ID and create an interconnect
// API key loaded from IConfiguration — never hardcoded

using System.Net.Http.Json;

public record ECGridIdSearchResult(
    int ECGridId,
    string IsaQualifier,
    string IsaId,
    string CompanyName,
    string Status);

public record SearchResponse(bool Success, List<ECGridIdSearchResult> Data);

public record CreatePartnerRequest(
    int ECGridIdFrom,
    int ECGridIdTo,
    string Status);

public record InterconnectInfo(
    int InterconnectId,
    int ECGridIdFrom,
    int ECGridIdTo,
    string Status,
    DateTimeOffset CreatedDate);

public record ApiResponse<T>(bool Success, T Data);

public class ECGridInterconnectService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridInterconnectService> _logger;

    public ECGridInterconnectService(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridInterconnectService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Finds a trading partner's ECGrid ID and creates an active interconnect.
    /// Throws InvalidOperationException if no matching ECGrid ID is found.
    /// </summary>
    /// <param name="myECGridId">Your ECGrid ID (the from side of the interconnect).</param>
    /// <param name="partnerIsaQualifier">Partner's ISA qualifier.</param>
    /// <param name="partnerIsaId">Partner's ISA ID.</param>
    public async Task<InterconnectInfo> SetupInterconnectAsync(
        int myECGridId,
        string partnerIsaQualifier,
        string partnerIsaId,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        // Step 1 — find the partner's ECGrid ID
        var searchUrl = $"/v2/ids/find?isaQualifier={Uri.EscapeDataString(partnerIsaQualifier)}" +
                        $"&isaId={Uri.EscapeDataString(partnerIsaId)}";

        var searchResponse = await http.GetFromJsonAsync<SearchResponse>(
            searchUrl, cancellationToken)
            ?? throw new InvalidOperationException("No response from ECGrid ID search.");

        if (searchResponse.Data.Count == 0)
            throw new InvalidOperationException(
                $"No ECGrid ID found for {partnerIsaQualifier}:{partnerIsaId}. " +
                "Use OnboardPartnerAsync to create one first.");

        // Take the first active match
        var partnerInfo = searchResponse.Data.FirstOrDefault(x => x.Status == "Active")
            ?? searchResponse.Data[0];

        _logger.LogInformation(
            "Found partner ECGrid ID: {ECGridId} ({Company})",
            partnerInfo.ECGridId, partnerInfo.CompanyName);

        // Step 2 — create the interconnect
        var partnerRequest = new CreatePartnerRequest(
            ECGridIdFrom: myECGridId,
            ECGridIdTo:   partnerInfo.ECGridId,
            Status:       "Active");

        var partnerResponse = await http.PostAsJsonAsync(
            "/v2/partners", partnerRequest, cancellationToken);
        partnerResponse.EnsureSuccessStatusCode();

        var result = await partnerResponse.Content
            .ReadFromJsonAsync<ApiResponse<InterconnectInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from partner create.");

        _logger.LogInformation(
            "Interconnect created: ID={InterconnectId} From={From} To={To} Status={Status}",
            result.Data.InterconnectId,
            result.Data.ECGridIdFrom,
            result.Data.ECGridIdTo,
            result.Data.Status);

        return result.Data;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — find partner ECGrid ID then create interconnect
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — search for partner ECGrid ID
var findReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO"))
    .header("X-API-Key", key).GET().build();
var findResp = http.send(findReq, BodyHandlers.ofString());
int partnerId = mapper.readTree(findResp.body()).path("data").get(0).path("ecGridId").asInt();

// Step 2 — create the interconnect
String body = String.format(
    "{\"ecGridIdFrom\":111111,\"ecGridIdTo\":%d,\"status\":\"Active\"}", partnerId);
var icReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(body)).build();
var icResp = http.send(icReq, BodyHandlers.ofString());
System.out.println(icResp.body()); // interconnectId
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — find partner ECGrid ID then create interconnect
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'X-API-Key': apiKey };

// Step 1 — find partner ECGrid ID
const findResp = await fetch(
  'https://rest.ecgrid.io/v2/ids/find?isaQualifier=01&isaId=PARTNERCO',
  { headers });
const { data: [partner] } = await findResp.json();

// Step 2 — create interconnect
const icResp = await fetch('https://rest.ecgrid.io/v2/partners', {
  method: 'POST',
  headers: { ...headers, 'Content-Type': 'application/json' },
  body: JSON.stringify({ ecGridIdFrom: 111111, ecGridIdTo: partner.ecGridId, status: 'Active' })
});
const { data: ic } = await icResp.json();
console.log(`Interconnect created: ID=${ic.interconnectId}`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

# Step 1 — find partner ECGrid ID
find = session.get("https://rest.ecgrid.io/v2/ids/find",
                   params={"isaQualifier": "01", "isaId": "PARTNERCO"})
find.raise_for_status()
partner_id = find.json()["data"][0]["ecGridId"]

# Step 2 — create interconnect
resp = session.post("https://rest.ecgrid.io/v2/partners",
    json={"ecGridIdFrom": 111111, "ecGridIdTo": partner_id, "status": "Active"})
resp.raise_for_status()
print(f"Interconnect: {resp.json()['data']['interconnectId']}")
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

builder.Services.AddScoped<ECGridInterconnectService>();
```

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Methods:**
- `TPSearch(SessionID, ISAQualifier, ISAID, ...)` — find an existing ECGrid ID
- `InterconnectAdd(SessionID, ECGridIDFrom, ECGridIDTo, ...)` — create the interconnect

### Step 1 — Log in and get a session ID

```csharp
var loginResult = await client.LoginAsync(username, password);
string sessionId = loginResult.LoginResult;
```

### Step 2 — Find the partner with TPSearch

```csharp
var searchResult = await client.TPSearchAsync(
    sessionId,
    isaQualifier: "01",
    isaId:        "PARTNERCO",
    pageNo:       1,
    recordsPerPage: 10);

var partner = searchResult.TPSearchResult?.FirstOrDefault()
    ?? throw new InvalidOperationException("Partner ECGrid ID not found.");

int partnerECGridId = partner.ECGridID;
Console.WriteLine($"Found partner: {partnerECGridId} — {partner.CompanyName}");
```

### Step 3 — Create the interconnect with InterconnectAdd

```csharp
int myECGridId = int.Parse(Environment.GetEnvironmentVariable("MY_ECGRID_ID")!);

var interconnect = await client.InterconnectAddAsync(
    sessionId,
    ecgridIdFrom: myECGridId,
    ecgridIdTo:   partnerECGridId);

Console.WriteLine($"Interconnect created: {interconnect.InterconnectAddResult.InterconnectID}");
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

    // Find the trading partner's ECGrid ID
    var searchResult = await client.TPSearchAsync(
        sessionId,
        isaQualifier:   "01",
        isaId:          "PARTNERCO",
        pageNo:         1,
        recordsPerPage: 10);

    var partner = searchResult.TPSearchResult?.FirstOrDefault()
        ?? throw new InvalidOperationException("No matching ECGrid ID found for this partner.");

    Console.WriteLine($"Partner found: ECGridID={partner.ECGridID}  Company={partner.CompanyName}");

    // Create the interconnect
    int myECGridId = int.Parse(Environment.GetEnvironmentVariable("MY_ECGRID_ID")!);

    var icResult = await client.InterconnectAddAsync(
        sessionId,
        ecgridIdFrom: myECGridId,
        ecgridIdTo:   partner.ECGridID);

    Console.WriteLine($"Interconnect created: ID={icResult.InterconnectAddResult.InterconnectID}");
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
// Java 11+ — SOAP TPSearch + InterconnectAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String searchEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:TPSearch>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>"
    + "<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>10</ecg:RecordsPerPage>"
    + "</ecg:TPSearch></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/TPSearch\"")
    .POST(BodyPublishers.ofString(searchEnv)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Parse ECGridID from XML, then call InterconnectAdd
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP TPSearch + InterconnectAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const searchEnv = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:TPSearch>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:Qualifier>01</ecg:Qualifier>
    <ecg:ID>PARTNERCO</ecg:ID>
    <ecg:PageNo>1</ecg:PageNo>
    <ecg:RecordsPerPage>10</ecg:RecordsPerPage>
  </ecg:TPSearch></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/TPSearch"' },
  body: searchEnv
});
// Parse ECGridID from XML, then call InterconnectAdd
console.log(await response.text());
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
    '<soap:Body><ecg:TPSearch>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:Qualifier>01</ecg:Qualifier><ecg:ID>PARTNERCO</ecg:ID>'
    '<ecg:PageNo>1</ecg:PageNo><ecg:RecordsPerPage>10</ecg:RecordsPerPage>'
    '</ecg:TPSearch></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/TPSearch"'}
)
resp.raise_for_status()
# Parse ECGridID from resp.text, then call InterconnectAdd
print(resp.text)
```

</TabItem>
</Tabs>

---

## Related

- [REST — IDs: Find](../rest-api/ids/find-id)
- [REST — Partners: Create](../rest-api/partners/create-partner)
- [REST — Partners: List](../rest-api/partners/list-partners)
- [SOAP — TPSearch](../soap-api/ids/tp-search)
- [SOAP — InterconnectAdd](../soap-api/partners/interconnect-add)
- [Onboard a Trading Partner](./onboard-trading-partner)
- [Send EDI to a Trading Partner](./send-edi-to-trading-partner)
