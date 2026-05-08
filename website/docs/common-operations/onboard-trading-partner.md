---
title: Onboard a Trading Partner
sidebar_position: 8
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create onboard-trading-partner common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Onboard a Trading Partner

Register a new trading partner in ECGrid by creating their ECGrid ID and establishing the interconnect that authorizes EDI exchange between your mailbox and theirs.

## Overview

A trading partner in ECGrid is represented by an ECGrid ID — a record that binds an ISA qualifier and ISA ID pair to a specific mailbox. Once the ECGrid ID exists, you create an interconnect (partnership) to enable routing between your ID and theirs. Both steps are required before EDI files can flow between the two parties.

Sequence:
1. Create the trading partner's ECGrid ID with `POST /v2/ids`.
2. Create the interconnect (partnership) with `POST /v2/partners`.

---

## REST

**Auth:** `X-API-Key: <key>` header

### Step 1 — Create the trading partner's ECGrid ID

An ECGrid ID represents an ISA sender/receiver identity. Each ID belongs to a mailbox and carries an ISA qualifier + ISA ID pair that appears in the EDI envelope.

```http
POST https://rest.ecgrid.io/v2/ids
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "networkId": 0,
  "mailboxId": 54321,
  "isaQualifier": "01",
  "isaId": "ACMECORP      ",
  "description": "Acme Corporation Production ID",
  "useType": "Production"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `networkId` | integer | No | Network ID. Pass `0` to use the network for the API key. |
| `mailboxId` | integer | Yes | The mailbox this ECGrid ID belongs to. |
| `isaQualifier` | string | Yes | Two-character ISA qualifier (e.g., `"01"` for DUNS, `"ZZ"` for mutually defined). |
| `isaId` | string | Yes | Up to 15-character ISA ID, padded with trailing spaces to 15 characters. |
| `description` | string | No | Human-readable label for this ID. |
| `useType` | string | No | `"Test"`, `"Production"`, or `"TestAndProduction"`. |

**Response:**

```json
{
  "success": true,
  "data": {
    "ecGridId": 678900,
    "mailboxId": 54321,
    "isaQualifier": "01",
    "isaId": "ACMECORP      ",
    "description": "Acme Corporation Production ID",
    "status": "Active"
  }
}
```

Record the `ecGridId` — you need it to create the interconnect.

### Step 2 — Create the interconnect

An interconnect authorizes and routes EDI traffic between two ECGrid IDs. You supply your ECGrid ID and the trading partner's ECGrid ID.

```http
POST https://rest.ecgrid.io/v2/partners
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "ecGridIdFrom": 111111,
  "ecGridIdTo": 678900,
  "status": "Active"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `ecGridIdFrom` | integer | Yes | Your ECGrid ID (the initiating party). |
| `ecGridIdTo` | integer | Yes | The trading partner's ECGrid ID created in Step 1. |
| `status` | string | No | Initial status. Use `"Active"` to enable routing immediately. |

**Response:**

```json
{
  "success": true,
  "data": {
    "interconnectId": 99001,
    "ecGridIdFrom": 111111,
    "ecGridIdTo": 678900,
    "status": "Active",
    "createdDate": "2026-05-07T10:15:00Z"
  }
}
```

Once the interconnect is `"Active"`, EDI files addressed to either ECGrid ID will route between the two parties.

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — create the trading partner's ECGrid ID
curl -s -X POST https://rest.ecgrid.io/v2/ids \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":54321,"isaQualifier":"01","isaId":"ACMECORP      ","description":"Acme Corporation"}' | jq .

# Step 2 — create the interconnect (replace PARTNER_ECGRID_ID with step 1 ecGridId)
curl -s -X POST https://rest.ecgrid.io/v2/partners \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"ecGridIdFrom\":111111,\"ecGridIdTo\":$PARTNER_ECGRID_ID,\"status\":\"Active\"}" | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — create ECGrid ID and interconnect using IHttpClientFactory (registered as "ECGrid")
// API key loaded from IConfiguration — never hardcoded

using System.Net.Http.Json;

public record CreateECGridIdRequest(
    int NetworkId,
    int MailboxId,
    string IsaQualifier,
    string IsaId,
    string Description,
    string UseType);

public record ECGridIdInfo(
    int ECGridId,
    int MailboxId,
    string IsaQualifier,
    string IsaId,
    string Status);

public record CreatePartnerRequest(
    int ECGridIdFrom,
    int ECGridIdTo,
    string Status);

public record InterconnectInfo(
    int InterconnectId,
    int ECGridIdFrom,
    int ECGridIdTo,
    string Status);

public record ApiResponse<T>(bool Success, T Data);

