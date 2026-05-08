---
title: Manage Users and Permissions
sidebar_position: 11
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Create manage-users-permissions common operations guide - Greg Kolinski 
| 2026-05-08: Add multi-language code tabs (cURL, C#, Java, Node.js, Python) - Greg Kolinski
*/}

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


# Manage Users and Permissions

Create user accounts and assign the appropriate authorization level to control what each user can see and do within ECGrid.

## Overview

ECGrid uses a role-based permission model built around the `AuthLevel` enum. Each user account is assigned one level that determines which API operations and administrative functions they can perform. Levels range from `General` (read-only visibility) up through `Root` (full system access). In most integrations, application service accounts are assigned `MailboxAdmin` or `NetworkAdmin` depending on their scope.

Sequence:
1. Create the user with `POST /v2/users`.
2. Set the user's authorization level with `POST /v2/users/role`.
3. Optionally list users with `POST /v2/users/list` to verify.

---

## REST

**Auth:** `X-API-Key: <key>` header

### Step 1 — Create a user

```http
POST https://rest.ecgrid.io/v2/users
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "networkId": 0,
  "mailboxId": 54321,
  "loginName": "jsmith",
  "password": "S3cur3P@ssword!",
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jsmith@example.com",
  "authLevel": "MailboxUser"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `networkId` | integer | No | Network to create the user under. Pass `0` for the API key's default network. |
| `mailboxId` | integer | No | Mailbox to associate with this user. Pass `0` for network-level users. |
| `loginName` | string | Yes | Unique login name (no spaces). |
| `password` | string | Yes | Must satisfy the complexity rule: uppercase, lowercase, digit, and special character. |
| `firstName` | string | Yes | User's first name. |
| `lastName` | string | Yes | User's last name. |
| `email` | string | Yes | Email address for notifications and password resets. |
| `authLevel` | string | No | Initial authorization level. Defaults to `"General"` if omitted. |

**Response:**

```json
{
  "success": true,
  "data": {
    "userId": 20100,
    "loginName": "jsmith",
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "jsmith@example.com",
    "authLevel": "MailboxUser",
    "status": "Active"
  }
}
```

### Step 2 — Set the authorization level

Use `POST /v2/users/role` to change a user's `AuthLevel` at any time, including at creation time if you want to set a different level than the default.

```http
POST https://rest.ecgrid.io/v2/users/role
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

```json
{
  "userId": 20100,
  "authLevel": "MailboxAdmin"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `userId` | integer | Yes | The user ID returned from Step 1. |
| `authLevel` | string | Yes | New authorization level. See [AuthLevel values](#authlevel-values) below. |

**Response:**

```json
{
  "success": true,
  "data": {
    "userId": 20100,
    "authLevel": "MailboxAdmin"
  }
}
```

#### AuthLevel Values

Levels are listed from highest privilege to lowest. A user can only perform actions at or below their assigned level.

| AuthLevel | Scope | Typical Use |
|---|---|---|
| `Root` | System-wide | Loren Data internal — do not assign |
| `TechOps` | System-wide | Loren Data internal — do not assign |
| `NetOps` | System-wide | Loren Data operations — do not assign |
| `NetworkAdmin` | Network | Full administrative access to a network and all its mailboxes |
| `NetworkUser` | Network | Read-only visibility across the network |
| `MailboxAdmin` | Mailbox | Full access to a specific mailbox and its trading partner relationships |
| `MailboxUser` | Mailbox | Standard EDI send/receive access within a mailbox |
| `TPUser` | Trading Partner | Limited access scoped to a specific ECGrid ID |
| `General` | None | Authenticated but no operational access — placeholder or pending setup |

For complete definitions see [Appendix: ENUMs — AuthLevel](../appendix/enums).

### Step 3 — List users to verify

```http
POST https://rest.ecgrid.io/v2/users/list
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

Confirm that the new user appears with the expected `authLevel` and `status: "Active"`.

### Code Examples

<Tabs groupId="lang">
<TabItem value="curl" label="cURL">

```bash
# Step 1 — create the user
curl -s -X POST https://rest.ecgrid.io/v2/users \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d '{"networkId":0,"mailboxId":54321,"loginName":"jsmith","password":"S3cur3P@ssword!","firstName":"Jane","lastName":"Smith","email":"jsmith@example.com","authLevel":"General"}' | jq .

# Step 2 — set the authorization level (replace USER_ID with userId from step 1)
curl -s -X POST https://rest.ecgrid.io/v2/users/role \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ECGRID_API_KEY" \
  -d "{\"userId\":$USER_ID,\"authLevel\":\"MailboxAdmin\"}" | jq .
```

