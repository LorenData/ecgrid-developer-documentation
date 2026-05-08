---
title: Authentication & Session Management
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created authentication and session management guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs to REST and SOAP auth examples - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Authentication & Session Management

ECGrid supports two separate authentication models — one for the REST API and one for the SOAP API. This guide covers both in depth, including C# examples for each pattern.

## REST Authentication

The REST API (v2.6) supports two credential types. You can use either within the same integration.

### API Key (Recommended for Server-to-Server)

An API key is a persistent credential that does not expire unless explicitly revoked. It is the best choice for automated, server-to-server workflows such as scheduled file polling or batch processing.

Pass the key in the `X-API-Key` request header on every call:

```http
GET /v2/mailboxes/12345 HTTP/1.1
Host: rest.ecgrid.io
X-API-Key: your-api-key-here
```

:::tip
API keys are long-lived and should be stored in environment variables or a secrets manager — never in source code. See `IConfiguration` usage in the C# examples below.
:::

To retrieve or generate your API key, use:

- `GET /v2/users/{userID}/api-key` — retrieve an existing key
- `POST /v2/users/{userID}/generate-api-key` — generate a new key

### Bearer JWT (Short-Lived Token)

A Bearer JWT is issued in exchange for credentials via `POST /v2/auth/login`. Tokens are short-lived and must be refreshed. This pattern is appropriate for user-facing flows where you need a time-bounded credential.

**Step 1 — Login to obtain a token:**

```http
POST /v2/auth/login HTTP/1.1
Host: rest.ecgrid.io
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "YourPassword1!"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
    "expiresAt": "2026-05-07T18:00:00Z"
  }
}
```

**Step 2 — Use the token in subsequent requests:**

```http
GET /v2/mailboxes/12345 HTTP/1.1
Host: rest.ecgrid.io
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Step 3 — Refresh before expiry:**

```http
POST /v2/auth/refresh HTTP/1.1
Host: rest.ecgrid.io
Content-Type: application/json

