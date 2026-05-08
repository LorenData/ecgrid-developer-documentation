---
title: Configure Callbacks
sidebar_position: 10
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create configure-callbacks common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Configure Callbacks

Register webhook endpoints that ECGrid calls in real time when EDI events occur, eliminating the need to poll for changes.

## Overview

ECGrid callbacks (webhooks) push event notifications to an HTTPS endpoint you control. When a parcel arrives, is downloaded, or an error occurs, ECGrid sends an HTTP POST to your registered URL with a JSON payload describing the event. This allows event-driven integrations that react immediately rather than polling on a schedule.

Callback events include inbound parcel arrivals (`InBox`), outbound delivery confirmations (`OutBox`), and error conditions. Each callback registration is scoped to an event type and optionally to a specific mailbox or ECGrid ID.

Sequence:
1. Create the callback with `POST /v2/callbacks/create`.
2. Confirm it works with `POST /v2/callbacks/test`.
3. Optionally inspect the queue with `POST /v2/callbacks/queue-list`.

---

## REST

**Auth:** `X-API-Key: <key>` header

### Step 1 — Create the callback

```http
POST https://rest.ecgrid.io/v2/callbacks/create
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "networkId": 0,
  "mailboxId": 0,
  "ecGridId": 0,
  "callBackUrl": "https://your-app.example.com/webhooks/ecgrid",
  "callBackEvent": "InBox",
  "frequency": 1,
  "retries": 3,
  "status": "Active"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `networkId` | integer | No | Scope to a specific network. Pass `0` for the API key's default network. |
| `mailboxId` | integer | No | Scope to a specific mailbox. Pass `0` for all mailboxes in the network. |
| `ecGridId` | integer | No | Scope to a specific ECGrid ID. Pass `0` for all IDs. |
| `callBackUrl` | string | Yes | Publicly reachable HTTPS URL that ECGrid will POST events to. |
| `callBackEvent` | string | Yes | Event type to monitor. See [Callback Events](#callback-events) below. |
| `frequency` | integer | No | Minimum seconds between repeated calls for the same event. Default: `1`. |
| `retries` | integer | No | Number of retry attempts on failure before the event is marked failed. Default: `3`. |
| `status` | string | No | `"Active"` to enable immediately. Default: `"Active"`. |

**Response:**

```json
{
  "success": true,
  "data": {
    "callBackQueueId": 7001,
    "callBackUrl": "https://your-app.example.com/webhooks/ecgrid",
    "callBackEvent": "InBox",
    "status": "Active"
  }
}
```

#### Callback Events

| Event | Description |
|---|---|
| `InBox` | A parcel has arrived and is ready for download. |
| `OutBox` | An outbound parcel was successfully delivered. |
| `InBoxError` | An inbound parcel failed to deliver to your mailbox. |
| `OutBoxError` | An outbound parcel could not be delivered to the trading partner. |
| `ConfirmDelivery` | A parcel download was confirmed by the recipient. |

### Step 2 — Send a test event

```http
POST https://rest.ecgrid.io/v2/callbacks/test
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "callBackQueueId": 7001
}
```

ECGrid posts a synthetic event payload to your registered URL. Verify that your endpoint receives it and returns `HTTP 200`.

**Example webhook payload ECGrid sends to your endpoint:**

```json
{
  "eventId": 900123,
  "callBackQueueId": 7001,
  "callBackEvent": "InBox",
  "ecGridId": 111111,
  "mailboxId": 54321,
  "parcelId": 98765,
  "fileName": "850_order.edi",
  "eventDateTime": "2026-05-07T14:32:00Z",
  "isTest": false
}
```

### Step 3 — Inspect the queue

List queued events to confirm delivery and check for any failures.

```http
POST https://rest.ecgrid.io/v2/callbacks/queue-list
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "callBackQueueId": 7001,
  "pageNo": 1,
  "recordsPerPage": 25
}
```

Events with a `status` of `"Failed"` have exceeded the retry count and need investigation. Check your endpoint's availability and response codes.

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — register the callback
curl -s -X POST https://rest.ecgrid.io/v2/callbacks/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":0,"ecGridId":0,"callBackUrl":"https://your-app.example.com/webhooks/ecgrid","callBackEvent":"InBox","frequency":1,"retries":3,"status":"Active"}' | jq .

# Step 2 — send a test event (replace QUEUE_ID with callBackQueueId from step 1)
curl -s -X POST https://rest.ecgrid.io/v2/callbacks/test \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"callBackQueueId":7001}' | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — register a callback and handle the test using IHttpClientFactory (registered as "ECGrid")
// API key loaded from IConfiguration — never hardcoded

using System.Net.Http.Json;

public record CreateCallbackRequest(
    int NetworkId,
    int MailboxId,
    int ECGridId,
    string CallBackUrl,
    string CallBackEvent,
    int Frequency,
    int Retries,
    string Status);

public record CallbackInfo(
    int CallBackQueueId,
    string CallBackUrl,
    string CallBackEvent,
    string Status);

public record TestCallbackRequest(int CallBackQueueId);

public record ApiResponse<T>(bool Success, T Data);

public class ECGridCallbackService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<ECGridCallbackService> _logger;

    public ECGridCallbackService(
        IHttpClientFactory httpClientFactory,
        ILogger<ECGridCallbackService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    /// <summary>
    /// Registers a webhook and fires a test event to verify connectivity.
    /// </summary>
    /// <param name="webhookUrl">Publicly reachable HTTPS URL.</param>
    /// <param name="eventType">ECGrid callback event type (e.g., "InBox").</param>
    public async Task<CallbackInfo> RegisterAndTestCallbackAsync(
        string webhookUrl,
        string eventType = "InBox",
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        // Register the callback
        var createRequest = new CreateCallbackRequest(
            NetworkId:     0,
            MailboxId:     0,
            ECGridId:      0,
            CallBackUrl:   webhookUrl,
            CallBackEvent: eventType,
            Frequency:     1,
            Retries:       3,
            Status:        "Active");

        var createResponse = await http.PostAsJsonAsync(
            "/v2/callbacks/create", createRequest, cancellationToken);
        createResponse.EnsureSuccessStatusCode();

        var result = await createResponse.Content
            .ReadFromJsonAsync<ApiResponse<CallbackInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from callback create.");

        _logger.LogInformation(
            "Callback registered: ID={Id} URL={Url} Event={Event}",
            result.Data.CallBackQueueId, result.Data.CallBackUrl, result.Data.CallBackEvent);

        // Send a test event to verify the endpoint is reachable
        var testRequest = new TestCallbackRequest(result.Data.CallBackQueueId);
        var testResponse = await http.PostAsJsonAsync(
            "/v2/callbacks/test", testRequest, cancellationToken);
        testResponse.EnsureSuccessStatusCode();

        _logger.LogInformation(
            "Test event sent to callback ID={Id}. Verify your endpoint received HTTP POST.",
            result.Data.CallBackQueueId);

        return result.Data;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — register a callback and fire a test event
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — register callback
String createBody = "{\"networkId\":0,\"mailboxId\":0,\"ecGridId\":0,"
    + "\"callBackUrl\":\"https://your-app.example.com/webhooks/ecgrid\","
    + "\"callBackEvent\":\"InBox\",\"frequency\":1,\"retries\":3,\"status\":\"Active\"}";

var createReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/create"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(createBody)).build();
var createResp = http.send(createReq, BodyHandlers.ofString());
int queueId = mapper.readTree(createResp.body()).path("data").path("callBackQueueId").asInt();
System.out.println("Callback registered: ID=" + queueId);

// Step 2 — send test event
String testBody = "{\"callBackQueueId\":" + queueId + "}";
var testReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/callbacks/test"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(testBody)).build();
http.send(testReq, BodyHandlers.ofString());
System.out.println("Test event sent — verify your endpoint.");
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — register a callback and fire a test event
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — register callback
const createResp = await fetch('https://rest.ecgrid.io/v2/callbacks/create', {
  method: 'POST', headers,
  body: JSON.stringify({
    networkId: 0, mailboxId: 0, ecGridId: 0,
    callBackUrl: 'https://your-app.example.com/webhooks/ecgrid',
    callBackEvent: 'InBox', frequency: 1, retries: 3, status: 'Active'
  })
});
const { data } = await createResp.json();
console.log(`Callback registered: ID=${data.callBackQueueId}`);

// Step 2 — test it
await fetch('https://rest.ecgrid.io/v2/callbacks/test', {
  method: 'POST', headers,
  body: JSON.stringify({ callBackQueueId: data.callBackQueueId })
});
console.log('Test event sent — verify your endpoint.');
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

# Step 1 — register callback
create = session.post("https://rest.ecgrid.io/v2/callbacks/create", json={
    "networkId": 0, "mailboxId": 0, "ecGridId": 0,
    "callBackUrl": "https://your-app.example.com/webhooks/ecgrid",
    "callBackEvent": "InBox", "frequency": 1, "retries": 3, "status": "Active"
})
create.raise_for_status()
queue_id = create.json()["data"]["callBackQueueId"]
print(f"Callback registered: ID={queue_id}")

# Step 2 — send test event
test = session.post("https://rest.ecgrid.io/v2/callbacks/test",
                    json={"callBackQueueId": queue_id})
test.raise_for_status()
print("Test event sent — verify your endpoint.")
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

builder.Services.AddScoped<ECGridCallbackService>();
```

