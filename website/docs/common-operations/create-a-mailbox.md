---
title: Create a Mailbox
sidebar_position: 7
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create create-a-mailbox common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Create a Mailbox

Create and configure a new ECGrid mailbox to establish a dedicated EDI message queue for a company, division, or trading partner group.

## Overview

A mailbox is the core unit of EDI message routing in ECGrid. Each mailbox holds an inbox and outbox, is associated with one or more ECGrid IDs (ISA sender/receiver identifiers), and has its own access controls. Creating a mailbox involves three steps: provisioning the mailbox, verifying it was created correctly, and optionally applying configuration settings such as delete-on-download or inbox timeout rules.

Sequence:
1. Create the mailbox with `POST /v2/mailboxes/create`.
2. Retrieve the new mailbox record with `GET /v2/mailboxes/{id}` to verify.
3. Optionally update mailbox configuration with `POST /v2/mailboxes/update-config`.

---

## REST

**Auth:** `X-API-Key: <key>` header

### Step 1 — Create the mailbox

```http
POST https://rest.ecgrid.io/v2/mailboxes/create
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "networkId": 0,
  "uniqueId": "ACME-EDI-01",
  "companyName": "Acme Corporation",
  "mailboxConfig": {
    "deleteOnDownload": false,
    "inBoxTimeout": 72
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `networkId` | integer | No | Parent network ID. Pass `0` to use the network associated with the API key. |
| `uniqueId` | string | Yes | A unique identifier for this mailbox within the network (alphanumeric, no spaces). |
| `companyName` | string | Yes | Human-readable company or division name for this mailbox. |
| `mailboxConfig.deleteOnDownload` | boolean | No | If `true`, parcels are automatically removed from the inbox after download confirmation. Default: `false`. |
| `mailboxConfig.inBoxTimeout` | integer | No | Hours before an undownloaded parcel triggers an alert. Common values: 24, 48, 72. |

**Response:**

```json
{
  "success": true,
  "data": {
    "mailboxId": 54321,
    "networkId": 1001,
    "uniqueId": "ACME-EDI-01",
    "companyName": "Acme Corporation",
    "status": "Active",
    "createdDate": "2026-05-07T10:00:00Z"
  }
}
```

Record the `mailboxId` — you will need it for all subsequent API calls targeting this mailbox.

### Step 2 — Verify the mailbox

```http
GET https://rest.ecgrid.io/v2/mailboxes/54321
X-API-Key: YOUR_API_KEY
```

Confirm that `status` is `"Active"` and all fields match your input.

### Step 3 — (Optional) Update mailbox configuration

Use `POST /v2/mailboxes/update-config` to adjust settings after creation, such as X12 delimiter preferences or inbox timeout values.

```http
POST https://rest.ecgrid.io/v2/mailboxes/update-config
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "mailboxId": 54321,
  "inBoxTimeout": 48,
  "deleteOnDownload": true
}
```

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
curl -s -X POST https://rest.ecgrid.io/v2/mailboxes/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"uniqueId":"ACME-EDI-01","companyName":"Acme Corporation"}' | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — create and verify a mailbox using IHttpClientFactory (registered as "ECGrid")
// API key loaded from IConfiguration — never hardcoded

using System.Net.Http.Json;

public record CreateMailboxRequest(
    int NetworkId,
    string UniqueId,
    string CompanyName);

public record MailboxInfo(
    int MailboxId,
    int NetworkId,
    string UniqueId,
    string CompanyName,
    string Status,
    DateTimeOffset CreatedDate);

public record ApiResponse<T>(bool Success, T Data);

public class ECGridMailboxService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridMailboxService> _logger;

    public ECGridMailboxService(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridMailboxService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Creates a new ECGrid mailbox and returns the provisioned mailbox info.
    /// </summary>
    public async Task<MailboxInfo> CreateMailboxAsync(
        string uniqueId,
        string companyName,
        int networkId = 0,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        var request = new CreateMailboxRequest(networkId, uniqueId, companyName);

        var response = await http.PostAsJsonAsync(
            "/v2/mailboxes/create", request, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content
            .ReadFromJsonAsync<ApiResponse<MailboxInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from mailbox create.");

        _logger.LogInformation(
            "Mailbox created: ID={MailboxId}, UniqueID={UniqueId}",
            result.Data.MailboxId, result.Data.UniqueId);

        // Verify the mailbox is reachable
        var verify = await http.GetFromJsonAsync<ApiResponse<MailboxInfo>>(
            $"/v2/mailboxes/{result.Data.MailboxId}", cancellationToken)
            ?? throw new InvalidOperationException("Could not verify mailbox after creation.");

        if (verify.Data.Status != "Active")
            _logger.LogWarning("Mailbox {Id} status is {Status} — expected Active.",
                verify.Data.MailboxId, verify.Data.Status);

        return verify.Data;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — create an ECGrid mailbox
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String body = "{\"networkId\":0,\"uniqueId\":\"ACME-EDI-01\",\"companyName\":\"Acme Corporation\"}";

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/create"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString(body))
    .build();

var response = http.send(request, BodyHandlers.ofString());
System.out.println(response.body()); // contains mailboxId
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — create an ECGrid mailbox
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/mailboxes/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
  body: JSON.stringify({ networkId: 0, uniqueId: 'ACME-EDI-01', companyName: 'Acme Corporation' })
});

const { data } = await response.json();
console.log(`Mailbox created: ID=${data.mailboxId}`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]

resp = requests.post(
    "https://rest.ecgrid.io/v2/mailboxes/create",
    headers={"X-API-Key": api_key},
    json={"networkId": 0, "uniqueId": "ACME-EDI-01", "companyName": "Acme Corporation"}
)
resp.raise_for_status()
mailbox_id = resp.json()["data"]["mailboxId"]
print(f"Mailbox created: ID={mailbox_id}")
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

builder.Services.AddScoped<ECGridMailboxService>();
```

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Method:** `MailboxAdd(SessionID, NetworkID, UniqueID, CompanyName, ...)`