public class ECGridOnboardingService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridOnboardingService> _logger;

    public ECGridOnboardingService(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridOnboardingService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Creates an ECGrid ID for a new trading partner and establishes an active interconnect.
    /// </summary>
    /// <param name="mailboxId">Mailbox to attach the new ECGrid ID to.</param>
    /// <param name="isaQualifier">ISA-06 qualifier (e.g., "01", "ZZ").</param>
    /// <param name="isaId">ISA-06 sender/receiver ID, padded to 15 chars.</param>
    /// <param name="myECGridId">Your existing ECGrid ID — the other side of the interconnect.</param>
    /// <param name="description">Optional human-readable label for the new ID.</param>
    public async Task<(ECGridIdInfo Id, InterconnectInfo Interconnect)> OnboardPartnerAsync(
        int mailboxId,
        string isaQualifier,
        string isaId,
        int myECGridId,
        string description = "",
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        // Step 1 — create the trading partner ECGrid ID
        var idRequest = new CreateECGridIdRequest(
            NetworkId:    0,
            MailboxId:    mailboxId,
            IsaQualifier: isaQualifier,
            IsaId:        isaId.PadRight(15),
            Description:  description,
            UseType:      "Production");

        var idResponse = await http.PostAsJsonAsync(
            "/v2/ids", idRequest, cancellationToken);
        idResponse.EnsureSuccessStatusCode();

        var idResult = await idResponse.Content
            .ReadFromJsonAsync<ApiResponse<ECGridIdInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from ECGrid ID create.");

        _logger.LogInformation(
            "ECGrid ID created: {ECGridId} ({IsaQualifier}:{IsaId})",
            idResult.Data.ECGridId, idResult.Data.IsaQualifier, idResult.Data.IsaId.Trim());

        // Step 2 — create the interconnect
        var partnerRequest = new CreatePartnerRequest(
            ECGridIdFrom: myECGridId,
            ECGridIdTo:   idResult.Data.ECGridId,
            Status:       "Active");

        var partnerResponse = await http.PostAsJsonAsync(
            "/v2/partners", partnerRequest, cancellationToken);
        partnerResponse.EnsureSuccessStatusCode();

        var partnerResult = await partnerResponse.Content
            .ReadFromJsonAsync<ApiResponse<InterconnectInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from partner create.");

        _logger.LogInformation(
            "Interconnect created: ID={InterconnectId} Status={Status}",
            partnerResult.Data.InterconnectId, partnerResult.Data.Status);

        return (idResult.Data, partnerResult.Data);
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — create ECGrid ID then interconnect
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — create trading partner ECGrid ID
String idBody = "{\"networkId\":0,\"mailboxId\":54321,\"isaQualifier\":\"01\"," +
    "\"isaId\":\"ACMECORP      \",\"description\":\"Acme Corporation\",\"useType\":\"Production\"}";

var idReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/ids"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(idBody)).build();
var idResp = http.send(idReq, BodyHandlers.ofString());
int partnerECGridId = mapper.readTree(idResp.body()).path("data").path("ecGridId").asInt();
System.out.println("ECGrid ID created: " + partnerECGridId);

// Step 2 — create interconnect
String partnerBody = String.format(
    "{\"ecGridIdFrom\":111111,\"ecGridIdTo\":%d,\"status\":\"Active\"}", partnerECGridId);
var pReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/partners"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(partnerBody)).build();
var pResp = http.send(pReq, BodyHandlers.ofString());
System.out.println(pResp.body()); // interconnectId
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — create ECGrid ID then interconnect
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — create trading partner ECGrid ID
const idResp = await fetch('https://rest.ecgrid.io/v2/ids', {
  method: 'POST', headers,
  body: JSON.stringify({ networkId: 0, mailboxId: 54321, isaQualifier: '01',
                         isaId: 'ACMECORP      ', description: 'Acme Corporation' })
});
const { data: idData } = await idResp.json();
console.log(`ECGrid ID created: ${idData.ecGridId}`);

// Step 2 — create interconnect
const pResp = await fetch('https://rest.ecgrid.io/v2/partners', {
  method: 'POST', headers,
  body: JSON.stringify({ ecGridIdFrom: 111111, ecGridIdTo: idData.ecGridId, status: 'Active' })
});
const { data: partner } = await pResp.json();
console.log(`Interconnect created: ID=${partner.interconnectId}`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})

# Step 1 — create trading partner ECGrid ID
id_resp = session.post("https://rest.ecgrid.io/v2/ids", json={
    "networkId": 0, "mailboxId": 54321, "isaQualifier": "01",
    "isaId": "ACMECORP      ", "description": "Acme Corporation"
})
id_resp.raise_for_status()
partner_ecgrid_id = id_resp.json()["data"]["ecGridId"]
print(f"ECGrid ID created: {partner_ecgrid_id}")

# Step 2 — create interconnect
p_resp = session.post("https://rest.ecgrid.io/v2/partners", json={
    "ecGridIdFrom": 111111, "ecGridIdTo": partner_ecgrid_id, "status": "Active"
})
p_resp.raise_for_status()
print(f"Interconnect: {p_resp.json()['data']['interconnectId']}")
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

builder.Services.AddScoped<ECGridOnboardingService>();
```

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Methods:**
- `TPAdd(SessionID, NetworkID, MailboxID, ISAQualifier, ISAID, ...)` — creates the ECGrid ID
- `InterconnectAdd(SessionID, ECGridIDFrom, ECGridIDTo, ...)` — creates the interconnect

### Step 1 — Log in and get a session ID

```csharp
var loginResult = await client.LoginAsync(username, password);
string sessionId = loginResult.LoginResult;
```

### Step 2 — Create the ECGrid ID with TPAdd

```csharp
var tpResult = await client.TPAddAsync(
    sessionId,
    networkId:    0,
    mailboxId:    54321,
    isaQualifier: "01",
    isaId:        "ACMECORP      ",
    description:  "Acme Corporation Production ID");

int newECGridId = tpResult.TPAddResult.ECGridID;
Console.WriteLine($"ECGrid ID created: {newECGridId}");
```

### Step 3 — Create the interconnect with InterconnectAdd

```csharp
var interconnect = await client.InterconnectAddAsync(
    sessionId,
    ecgridIdFrom: 111111,    // your ECGrid ID
    ecgridIdTo:   newECGridId);

Console.WriteLine($"Interconnect ID: {interconnect.InterconnectAddResult.InterconnectID}");
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

    // Create trading partner ECGrid ID
    var tpResult = await client.TPAddAsync(
        sessionId,
        networkId:    0,
        mailboxId:    54321,
        isaQualifier: "01",
        isaId:        "ACMECORP      ",
        description:  "Acme Corporation Production ID");

    int partnerECGridId = tpResult.TPAddResult.ECGridID;
    Console.WriteLine($"ECGrid ID created: {partnerECGridId}");

    // Create the interconnect between your ID and the partner's ID
    int myECGridId = int.Parse(Environment.GetEnvironmentVariable("MY_ECGRID_ID")!);

    var interconnect = await client.InterconnectAddAsync(
        sessionId,
        ecgridIdFrom: myECGridId,
        ecgridIdTo:   partnerECGridId);

    Console.WriteLine($"Interconnect created: {interconnect.InterconnectAddResult.InterconnectID}");
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
// Java 11+ — SOAP TPAdd + InterconnectAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String tpEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:TPAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>"
    + "<ecg:ISAQualifier>01</ecg:ISAQualifier>"
    + "<ecg:ISAID>ACMECORP      </ecg:ISAID>"
    + "<ecg:Description>Acme Corporation</ecg:Description>"
    + "</ecg:TPAdd></soap:Body></soap:Envelope>";

var tpReq = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/TPAdd\"")
    .POST(BodyPublishers.ofString(tpEnv)).build();