### Webhook Receiver — ASP.NET Core Minimal API

Host your webhook handler in an ASP.NET Core application. The handler must return `HTTP 200` quickly — offload any heavy processing to a background queue.

```csharp
// .NET 10 — Minimal API webhook receiver for ECGrid callbacks
// Validate origin by IP allowlist or a shared secret in a custom header per your security policy

using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapPost("/webhooks/ecgrid", async (
    [FromBody] JsonElement payload,
    ILogger<Program> logger,
    CancellationToken cancellationToken) =>
{
    // Log the raw event for diagnostics
    logger.LogInformation("ECGrid callback received: {Payload}", payload.ToString());

    // Parse key fields
    string eventType  = payload.GetProperty("callBackEvent").GetString() ?? "Unknown";
    long   parcelId   = payload.TryGetProperty("parcelId", out var pid) ? pid.GetInt64() : 0;
    string fileName   = payload.TryGetProperty("fileName", out var fn) ? fn.GetString() ?? "" : "";

    logger.LogInformation(
        "Event={Event} ParcelId={ParcelId} File={File}",
        eventType, parcelId, fileName);

    // Offload processing — do NOT block the response waiting for download/processing
    // Use IBackgroundTaskQueue or Channel<T> to enqueue work here

    // ECGrid requires a 200 OK response to consider the delivery successful
    return Results.Ok(new { received = true });
});

app.Run();
```