</TabItem>
<TabItem value="csharp" label="C#" default>

```csharp
// .NET 10 — create a user and assign a role using IHttpClientFactory (registered as "ECGrid")
// API key loaded from IConfiguration — never hardcoded
// Password loaded from IConfiguration — never hardcoded

using System.Net.Http.Json;

public record CreateUserRequest(
    int NetworkId,
    int MailboxId,
    string LoginName,
    string Password,
    string FirstName,
    string LastName,
    string Email,
    string AuthLevel);

public record SetRoleRequest(
    int UserId,
    string AuthLevel);

public record UserInfo(
    int UserId,
    string LoginName,
    string FirstName,
    string LastName,
    string Email,
    string AuthLevel,
    string Status);

public record ApiResponse<T>(bool Success, T Data);

public class ECGridUserService
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly IConfiguration _configuration;
    private readonly ILogger<ECGridUserService> _logger;

    public ECGridUserService(
        IHttpClientFactory httpClientFactory,
        IConfiguration configuration,
        ILogger<ECGridUserService> logger)
    {
        _httpClientFactory = httpClientFactory;
        _configuration    = configuration;
        _logger           = logger;
    }

    /// <summary>
    /// Creates a new ECGrid user and assigns the specified authorization level.
    /// </summary>
    /// <param name="loginName">Unique login name (no spaces).</param>
    /// <param name="firstName">User's first name.</param>
    /// <param name="lastName">User's last name.</param>
    /// <param name="email">Email address for the account.</param>
    /// <param name="authLevel">ECGrid AuthLevel to assign (e.g., "MailboxAdmin").</param>
    /// <param name="mailboxId">Mailbox to scope the user to. Pass 0 for network-level.</param>
    public async Task<UserInfo> CreateUserWithRoleAsync(
        string loginName,
        string firstName,
        string lastName,
        string email,
        string authLevel,
        int mailboxId = 0,
        CancellationToken cancellationToken = default)
    {
        var http = _httpClientFactory.CreateClient("ECGrid");

        // Load the initial password from configuration — do not hardcode
        string initialPassword = _configuration["ECGrid:NewUserPassword"]
            ?? throw new InvalidOperationException(
                "ECGrid:NewUserPassword is not configured. " +
                "Set it in appsettings or environment variables.");

        // Step 1 — create the user
        var createRequest = new CreateUserRequest(
            NetworkId:  0,
            MailboxId:  mailboxId,
            LoginName:  loginName,
            Password:   initialPassword,
            FirstName:  firstName,
            LastName:   lastName,
            Email:      email,
            AuthLevel:  "General");   // start at General, elevate below

        var createResponse = await http.PostAsJsonAsync(
            "/v2/users", createRequest, cancellationToken);
        createResponse.EnsureSuccessStatusCode();

        var createResult = await createResponse.Content
            .ReadFromJsonAsync<ApiResponse<UserInfo>>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("Empty response from user create.");

        _logger.LogInformation(
            "User created: ID={UserId} Login={Login}",
            createResult.Data.UserId, createResult.Data.LoginName);

        // Step 2 — elevate to the desired role
        var roleRequest = new SetRoleRequest(createResult.Data.UserId, authLevel);

        var roleResponse = await http.PostAsJsonAsync(
            "/v2/users/role", roleRequest, cancellationToken);
        roleResponse.EnsureSuccessStatusCode();

        _logger.LogInformation(
            "Role set: UserId={UserId} AuthLevel={AuthLevel}",
            createResult.Data.UserId, authLevel);

        // Return updated user info
        var verify = await http.GetFromJsonAsync<ApiResponse<UserInfo>>(
            $"/v2/users/{createResult.Data.UserId}", cancellationToken)
            ?? throw new InvalidOperationException("Could not retrieve user after role assignment.");

        return verify.Data;
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
// Java 11+ — create user then set authorization level
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

var http   = HttpClient.newHttpClient();
String key = System.getenv("ECGRID_API_KEY");
var mapper = new ObjectMapper();

// Step 1 — create user
String createBody = "{\"networkId\":0,\"mailboxId\":54321,\"loginName\":\"jsmith\","
    + "\"password\":\"S3cur3P@ssword!\",\"firstName\":\"Jane\",\"lastName\":\"Smith\","
    + "\"email\":\"jsmith@example.com\",\"authLevel\":\"General\"}";

var createReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(createBody)).build();
var createResp = http.send(createReq, BodyHandlers.ofString());
int userId = mapper.readTree(createResp.body()).path("data").path("userId").asInt();
System.out.println("User created: ID=" + userId);

// Step 2 — set role
String roleBody = "{\"userId\":" + userId + ",\"authLevel\":\"MailboxAdmin\"}";
var roleReq = HttpRequest.newBuilder()
    .uri(URI.create("https://rest.ecgrid.io/v2/users/role"))
    .header("Content-Type", "application/json").header("X-API-Key", key)
    .POST(BodyPublishers.ofString(roleBody)).build();
http.send(roleReq, BodyHandlers.ofString());
System.out.println("AuthLevel set to MailboxAdmin");
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — create user then set authorization level
const apiKey  = process.env.ECGRID_API_KEY;
const headers = { 'Content-Type': 'application/json', 'X-API-Key': apiKey };

// Step 1 — create user
const createResp = await fetch('https://rest.ecgrid.io/v2/users', {
  method: 'POST', headers,
  body: JSON.stringify({
    networkId: 0, mailboxId: 54321, loginName: 'jsmith',
    password: process.env.NEW_USER_PASSWORD,
    firstName: 'Jane', lastName: 'Smith',
    email: 'jsmith@example.com', authLevel: 'General'
  })
});
const { data: user } = await createResp.json();
console.log(`User created: ID=${user.userId}`);

// Step 2 — set role
await fetch('https://rest.ecgrid.io/v2/users/role', {
  method: 'POST', headers,
  body: JSON.stringify({ userId: user.userId, authLevel: 'MailboxAdmin' })
});
console.log('AuthLevel set to MailboxAdmin');
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

api_key = os.environ["ECGRID_API_KEY"]
session = requests.Session()
session.headers.update({"X-API-Key": api_key})

# Step 1 — create user
create = session.post("https://rest.ecgrid.io/v2/users", json={
    "networkId": 0, "mailboxId": 54321, "loginName": "jsmith",
    "password": os.environ["NEW_USER_PASSWORD"],
    "firstName": "Jane", "lastName": "Smith",
    "email": "jsmith@example.com", "authLevel": "General"
})
create.raise_for_status()
user_id = create.json()["data"]["userId"]
print(f"User created: ID={user_id}")

# Step 2 — set role
role = session.post("https://rest.ecgrid.io/v2/users/role",
                    json={"userId": user_id, "authLevel": "MailboxAdmin"})
role.raise_for_status()
print("AuthLevel set to MailboxAdmin")
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

builder.Services.AddScoped<ECGridUserService>();
```

