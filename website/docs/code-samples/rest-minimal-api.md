---
title: REST Minimal API Sample
sidebar_position: 5
---
{/* AI Attribution — Loren Data AI Use Policy §8.2 | Tool: Claude Code (Anthropic) | 2026-05-07: Created REST Minimal API sample documentation page - Greg Kolinski */}

# REST Minimal API Sample

The `ECGrid-REST-dotnet10-MinimalAPI` project shows how to expose a lightweight ASP.NET Core Minimal API that proxies key ECGrid REST endpoints. This pattern is useful when you need to add authentication, logging, or transformation between your own clients and the ECGrid API.

## Project Location

```
samples/rest/ECGrid-REST-dotnet10-MinimalAPI/
```

## What It Demonstrates

- ASP.NET Core Minimal API with `WebApplication.CreateBuilder`
- `MapGet` / `MapPost` endpoint registration with inline handlers
- `IHttpClientFactory` injected directly into endpoint handlers
- ECGrid API key applied at the client level — not re-exposed to callers
- Exposed proxy endpoints: `GET /inbox`, `POST /upload`, `GET /parcel/{id}`

## Key Files

| File | Purpose |
|---|---|
| `Program.cs` | All endpoint registration and handler logic |
| `appsettings.json` | Base configuration |
| `Models/` | Shared response model classes |

## Configuration

```json
{
  "ECGrid": {
    "BaseUrl": "https://rest.ecgrid.io",
    "ApiKey": "",
    "MailboxId": 0
  }
}
```

Set the API key locally with user-secrets:

```bash
cd samples/rest/ECGrid-REST-dotnet10-MinimalAPI
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
```

## Key Patterns

### Application Setup and Client Registration (`Program.cs`)

```csharp
// Program.cs — Minimal API setup with ECGrid HttpClient
var builder = WebApplication.CreateBuilder(args);

// Register a named client; the ECGrid API key is applied here, not in each handler
builder.Services.AddHttpClient("ecgrid", (sp, client) =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    client.BaseAddress = new Uri(config["ECGrid:BaseUrl"]!);
    // API key from IConfiguration — never exposed to the proxy's callers
    client.DefaultRequestHeaders.Add("X-API-Key", config["ECGrid:ApiKey"]!);
});

var app = builder.Build();
```

### Endpoint Registration

```csharp
// GET /inbox — returns parcels waiting in the configured mailbox
app.MapGet("/inbox", async (IHttpClientFactory factory, IConfiguration config) =>
{
    var http = factory.CreateClient("ecgrid");
    var mailboxId = config.GetValue<int>("ECGrid:MailboxId");

    var resp = await http.PostAsJsonAsync(
        "v2/parcels/pending-inbox-list",
        new { mailboxId, pageNo = 1, recordsPerPage = 25 });
    var result = await resp.Content.ReadFromJsonAsync<ApiResponse<List<ParcelSummary>>>();

    return Results.Ok(result?.Data ?? []);
});

// GET /parcel/{id} — downloads a single parcel's EDI content
app.MapGet("/parcel/{id:long}", async (long id, IHttpClientFactory factory) =>
{
    var http = factory.CreateClient("ecgrid");
    var response = await http.GetAsync($"/v2/parcels/{id}/download");

    if (!response.IsSuccessStatusCode)
        return Results.StatusCode((int)response.StatusCode);

    var bytes = await response.Content.ReadAsByteArrayAsync();

    // Confirm download so ECGrid marks the parcel as delivered
    await http.PostAsync($"/v2/parcels/{id}/confirm", null);

    return Results.File(bytes, "application/octet-stream", $"parcel-{id}.edi");
});

// POST /upload — accepts an EDI file and forwards it to ECGrid
app.MapPost("/upload", async (IFormFile file, IHttpClientFactory factory) =>
{
    var http = factory.CreateClient("ecgrid");

    using var ms = new MemoryStream();
    await file.CopyToAsync(ms);

    using var content = new ByteArrayContent(ms.ToArray());
    content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
    content.Headers.ContentDisposition =
        new ContentDispositionHeaderValue("attachment") { FileName = file.FileName };

    var response = await http.PostAsync("/v2/parcels/upload", content);
    response.EnsureSuccessStatusCode();

    var result = await response.Content.ReadFromJsonAsync<ApiResponse<ParcelUploadResult>>();
    return Results.Ok(result?.Data);
});

app.Run();
```

## Exposed Proxy Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/inbox` | Lists parcels in the configured mailbox inbox |
| `GET` | `/parcel/{id}` | Downloads a parcel and confirms delivery |
| `POST` | `/upload` | Uploads a multipart EDI file to ECGrid |

## How to Run

```bash
cd samples/rest/ECGrid-REST-dotnet10-MinimalAPI
dotnet user-secrets set "ECGrid:ApiKey" "your-key-here"
dotnet run
```

The API will start on `https://localhost:5001` (or as configured). Use a tool like `curl` or Postman to call the proxy endpoints.

```bash
# Example: check inbox
curl https://localhost:5001/inbox
```

## See Also

- [REST API Overview](../rest-api/overview.md)
- [Parcels — Pending Inbox List](../rest-api/parcels/pending-inbox-list.md)
- [Parcels — Download](../rest-api/parcels/download-parcel.md)
- [Parcels — Upload](../rest-api/parcels/upload-parcel.md)
- [Upload a File](../common-operations/upload-a-file.md)