:::tip Response Time Matters
ECGrid marks a callback delivery as failed if your endpoint does not respond with `HTTP 200` within the timeout window. Keep your handler fast: log the event, enqueue it for background processing, and return `200` immediately.
:::

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Methods:**
- `CallBackAdd(SessionID, NetworkID, MailboxID, ECGridID, CallBackURL, CallBackEvent, ...)` — register a callback
- `CallBackTest(SessionID, CallBackQueueID)` — fire a test event

### Step 1 — Log in and get a session ID

```csharp
var loginResult = await client.LoginAsync(username, password);
string sessionId = loginResult.LoginResult;
```

### Step 2 — Register the callback with CallBackAdd

```csharp
var result = await client.CallBackAddAsync(
    sessionId,
    networkId:     0,
    mailboxId:     0,
    ecgridId:      0,
    callBackUrl:   "https://your-app.example.com/webhooks/ecgrid",
    callBackEvent: CallBackEventType.InBox,
    frequency:     1,
    retries:       3);

int callBackQueueId = result.CallBackAddResult.CallBackQueueID;
Console.WriteLine($"Callback registered: ID={callBackQueueId}");
```

### Step 3 — Test the callback with CallBackTest

```csharp
await client.CallBackTestAsync(sessionId, callBackQueueId);
Console.WriteLine("Test event sent — verify your endpoint.");
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

    // Register the callback
    var cbResult = await client.CallBackAddAsync(
        sessionId,
        networkId:     0,
        mailboxId:     0,
        ecgridId:      0,
        callBackUrl:   "https://your-app.example.com/webhooks/ecgrid",
        callBackEvent: CallBackEventType.InBox,
        frequency:     1,
        retries:       3);

    int cbId = cbResult.CallBackAddResult.CallBackQueueID;
    Console.WriteLine($"Callback ID: {cbId}");

    // Send test event
    await client.CallBackTestAsync(sessionId, cbId);
    Console.WriteLine("Test event sent — check your endpoint.");
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
// Java 11+ — SOAP CallBackAdd + CallBackTest via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";

String addEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:CallBackAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>"
    + "<ecg:ECGridID>0</ecg:ECGridID>"
    + "<ecg:CallBackURL>https://your-app.example.com/webhooks/ecgrid</ecg:CallBackURL>"
    + "<ecg:CallBackEvent>InBox</ecg:CallBackEvent>"
    + "<ecg:Frequency>1</ecg:Frequency><ecg:Retries>3</ecg:Retries>"
    + "</ecg:CallBackAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/CallBackAdd\"")
    .POST(BodyPublishers.ofString(addEnv)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Extract CallBackQueueID from XML, then call CallBackTest
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP CallBackAdd + CallBackTest via raw HTTP
const sessionId = 'YOUR_SESSION_ID';

const addEnvelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:CallBackAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>
    <ecg:ECGridID>0</ecg:ECGridID>
    <ecg:CallBackURL>https://your-app.example.com/webhooks/ecgrid</ecg:CallBackURL>
    <ecg:CallBackEvent>InBox</ecg:CallBackEvent>
    <ecg:Frequency>1</ecg:Frequency><ecg:Retries>3</ecg:Retries>
  </ecg:CallBackAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/CallBackAdd"' },
  body: addEnvelope
});
// Extract CallBackQueueID from XML, then call CallBackTest
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
    '<soap:Body><ecg:CallBackAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>0</ecg:MailboxID>'
    '<ecg:ECGridID>0</ecg:ECGridID>'
    '<ecg:CallBackURL>https://your-app.example.com/webhooks/ecgrid</ecg:CallBackURL>'
    '<ecg:CallBackEvent>InBox</ecg:CallBackEvent>'
    '<ecg:Frequency>1</ecg:Frequency><ecg:Retries>3</ecg:Retries>'
    '</ecg:CallBackAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/CallBackAdd"'}
)
resp.raise_for_status()
# Extract CallBackQueueID from resp.text, then call CallBackTest
print(resp.text)
```

</TabItem>
</Tabs>

---

## Related

- [REST — Callbacks: Create](../rest-api/callbacks/create-callback)
- [REST — Callbacks: Test](../rest-api/callbacks/test-callback)
- [REST — Callbacks: Queue List](../rest-api/callbacks/queue-list)
- [REST — Callbacks: Event List](../rest-api/callbacks/event-list)
- [SOAP — CallBackAdd](../soap-api/callbacks/callback-add)
- [SOAP — CallBackTest](../soap-api/callbacks/callback-test)
- [Poll for Inbound Files](./poll-inbound-files)