:::caution Password Security
Never hardcode passwords in source code or configuration files committed to source control. Load the initial password from environment variables or a secrets manager (e.g., Azure Key Vault, AWS Secrets Manager, .NET User Secrets for local development).
:::

---

## SOAP

:::caution Established API
The SOAP API is in maintenance mode. For new integrations use REST above.
:::

**Methods:**
- `UserAdd(SessionID, NetworkID, MailboxID, LoginName, Password, ...)` — create a user
- `UserSetAuthLevel(SessionID, UserID, AuthLevel)` — assign the authorization level

### Step 1 — Log in and get a session ID

```csharp
var loginResult = await client.LoginAsync(username, password);
string sessionId = loginResult.LoginResult;
```

### Step 2 — Create the user with UserAdd

```csharp
var addResult = await client.UserAddAsync(
    sessionId,
    networkId:  0,
    mailboxId:  54321,
    loginName:  "jsmith",
    password:   Environment.GetEnvironmentVariable("NEW_USER_PASSWORD")!,
    firstName:  "Jane",
    lastName:   "Smith",
    email:      "jsmith@example.com");

int userId = addResult.UserAddResult.UserID;
Console.WriteLine($"User created: ID={userId}");
```

### Step 3 — Assign the role with UserSetAuthLevel

```csharp
await client.UserSetAuthLevelAsync(
    sessionId,
    userId:    userId,
    authLevel: AuthLevel.MailboxAdmin);

Console.WriteLine($"AuthLevel set to MailboxAdmin for user {userId}");
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

    // Create the user
    var addResult = await client.UserAddAsync(
        sessionId,
        networkId:  0,
        mailboxId:  54321,
        loginName:  "jsmith",
        password:   Environment.GetEnvironmentVariable("NEW_USER_PASSWORD")!,
        firstName:  "Jane",
        lastName:   "Smith",
        email:      "jsmith@example.com");

    int userId = addResult.UserAddResult.UserID;
    Console.WriteLine($"User created: ID={userId}");

    // Assign the authorization level
    await client.UserSetAuthLevelAsync(
        sessionId,
        userId:    userId,
        authLevel: AuthLevel.MailboxAdmin);

    Console.WriteLine("AuthLevel assigned: MailboxAdmin");
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
// Java 11+ — SOAP UserAdd + UserSetAuthLevel via raw HTTP
import java.net.URI;
import java.net.http.*;
import java.net.http.HttpRequest.BodyPublishers;

var http = HttpClient.newHttpClient();
String sessionId = "YOUR_SESSION_ID";
String password  = System.getenv("NEW_USER_PASSWORD");

String addEnv = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    + "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\""
    + " xmlns:ecg=\"http://www.ecgridos.net/\"><soap:Body><ecg:UserAdd>"
    + "<ecg:SessionID>" + sessionId + "</ecg:SessionID>"
    + "<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>"
    + "<ecg:LoginName>jsmith</ecg:LoginName>"
    + "<ecg:Password>" + password + "</ecg:Password>"
    + "<ecg:FirstName>Jane</ecg:FirstName><ecg:LastName>Smith</ecg:LastName>"
    + "<ecg:EMail>jsmith@example.com</ecg:EMail>"
    + "</ecg:UserAdd></soap:Body></soap:Envelope>";

var req = HttpRequest.newBuilder()
    .uri(URI.create("https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx"))
    .header("Content-Type", "text/xml; charset=utf-8")
    .header("SOAPAction", "\"http://www.ecgridos.net/UserAdd\"")
    .POST(BodyPublishers.ofString(addEnv)).build();

var response = http.send(req, HttpResponse.BodyHandlers.ofString());
// Extract UserID from XML, then call UserSetAuthLevel
System.out.println(response.body());
```

