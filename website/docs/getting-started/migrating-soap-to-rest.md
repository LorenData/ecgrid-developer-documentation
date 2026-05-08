---
title: Migrating from SOAP to REST
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created SOAP to REST migration guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs to SOAP-to-REST migration examples - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Migrating from SOAP to REST

This guide helps you migrate an existing ECGridOS SOAP integration to the ECGrid REST API. The REST API (v2.6) is actively developed and is the recommended path for all new and maintained integrations.

## Why Migrate?

| Reason | Detail |
|---|---|
| **REST is the active API** | New features, endpoints, and improvements are added to REST only |
| **SOAP is established** | ECGridOS v4.1 receives security patches and critical updates only |
| **Simpler authentication** | Replace stateful `Login()` / `SessionID` with a single `X-API-Key` header |
| **Standard tooling** | REST works with any HTTP client, OpenAPI generators, Postman, and curl |
| **JSON vs XML** | JSON is lighter and easier to work with in modern .NET |
| **Better error handling** | Typed JSON error responses instead of SOAP Faults |

## Migration Strategy

A typical SOAP-to-REST migration involves three parallel workstreams:

1. **Authentication** — Replace `Login()` / `SessionID` with API key or Bearer JWT
2. **Method calls** — Map each SOAP method to its REST equivalent endpoint
3. **Data handling** — Replace XML deserialization with `System.Text.Json`

You do not need to migrate everything at once. The two APIs are independent — you can migrate one workflow at a time.

---

## Step 1 — Authentication Migration

This is the most impactful change. Every SOAP method takes a `SessionID` as its first parameter. In REST, authentication is a single header on every request.

**SOAP — before:**

```csharp
// Must call Login() first; SessionID required on every method
var sessionID = await client.LoginAsync(email, password);
var mailbox   = await client.MailboxInfoAsync(sessionID, mailboxID);
await client.LogoutAsync(sessionID);
```

**REST — after:**

```csharp
// API key is set once on the HttpClient; no Login/Logout needed
http.DefaultRequestHeaders.Add("X-API-Key", apiKey);
var mailbox = await http.GetFromJsonAsync<ApiResponse<MailboxInfo>>($"/v2/mailboxes/{mailboxID}");
```

To obtain your API key:

```http
GET /v2/users/{userID}/api-key HTTP/1.1
Host: rest.ecgrid.io
X-API-Key: your-existing-api-key
```

Or generate a new one:

```http
POST /v2/users/{userID}/generate-api-key HTTP/1.1
```

---

## Step 2 — Method Mapping

The table below maps the most commonly used SOAP methods to their REST equivalents.

### Authentication

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `Login()` | `POST /v2/auth/login` | Or skip login entirely — use `X-API-Key` |
| `Logout()` | `POST /v2/auth/logout` | Not needed when using API key |
| `WhoAmI()` | `GET /v2/users/me` | |
| `SessionInfo()` | `POST /v2/auth/session` | |
| `Version()` | `GET /v2/auth/version` | |

### Networks

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `NetworkInfo()` | `GET /v2/networks/{networkID}` | |
| `NetworkList()` | `GET /v2/networks` | |
| `NetworkAdd()` | `POST /v2/networks` | |
| `NetworkUpdate()` | `PUT /v2/networks/{networkID}` | |

### Mailboxes

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `MailboxInfo()` | `GET /v2/mailboxes/{mailboxID}` | |
| `MailboxList()` | `GET /v2/mailboxes` | |
| `MailboxAdd()` | `POST /v2/mailboxes` | |

### IDs (Trading Partners)

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `TPInfo()` | `GET /v2/ids/{ecgridID}` | |
| `TPList()` | `GET /v2/ids` | |
| `TPAdd()` | `POST /v2/ids` | |
| `TPSearch()` | `GET /v2/ids/find` | |
| `TPMove()` | `POST /v2/ids/{ecgridID}/move-tp` | |

