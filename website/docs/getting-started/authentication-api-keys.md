---
title: Authentication & API Keys
sidebar_position: 2
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create authentication and API keys page - Greg Kolinski
    2026-05-07: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski */}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Authentication & API Keys

The ECGrid REST API supports two authentication methods: a long-lived **API Key** for server-to-server integrations, and a short-lived **Bearer JWT** for interactive or session-scoped access. Choose the method that fits your use case; both are accepted on every authenticated endpoint.

For SOAP authentication, see [SOAP Authentication](../soap-api/auth/login.md).

## Method 1 — API Key (Recommended)

An API Key is a stable credential tied to a specific ECGrid User account. Pass it in the `X-API-Key` request header on every call.

```http
GET /v2/parcels/inbox-list
X-API-Key: your-api-key-here
```

API keys do not expire automatically. They are best suited for:

- Automated server processes and scheduled jobs
- Daemon/worker service integrations
- CI/CD pipelines and integration testing

### Obtaining an API Key

You can obtain an API key in two ways:

1. **ECGrid Portal** — Log in to the ECGrid portal and navigate to your user profile to generate or retrieve your key.
2. **REST API** — Call `GET /v2/users/key/{userID}` with an existing authenticated session. See the [Get API Key](../rest-api/users/get-api-key.md) reference page.

:::caution
Treat your API key like a password. Never commit it to source control, include it in client-side code, or log it. Load it from `IConfiguration` or an environment variable at runtime.
:::

## Method 2 — Bearer JWT

A Bearer JWT (JSON Web Token) is a short-lived token obtained by calling the login endpoint with your username and password. Pass it in the `Authorization` header.

```http
POST /v2/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "YourPassword1!"
}
```

The response returns a token:

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJSUzI1NiIs...",
    "expires": "2026-05-07T18:00:00Z"
  }
}
```

Use the token in subsequent requests:

```http
GET /v2/parcels/inbox-list
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

Bearer tokens are best suited for:

- Interactive applications where a user logs in
- Short-duration automation sessions
- Scenarios where you want token expiration as a security boundary

See [Login](../rest-api/auth/login.md) and [Refresh Token](../rest-api/auth/refresh-token.md) for full endpoint details.

## Password Requirements

All ECGrid passwords must satisfy the following pattern:

```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).+$
```

In plain terms: at least one lowercase letter, one uppercase letter, one digit, and one special character. There is no maximum length restriction.

## Code Examples

### API Key Authentication

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

        // Set the API key on the shared HttpClient instance at construction time
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

// Pass the API key header on every call
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

# Include the API key in every call via a session
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

### Bearer JWT Authentication

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
// Authenticate with username and password, then use the returned token
public async Task<string> GetBearerTokenAsync(
    IHttpClientFactory httpClientFactory,
    IConfiguration config)
{
    var http = httpClientFactory.CreateClient("ecgrid-anon");

    var credentials = new
    {
        email = config["ECGrid:Email"],
        password = config["ECGrid:Password"]
    };

    var response = await http.PostAsJsonAsync("/v2/auth/login", credentials);
    response.EnsureSuccessStatusCode();

    using var doc = await JsonDocument.ParseAsync(
        await response.Content.ReadAsStreamAsync());

    return doc.RootElement
        .GetProperty("data")
        .GetProperty("token")
        .GetString()
        ?? throw new InvalidOperationException("Login response did not contain a token.");
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
import java.net.URI;
import java.net.http.*;

HttpClient client = HttpClient.newHttpClient();

// Step 1 — obtain a Bearer token
HttpRequest loginRequest = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/auth/login"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(
        "{\"email\":\"user@example.com\",\"password\":\"YourPassword1!\"}"))
    .build();

HttpResponse<String> loginResp = client.send(
    loginRequest, HttpResponse.BodyHandlers.ofString());

// Extract the token — use Jackson or Gson in production
String token = loginResp.body().split("\"token\":\"")[1].split("\"")[0];

// Step 2 — use the token
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/parcels/pending-inbox-list"))
    .header("Authorization", "Bearer " + token)
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
// Step 1 — obtain a Bearer token
const loginRes = await fetch('https://rest.ecgrid.io/v2/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'YourPassword1!' }),
});
const { data: { token } } = await loginRes.json();

// Step 2 — use the token on subsequent calls
const response = await fetch('https://rest.ecgrid.io/v2/parcels/pending-inbox-list', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
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
import requests

# Step 1 — obtain a Bearer token
login = requests.post(
    "https://rest.ecgrid.io/v2/auth/login",
    json={"email": "user@example.com", "password": "YourPassword1!"},
)
login.raise_for_status()
token = login.json()["data"]["token"]

# Step 2 — use the token on subsequent calls
response = requests.post(
    "https://rest.ecgrid.io/v2/parcels/pending-inbox-list",
    json={"mailboxId": 0},
    headers={"Authorization": f"Bearer {token}"},
)
response.raise_for_status()
print(response.json())
```

</TabItem>
</Tabs>

## Environment Variable Reference

| Variable | Description |
|---|---|
| `ECGrid__ApiKey` | API key for `X-API-Key` header authentication |
| `ECGrid__Email` | User email for Bearer JWT login |
| `ECGrid__Password` | User password for Bearer JWT login |

:::note
The double-underscore (`__`) is the standard .NET environment variable delimiter for nested configuration keys (equivalent to `ECGrid:ApiKey` in JSON).
:::

## See Also

- [Login](../rest-api/auth/login.md) — `POST /v2/auth/login`
- [Refresh Token](../rest-api/auth/refresh-token.md) — extend a Bearer session
- [Get API Key](../rest-api/users/get-api-key.md) — retrieve your API key via the REST API
- [Generate API Key](../rest-api/users/generate-api-key.md) — rotate your API key
- [SOAP Authentication](../soap-api/auth/login.md) — `Login()` / `Logout()` for SOAP