### Step 1 — Log in and get a session ID

```csharp
var loginResult = await client.LoginAsync(username, password);
string sessionId = loginResult.LoginResult;
```

### Step 2 — Create the mailbox with MailboxAdd

```csharp
var result = await client.MailboxAddAsync(
    sessionId,
    networkId:   0,               // 0 = network associated with session
    uniqueId:    "ACME-EDI-01",
    companyName: "Acme Corporation");

int newMailboxId = result.MailboxAddResult.MailboxID;
Console.WriteLine($"New mailbox ID: {newMailboxId}");
```

### Step 3 — Apply configuration with MailboxConfig

```csharp
await client.MailboxConfigAsync(
    sessionId,
    mailboxId:       newMailboxId,
    deleteOnDownload: false,
    inBoxTimeout:    72);
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

    // Create the mailbox
    var addResult = await client.MailboxAddAsync(
        sessionId,
        networkId:   0,
        uniqueId:    "ACME-EDI-01",
        companyName: "Acme Corporation");

    int mailboxId = addResult.MailboxAddResult.MailboxID;
    Console.WriteLine($"Mailbox created: ID={mailboxId}");

    // Apply configuration
    await client.MailboxConfigAsync(
        sessionId,
        mailboxId:        mailboxId,
        deleteOnDownload: false,
        inBoxTimeout:     72);

    Console.WriteLine("Mailbox configuration applied.");
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
// Java 11+ — SOAP MailboxAdd via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String envelope = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:MailboxAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID>"
    + "<ecg:UniqueID>ACME-EDI-01</ecg:UniqueID>"
    + "<ecg:CompanyName>Acme Corporation</ecg:CompanyName>"
    + "</ecg:MailboxAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/MailboxAdd\"")
    .POST(BodyPublishers.ofString(envelope))
    .build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body()); // extract MailboxAddResult (mailboxId)
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP MailboxAdd via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const envelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:MailboxAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID>
    <ecg:UniqueID>ACME-EDI-01</ecg:UniqueID>
    <ecg:CompanyName>Acme Corporation</ecg:CompanyName>
  </ecg:MailboxAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/MailboxAdd"' },
  body: envelope
});
console.log(await response.text()); // extract MailboxAddResult (mailboxId)
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
    '<soap:Body><ecg:MailboxAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID>'
    '<ecg:UniqueID>ACME-EDI-01</ecg:UniqueID>'
    '<ecg:CompanyName>Acme Corporation</ecg:CompanyName>'
    '</ecg:MailboxAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/MailboxAdd"'}
)
resp.raise_for_status()
print(resp.text)  # extract MailboxAddResult (mailboxId)
```

</TabItem>
</Tabs>

:::tip Next Step
After creating a mailbox, assign at least one ECGrid ID to it. See [Onboard a Trading Partner](./onboard-trading-partner) for the full flow including ECGrid ID creation.
:::

---

## Related

- [REST — Mailboxes: Create](../rest-api/mailboxes/create-mailbox)
- [REST — Mailboxes: Get](../rest-api/mailboxes/get-mailbox)
- [REST — Mailboxes: Update Config](../rest-api/mailboxes/update-config)
- [SOAP — MailboxAdd](../soap-api/mailboxes/mailbox-add)
- [SOAP — MailboxConfig](../soap-api/mailboxes/mailbox-config)
- [Onboard a Trading Partner](./onboard-trading-partner)