### Partners (Interconnects)

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `InterconnectInfo()` | `GET /v2/partners/{partnerID}` | |
| `InterconnectAdd()` | `POST /v2/partners` | |
| `InterconnectList()` | `GET /v2/partners` | |
| `InterconnectCancel()` | `DELETE /v2/partners/{partnerID}` | |
| `InterconnectCount()` | `GET /v2/partners/count` | |

### Parcels (File Transfer)

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `ParcelInBox()` | `POST /v2/parcels/inbox-list` | |
| `ParcelOutBox()` | `POST /v2/parcels/outbox-list` | |
| `ParcelUpload()` | `POST /v2/parcels/upload` | |
| `ParcelDownload()` | `POST /v2/parcels/download` | |
| `ParcelDownloadConfirm()` | `POST /v2/parcels/confirm` | |
| `ParcelInfo()` | `GET /v2/parcels/{parcelID}` | |
| `ParcelResend()` | `POST /v2/parcels/{parcelID}/reset-to-inbox` | |
| `ParcelCancel()` | `POST /v2/parcels/{parcelID}/cancel` | |

### Interchanges

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `InterchangeInBox()` | `POST /v2/interchanges/inbox-list` | |
| `InterchangeOutBox()` | `POST /v2/interchanges/outbox-list` | |
| `InterchangeInfo()` | `GET /v2/interchanges/{interchangeID}` | |
| `InterchangeResend()` | `POST /v2/interchanges/{interchangeID}/resend` | |
| `InterchangeCancel()` | `POST /v2/interchanges/{interchangeID}/cancel` | |

### Users

| SOAP Method | REST Endpoint | Notes |
|---|---|---|
| `UserInfo()` | `GET /v2/users/{userID}` | |
| `UserList()` | `GET /v2/users` | |
| `UserAdd()` | `POST /v2/users` | |
| `UserUpdate()` | `PUT /v2/users/{userID}` | |
| `UserSetAuthLevel()` | `POST /v2/users/{userID}/set-role` | |
| `UserGetAPIKey()` | `GET /v2/users/{userID}/api-key` | |
| `UserGenerateAPIKey()` | `POST /v2/users/{userID}/generate-api-key` | |

---

## Step 3 — Data Format Migration

SOAP returns XML; REST returns JSON. The field names are similar but not identical.

**SOAP — XML response (MailboxInfo):**

```xml
<MailboxInfoResult>
  <MailboxID>12345</MailboxID>
  <MailboxName>My Mailbox</MailboxName>
  <Status>Active</Status>
</MailboxInfoResult>
```

