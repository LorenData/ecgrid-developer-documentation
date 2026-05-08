---
title: Authentication & API Keys
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create authentication and API keys page - Greg Kolinski
    | 2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
    | 2026-05-08: Merge authentication-api-keys and authentication-session-management into one page - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Authentication & API Keys

ECGrid supports two separate authentication models — one for the REST API and one for the SOAP API. This page covers both in depth, including credential types, session lifecycle, and code examples for each pattern.

## REST Authentication

The REST API (v2.6) supports two credential types. You can use either within the same integration.

### Method 1 — API Key (Recommended)

An API key is a persistent credential tied to a specific ECGrid User account. It does not expire unless explicitly revoked and is the best choice for automated, server-to-server workflows such as scheduled file polling or batch processing.

Pass the key in the `X-API-Key` request header on every call:

```http
GET /v2/parcels/inbox-list HTTP/1.1
Host: rest.ecgrid.io
X-API-Key: your-api-key-here
```

:::tip
API keys are long-lived. Store them in environment variables or a secrets manager — never in source code or client-side code. See `IConfiguration` usage in the C# examples below.
:::

**Obtaining an API key:**

1. **ECGrid Portal** — Log in and navigate to your user profile to generate or retrieve your key.
2. **REST API** — Call `GET /v2/users/key/{userID}` with an existing authenticated session. See [Get API Key](../rest-api/users/get-api-key.md).

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Pass X-API-Key on every request
curl -X POST "https://rest.ecgrid.io/v2/parcels/pending-inbox-list" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mailboxId": 0}'
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
// Load the API key from configuration — never hardcode credentials
// IHttpClientFactory is injected; do not use new HttpClient() in production code
public class EcGridRestClient
{
    private readonly HttpClient _http;

    public EcGridRestClient(IHttpClientFactory httpClientFactory, IConfiguration config)
    {
        _http = httpClientFactory.CreateClient("ecgrid");

        var apiKey = config["ECGrid:ApiKey"]
            ?? throw new InvalidOperationException("ECGrid:ApiKey is not configured.");

        _http.DefaultRequestHeaders.Add("X-API-Key", apiKey);
        _http.BaseAddress = new Uri("https://rest.ecgrid.io");
    }

    public async Task<HttpResponseMessage> GetAsync(string path)
        => await _http.GetAsync(path);
}
```

Register the named client in `Program.cs`:

```csharp
builder.Services.AddHttpClient("ecgrid", client =>
{
    client.BaseAddress = new Uri("https://rest.ecgrid.io");
});
```

Set the key in `appsettings.json` (or override via environment variable):

```json
{
  "ECGrid": {
    "ApiKey": ""
  }
}
```

```bash
# .NET environment variable override
export ECGrid__ApiKey="your-api-key-here"
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

// Apply the API key to every request via a shared client helper
String apiKey = System.getenv("ECGRID_API_KEY");

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/pending-inbox-list"))
    .header("X-API-Key", apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString("{\"mailboxId\": 0}"))
    .build();

