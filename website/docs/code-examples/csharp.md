{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-06-17: Code examples section - Christian Nichols */}

---
title: C#
sidebar_position: 1
---

# C# Examples

These examples use `HttpClient` and `System.Text.Json` (.NET 6+). No third-party packages required.

**Base URL:** `https://rest.ecgrid.io`

---

## Setup

```csharp
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;

var client = new HttpClient
{
    BaseAddress = new Uri("https://rest.ecgrid.io")
};

var jsonOptions = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
};
```

---

## Authentication

Exchange your API key for a session key. Session keys are time-limited — store and reuse them until you receive a 401, then re-authenticate.

```csharp
// POST /v2/auth/login
var loginPayload = new { apiKey = "YOUR_API_KEY" };

var loginResponse = await client.PostAsJsonAsync("/v2/auth/login", loginPayload, jsonOptions);
loginResponse.EnsureSuccessStatusCode();

var loginResult = await loginResponse.Content.ReadFromJsonAsync<JsonElement>();
var sessionKey = loginResult
    .GetProperty("data")
    .GetProperty("sessionKey")
    .GetString();

Console.WriteLine($"Session key: {sessionKey}");

// Attach session key to all subsequent requests
client.DefaultRequestHeaders.Add("Authorization", $"Bearer {sessionKey}");
```

### Handling session expiry

```csharp
async Task<string> EnsureSessionAsync(string apiKey, string? existingSessionKey)
{
    if (existingSessionKey != null)
    {
        // Test the existing key with a lightweight call
        var probe = await client.GetAsync("/v2/auth/version");
        if (probe.IsSuccessStatusCode) return existingSessionKey;
    }

    // Re-authenticate
    var response = await client.PostAsJsonAsync("/v2/auth/login",
        new { apiKey }, jsonOptions);
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<JsonElement>();
    return result.GetProperty("data").GetProperty("sessionKey").GetString()!;
}
```

---

## Mailboxes

### Get a mailbox by ID

```csharp
// GET /v2/mailboxes/{id}
int mailboxId = 1234;

var response = await client.GetAsync($"/v2/mailboxes/{mailboxId}");
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<JsonElement>();
var mailbox = result.GetProperty("data");

Console.WriteLine($"Mailbox: {mailbox.GetProperty("mailboxName").GetString()}");
Console.WriteLine($"Network: {mailbox.GetProperty("networkName").GetString()}");
```

### List mailboxes on a network

```csharp
// POST /v2/mailboxes/list
var payload = new
{
    networkId = 5050,
    mailboxId = 0,        // 0 = all mailboxes on the network
    showInactive = false
};

var response = await client.PostAsJsonAsync("/v2/mailboxes/list", payload, jsonOptions);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<JsonElement>();
foreach (var mb in result.GetProperty("data").EnumerateArray())
{
    Console.WriteLine($"{mb.GetProperty("mailboxId").GetInt32()}: " +
                      $"{mb.GetProperty("mailboxName").GetString()}");
}
```

---

## Interchanges

### List inbound interchanges

```csharp
// POST /v2/interchanges/inbox-list
var payload = new
{
    networkId   = 5050,
    mailboxId   = 0,
    startDate   = DateTime.UtcNow.AddDays(-7).ToString("yyyy-MM-dd"),
    endDate     = DateTime.UtcNow.ToString("yyyy-MM-dd"),
    pageSize    = 50,
    pageIndex   = 1
};

var response = await client.PostAsJsonAsync("/v2/interchanges/inbox-list", payload, jsonOptions);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<JsonElement>();
foreach (var interchange in result.GetProperty("data").EnumerateArray())
{
    Console.WriteLine($"ID: {interchange.GetProperty("interchangeId").GetInt64()} | " +
                      $"From: {interchange.GetProperty("senderEDIId").GetString()} | " +
                      $"Status: {interchange.GetProperty("statusDescription").GetString()}");
}
```

---

## Callbacks

### Create a webhook callback

```csharp
// POST /v2/callbacks/create
var payload = new
{
    networkId        = 5050,
    mailboxId        = 0,
    userId           = 1001,
    systemObject     = "Interchange",
    objectStatus     = 5,             // 5 = Ready (delivered to inbox)
    direction        = "InBox",
    frequency        = 60,            // retry interval in seconds
    maxRetries       = 24,
    url              = "https://your-system.com/webhook/ecgrid",
    httpAuthentication = (string?)null,
    status           = "Active"
};

var response = await client.PostAsJsonAsync("/v2/callbacks/create", payload, jsonOptions);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<JsonElement>();
var eventId = result.GetProperty("data").GetProperty("callBackEventId").GetInt32();
Console.WriteLine($"Callback created with event ID: {eventId}");
```

### List callbacks for a mailbox

```csharp
// POST /v2/callbacks/event-list
var payload = new
{
    networkId    = 5050,
    mailboxId    = 0,
    showInactive = false
};

var response = await client.PostAsJsonAsync("/v2/callbacks/event-list", payload, jsonOptions);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<JsonElement>();
foreach (var cb in result.GetProperty("data").EnumerateArray())
{
    Console.WriteLine($"Event {cb.GetProperty("callBackEventId").GetInt32()}: " +
                      $"{cb.GetProperty("url").GetString()} " +
                      $"[{cb.GetProperty("statusDescription").GetString()}]");
}
```

---

## Keys (Metadata)

### Create a metadata key on a mailbox

```csharp
// POST /v2/keys/create
var payload = new
{
    key          = "integration.vendorCode",
    systemObject = "Mailbox",
    objectId     = 1234L,
    visibility   = "Private",
    value        = "ACME-001",
    meta         = "Vendor code for ACME Corp integration",
    daysToLive   = -1    // -1 = no expiry
};

var response = await client.PostAsJsonAsync("/v2/keys/create", payload, jsonOptions);
response.EnsureSuccessStatusCode();
Console.WriteLine("Key created.");
```

### List all keys on an object

```csharp
// POST /v2/keys/list
var payload = new
{
    systemObject = "Mailbox",
    objectId     = 1234L
};

var response = await client.PostAsJsonAsync("/v2/keys/list", payload, jsonOptions);
response.EnsureSuccessStatusCode();

var result = await response.Content.ReadFromJsonAsync<JsonElement>();
foreach (var key in result.GetProperty("data").EnumerateArray())
{
    Console.WriteLine($"{key.GetProperty("key").GetString()}: " +
                      $"{key.GetProperty("value").GetString()}");
}
```

---

## Error Handling

```csharp
try
{
    var response = await client.PostAsJsonAsync("/v2/mailboxes/list", payload, jsonOptions);

    if (!response.IsSuccessStatusCode)
    {
        var error = await response.Content.ReadFromJsonAsync<JsonElement>();
        var title   = error.GetProperty("title").GetString();
        var detail  = error.GetProperty("detail").GetString();
        var traceId = error.GetProperty("traceId").GetString();

        Console.WriteLine($"Error {(int)response.StatusCode}: {title}");
        Console.WriteLine($"Detail: {detail}");
        Console.WriteLine($"Trace ID: {traceId}");

        // Re-authenticate on 401
        if (response.StatusCode == System.Net.HttpStatusCode.Unauthorized)
        {
            sessionKey = await EnsureSessionAsync(apiKey, null);
            client.DefaultRequestHeaders.Remove("Authorization");
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {sessionKey}");
        }
    }
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"Network error: {ex.Message}");
}
```