</TabItem>
<TabItem value="nodejs" label="Node.js">

```javascript
// Node.js 18+ — SOAP UserAdd + UserSetAuthLevel via raw HTTP
const sessionId = 'YOUR_SESSION_ID';
const password  = process.env.NEW_USER_PASSWORD;

const addEnvelope = `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ecg="http://www.ecgridos.net/">
  <soap:Body><ecg:UserAdd>
    <ecg:SessionID>${sessionId}</ecg:SessionID>
    <ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>
    <ecg:LoginName>jsmith</ecg:LoginName>
    <ecg:Password>${password}</ecg:Password>
    <ecg:FirstName>Jane</ecg:FirstName><ecg:LastName>Smith</ecg:LastName>
    <ecg:EMail>jsmith@example.com</ecg:EMail>
  </ecg:UserAdd></soap:Body>
</soap:Envelope>`;

const response = await fetch('https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx', {
  method: 'POST',
  headers: { 'Content-Type': 'text/xml; charset=utf-8',
             'SOAPAction': '"http://www.ecgridos.net/UserAdd"' },
  body: addEnvelope
});
// Extract UserID from XML, then call UserSetAuthLevel
console.log(await response.text());
```

</TabItem>
<TabItem value="python" label="Python">

```python
import os, requests

session_id = "YOUR_SESSION_ID"  # obtain from Login
password   = os.environ["NEW_USER_PASSWORD"]

envelope = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"'
    ' xmlns:ecg="http://www.ecgridos.net/">'
    '<soap:Body><ecg:UserAdd>'
    '<ecg:SessionID>' + session_id + '</ecg:SessionID>'
    '<ecg:NetworkID>0</ecg:NetworkID><ecg:MailboxID>54321</ecg:MailboxID>'
    '<ecg:LoginName>jsmith</ecg:LoginName>'
    '<ecg:Password>' + password + '</ecg:Password>'
    '<ecg:FirstName>Jane</ecg:FirstName><ecg:LastName>Smith</ecg:LastName>'
    '<ecg:EMail>jsmith@example.com</ecg:EMail>'
    '</ecg:UserAdd></soap:Body></soap:Envelope>'
)

resp = requests.post(
    "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
    data=envelope.encode("utf-8"),
    headers={"Content-Type": "text/xml; charset=utf-8",
             "SOAPAction": '"http://www.ecgridos.net/UserAdd"'}
)
resp.raise_for_status()
# Extract UserID from resp.text, then call UserSetAuthLevel
print(resp.text)
```

</TabItem>
</Tabs>

---

## Related

- [REST — Users: Create](../rest-api/users/create-user)
- [REST — Users: Set Role](../rest-api/users/set-role)
- [REST — Users: List](../rest-api/users/list-users)
- [REST — Users: Get](../rest-api/users/get-user)
- [SOAP — UserAdd](../soap-api/users/user-add)
- [SOAP — UserSetAuthLevel](../soap-api/users/user-set-auth-level)
- [Appendix: ENUMs — AuthLevel](../appendix/enums)