**REST — JSON response (GET /v2/mailboxes/&#123;id&#125;):**

```json
{
  "success": true,
  "data": {
    "mailboxID": 12345,
    "mailboxName": "My Mailbox",
    "status": "Active"
  }
}
```

In .NET 10, use `System.Text.Json` for deserialization

```csharp
using System.Net.Http.Json;

// REST — read typed response
var response = await http.GetFromJsonAsync<ApiResponse<MailboxInfo>>($"/v2/mailboxes/{mailboxID}");
var mailbox  = response!.Data;
```

---

## Before and After — Parcel Download Workflow

This example shows a complete SOAP workflow and its REST equivalent.

### SOAP — before

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — SOAP parcel download workflow (before migration)
using var client = new ECGridOSPortTypeClient();

var sessionID  = await client.LoginAsync(email, password);
var parcelList = await client.ParcelInBoxAsync(sessionID);

foreach (var parcel in parcelList)
{
    // Download the parcel
    var data = await client.ParcelDownloadAsync(sessionID, parcel.ParcelID);

    // Save to disk
    await File.WriteAllBytesAsync($"{parcel.ParcelID}.edi", data.ParcelBytes);

    // Confirm receipt
    await client.ParcelDownloadConfirmAsync(sessionID, parcel.ParcelID);
}

await client.LogoutAsync(sessionID);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP parcel download workflow (before migration)
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.*;
import java.util.Base64;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login — extract sessionId from XML response
String loginEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\"><soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>pass</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";
// Send login, extract sessionId from response XML...
String sessionId = "...";

// ParcelInBox — extract parcel IDs from XML response
String inboxEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\"><soap:Body><ecg:ParcelInBox>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "</ecg:ParcelInBox></soap:Body></soap:Envelope>";
// Send inbox request, parse parcel list from XML...

// For each parcel: ParcelDownload → save file → ParcelDownloadConfirm → Logout
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP parcel download workflow (before migration)
const endpoint = 'https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx';
const ns = 'http://www.ecgridos.net/';

async function soapCall(action, body) {
  const env = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ecg="${ns}">
  <soap:Body>${body}</soap:Body>
</soap:Envelope>`;
  const r = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'text/xml; charset=utf-8', SOAPAction: `"${ns}${action}"` },
    body: env
  });
  return r.text();
}

// Login — extract sessionId from XML
const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>pass</ecg:Password></ecg:Login>');
const sessionId = '...extracted from loginXml...';

// ParcelInBox — extract parcel IDs from XML
const inboxXml = await soapCall('ParcelInBox',
  `<ecg:ParcelInBox><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:ParcelInBox>`);

// For each parcel: ParcelDownload → save → ParcelDownloadConfirm → Logout
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — SOAP parcel download workflow (before migration)
import requests, base64

endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"
ns = "http://www.ecgridos.net/"

def soap_call(action, body):
    env = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:ecg="' + ns + '">'
        '<soap:Body>' + body + '</soap:Body></soap:Envelope>'
    )
    return requests.post(endpoint, data=env.encode(), headers={
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f'"{ns}{action}"'
    })

# Login — extract session_id from XML
login = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>pass</ecg:Password></ecg:Login>")
session_id = "...extracted from login.text..."

# ParcelInBox, ParcelDownload, ParcelDownloadConfirm, Logout follow the same pattern
```

</TabItem>
</Tabs>

### REST — after

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — get inbox list
curl -s -X POST https://rest.ecgrid.io/v2/parcels/pending-inbox-list \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"mailboxId":0,"pageNo":1,"recordsPerPage":25}' | jq .

# Step 2 — download a parcel (replace PARCEL_ID)
curl -s -X POST https://rest.ecgrid.io/v2/parcels/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"parcelID\":$PARCEL_ID}" -o "parcel-$PARCEL_ID.edi"

# Step 3 — confirm receipt
curl -s -X POST https://rest.ecgrid.io/v2/parcels/confirm \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"parcelID\":$PARCEL_ID}"
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — REST parcel download workflow (after migration)
// IHttpClientFactory injected via DI; API key pre-configured on the named client

var http = httpClientFactory.CreateClient("ECGrid");

// Step 1 — get the inbox list
var inboxResponse = await http.PostAsJsonAsync("/v2/parcels/pending-inbox-list");

inboxResponse.EnsureSuccessStatusCode();
var inbox = await inboxResponse.Content.ReadFromJsonAsync<ApiResponse<List<ParcelInfo>>>();

foreach (var parcel in inbox!.Data!)
{
    // Step 2 — download
    var downloadResponse = await http.PostAsJsonAsync("/v2/parcels/download",
        new { parcelID = parcel.ParcelID });

    downloadResponse.EnsureSuccessStatusCode();

    var bytes = await downloadResponse.Content.ReadAsByteArrayAsync();
    await File.WriteAllBytesAsync($"{parcel.ParcelID}.edi", bytes);

    // Step 3 — confirm receipt
    await http.PostAsJsonAsync("/v2/parcels/confirm",
        new { parcelID = parcel.ParcelID });
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — REST parcel download workflow (after migration)
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.Files;
import java.nio.file.Path;

var http = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");
String base = "https://rest.ecgrid.io";

// Step 1 — get inbox list
var inboxResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/pending-inbox-list"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"mailboxId\":0,\"pageNo\":1,\"recordsPerPage\":25}"))
    .build(), BodyHandlers.ofString());