{
  "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

**Step 4 — Validate the current session:**

```http
POST /v2/auth/session HTTP/1.1
Host: rest.ecgrid.io
X-API-Key: your-api-key-here
```

Returns the current session's context (user, mailbox, network, auth level).

**Step 5 — Logout to invalidate the session:**

```http
POST /v2/auth/logout HTTP/1.1
Host: rest.ecgrid.io
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### REST C# Example — API Key

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# API key in X-API-Key header — set once, reuse on every request
curl -s \
  -H "X-API-Key: $ECGRID_API_KEY" \
  https://rest.ecgrid.io/v2/mailboxes/12345 | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — IHttpClientFactory with API key loaded from IConfiguration
// API key is never hardcoded; it is read from environment or appsettings.json

using Microsoft.Extensions.Configuration;
using System.Net.Http.Json;

var config = new ConfigurationBuilder()
    .AddEnvironmentVariables()
    .AddJsonFile("appsettings.json", optional: true)
    .Build();

var apiKey = config["ECGrid:ApiKey"]
    ?? throw new InvalidOperationException("ECGrid:ApiKey is not configured.");

// In a real app, inject IHttpClientFactory via DI instead
var factory = /* injected IHttpClientFactory */;
var http = factory.CreateClient("ECGrid");
http.DefaultRequestHeaders.Add("X-API-Key", apiKey);
http.BaseAddress = new Uri("https://rest.ecgrid.io");

var mailbox = await http.GetFromJsonAsync<ApiResponse<MailboxInfo>>("/v2/mailboxes/12345");
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — X-API-Key header on every request
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;

var client = HttpClient.newHttpClient();
String apiKey = System.getenv("ECGRID_API_KEY");

var request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/mailboxes/12345"))
    .header("X-API-Key", apiKey)
    .GET()
    .build();

var response = client.send(request, BodyHandlers.ofString());
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — X-API-Key header on every request
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/mailboxes/12345', {
  headers: { 'X-API-Key': apiKey }
});

const data = await response.json();
console.log(data);
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

resp = session.get("https://rest.ecgrid.io/v2/mailboxes/12345")
resp.raise_for_status()
print(resp.json())
```

</TabItem>
</Tabs>

### REST C# Example — Bearer JWT

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — login to obtain a Bearer token
TOKEN=$(curl -s -X POST https://rest.ecgrid.io/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"YourPassword1!"}' \
  | jq -r '.data.token')

# Step 2 — use the token in subsequent requests
curl -s -H "Authorization: Bearer $TOKEN" \
  -X POST https://rest.ecgrid.io/v2/auth/session | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — obtain a JWT, use it, then refresh
using System.Net.Http.Json;

record LoginRequest(string Email, string Password);
record LoginData(string Token, string RefreshToken, DateTimeOffset ExpiresAt);
record ApiResponse<T>(bool Success, T? Data, string? ErrorCode, string? Message);

var http = httpClientFactory.CreateClient("ECGrid");
http.BaseAddress = new Uri("https://rest.ecgrid.io");

// Login
var loginResponse = await http.PostAsJsonAsync("/v2/auth/login",
    new LoginRequest(email, password));

loginResponse.EnsureSuccessStatusCode();

var loginResult = await loginResponse.Content
    .ReadFromJsonAsync<ApiResponse<LoginData>>();

var token = loginResult!.Data!.Token;

// Use the token
http.DefaultRequestHeaders.Authorization =
    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

var session = await http.PostAsync("/v2/auth/session", null);
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — login then use Bearer token
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();

// Step 1 — login
String loginBody = "{\"email\":\"user@example.com\",\"password\":\"YourPassword1!\"}";
var loginReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/login"))
    .header("Content-Type", "application/json")
    .POST(BodyPublishers.ofString(loginBody))
    .build();

var loginResp = http.send(loginReq, BodyHandlers.ofString());
// Parse token from loginResp.body() using a JSON library
String token = "...extracted from JSON...";

// Step 2 — use the token
var req = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/session"))
    .header("Authorization", "Bearer " + token)
    .POST(BodyPublishers.noBody())
    .build();
var resp = http.send(req, BodyHandlers.ofString());
System.out.println(resp.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — login then use Bearer token
// Step 1 — login
const loginResp = await fetch('https://rest.ecgrid.io/v2/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'YourPassword1!' })
});
const loginData = await loginResp.json();
const token = loginData.data.token;

// Step 2 — use the token
const resp = await fetch('https://rest.ecgrid.io/v2/auth/session', {
  method: 'POST',
  headers: { Authorization: `Bearer ${token}` }
});
console.log(await resp.json());
```

</TabItem>
<TabItem value="python" label="Python">

```python
import requests

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

# Step 1 — login
login = session.post(
    "https://rest.ecgrid.io/v2/auth/login",
    json={"email": "user@example.com", "password": "YourPassword1!"}
)
login.raise_for_status()
token = login.json()["data"]["token"]

# Step 2 — use the token
session.headers.update({"Authorization": f"Bearer {token}"})
resp = session.post("https://rest.ecgrid.io/v2/auth/session")
print(resp.json())
```

</TabItem>
</Tabs>

---

## SOAP Authentication

The SOAP API uses a stateful session model. Every method call requires a `SessionID` string obtained from `Login()`. Your API Key can be use in place of the `SessionID` for automated, server-to-server workflows. You do not need to `Login()` if you use your API Key you can make the calls dircetly.

### Login

Call `Login()` with your ECGrid email and password to receive a `SessionID`:

```csharp
// .NET 10 — dotnet-svcutil generated proxy
var client = new ECGridOSPortTypeClient();

string sessionID = await client.LoginAsync(email, password);
// sessionID is now valid for subsequent calls
```

The `SessionID` is a short alphanumeric string. Pass it as the first argument to every subsequent method:

```csharp
var parcelList = await client.ParcelInBoxAsync(sessionID, mailboxID, beginDate, endDate);
var networkInfo = await client.NetworkInfoAsync(sessionID, networkID);
```

### Session Lifespan

SOAP sessions expire after a period of inactivity. For long-running processes, either:

- Reuse a persistent API key (available via `UserGetAPIKeyAsync()`)
- Re-login if a session-expired SOAP fault is received

### SessionInfo and SessionLog

You can inspect the current session with `SessionInfo()`:

```csharp
var info = await client.SessionInfoAsync(sessionID);
// Returns user, mailbox, network, auth level, and expiry time
```

Review recent session activity with `SessionLog()`:

```csharp
var log = await client.SessionLogAsync(sessionID, beginDate, endDate);
```

### Logout

Always call `Logout()` when the session is no longer needed to release server-side resources:

```csharp
await client.LogoutAsync(sessionID);
```

### SOAP C# Example — Full Session Lifecycle

<Tabs groupId="lang">
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — dotnet-svcutil generated proxy, full session lifecycle
using var client = new ECGridOSPortTypeClient();

var sessionID = string.Empty;
try
{
    // Authenticate — credentials from IConfiguration
    sessionID = await client.LoginAsync(
        config["ECGrid:Email"]!,
        config["ECGrid:Password"]!);

    // Use the session
    var mailbox = await client.MailboxInfoAsync(sessionID, mailboxID);
    Console.WriteLine($"Mailbox: {mailbox.MailboxName}");
}
finally
{
    // Always logout, even on exception
    if (!string.IsNullOrEmpty(sessionID))
        await client.LogoutAsync(sessionID);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — SOAP Login → MailboxInfo → Logout
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;

var http = HttpClient.newHttpClient();
String endpoint = "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx";
String ns = "http://www.ecgridos.net/";

// Login
String loginEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Login>"
    + "<ecg:Email>user@example.com</ecg:Email>"
    + "<ecg:Password>YourPassword1!</ecg:Password>"
    + "</ecg:Login></soap:Body></soap:Envelope>";

var loginResp = http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Login\"")
    .POST(BodyPublishers.ofString(loginEnv)).build(), BodyHandlers.ofString());

// Extract sessionId from loginResp.body() using an XML parser
String sessionId = "...extracted...";

// Use sessionId for subsequent calls (e.g., MailboxInfo), then Logout
String logoutEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Logout><ecg:SessionID>" + sessionId + "</ecg:SessionID></ecg:Logout></soap:Body></soap:Envelope>";

http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Logout\"")
    .POST(BodyPublishers.ofString(logoutEnv)).build(), BodyHandlers.ofString());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP Login → MailboxInfo → Logout
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

// Login — extract SessionID from the XML response
const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>YourPassword1!</ecg:Password></ecg:Login>');

const sessionId = '...extracted from loginXml...';

// Use sessionId for subsequent calls, then Logout
await soapCall('Logout', `<ecg:Logout><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:Logout>`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
# Python — SOAP Login → MailboxInfo → Logout
import requests

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

# Login — extract session_id from XML response
login_resp = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>YourPassword1!</ecg:Password></ecg:Login>")
session_id = "...extracted from login_resp.text..."

# Use session_id for subsequent calls, then Logout
soap_call("Logout", f"<ecg:Logout><ecg:SessionID>{session_id}</ecg:SessionID></ecg:Logout>")
```

</TabItem>
</Tabs>

---

## Best Practices

| Scenario | Recommended approach |
|---|---|
| Scheduled file polling | REST with API key — stateless, no session management |
| Batch processing service | REST with API key — long-lived, no expiry |
| User-facing web application | REST with Bearer JWT — scoped to user session |
| Existing SOAP integration | SOAP SessionID — minimize changes until migration |
| Migrating SOAP to REST | Swap `Login()` / `SessionID` for `X-API-Key` header |

:::note Password Requirements
Both APIs enforce the same password pattern: at least one uppercase letter, one lowercase letter, one digit, and one special character.
:::

## Related

- [REST vs SOAP — Choosing the Right API](./rest-vs-soap.md)
- [REST Auth — Login](../rest-api/auth/login.md)
- [REST Auth — Refresh Token](../rest-api/auth/refresh-token.md)
- [REST Auth — Session](../rest-api/auth/session.md)
- [SOAP Auth — Login](../soap-api/auth/login.md)
- [SOAP Auth — Session Info](../soap-api/auth/session-info.md)