var tpResp = http.send(tpReq, HttpResponse.BodyHandlers.ofString());
// Extract ECGridID from tpResp XML, then call InterconnectAdd
System.out.println(tpResp.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP TPAdd + InterconnectAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const tpEnvelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:TPAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>
    <ecg:ISAQualifier>01</ecg:ISAQualifier>
    <ecg:ISAID>ACMECORP      </ecg:ISAID>
    <ecg:Description>Acme Corporation</ecg:Description>
  </ecg:TPAdd></soap:Body>
</soap:Envelope>`;

const tpResp = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/TPAdd"' },
  body: tpEnvelope
});
// Extract ECGridID from XML, then call InterconnectAdd
console.log(await tpResp.text());
```

</TabItem>
<TabItem value="python" label="Python">

```python
import requests

session_id = "YOUR_SESSION_ID"  # obtain from Login

tp_env = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:TPAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>'
    '<ecg:ISAQualifier>01</ecg:ISAQualifier>'
    '<ecg:ISAID>ACMECORP      </ecg:ISAID>'
    '<ecg:Description>Acme Corporation</ecg:Description>'
    '</ecg:TPAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=tp_env.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/TPAdd"'}
)
resp.raise_for_status()
# Extract ECGridID from resp.text, then call InterconnectAdd
print(resp.text)
```

</TabItem>
</Tabs>

---

## Related

- [REST — IDs: Create](../rest-api/ids/create-id)
- [REST — Partners: Create](../rest-api/partners/create-partner)
- [SOAP — TPAdd](../soap-api/ids/tp-add)
- [SOAP — InterconnectAdd](../soap-api/partners/interconnect-add)
- [Set Up an Interconnect](./setup-interconnect)
- [Create a Mailbox](./create-a-mailbox)
- [Appendix: ENUMs — UseType](../appendix/enums)