// Parse parcel list from inboxResp.body() and iterate...

// Step 2 — download (for each parcelId)
long parcelId = 12345L;
var downloadResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/download"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"parcelID\":" + parcelId + "}"))
    .build(), BodyHandlers.ofByteArray());
Files.write(Path.of("parcel-" + parcelId + ".edi"), downloadResp.body());

// Step 3 — confirm receipt
http.send(HttpRequest.newBuilder()
    .uri(URI.create(base + "/v2/parcels/confirm"))
    .header("Content-Type", "application/json")
    .header("X-API-Key", apiKey)
    .POST(BodyPublishers.ofString("{\"parcelID\":" + parcelId + "}"))
    .build(), BodyHandlers.discarding());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — REST parcel download workflow (after migration)
const apiKey = process.env.ECGRID_API_KEY;
const base = 'https://rest.ecgrid.io';
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — get inbox list
const inboxResp = await fetch(`${base}/v2/parcels/pending-inbox-list`, {
  method: 'POST', headers,
  body: JSON.stringify({ mailboxId: 0, pageNo: 1, recordsPerPage: 25 })
});
const inbox = await inboxResp.json();

for (const parcel of inbox.data ?? []) {
  // Step 2 — download
  const downloadResp = await fetch(`${base}/v2/parcels/download`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
  const bytes = Buffer.from(await downloadResp.arrayBuffer());
  require('fs').writeFileSync(`parcel-${parcel.parcelId}.edi`, bytes);

  // Step 3 — confirm receipt
  await fetch(`${base}/v2/parcels/confirm`, {
    method: 'POST', headers,
    body: JSON.stringify({ parcelID: parcel.parcelId })
  });
}
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — REST parcel download workflow (after migration)
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key, "Content-Type": "application/json"})
base = "https://rest.ecgrid.io"

# Step 1 — get inbox list
inbox = session.post(f"{base}/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0, "pageNo": 1, "recordsPerPage": 25}).json()

for parcel in inbox.get("data", []):
    parcel_id = parcel["parcelId"]

    # Step 2 — download
    data = session.post(f"{base}/v2/parcels/download",
        json={"parcelID": parcel_id}).content
    with open(f"parcel-{parcel_id}.edi", "wb") as f:
        f.write(data)

    # Step 3 — confirm receipt
    session.post(f"{base}/v2/parcels/confirm", json={"parcelID": parcel_id})
```

</TabItem>
</Tabs>

Key differences:
- No `Login()` / `Logout()` — API key is set once on the `HttpClient`
- JSON bodies instead of strongly-typed proxy parameters
- Standard `HttpResponseMessage` error handling instead of SOAP Faults

---

## Error Handling Migration

**SOAP — catch FaultException:**

```csharp
catch (FaultException fault)
{
    Console.Error.WriteLine($"SOAP Fault: {fault.Message}");
}
```

**REST — check HTTP status and parse JSON error:**

```csharp
if (!response.IsSuccessStatusCode)
{
    var error = await response.Content.ReadFromJsonAsync<ApiError>();
    Console.Error.WriteLine($"[{error?.ErrorCode}] {error?.Message}");
}
```

See [Error Handling & Troubleshooting](./error-handling-troubleshooting.md) for full patterns.

---

## Related

- [REST vs SOAP — Choosing the Right API](./rest-vs-soap.md)
- [Authentication & Session Management](./authentication.md)
- [Error Handling & Troubleshooting](./error-handling-troubleshooting.md)
- [REST API Overview](../rest-api/overview.md)
- [Common Operations — Poll Inbound Files](../common-operations/poll-inbound-files.md)
- [Common Operations — Download a File](../common-operations/download-a-file.md)