HttpResponse<String> response = client.send(
    request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
const apiKey = process.env.ECGRID_API_KEY;

const response = await fetch('https://rest.ecgrid.io/v2/parcels/pending-inbox-list', {
  method: 'POST',
  headers: {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ mailboxId: 0 }),
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

response = session.post(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0},
)
response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

---

### Method 2 — Bearer JWT (Short-Lived Token)

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
GET /v2/parcels/inbox-list HTTP/1.1
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

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — obtain a token
TOKEN=$(curl -s -X POST "https://rest.ecgrid.io/v2/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"YourPassword1!"}' \
  | jq -r '.data.token')

# Step 2 — use the token on subsequent calls
curl -X POST "https://rest.ecgrid.io/v2/parcels/pending-inbox-list" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mailboxId": 0}'
```

</TabItem>
<TabItem value="csharp" label="C#">

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

# Step 1 — login
login = session.post(
    "https://rest.ecgrid.io/v2/auth/login",
    json={"email": "user@example.com", "password": "YourPassword1!"}
)
login.raise_for_status()
token = login.json()["data"]["token"]

# Step 2 — use the token on subsequent calls
session.headers.update({"Authorization": f"Bearer {token}"})
resp = session.post("https://rest.ecgrid.io/v2/auth/session")
print(resp.json())
```

</TabItem>
</Tabs>

---

## SOAP Authentication

The SOAP API uses a stateful session model. Every method call requires a `SessionID` string obtained from `Login()`. Your API Key can be used in place of the `SessionID` for automated, server-to-server workflows — you do not need to call `Login()` when using your API Key directly.

### Login

Call `Login()` with your ECGrid email and password to receive a `SessionID`:

```csharp
// .NET 10 — dotnet-svcutil generated proxy
var client = new ECGridOSPortTypeClient();

string sessionID = await client.LoginAsync(email, password);
// sessionID is now valid for subsequent calls
```

Pass the `SessionID` as the first argument to every subsequent method:

```csharp
var parcelList = await client.ParcelInBoxAsync(sessionID, mailboxID, beginDate, endDate);
var networkInfo = await client.NetworkInfoAsync(sessionID, networkID);
```

### Session Lifespan

SOAP sessions expire after a period of inactivity. For long-running processes, either:

- Use a persistent API key (available via `UserGetAPIKeyAsync()`)
- Re-login when a session-expired SOAP fault is received

### SessionInfo and SessionLog

Inspect the current session with `SessionInfo()`:

```csharp
var info = await client.SessionInfoAsync(sessionID);
// Returns user, mailbox, network, auth level, and expiry time
```

Review recent activity with `SessionLog()`:

```csharp
var log = await client.SessionLogAsync(sessionID, beginDate, endDate);
```

### Logout

Always call `Logout()` when the session is no longer needed:

```csharp
await client.LogoutAsync(sessionID);
```

### SOAP Full Session Lifecycle

<Tabs groupId="lang">
<TabItem value="csharp" label="C#">

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

// Use sessionId for subsequent calls, then Logout
String logoutEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ecg=\""
    + ns + "\">"
    + "<soap:Body><ecg:Logout><ecg:SessionID>" + sessionId
    + "</ecg:SessionID></ecg:Logout></soap:Body></soap:Envelope>";

http.send(HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"" + ns + "Logout\"")
    .POST(BodyPublishers.ofString(logoutEnv)).build(), BodyHandlers.ofString());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
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

const loginXml = await soapCall('Login',
  '<ecg:Login><ecg:Email>user@example.com</ecg:Email><ecg:Password>YourPassword1!</ecg:Password></ecg:Login>');

const sessionId = '...extracted from loginXml...';

await soapCall('Logout', `<ecg:Logout><ecg:SessionID>${sessionId}</ecg:SessionID></ecg:Logout>`);
```

</TabItem>
<TabItem value="python" label="Python">

```python
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

login_resp = soap_call("Login",
    "<ecg:Login><ecg:Email>user@example.com</ecg:Email>"
    "<ecg:Password>YourPassword1!</ecg:Password></ecg:Login>")
session_id = "...extracted from login_resp.text..."

soap_call("Logout", f"<ecg:Logout><ecg:SessionID>{session_id}</ecg:SessionID></ecg:Logout>")
```

</TabItem>
</Tabs>

---

## Password Requirements

All ECGrid passwords must satisfy:

```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$
```

At least one lowercase letter, one uppercase letter, one digit, and one special character. No maximum length.

---

## Best Practices

| Scenario | Recommended approach |
|---|---|
| Scheduled file polling | REST with API key — stateless, no session management |
| Batch processing service | REST with API key — long-lived, no expiry |
| User-facing web application | REST with Bearer JWT — scoped to user session |
| Existing SOAP integration | SOAP SessionID — minimize changes until migration |
| Migrating SOAP to REST | Swap `Login()` / `SessionID` for `X-API-Key` header |

## Environment Variable Reference

| Variable | Description |
|---|---|
| `ECGrid__ApiKey` | API key for `X-API-Key` header authentication |
| `ECGrid__Email` | User email for Bearer JWT or SOAP login |
| `ECGrid__Password` | User password for Bearer JWT or SOAP login |

:::note
The double-underscore (`__`) is the standard .NET environment variable delimiter for nested configuration keys (equivalent to `ECGrid:ApiKey` in JSON).
:::

## See Also

- [Login](../rest-api/auth/login.md) — `POST /v2/auth/login`
- [Refresh Token](../rest-api/auth/refresh-token.md) — extend a Bearer session
- [Get API Key](../rest-api/users/get-api-key.md) — retrieve your API key via REST
- [Generate API Key](../rest-api/users/generate-api-key.md) — rotate your API key
- [SOAP Auth — Login](../soap-api/auth/login.md) — `Login()` / `Logout()` for SOAP
- [REST vs SOAP](./rest-vs-soap.md) — choosing the right API
